#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2015:
#   Frederic Mohier, frederic.mohier@gmail.com
#
# This file is part of (WebUI).
#
# (WebUI) is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# (WebUI) is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with (WebUI).  If not, see <http://www.gnu.org/licenses/>.
# import the unit testing module

import os
import unittest

from nose import with_setup # optional
from nose.tools import *

def setup_module(module):
    print ("") # this is to get a newline after the dots
    print ("setup_module before anything in this file")

def teardown_module(module):
    print ("") # this is to get a newline after the dots
    print ("teardown_module after everything in this file")

# import alignak_backend_client
from alignak_backend_client.client import Backend, BackendException

# extend the class unittest.TestCase
class test_login_logout(unittest.TestCase):

    def test_01_creation(self):
        print ''
        print 'test creation'

        print 'Create client API'
        backend = Backend("http://localhost:5000")

        print 'object:', backend
        print 'authenticated:', backend.authenticated
        print 'endpoint:', backend.url_endpoint_root
        print 'token:', backend.token
        assert_false(backend.connected)
        assert_false(backend.authenticated)
        assert_true(backend.url_endpoint_root == "http://localhost:5000")
        assert_true(backend.token == None)

        print 'Create client API (trailing slash is removed)'
        backend = Backend("http://localhost:5000/")

        print 'object:', backend
        print 'authenticated:', backend.authenticated
        print 'endpoint:', backend.url_endpoint_root
        print 'token:', backend.token
        assert_false(backend.connected)
        assert_false(backend.authenticated)
        assert_true(backend.url_endpoint_root == "http://localhost:5000")
        assert_true(backend.token == None)

    def test_02_refused_connection_username(self):
        print ''
        print 'test refused connection with username/password'

        # Create client API
        backend = Backend("http://localhost:5000/")

        print "no username or no password, login refused - exception 1001"
        with assert_raises(BackendException) as cm:
            result = backend.login(None, None)
        ex = cm.exception # raised exception is available through exception property of context
        print 'exception:', str(ex.code)
        assert_true(ex.code == 1001)
        print 'authenticated:', backend.authenticated

        print "invalid username/password, login refused - returns false"
        result = backend.login('admin', 'bad_password')
        assert_false(backend.authenticated)

    def test_03_token_generate(self):
        print ''
        print 'force authentication token generation'

        # Create client API
        backend = Backend("http://localhost:5000")

        print 'request new token generation'
        result = backend.login('admin', 'admin', 'force')
        assert_true(backend.authenticated)
        token1 = backend.token
        print 'token1:', token1
        print 'request new token generation'
        result = backend.login('admin', 'admin', 'force')
        print 'authenticated:', backend.authenticated
        assert_true(backend.authenticated)
        token2 = backend.token
        print 'token2:', token2
        assert_true(token1 != token2)

    def test_04_connection_username(self):
        print ''
        print 'test accepted connection with username/password'

        # Create client API
        backend = Backend("http://localhost:5000")

        print 'Login ...'
        result = backend.login('admin', 'admin')
        print 'authenticated:', backend.authenticated
        print 'token:', backend.token
        assert_true(backend.authenticated)

        print 'Logout ...'
        result = backend.logout()
        print 'authenticated:', backend.authenticated
        print 'token:', backend.token
        assert_false(backend.authenticated)

        print 'Login ...'
        print 'authenticated:', backend.authenticated
        result = backend.login('admin', 'admin')
        print 'authenticated:', backend.authenticated
        print 'token:', backend.token
        assert_true(backend.authenticated)

        print 'Logout ...'
        result = backend.logout()
        print 'authenticated:', backend.authenticated
        print 'token:', backend.token
        assert_false(backend.authenticated)

        print 'Logout ...'
        result = backend.logout()
        print 'authenticated:', backend.authenticated
        print 'token:', backend.token
        assert_false(backend.authenticated)

        print 'get all domains ... must be refused!'
        with assert_raises(BackendException) as cm:
            items = backend.get_domains()
        ex = cm.exception # raised exception is available through exception property of context
        print 'exception:', str(ex.code)
        assert_true(ex.code == 1001)

        print 'post data ... must be refused!'
        with assert_raises(BackendException) as cm:
            data = { 'fake': 'fake' }
            response = backend.method_post('contact', data=data)
        print 'exception:', str(ex.code)
        assert_true(ex.code == 1001)


