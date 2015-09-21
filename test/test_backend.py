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


from alignakbackend_api_client.client import Backend, BackendException

# extend the class unittest.TestCase
class test_login_logout(unittest.TestCase):

    def test_1_creation(self):
        print ''
        print 'test creation'
        try:
            # Create client API
            backend = Backend("http://localhost:5000")

            print 'object:', backend
            print 'authenticated:', backend.authenticated
            print 'endpoint:', backend.url_endpoint_root
            print 'token:', backend.token
            ok_(backend.connected == False)
            ok_(backend.authenticated == False)
            ok_(backend.url_endpoint_root == "http://localhost:5000")
            ok_(backend.token == None)
        except Exception as e:
            print 'exception:', str(e)
            ok_(False)

    def test_2_refused_connection_username(self):
        print ''
        print 'test refused connection with username/password'
        try:
            # Create client API
            backend = Backend("http://localhost:5000/")

            print 'authenticated:', backend.authenticated
            result = backend.login('admin', 'bad_password')
            print 'authenticated:', backend.authenticated
        except BackendException as e:
            print 'exception:', str(e)
        except Exception as e:
            print 'exception:', str(e)
            ok_(False)

    def test_3_token_generate(self):
        print ''
        print 'force authentication token generation'
        try:
            # Create client API
            backend = Backend("http://localhost:5000")

            print 'authenticated:', backend.authenticated
            result = backend.login('admin', 'admin', 'force')
            print 'authenticated:', backend.authenticated
            ok_(backend.authenticated == True)
            token1 = backend.token
            print 'token1:', token1
            result = backend.login('admin', 'admin', 'force')
            print 'authenticated:', backend.authenticated
            ok_(backend.authenticated == True)
            token2 = backend.token
            print 'token2:', token2
            ok_(token1 != token2)
        except BackendException as e:
            print 'exception:', str(e)
            ok_(False)
        except Exception as e:
            print 'exception:', str(e)

    def test_4_connection_username(self):
        print ''
        print 'test accepted connection with username/password'
        try:
            # Create client API
            backend = Backend("http://localhost:5000")

            print 'Login ...'
            print 'authenticated:', backend.authenticated
            result = backend.login('admin', 'admin')
            print 'authenticated:', backend.authenticated
            print 'token:', backend.token
            ok_(backend.authenticated == True)

            print 'Logout ...'
            result = backend.logout()
            print 'authenticated:', backend.authenticated
            print 'token:', backend.token
            ok_(backend.authenticated == False)

            print 'Login ...'
            print 'authenticated:', backend.authenticated
            result = backend.login('admin', 'admin')
            print 'authenticated:', backend.authenticated
            print 'token:', backend.token
            ok_(backend.authenticated == True)

        except BackendException as e:
            print 'exception:', str(e)
            ok_(False)
        except Exception as e:
            print 'exception:', str(e)

