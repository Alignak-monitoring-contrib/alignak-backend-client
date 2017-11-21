#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Test the PUT request (update items of resource/endpoint) in the backend
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


class TestPutClient(unittest2.TestCase):
    """
    Test put (replace) items
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

        # add an alignakretention item
        data = {
            'host': 'srv001',
            'latency': 0,
            'last_state_type': 'HARD',
            'state': 'UP',
            'last_chk': 0,
        }
        response = requests.post(cls.backend_address + '/alignakretention', json=data,
                                 headers=headers, auth=cls.auth)
        resp = response.json()
        assert resp['_status'] == 'OK'

    @classmethod
    def tearDownClass(cls):
        """
        Stop the backend at the end of the tests

        :param module:
        :return: None
        """
        print("stop alignak backend")
        cls.pid.kill()

    def test_1_put_successful(self):
        """
        Test put an alignakretention successfully

        :return: None
        """
        backend = Backend(self.backend_address)
        backend.login('admin', 'admin')

        # get alignakretention
        params = {}
        response = requests.get(self.backend_address + '/alignakretention', json=params,
                                auth=self.auth)
        resp = response.json()
        ar_id = resp['_items'][0]['_id']
        ar_etag = resp['_items'][0]['_etag']

        data = {
            'host': 'srv001',
            'latency': 2,
            'last_state_type': 'HARD',
            'state': 'UP',
            'last_chk': 0,
        }
        headers = {'If-Match': ar_etag}
        response = backend.put('/'.join(['alignakretention', ar_id]), data=data, headers=headers)
        assert_true(response['_status'] == 'OK')

        response = requests.get(self.backend_address + '/alignakretention', json=params,
                                auth=self.auth)
        resp = response.json()
        self.assertEqual('srv001', resp['_items'][0]['host'])
        self.assertEqual(2, resp['_items'][0]['latency'])

    def test_1_put_successful_inception(self):
        """
        Test put an alignakretention successfully with inception

        :return: None
        """
        backend = Backend(self.backend_address)
        backend.login('admin', 'admin')

        # get alignakretention
        params = {}
        response = requests.get(self.backend_address + '/alignakretention', json=params,
                                auth=self.auth)
        resp = response.json()
        ar_id = resp['_items'][0]['_id']

        data = {'alias': 'modified test'}
        headers = {'If-Match': 'foo'}
        response = backend.put('/'.join(['alignakretention', ar_id]), data=data, headers=headers,
                               inception=True)
        assert_true(response['_status'] == 'OK')

    def test_2_put_exception_method_not_allowed(self):
        """
        Test put a user with errors (so exceptions) because PUT method not allowed on this endpoint

        :return: None
        """
        backend = Backend(self.backend_address)
        backend.login('admin', 'admin')

        # get user admin
        params = {"where": {"name": "admin"}}
        response = requests.get(self.backend_address + '/user', json=params, auth=self.auth)
        resp = response.json()
        user_id = resp['_items'][0]['_id']

        with assert_raises(BackendException) as cm:
            data = {'alias': 'modified with no header'}
            backend.put('/'.join(['user', user_id]), data=data)
        ex = cm.exception
        print('exception:', str(ex.code))
        assert_true(ex.code == 1000, str(ex))

        with assert_raises(BackendException) as cm:
            data = {'alias': 'modified test again and again'}
            headers = {'If-Match': "567890987678"}
            response = backend.put('/'.join(['user', user_id]), data=data, headers=headers)
        ex = cm.exception
        print('exception:', str(ex.code))
        assert_true(ex.code == 405, str(ex))

    def test_3_put_exception_method_allowed(self):
        """
        Test put a user with errors (so exceptions) because PUT method not allowed on this endpoint

        :return: None
        """
        backend = Backend(self.backend_address)
        backend.login('admin', 'admin')

        # get alignakretention
        params = {}
        response = requests.get(self.backend_address + '/alignakretention', json=params,
                                auth=self.auth)
        resp = response.json()
        ar_id = resp['_items'][0]['_id']

        with assert_raises(BackendException) as cm:
            data = {
                'host': 'srv001',
                'latency': 2,
                'last_state_type': 'HARD',
                'state': 'UP',
                'last_chk': 0,
            }
            backend.put('/'.join(['alignakretention', ar_id]), data=data)
        ex = cm.exception
        print('exception:', str(ex.code))
        assert_true(ex.code == 1000, str(ex))

        with assert_raises(BackendException) as cm:
            data = {
                'host': 'srv001',
                'latency': 2,
                'last_state_type': 'HARD',
                'state': 'UP',
                'last_chk': 0,
            }
            headers = {'If-Match': "567890987678"}
            response = backend.put('/'.join(['alignakretention', ar_id]), data=data,
                                   headers=headers)
        ex = cm.exception
        print('exception:', str(ex.code))
        assert_true(ex.code == 412, str(ex))

    def test_4_put_connection_error(self):
        """
        Backend connection error when replacing an object...

        :return: None
        """
        print('test connection error when replacing an object')

        # Create client API
        backend = Backend(self.backend_address)
        backend.login('admin', 'admin')

        # get alignakretention
        params = {}
        response = requests.get(self.backend_address + '/alignakretention', json=params,
                                auth=self.auth)
        resp = response.json()
        ar_id = resp['_items'][0]['_id']
        ar_etag = resp['_items'][0]['_etag']

        print("stop the alignak backend")
        self.pid.kill()

        with assert_raises(BackendException) as cm:
            data = {
                'host': 'srv001',
                'latency': 2,
                'last_state_type': 'HARD',
                'state': 'UP',
                'last_chk': 0,
            }
            headers = {'If-Match': ar_etag}
            response = backend.put('/'.join(['alignakretention', ar_id]), data=data,
                                   headers=headers)
            assert_true(response['_status'] == 'OK')
        ex = cm.exception
        self.assertEqual(ex.code, 1000)
