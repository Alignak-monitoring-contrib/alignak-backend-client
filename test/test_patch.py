#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Test the PATCH request (update items of resource/endpoint) in the backend
"""

from __future__ import print_function
import os
import time
import shlex
import subprocess
import requests
import unittest2
from nose import with_setup  # optional
from nose.tools import assert_true, assert_false, assert_equal, assert_raises
from alignak_backend_client.client import Backend, BackendException


class TestPatchClient(unittest2.TestCase):
    """
    Test patch (update) items
    """
    @classmethod
    def setUpClass(cls):
        """
        Function used in the beginning of test to prepare the backend

        :param module:
        :return: None
        """
        print("")
        print("start alignak backend")

        cls.backend_address = "http://localhost:5000"

        # Set test mode for applications backend
        os.environ['TEST_ALIGNAK_BACKEND'] = '1'
        os.environ['TEST_ALIGNAK_BACKEND_DB'] = 'alignak-backend'

        # Delete used mongo DBs
        exit_code = subprocess.call(
            shlex.split(
                'mongo %s --eval "db.dropDatabase()"' % os.environ['TEST_ALIGNAK_BACKEND_DB'])
        )
        assert exit_code == 0

        cls.pid = subprocess.Popen(
            shlex.split('alignak_backend')
        )
        time.sleep(2)

        headers = {'Content-Type': 'application/json'}
        params = {'username': 'admin', 'password': 'admin', 'action': 'generate'}
        # get token
        response = requests.post(cls.backend_address + '/login', json=params, headers=headers)
        resp = response.json()
        cls.token = resp['token']
        cls.auth = requests.auth.HTTPBasicAuth(cls.token, '')

        # get realms
        response = requests.get(cls.backend_address + '/realm',
                                auth=cls.auth)
        resp = response.json()
        cls.realmAll_id = resp['_items'][0]['_id']

    @classmethod
    def tearDownClass(cls):
        """
        Stop the backend at the end of the tests

        :param module:
        :return: None
        """
        print("")
        print("stop alignak backend")
        cls.pid.kill()

    def test_1_patch_successful(self):
        """
        Test patch a user successfully

        :return: None
        """
        backend = Backend(self.backend_address)
        backend.login('admin', 'admin')

        # get user admin
        params = {"where": {"name": "admin"}}
        response = requests.get(self.backend_address + '/user', json=params, auth=self.auth)
        resp = response.json()
        user_id = resp['_items'][0]['_id']
        user_etag = resp['_items'][0]['_etag']

        data = {'alias': 'modified test'}
        headers = {'If-Match': user_etag}
        response = backend.patch('/'.join(['user', user_id]), data=data, headers=headers)
        assert_true(response['_status'] == 'OK')

    def test_2_patch_exception(self):
        """
        Test patch a user with errors (so exceptions)

        :return: None
        """
        backend = Backend(self.backend_address)
        backend.login('admin', 'admin')

        # get user admin
        params = {"where": {"name": "admin"}}
        response = requests.get(self.backend_address + '/user', json=params, auth=self.auth)
        resp = response.json()
        user_id = resp['_items'][0]['_id']
        user_etag = resp['_items'][0]['_etag']

        with assert_raises(BackendException) as cm:
            data = {'alias': 'modified with no header'}
            backend.patch('/'.join(['user', user_id]), data=data)
        ex = cm.exception
        print('exception:', str(ex.code))
        assert_true(ex.code == 1005, str(ex))

        with assert_raises(BackendException) as cm:
            data = {'bad_field': 'bad field name ... unknown in data model'}
            headers = {'If-Match': user_etag}
            backend.patch('/'.join(['user', user_id]), data=data, headers=headers, inception=True)
        ex = cm.exception
        print('exception:', str(ex.code), ex.message, ex.response)
        if "_issues" in ex.response:
            for issue in ex.response["_issues"]:
                print("Issue: %s - %s" % (issue, ex.response["_issues"][issue]))
        assert_true(ex.code == 422)
        assert_true(ex.response["_issues"])

        with assert_raises(BackendException) as cm:
            data = {'alias': 'modified test again and again'}
            headers = {'If-Match': "567890987678"}
            response = backend.patch('/'.join(['user', user_id]), data=data, headers=headers)
        ex = cm.exception
        print('exception:', str(ex.code))
        assert_true(ex.code == 412, str(ex))