# extend the class unittest.TestCase
class test_get(unittest.TestCase):

    def test_1_domains_and_some_elements(self):
        print ''
        print 'get all domains and some elements'
        try:
            # Create client API
            backend = Backend("http://localhost:5000")

            print 'Login ...'
            print 'authenticated:', backend.authenticated
            result = backend.login('admin', 'admin')
            print 'authenticated:', backend.authenticated
            print 'token:', backend.token
            ok_(backend.authenticated == True)

            # Get all available endpoints
            print 'get all domains'
            # Filter the templates ...
            items = backend.get_domains()
            print "Got %d elements:" % len(items)
            ok_('_items' not in items)
            ok_(len(items) > 0)
            for item in items:
                ok_('href' in item)
                ok_('title' in item)
                print "Domain: ", item

            # Get all hosts
            print 'get all hosts at once'
            # Filter the templates ...
            parameters = { 'where': '{"register":true}' }
            items = backend.method_get_all('host', parameters=parameters)
            print "Got %d elements:" % len(items)
            ok_('_items' not in items)
            ok_(len(items) > 0)
            for item in items:
                ok_('host_name' in item)
                print "Host: ", item['host_name']

            # Get all services
            print 'get all services at once'
            # Filter the templates ...
            parameters = { 'where': '{"register":true}' }
            items = backend.method_get_all('service', parameters=parameters)
            print "Got %d elements:" % len(items)
            ok_('_items' not in items)
            # ok_(len(items) > 0)
            for item in items:
                ok_('host_name' in item)
                ok_('service_description' in item)
                print "Service: %s/%s" % (item['host_name'], item['service_description'])

            # Get all contacts
            print 'get all contacts at once'
            # Filter the templates ...
            parameters = { 'where': '{"register":true}' }
            items = backend.method_get_all('contact', parameters=parameters)
            print "Got %d elements:" % len(items)
            ok_('_items' not in items)
            ok_(len(items) > 0)
            for item in items:
                ok_('contact_name' in item)
                print "Contact: ", item['contact_name']
        except BackendException as e:
            print 'exception:', str(e)
            ok_(False)
        except Exception as e:
            print 'exception:', str(e)

    def test_2_all_pages(self):
        print ''
        print 'get all elements on an endpoint'
        try:
            # Create client API
            backend = Backend("http://localhost:5000")

            print 'Login ...'
            print 'authenticated:', backend.authenticated
            result = backend.login('admin', 'admin')
            print 'authenticated:', backend.authenticated
            print 'token:', backend.token
            ok_(backend.authenticated == True)

            # Get all available endpoints
            print 'get all domains'
            # Filter the templates ...
            items = backend.get_domains()
            print "Got %d elements:" % len(items)
            ok_('_items' not in items)
            ok_(len(items) > 0)
            for item in items:
                ok_('href' in item)
                ok_('title' in item)
                print "Domain: ", item

                # Get all elements
                print 'get all %s at once' % item['href']
                items = backend.method_get_all(item['href'])
                print "Got %d elements:" % len(items)
                ok_('_items' not in items)
                # ok_(len(items) > 0)
                for item in items:
                    ok_('_etag' in item)
                    print "etag: ", item['_etag']
        except BackendException as e:
            print 'exception:', str(e)
            ok_(False)
        except Exception as e:
            print 'exception:', str(e)

    def test_3_page_after_page(self):
        print ''
        print 'backend connection with username/password'

        try:
            # Create client API
            backend = Backend("http://localhost:5000")

            print 'Login ...'
            print 'authenticated:', backend.authenticated
            result = backend.login('admin', 'admin')
            print 'authenticated:', backend.authenticated
            print 'token:', backend.token
            ok_(backend.authenticated == True)

            # Start with first page ...
            last_page = False
            parameters = { 'where': '{"register":true}', 'max_results': 2, 'page': 1 }
            items = []
            while not last_page:
                resp = backend.method_get('host', parameters=parameters)
                ok_('_items' in resp)
                ok_('_links' in resp)
                ok_('_meta' in resp)
                print resp['_meta']
                page_number = int(resp['_meta']['page'])
                total = int(resp['_meta']['total'])
                max_results = int(resp['_meta']['max_results'])
                print "Got %d elements out of %d (page %d):" % (max_results, total, page_number)
                for item in resp['_items']:
                    ok_('host_name' in item)
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
            ok_('_items' not in items)
            # ok_(len(items) > 0)
            for item in items:
                ok_('host_name' in item)
                print "Host: ", item['host_name']

            # Start with first page ...
            last_page = False
            parameters = { 'where': '{"register":true}', 'max_results': 10, 'page': 1 }
            items = []
            while not last_page:
                resp = backend.method_get('service', parameters=parameters)
                ok_('_items' in resp)
                ok_('_links' in resp)
                ok_('_meta' in resp)
                print resp['_meta']
                page_number = int(resp['_meta']['page'])
                total = int(resp['_meta']['total'])
                max_results = int(resp['_meta']['max_results'])
                print "Got %d elements out of %d (page %d):" % (max_results, total, page_number)
                for item in resp['_items']:
                    ok_('host_name' in item)
                    ok_('service_description' in item)
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
            ok_('_items' not in items)
            # ok_(len(items) > 0)
            for item in items:
                ok_('host_name' in item)
                ok_('service_description' in item)
                print "Service: %s/%s" % (item['host_name'], item['service_description'])
        except BackendException as e:
            print 'exception:', str(e)
            ok_(False)
        except Exception as e:
            print 'exception:', str(e)

# extend the class unittest.TestCase
class test_update(unittest.TestCase):

    def test_1_domains_and_some_elements(self):
        print ''
        print 'get all domains and some elements'
        try:
            # Create client API
            backend = Backend("http://localhost:5000")

            print 'Login ...'
            print 'authenticated:', backend.authenticated
            result = backend.login('admin', 'admin')
            print 'authenticated:', backend.authenticated
            print 'token:', backend.token
            ok_(backend.authenticated == True)

            # Get all available endpoints
            print 'get all domains'
            # Filter the templates ...
            items = backend.get_domains()
            print "Got %d elements:" % len(items)
            ok_('_items' not in items)
            ok_(len(items) > 0)
            for item in items:
                ok_('href' in item)
                ok_('title' in item)
                print "Domain: ", item

            # Get all hosts
            print 'get all hosts at once'
            # Filter the templates ...
            parameters = { 'where': '{"register":true}' }
            items = backend.method_get_all('host', parameters=parameters)
            print "Got %d elements:" % len(items)
            ok_('_items' not in items)
            ok_(len(items) > 0)
            for item in items:
                ok_('host_name' in item)
                print "Host: ", item['host_name']

            # Get all services
            print 'get all services at once'
            # Filter the templates ...
            parameters = { 'where': '{"register":true}' }
            items = backend.method_get_all('service', parameters=parameters)
            print "Got %d elements:" % len(items)
            ok_('_items' not in items)
            # ok_(len(items) > 0)
            for item in items:
                ok_('host_name' in item)
                ok_('service_description' in item)
                print "Service: %s/%s" % (item['host_name'], item['service_description'])

            # Get all contacts
            print 'get all contacts at once'
            # Filter the templates ...
            parameters = { 'where': '{"register":true}' }
            items = backend.method_get_all('contact', parameters=parameters)
            print "Got %d elements:" % len(items)
            ok_('_items' not in items)
            ok_(len(items) > 0)
            for item in items:
                ok_('contact_name' in item)
                print "Contact: ", item['contact_name']
        except BackendException as e:
            print 'exception:', str(e)
            ok_(False)
        except Exception as e:
            print 'exception:', str(e)
