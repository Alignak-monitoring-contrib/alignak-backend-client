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
from nose import with_setup  # optional
from nose.tools import assert_true, assert_false, assert_equal, assert_raises
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

        # Add many hosts
        headers = {'Content-Type': 'application/json'}
        params = {'name': 'group', '_realm': cls.realmAll_id}
        for num in range(100):
            params['name'] = 'group ' + str(num)
            response = requests.post(cls.backend_address + '/hostgroup', json=params,
                                     headers=headers, auth=cls.auth)
            assert_equal(response.status_code, 201)

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
        print('')
        print('get all elements on an endpoint')

        # Create client API
        backend = Backend(self.backend_address)
        backend.login('admin', 'admin')

        # Get all elements
        print('get all hostgroups at once')
        params = {'max_results': 3}
        items = backend.get_all('hostgroup', params=params)
        hosts = items['_items']
        self.assertEqual(len(hosts), 101)

    def test_3_page_after_page(self):
        """
        Get page after page manually

        :return: None
        """
        print('')
        print('backend connection with username/password')

        # Create client API
        backend = Backend(self.backend_address)
        backend.login('admin', 'admin')

        # Start with first page ...
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

        # Start with first page ...
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

        print("----------")
        print("Got %d elements:" % len(items))
        assert_equal(len(items), 101)
