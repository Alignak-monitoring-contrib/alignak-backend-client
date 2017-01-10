#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Test the GET request (get items of resource/endpoint) in the backend
"""

from __future__ import print_function
import os
import time
import shlex
import subprocess
import requests
import unittest2
from nose.tools import assert_true, assert_equal, assert_raises
from alignak_backend_client.client import Backend, BackendException


class TestGetClient(unittest2.TestCase):
    """
    Test get items
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

        # Add many hosts
        headers = {'Content-Type': 'application/json'}
        params = {'name': 'group', '_realm': cls.realmAll_id}
        for num in range(100):
            params['name'] = 'group ' + str(num)
            response = requests.post(cls.backend_address + '/hostgroup', json=params,
                                     headers=headers, auth=cls.auth)
            print(response.__dict__)
            assert_equal(response.status_code, 201)

    @classmethod
    def tearDownClass(cls):
        """
        Stop the backend at the end of the tests

        :param module:
        :return: None
        """
        print("stop alignak backend")
        cls.pid.kill()

    def test_1_domains(self):
        """
        Test get domains (= all resource/enpoints available)

        :return: None
        """
        # Create client API
        backend = Backend(self.backend_address)
        backend.login('admin', 'admin')

        # Get all available endpoints
        print('get all domains')
        # Filter the templates ...
        items = backend.get_domains()
        print("Got %d elements: %s" % (len(items), items))
        assert_true('_items' not in items)
        # assert_true(len(items) == 26)
        for item in items:
            assert_true('href' in item)
            assert_true('title' in item)
            print("Domain: ", item)

    def test_2_all_pages(self):
        """
        Get all items (so all pages) of a resource

        :return: None
        """
        print('get all elements on an endpoint')

        # Create client API
        backend = Backend(self.backend_address)
        backend.login('admin', 'admin')

        # Get all elements
        print('get all hostgroups at once')
        params = {'max_results': 3}
        items = backend.get_all('hostgroup', params=params)
        hostgroups = items['_items']
        for hostgroup in hostgroups:
            print("Group: %s" % hostgroup['name'])
        self.assertEqual(len(hostgroups), 101)

    def test_3_page_after_page(self):
        """
        Get page after page manually

        :return: None
        """
        print('backend connection with username/password')

        # Create client API
        backend = Backend(self.backend_address)
        backend.login('admin', 'admin')

        # Start with first page ... max_results=3
        last_page = False
        parameters = {'max_results': 3, 'page': 1}
        items = []
        while not last_page:
            resp = backend.get('hostgroup', params=parameters)
            assert_true('_items' in resp)
            assert_true('_links' in resp)
            assert_true('_meta' in resp)
            page_number = int(resp['_meta']['page'])
            total = int(resp['_meta']['total'])
            max_results = int(resp['_meta']['max_results'])
            assert_equal(total, 101)
            assert_equal(max_results, 3)
            if 'next' in resp['_links']:
                # It has pagination, so get items of all pages
                parameters['page'] = page_number + 1
            else:
                last_page = True
                assert_equal(page_number, 34)
            items.extend(resp['_items'])

        print("----------")
        print("Got %d elements:" % len(items))
        assert_equal(len(items), 101)

        # Start with first page ... max_results=10
        last_page = False
        parameters = {'max_results': 10, 'page': 1}
        items = []
        while not last_page:
            resp = backend.get('hostgroup', params=parameters)
            assert_true('_items' in resp)
            assert_true('_links' in resp)
            assert_true('_meta' in resp)
            page_number = int(resp['_meta']['page'])
            total = int(resp['_meta']['total'])
            max_results = int(resp['_meta']['max_results'])
            assert_equal(total, 101)
            assert_equal(max_results, 10)
            if 'next' in resp['_links']:
                # It has pagination, so get items of all pages
                parameters['page'] = page_number + 1
            else:
                last_page = True
                assert_equal(page_number, 11)
            items.extend(resp['_items'])

        # Start with first page ... no max_results
        last_page = False
        parameters = {'page': 1}
        items = []
        while not last_page:
            resp = backend.get('hostgroup', params=parameters)
            assert_true('_items' in resp)
            assert_true('_links' in resp)
            assert_true('_meta' in resp)
            page_number = int(resp['_meta']['page'])
            total = int(resp['_meta']['total'])
            max_results = int(resp['_meta']['max_results'])
            assert_equal(total, 101)
            assert_equal(max_results, 25)
            if 'next' in resp['_links']:
                # It has pagination, so get items of all pages
                parameters['page'] = page_number + 1
            else:
                last_page = True
                assert_equal(page_number, 5)
            items.extend(resp['_items'])

        print("----------")
        print("Got %d elements:" % len(items))
        assert_equal(len(items), 101)

    def test_4_connection_error(self):
        """
        Backend connection error when getting an object...

        :return: None
        """
        print('test connection error when getting an object')

        # Create client API
        backend = Backend(self.backend_address)
        backend.login('admin', 'admin')

        print("stop the alignak backend")
        self.pid.kill()

        with assert_raises(BackendException) as cm:
            print('get all hostgroups at once')
            params = {'max_results': 3}
            backend.get_all('hostgroup', params=params)
        ex = cm.exception
        self.assertEqual(ex.code, 1000)