# extend the class unittest.TestCase
class test_get(unittest.TestCase):

    def test_11_domains_and_some_elements(self):
        print ''
        print 'get all domains and some elements'

        # Create client API
        backend = Backend("http://localhost:5000")

        print 'Login ...'
        print 'authenticated:', backend.authenticated
        result = backend.login('admin', 'admin')
        print 'authenticated:', backend.authenticated
        print 'token:', backend.token
        assert_true(backend.authenticated)

        # Get all available endpoints
        print 'get all domains'
        # Filter the templates ...
        items = backend.get_domains()
        print "Got %d elements:" % len(items)
        assert_true('_items2' not in items)
        assert_true(len(items) > 0)
        for item in items:
            assert_true('href' in item)
            assert_true('title' in item)
            print "Domain: ", item

        # Get all hosts
        print 'get all hosts at once'
        # Filter the templates ...
        parameters = { 'where': '{"register":true}' }
        items = backend.get_all('host', params=parameters)
        print "Got %d elements:" % len(items)
        assert_true('_items' not in items)
        assert_true(len(items) > 0)
        for item in items:
            assert_true('host_name' in item)
            print "Host: ", item['host_name']

        # Get all services
        print 'get all services at once'
        # Filter the templates ...
        parameters = { 'where': '{"register":true}' }
        items = backend.get_all('service', params=parameters)
        print "Got %d elements:" % len(items)
        assert_true('_items' not in items)
        # assert_true(len(items) > 0)
        for item in items:
            assert_true('host_name' in item)
            assert_true('service_description' in item)
            print "Service: %s/%s" % (item['host_name'], item['service_description'])

        # Get all contacts
        print 'get all contacts at once'
        # Filter the templates ...
        parameters = { 'where': '{"register":true}' }
        items = backend.get_all('contact', params=parameters)
        print "Got %d elements:" % len(items)
        assert_true('_items' not in items)
        assert_true(len(items) > 0)
        for item in items:
            assert_true('contact_name' in item)
            print "Contact: ", item['contact_name']

    def test_12_all_pages(self):
        print ''
        print 'get all elements on an endpoint'

        # Create client API
        backend = Backend("http://localhost:5000")

        print 'Login ...'
        print 'authenticated:', backend.authenticated
        result = backend.login('admin', 'admin')
        print 'authenticated:', backend.authenticated
        print 'token:', backend.token
        assert_true(backend.authenticated)

        # Get all available endpoints
        print 'get all domains'
        # Filter the templates ...
        items = backend.get_domains()
        print "Got %d elements:" % len(items)
        assert_true('_items' not in items)
        assert_true(len(items) > 0)
        for item in items:
            assert_true('href' in item)
            assert_true('title' in item)
            print "Domain: ", item

            # Get all elements
            print 'get all %s at once' % item['href']
            items = backend.get_all(item['href'])
            print "Got %d elements:" % len(items)
            assert_true('_items' not in items)
            # assert_true(len(items) > 0)
            for item in items:
                assert_true('_etag' in item)
                print "etag: ", item['_etag']

    def test_13_page_after_page(self):
        print ''
        print 'backend connection with username/password'


        # Create client API
        backend = Backend("http://localhost:5000")

        print 'Login ...'
        print 'authenticated:', backend.authenticated
        result = backend.login('admin', 'admin')
        print 'authenticated:', backend.authenticated
        print 'token:', backend.token
        assert_true(backend.authenticated)

        # Start with first page ...
        last_page = False
        parameters = { 'where': '{"register":true}', 'max_results': 2, 'page': 1 }
        items = []
        while not last_page:
            resp = backend.get('host', params=parameters)
            assert_true('_items' in resp)
            assert_true('_links' in resp)
            assert_true('_meta' in resp)
            print resp['_meta']
            page_number = int(resp['_meta']['page'])
            total = int(resp['_meta']['total'])
            max_results = int(resp['_meta']['max_results'])
            print "Got %d elements out of %d (page %d):" % (max_results, total, page_number)
            for item in resp['_items']:
                assert_true('host_name' in item)
                print "Host: ", item['host_name']

            if 'next' in resp['_links']:
                # It has pagination, so get items of all pages
                parameters['page'] = page_number + 1
                parameters['max_results'] = max_results
            else:
                last_page = True
            items.extend(resp['_items'])

        print "----------"
        print "Got %d elements:" % len(items)
        assert_true('_items' not in items)
        # assert_true(len(items) > 0)
        for item in items:
            assert_true('host_name' in item)
            print "Host: ", item['host_name']

        # Start with first page ...
        last_page = False
        parameters = { 'where': '{"register":true}', 'max_results': 10, 'page': 1 }
        items = []
        while not last_page:
            resp = backend.get('service', params=parameters)
            assert_true('_items' in resp)
            assert_true('_links' in resp)
            assert_true('_meta' in resp)
            print resp['_meta']
            page_number = int(resp['_meta']['page'])
            total = int(resp['_meta']['total'])
            max_results = int(resp['_meta']['max_results'])
            print "Got %d elements out of %d (page %d):" % (max_results, total, page_number)
            for item in resp['_items']:
                assert_true('host_name' in item)
                assert_true('service_description' in item)
                print "Service: %s/%s" % (item['host_name'], item['service_description'])

            if 'next' in resp['_links']:
                # It has pagination, so get items of all pages
                parameters['page'] = page_number + 1
                parameters['max_results'] = max_results
            else:
                last_page = True
            items.extend(resp['_items'])

        print "----------"
        print "Got %d elements:" % len(items)
        assert_true('_items' not in items)
        # assert_true(len(items) > 0)
        for item in items:
            assert_true('host_name' in item)
            assert_true('service_description' in item)
            print "Service: %s/%s" % (item['host_name'], item['service_description'])

