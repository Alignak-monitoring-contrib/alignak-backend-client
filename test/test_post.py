#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Test the POST request (add items of resource/endpoint) in the backend
"""

from __future__ import print_function
import os
import time
import shlex
import subprocess
import requests
import unittest2
from nose.tools import assert_true, assert_raises
from alignak_backend_client.client import Backend, BackendException


class TestPostClient(unittest2.TestCase):
    """
    Test post (add) items
    """
    @classmethod
    def setUpClass(cls):
        """
        Function used in the beginning of test to prepare the backend

        :param module:
        :return: None
        """
        print("start alignak backend")

        cls.backend_address = "http://localhost:5000"

        # Set DB name for tests
        os.environ['ALIGNAK_BACKEND_MONGO_DBNAME'] = 'alignak-backend-test'

        # Delete used mongo DBs
        exit_code = subprocess.call(
            shlex.split(
                'mongo %s --eval "db.dropDatabase()"' % os.environ['ALIGNAK_BACKEND_MONGO_DBNAME'])
        )
        assert exit_code == 0

        cls.pid = subprocess.Popen([
            'uwsgi', '--plugin', 'python', '-w', 'alignakbackend:app',
            '--socket', '0.0.0.0:5000', '--protocol=http', '--enable-threads', '--pidfile',
            '/tmp/uwsgi.pid'
        ])
        time.sleep(3)

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
        print("stop alignak backend")
        cls.pid.kill()

    def test_1_post_successful(self):
        """
        Test post a timeperiod successfully

        :return: None
        """
        backend = Backend(self.backend_address)
        backend.login('admin', 'admin')

        # Create a new timeperiod
        print('create a timeperiod')
        data = {
            "name": "Testing TP",
            "alias": "Test TP",
            "dateranges": [
                {u'monday': u'09:00-17:00'},
                {u'tuesday': u'09:00-17:00'},
                {u'wednesday': u'09:00-17:00'},
                {u'thursday': u'09:00-17:00'},
                {u'friday': u'09:00-17:00'}
            ],
            "_realm": self.realmAll_id
        }
        response = backend.post('timeperiod', data=data)
        assert_true('_created' in response)
        assert_true('_updated' in response)
        assert_true(response['_created'] == response['_updated'])

    def test_2_post_exceptions(self):
        """
        Test post a user with errors (so exceptions)

        :return: None
        """
        backend = Backend(self.backend_address)
        backend.login('admin', 'admin')

        # Create a new user, bad parameters
        # Mandatory field user_name is missing ...
        data = {
            "name": "Testing user",
            "alias": "Fred",
            "back_role_super_admin": False,
            "back_role_admin": [],
            "min_business_impact": 0,
        }
        with assert_raises(BackendException) as cm:
            backend.post('user', data=data)
        ex = cm.exception
        assert_true(ex.code == 422)

    def test_3_post_connection_error(self):
        """
        Backend connection error when creating an object...

        :return: None
        """
        print('test connection error when creating an object')

        # Create client API
        backend = Backend(self.backend_address)
        backend.login('admin', 'admin')

        print("stop the alignak backend")
        self.pid.kill()

        with assert_raises(BackendException) as cm:
            # Create a new timeperiod
            print('create a timeperiod')
            data = {
                "name": "Testing TP",
                "alias": "Test TP",
                "dateranges": [
                    {u'monday': u'09:00-17:00'},
                    {u'tuesday': u'09:00-17:00'},
                    {u'wednesday': u'09:00-17:00'},
                    {u'thursday': u'09:00-17:00'},
                    {u'friday': u'09:00-17:00'}
                ],
                "_realm": self.realmAll_id
            }
            response = backend.post('timeperiod', data=data)
            assert_true('_created' in response)
            assert_true('_updated' in response)
            assert_true(response['_created'] == response['_updated'])
        ex = cm.exception
        self.assertEqual(ex.code, 1000)
