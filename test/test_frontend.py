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
class test_config(unittest.TestCase):

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
            backend = Backend("http://localhost:5000")

            print 'authenticated:', backend.authenticated
            result = backend.login('admin', 'bad_password')
            print 'authenticated:', backend.authenticated
        except BackendException as e:
            print 'exception:', str(e)
        except Exception as e:
            print 'exception:', str(e)
            ok_(False)

    def test_3_refused_connection_token(self):
        print ''
        print 'test refused connection with token'
        try:
            # Create/initialize application
            appli = Application()
            appli.initialize(debug=True, test=True)
            frontend = appli.frontend

            print 'authenticated:', frontend.authenticated
            connection = frontend.connect(token='anything')
            print 'authenticated:', frontend.authenticated
        except backend.BackendException as e:
            print 'exception:', str(e)
        except Exception as e:
            print 'exception:', str(e)
            ok_(False)

    def test_4_connection_username(self):
        print ''
        print 'test connection with username/password'
        try:
            # Create/initialize application
            appli = Application()
            appli.initialize(debug=True, test=True)
            frontend = appli.frontend

            print 'authenticated:', frontend.authenticated
            connection = frontend.connect('admin', 'admin')
            print 'authenticated:', frontend.authenticated
            ok_(connection == True)
        except backend.BackendException as e:
            print 'exception:', str(e)
        except Exception as e:
            print 'exception:', str(e)

    def test_5_connection_token(self):
        print ''
        print 'test connection with token'
        try:
            # Create/initialize application
            appli = Application()
            appli.initialize(debug=True, test=True)
            frontend = appli.frontend

            print 'authenticated:', frontend.authenticated
            connection = frontend.connect(token='1442583814636-bed32565-2ff7-4023-87fb-34a3ac93d34c')
            print 'authenticated:', frontend.authenticated
            ok_(connection == True)
        except Exception as e:
            print 'exception:', str(e)


    def test_6_all_pages(self):
        print ''
        print 'get all elements on an endpoint'

        # Create/initialize application
        appli = Application()
        appli.initialize(debug=True, test=True)
        frontend = appli.frontend

        # Backend connection
        connection = frontend.connect('admin', 'admin')
        print connection
        ok_(connection)

        # Get all pages
        print 'get all elements at once'
        # Filter the templates ...
        parameters = { 'where': '{"register":true}' }
        items = frontend.get_objects('host', parameters=parameters, all=True)
        print "Got %s elements:" % len(items)
        ok_('_items' not in items)
        # ok_(len(items) > 0)
        for item in items:
            ok_('host_name' in item)
            print "Host: ", item['host_name']

        # Get all pages
        print 'get all elements at once'
        # Filter the templates ...
        parameters = { 'where': '{"register":true}' }
        items = frontend.get_objects('service', parameters=parameters, all=True)
        print "Got %s elements:" % len(items)
        ok_('_items' not in items)
        # ok_(len(items) > 0)
        for item in items:
            ok_('host_name' in item)
            ok_('service_description' in item)
            print "Service: %s/%s" % (item['host_name'], item['service_description'])

    def test_6_page_after_page(self):
        print ''
        print 'backend connection with username/password'

        # Create/initialize application
        appli = Application()
        appli.initialize(debug=True, test=True)
        frontend = appli.frontend

        # Backend connection
        connection = frontend.connect('admin', 'admin')
        ok_(connection == True)

        # Start with first page ...
        last_page = False
        parameters = { 'where': '{"register":false}', 'max_results': 10, 'page': 1 }
        items = []
        while not last_page:
            resp = frontend.get_objects('host', parameters=parameters, all=False)
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
        print "Got %s elements:" % len(items)
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
            resp = frontend.get_objects('service', parameters=parameters, all=False)
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
        print "Got %s elements:" % len(items)
        ok_('_items' not in items)
        # ok_(len(items) > 0)
        for item in items:
            ok_('host_name' in item)
            ok_('service_description' in item)
            print "Service: %s/%s" % (item['host_name'], item['service_description'])