# extend the class unittest.TestCase
class test_update(unittest.TestCase):

    def test_21_post(self):
        print ''
        print 'post some elements'

        # Create client API
        backend = Backend("http://localhost:5000")

        print 'Login ...'
        print 'authenticated:', backend.authenticated
        result = backend.login('admin', 'admin')
        print 'authenticated:', backend.authenticated
        print 'token:', backend.token
        assert_true(backend.authenticated)

        # Get all contacts
        print 'get all contacts at once'
        # Filter the templates ...
        parameters = { 'where': '{"register":true}' }
        items = backend.get_all('contact', params=parameters)
        print "Got %d elements:" % len(items)
        assert_true('_items' not in items)
        for item in items:
            assert_true('contact_name' in item)
            assert_true('_id' in item)
            assert_true('_etag' in item)
            print "Contact: ", item['contact_name'], item['_id']
            # Test contact still exists ... delete him!
            if item['contact_name'] == 'test':
                headers = { 'If-Match': item['_etag'] }
                response = backend.method_delete('/'.join(['contact', item['_id']]), headers)
                print "Response:", response

        # Get all timeperiods
        print 'get all timeperiods at once'
        # Filter the templates ...
        parameters = { 'where': '{"register":true}' }
        items = backend.get_all('timeperiod', params=parameters)
        print "Got %d elements:" % len(items)
        assert_true('_items' not in items)
        tp_id = ''
        for item in items:
            assert_true('timeperiod_name' in item)
            assert_true('_id' in item)
            tp_id = item['_id']
            print "TP: %s (%s), id=%s" % (item['timeperiod_name'], item['name'], item['_id'])

        # Create a new contact
        print 'create a contact'
        data = {
            "contact_name": "test",
            "name": "Testing contact",
            "alias": "Fred",
            "back_role_super_admin": False,
            "back_role_admin": [],
            "min_business_impact": 0,
            "email": "frederic.mohier@gmail.com",

            "is_admin": False,
            "expert": False,
            "can_submit_commands": False,

            "host_notifications_enabled": True,
            "host_notification_period": tp_id,
            "host_notification_commands": [
            ],
            "host_notification_options": [
                "d",
                "u",
                "r"
            ],

            "service_notifications_enabled": True,
            "service_notification_period": tp_id,
            "service_notification_commands": [ ],
            "service_notification_options": [
                "w",
                "u",
                "c",
                "r"
            ],
            "retain_status_information": False,
            "note": "Monitoring template : default",
            "retain_nonstatus_information": False,
            "definition_order": 100,
            "address1": "",
            "address2": "",
            "address3": "",
            "address4": "",
            "address5": "",
            "address6": "",
            "pager": "",
            "notificationways": [],
            "register": True
        }
        response = backend.method_post('contact', data=data)
        print "Response:", response
        assert_true('_created' in response)
        assert_true('_updated' in response)
        assert_true(response['_created'] == response['_updated'])

        # Get all contacts
        print 'get all contacts at once'
        # Filter the templates ...
        parameters = { 'where': '{"register":true}' }
        items = backend.get_all('contact', params=parameters)
        print "Got %d elements:" % len(items)
        assert_true('_items' not in items)
        assert_true(len(items) > 0)
        for item in items:
            assert_true('contact_name' in item)
            print "Contact: ", item['contact_name']
