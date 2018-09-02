#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Test the login / logout in the backend with the client
"""

from __future__ import print_function
import os
import time
import shlex
import subprocess
import unittest2

from nose.tools import assert_true, assert_false, assert_equal, assert_raises

from alignak_backend_client.client import Backend, BackendException


class TestLoginLogout(unittest2.TestCase):
    """
    Test login and logout to the backend
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

    def test_01_creation(self):
        """
        Create connection with the backend

        :return: None
        """
        print('')
        print('test creation')

        print('Create client API for URL:', self.backend_address)
        backend = Backend(self.backend_address)

        print('object:', backend)
        print('authenticated:', backend.authenticated)
        print('endpoint:', backend.url_endpoint_root)
        print('token:', backend.token)
        assert_false(backend.authenticated)
        assert_true(backend.url_endpoint_root == self.backend_address)
        assert_equal(backend.token, None)

        print('Create client API (trailing slash is removed)')
        backend = Backend(self.backend_address + '/')

        print('object:', backend)
        print('authenticated:', backend.authenticated)
        print('endpoint:', backend.url_endpoint_root)
        print('token:', backend.token)
        assert_false(backend.authenticated)
        assert_true(backend.url_endpoint_root == self.backend_address)
        assert_equal(backend.token, None)

    def test_02_bad_parameters(self):
        """
        Test with bad username/password

        :return: None
        """
        print('')
        print('test refused connection with username/password')

        # Create client API
        backend = Backend(self.backend_address)

        print('Login - missing credentials ...')
        with assert_raises(BackendException) as cm:
            backend.login(None, None)
        ex = cm.exception
        print('exception:', str(ex.code))
        assert_true(ex.code == 1000, str(ex))
        assert_true("Missing mandatory parameters" in str(ex))

        print('Login - missing credentials ...')
        with assert_raises(BackendException) as cm:
            backend.login('', '')
        ex = cm.exception
        print('exception:', str(ex.code))
        assert_true(ex.code == 1000, str(ex))
        assert_true("Missing mandatory parameters" in str(ex))

        print('Login - missing credentials ...')
        with assert_raises(BackendException) as cm:
            backend.login('admin', '')
        ex = cm.exception
        print('exception:', str(ex.code))
        assert_true(ex.code == 1000, str(ex))

        print("invalid username/password, login refused")
        result = backend.login('admin', 'bad_password')
        assert_false(result)
        assert_false(backend.authenticated)

    def test_03_token_generate(self):
        """
        Test token generation

        :return: None
        """
        print('')
        print('force authentication token generation')

        # Create client API
        backend = Backend(self.backend_address)

        print('request new token generation')
        backend.login('admin', 'admin', 'force')
        assert_true(backend.authenticated)
        token1 = backend.token
        print('token1:', token1)
        print('request new token generation')
        backend.login('admin', 'admin', 'force')
        print('authenticated:', backend.authenticated)
        assert_true(backend.authenticated)
        token2 = backend.token
        print('token2:', token2)
        assert_true(token1 != token2)

    def test_04_login(self):
        """
        Test with right username / password

        :return: None
        """
        print('')
        print('test accepted connection with username/password')

        # Create client API
        backend = Backend(self.backend_address)

        print('Login ...')
        assert backend.login('admin', 'admin')
        print('authenticated:', backend.authenticated)
        print('token:', backend.token)
        assert_true(backend.authenticated)

        print('Logout ...')
        backend.logout()
        print('authenticated:', backend.authenticated)
        print('token:', backend.token)
        assert_false(backend.authenticated)

        print('Login ...')
        print('authenticated:', backend.authenticated)
        assert backend.login('admin', 'admin')
        print('authenticated:', backend.authenticated)
        print('token:', backend.token)
        assert_true(backend.authenticated)

        print('Logout ...')
        backend.logout()
        print('authenticated:', backend.authenticated)
        print('token:', backend.token)
        assert_false(backend.authenticated)

        print('Logout ...')
        backend.logout()
        print('authenticated:', backend.authenticated)
        print('token:', backend.token)
        assert_false(backend.authenticated)

        print('get object ... must be refused!')
        with assert_raises(BackendException) as cm:
            backend.get('host')
        ex = cm.exception
        print('exception:', str(ex.code))
        assert_true(ex.code == 401, str(ex))

        print('get_all object ... must be refused!')
        with assert_raises(BackendException) as cm:
            backend.get_all('host')
        ex = cm.exception
        print('exception:', str(ex.code))
        assert_true(ex.code == 401, str(ex))

        print('get all domains ... must be refused!')
        with assert_raises(BackendException) as cm:
            backend.get_domains()
        ex = cm.exception
        print('exception:', str(ex.code))
        assert_true(ex.code == 401, str(ex))

        print('post data ... must be refused!')
        with assert_raises(BackendException) as cm:
            data = {'fake': 'fake'}
            backend.post('user', data=data)
        ex = cm.exception
        print('exception:', str(ex.code))
        assert_true(ex.code == 401, str(ex))

        print('patch data ... must be refused!')
        with assert_raises(BackendException) as cm:
            data = {'fake': 'fake'}
            headers = {'If-Match': ''}
            backend.patch('user', data=data, headers=headers)
        ex = cm.exception
        print('exception:', str(ex.code))
        assert_true(ex.code == 405, str(ex))

        print('delete data ... must be refused!')
        with assert_raises(BackendException) as cm:
            headers = {'If-Match': ''}
            backend.delete('user', headers=headers)
        ex = cm.exception
        print('exception:', str(ex.code))
        assert_true(ex.code == 401, str(ex))


class TestLoginLogoutConnection(unittest2.TestCase):
    """
    Test login and logout to the backend - backend is not available
    """

    @classmethod
    def setUpClass(cls):
        """
        Function used in the beginning of test to prepare the backend

        :param module:
        :return: None
        """
        print("Do not start alignak backend")

        cls.backend_address = "http://localhost:5000"

    def test_05_login(self):
        """
        Test with right username / password

        :return: None
        """
        print('test connection error when login')

        # Create client API
        backend = Backend(self.backend_address)

        print('Login ... must be refused!')
        with assert_raises(BackendException) as cm:
            backend.login('admin', 'admin')
        ex = cm.exception
        self.assertEqual(ex.code, 1000)
