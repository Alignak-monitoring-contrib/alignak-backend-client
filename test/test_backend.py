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
import time
import unittest2
import subprocess

from nose import with_setup # optional
from nose.tools import *

pid = None
backend_address = "http://localhost:5000"

def setup_module(module):
    print ("")
    print ("start alignak backend")

    global pid
    global backend_address
    pid = subprocess.Popen(['uwsgi', '-w', 'alignakbackend:app', '--socket', '0.0.0.0:5000', '--protocol=http', '--enable-threads'])
    time.sleep(3)
    # backend = Backend(backend_address)
    # backend.login("admin", "admin", "force")

def teardown_module(module):
    print ("")
    print ("stop alignak backend")

    global pid
    pid.kill()

from alignak_backend_client.client import Backend, BackendException

class test_0_login_logout(unittest2.TestCase):

    # @classmethod
    # def setUpClass(cls):

    # @classmethod
    # def tearDownClass(cls):

    def test_01_creation(self):
        global backend_address

        print ''
        print 'test creation'

        print 'Create client API for URL:', backend_address
        backend = Backend(backend_address)

        print 'object:', backend
        print 'authenticated:', backend.authenticated
        print 'endpoint:', backend.url_endpoint_root
        print 'token:', backend.token
        assert_false(backend.connected)
        assert_false(backend.authenticated)
        assert_true(backend.url_endpoint_root == backend_address)
        assert_true(backend.token == None)

        print 'Create client API (trailing slash is removed)'
        backend = Backend(backend_address)

        print 'object:', backend
        print 'authenticated:', backend.authenticated
        print 'endpoint:', backend.url_endpoint_root
        print 'token:', backend.token
        assert_false(backend.connected)
        assert_false(backend.authenticated)
        assert_true(backend.url_endpoint_root == backend_address)
        assert_true(backend.token == None)

    def test_02_bad_parameters(self):
        global backend_address

        print ''
        print 'test refused connection with username/password'

        # Create client API
        backend = Backend(backend_address)

        print "no username or no password, login refused - exception 1001"
        with assert_raises(BackendException) as cm:
            result = backend.login(None, None)
        ex = cm.exception # raised exception is available through exception property of context
        print 'exception:', str(ex.code)
        assert_true(ex.code == 1001, str(ex))
        print 'authenticated:', backend.authenticated

        print "invalid username/password, login refused - returns false"
        result = backend.login('admin', 'bad_password')
        assert_false(backend.authenticated)

    def test_03_token_generate(self):
        global backend_address

        print ''
        print 'force authentication token generation'

        # Create client API
        backend = Backend(backend_address)

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
        global backend_address

        print ''
        print 'test accepted connection with username/password'

        # Create client API
        backend = Backend(backend_address)

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

        print 'get object ... must be refused!'
        with assert_raises(BackendException) as cm:
            items = backend.get('host')
        ex = cm.exception
        print 'exception:', str(ex.code)
        assert_true(ex.code == 1001, str(ex))

        print 'get_all object ... must be refused!'
        with assert_raises(BackendException) as cm:
            items = backend.get_all('host')
        ex = cm.exception
        print 'exception:', str(ex.code)
        assert_true(ex.code == 1001, str(ex))

        print 'get all domains ... must be refused!'
        with assert_raises(BackendException) as cm:
            items = backend.get_domains()
        ex = cm.exception
        print 'exception:', str(ex.code)
        assert_true(ex.code == 1001, str(ex))

        print 'post data ... must be refused!'
        with assert_raises(BackendException) as cm:
            data = { 'fake': 'fake' }
            response = backend.post('contact', data=data)
        ex = cm.exception
        print 'exception:', str(ex.code)
        assert_true(ex.code == 1001, str(ex))

        print 'patch data ... must be refused!'
        with assert_raises(BackendException) as cm:
            data = { 'fake': 'fake' }
            headers = { 'If-Match': '' }
            response = backend.patch('contact', data=data, headers=headers)
        ex = cm.exception
        print 'exception:', str(ex.code)
        assert_true(ex.code == 1001, str(ex))

        print 'delete data ... must be refused!'
        with assert_raises(BackendException) as cm:
            data = { 'fake': 'fake' }
            headers = { 'If-Match': '' }
            response = backend.delete('contact', headers=headers)
        ex = cm.exception
        print 'exception:', str(ex.code)
        assert_true(ex.code == 1001, str(ex))


class test_1_get(unittest2.TestCase):

    def test_11_domains_and_some_elements(self):
        global backend_address

        print ''
        print 'get all domains and some elements'

        # Create client API
        backend = Backend(backend_address)

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
        parameters = { 'where': '{"register":true}', 'max_results': 1 }
        items = backend.get_all('host', params=parameters)
        print "Got %d elements:" % len(items)
        assert_true('_items' not in items)
        # assert_true(len(items) > 0)
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
        # assert_true(len(items) > 0)
        for item in items:
            assert_true('contact_name' in item)
            print "Contact: ", item['contact_name']

    def test_12_all_pages(self):
        global backend_address

        print ''
        print 'get all elements on an endpoint'

        # Create client API
        backend = Backend(backend_address)

        print 'Login ...'
        print 'authenticated:', backend.authenticated
        result = backend.login('admin', 'admin')
        print 'authenticated:', backend.authenticated
        print 'token:', backend.token
        assert_true(backend.authenticated)

        # Get all available endpoints
        print 'get all domains'
        items = backend.get_domains()
        print "Got %d elements:" % len(items)
        assert_true('_items' not in items)
        assert_true(len(items) > 0)
        for item in items:
            if item['href'] in ['loghost', 'logservice']:
                continue
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

        # Get all available endpoints
        print 'get all domains'
        items = backend.get_domains()
        print "Got %d elements:" % len(items)
        assert_true('_items' not in items)
        assert_true(len(items) > 0)
        for item in items:
            if item['href'] in ['loghost', 'logservice']:
                continue
            assert_true('href' in item)
            assert_true('title' in item)
            print "Domain: ", item

            # Get all elements
            print 'get all %s at once' % item['href']
            params = {'max_results': 2}
            items = backend.get_all(item['href'], params=params)
            print "Got %d elements:" % len(items)
            assert_true('_items' not in items)
            # assert_true(len(items) > 0)
            for item in items:
                assert_true('_etag' in item)
                print "etag: ", item['_etag']

        # Get all hosts
        print 'get all hosts at once, 1 item per page'
        params = {'max_results':1}
        items = backend.get_all(item['href'], params=params)
        print "Got %d elements:" % len(items)
        assert_true('_items' not in items)
        # assert_true(len(items) > 0)
        for item in items:
            assert_true('_etag' in item)
            print "etag: ", item['_etag']

    def test_13_page_after_page(self):
        global backend_address

        print ''
        print 'backend connection with username/password'


        # Create client API
        backend = Backend(backend_address)

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


class test_2_update(unittest2.TestCase):

    def test_21_post_pacth_delete(self):
        global backend_address

        print ''
        print 'post/delete/patch some elements'

        # Create client API
        backend = Backend(backend_address)

        print 'Login ...'
        print 'authenticated:', backend.authenticated
        result = backend.login('admin', 'admin')
        print 'authenticated:', backend.authenticated
        print 'token:', backend.token
        assert_true(backend.authenticated)

        # Get all contacts
        print 'get all contacts at once'
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
                response = backend.delete('/'.join(['contact', item['_id']]), headers)
                print "Response:", response

        # Get all timeperiods
        print 'get all timeperiods at once'
        parameters = { 'where': '{"register":true}' }
        items = backend.get_all('timeperiod', params=parameters)
        print "Got %d elements:" % len(items)
        assert_true('_items' not in items)
        tp_id = ''
        for item in items:
            assert_true('timeperiod_name' in item)
            assert_true('_id' in item)
            tp_id = item['_id']
            print item
            print "TP: %s (%s), id=%s" % (item['timeperiod_name'], item['name'], item['_id'])

        if not tp_id:
            # Create a new timeperiod
            print 'create a timeperiod'
            data = {
                "timeperiod_name": "test",
                "name": "Testing TP",
                "alias": "Test TP",
                "dateranges": [
                    {u'monday': u'09:00-17:00'},
                    {u'tuesday': u'09:00-17:00'},
                    {u'wednesday': u'09:00-17:00'},
                    {u'thursday': u'09:00-17:00'},
                    {u'friday': u'09:00-17:00'}
                ],
                "register": True
            }
            response = backend.post('timeperiod', data=data)
            print "Response:", response
            assert_true('_created' in response)
            assert_true('_updated' in response)
            assert_true(response['_created'] == response['_updated'])

            # Get all timeperiods
            print 'get all timeperiods at once'
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

        assert_true(tp_id != '')

        # Create a new contact, bad parameters
        print 'create a contact, missing fields'
        # Mandatory field contact_name is missing ...
        data = {
            "name": "Testing contact",
            "alias": "Fred",
            "back_role_super_admin": False,
            "back_role_admin": [],
            "min_business_impact": 0,
        }
        with assert_raises(BackendException) as cm:
            response = backend.post('contact', data=data)
        ex = cm.exception
        print 'exception:', str(ex.code), ex.message, ex.response
        if "_issues" in ex.response:
            for issue in ex.response["_issues"]:
                print "Issue: %s - %s" %(issue, ex.response["_issues"][issue])
        assert_true(ex.code == 422)
        assert_true(ex.response["_issues"])

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
        response = backend.post('contact', data=data)
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
        # Search test contact
        contact_id = ''
        contact_etag = ''
        for item in items:
            assert_true('contact_name' in item)
            print "Contact: ", item['contact_name']
            if item['contact_name'] == 'test':
                contact_id = item['_id']
                contact_etag = item['_etag']
        assert_true(contact_id != '')
        assert_true(contact_etag != '')

        print 'changing contact alias ... no _etag'
        print 'id:', contact_id
        print 'etag:', contact_etag
        with assert_raises(BackendException) as cm:
            data = {'alias': 'modified with no header'}
            # headers['If-Match'] = contact_etag
            response = backend.patch('/'.join(['contact', contact_id]), data=data)
        ex = cm.exception
        print 'exception:', str(ex.code)
        assert_true(ex.code == 1005, str(ex))

        print 'changing contact alias ...'
        print 'id:', contact_id
        print 'etag:', contact_etag
        data = {'alias': 'modified test'}
        headers = {'If-Match': contact_etag}
        response = backend.patch('/'.join(['contact', contact_id]), data=data, headers=headers)
        print 'response:', response
        assert_true(response['_status'] == 'OK')

        response = backend.get('/'.join(['contact', contact_id]))
        print 'response:', response
        assert_true(response['alias'] == 'modified test')

        print 'changing contact alias ... bad _etag (inception = True)'
        print 'id:', contact_id
        print 'etag:', contact_etag
        data = {'alias': 'modified test again'}
        headers = {'If-Match': contact_etag}
        response = backend.patch('/'.join(['contact', contact_id]), data=data, headers=headers, inception=True)
        print 'response:', response
        assert_true(response['_status'] == 'OK')

        response = backend.get('/'.join(['contact', contact_id]))
        print 'response:', response
        assert_true(response['alias'] == 'modified test again')

        print 'changing contact unknown field ... must be refused'
        print 'id:', contact_id
        print 'etag:', contact_etag
        with assert_raises(BackendException) as cm:
            data = {'bad_field': 'bad field name ... unknown in data model'}
            headers = {'If-Match': contact_etag}
            response = backend.patch('/'.join(['contact', contact_id]), data=data, headers=headers, inception=True)
        ex = cm.exception
        print 'exception:', str(ex.code), ex.message, ex.response
        if "_issues" in ex.response:
            for issue in ex.response["_issues"]:
                print "Issue: %s - %s" %(issue, ex.response["_issues"][issue])
        assert_true(ex.code == 422)
        assert_true(ex.response["_issues"])

        print 'changing contact alias ... bad _etag (inception = False)'
        print 'id:', contact_id
        print 'etag:', contact_etag
        with assert_raises(BackendException) as cm:
            data = {'alias': 'modified test again and again'}
            headers = {'If-Match': contact_etag}
            response = backend.patch('/'.join(['contact', contact_id]), data=data, headers=headers)
        ex = cm.exception
        print 'exception:', str(ex.code)
        assert_true(ex.code == 412, str(ex))

        response = backend.get('/'.join(['contact', contact_id]))
        print 'response:', response
        # Not changed !
        assert_true(response['alias'] == 'modified test again')

        response = backend.get('/'.join(['contact', contact_id]))
        print 'response:', response
        # Not changed !
        assert_true(response['alias'] == 'modified test again')

        print 'deleting contact ... bad href'
        with assert_raises(BackendException) as cm:
            headers = { 'If-Match': item['_etag'] }
            response = backend.delete('/'.join(['contact', '5'+item['_id']]), headers)
            print "Response:", response
        ex = cm.exception
        print 'exception:', str(ex.code)
        assert_true(ex.code == 1003, str(ex))

    def test_22_post_pacth_delete(self):
        global backend_address

        print ''
        print 'post/delete/patch some hostgroups'

        # Create client API
        backend = Backend(backend_address)

        print 'Login ...'
        print 'authenticated:', backend.authenticated
        result = backend.login('admin', 'admin')
        print 'authenticated:', backend.authenticated
        print 'token:', backend.token
        assert_true(backend.authenticated)

        # Get all hostgroups
        print 'get all hostgroups at once'
        items = backend.get_all('hostgroup')
        print "Got %d elements:" % len(items)
        assert_true('_items' not in items)
        for item in items:
            assert_true('hostgroup_name' in item)
            assert_true('_id' in item)
            assert_true('_etag' in item)
            print "Group: ", item['hostgroup_name'], item['_id']
            # Test contact still exists ... delete him!
            if item['hostgroup_name'] == 'test':
                headers = { 'If-Match': item['_etag'] }
                response = backend.delete('/'.join(['hostgroup', item['_id']]), headers)
                print "Response:", response

        # Create a new hostgroup, bad parameters
        print 'create a hostgroup, missing fields'
        # Mandatory field hostgroup_name is missing ...
        data = {
            "name": "Testing hostgroup",
            "alias": "Fred",
            "back_role_super_admin": False,
            "back_role_admin": [],
            "min_business_impact": 0,
        }
        with assert_raises(BackendException) as cm:
            response = backend.post('hostgroup', data=data)
        ex = cm.exception
        print 'exception:', str(ex.code), ex.message, ex.response
        if "_issues" in ex.response:
            for issue in ex.response["_issues"]:
                print "Issue: %s - %s" %(issue, ex.response["_issues"][issue])
        assert_true(ex.code == 422)
        assert_true(ex.response["_issues"])

        # Create a new hostgroup
        print 'create a hostgroup'
        data = {
            "hostgroup_name": "test",
            "name": "Testing hostgroup",
            "alias": "Fred",
            "note": "Hostgroup note ...",
            "realm": "all"
        }
        response = backend.post('hostgroup', data=data)
        print "Response:", response
        assert_true('_created' in response)
        assert_true('_updated' in response)
        assert_true(response['_created'] == response['_updated'])

        # Get all hostgroups
        print 'get all hostgroups at once'
        # Filter the templates ...
        items = backend.get_all('hostgroup')
        print "Got %d elements:" % len(items)
        assert_true('_items' not in items)
        assert_true(len(items) > 0)
        # Search test hostgroup
        hostgroup_id = ''
        hostgroup_etag = ''
        for item in items:
            assert_true('hostgroup_name' in item)
            print "hostgroup: ", item['hostgroup_name']
            if item['hostgroup_name'] == 'test':
                hostgroup_id = item['_id']
                hostgroup_etag = item['_etag']
        assert_true(hostgroup_id != '')
        assert_true(hostgroup_etag != '')

        print 'changing hostgroup alias ... no _etag'
        print 'id:', hostgroup_id
        print 'etag:', hostgroup_etag
        with assert_raises(BackendException) as cm:
            data = {'alias': 'modified with no header'}
            # headers['If-Match'] = hostgroup_etag
            response = backend.patch('/'.join(['hostgroup', hostgroup_id]), data=data)
        ex = cm.exception
        print 'exception:', str(ex.code)
        assert_true(ex.code == 1005, str(ex))

        print 'changing hostgroup alias ...'
        print 'id:', hostgroup_id
        print 'etag:', hostgroup_etag
        data = {'alias': 'modified test'}
        headers = {'If-Match': hostgroup_etag}
        response = backend.patch('/'.join(['hostgroup', hostgroup_id]), data=data, headers=headers)
        print 'response:', response
        assert_true(response['_status'] == 'OK')

        response = backend.get('/'.join(['hostgroup', hostgroup_id]))
        print 'response:', response
        assert_true(response['alias'] == 'modified test')

        print 'changing hostgroup alias ... bad _etag (inception = True)'
        print 'id:', hostgroup_id
        print 'etag:', hostgroup_etag
        data = {'alias': 'modified test again'}
        headers = {'If-Match': hostgroup_etag}
        response = backend.patch('/'.join(['hostgroup', hostgroup_id]), data=data, headers=headers, inception=True)
        print 'response:', response
        assert_true(response['_status'] == 'OK')

        response = backend.get('/'.join(['hostgroup', hostgroup_id]))
        print 'response:', response
        assert_true(response['alias'] == 'modified test again')

        print 'changing hostgroup alias ... bad _etag (inception = False)'
        print 'id:', hostgroup_id
        print 'etag:', hostgroup_etag
        with assert_raises(BackendException) as cm:
            data = {'alias': 'modified test again and again'}
            headers = {'If-Match': hostgroup_etag}
            response = backend.patch('/'.join(['hostgroup', hostgroup_id]), data=data, headers=headers)
        ex = cm.exception
        print 'exception:', str(ex.code)
        assert_true(ex.code == 412, str(ex))

        response = backend.get('/'.join(['hostgroup', hostgroup_id]))
        print 'response:', response
        # Not changed !
        assert_true(response['alias'] == 'modified test again')

        response = backend.get('/'.join(['hostgroup', hostgroup_id]))
        print 'response:', response
        # Not changed !
        assert_true(response['alias'] == 'modified test again')

        print 'deleting hostgroup ... bad href'
        with assert_raises(BackendException) as cm:
            headers = { 'If-Match': item['_etag'] }
            response = backend.delete('/'.join(['hostgroup', '5'+item['_id']]), headers)
            print "Response:", response
        ex = cm.exception
        print 'exception:', str(ex.code)
        assert_true(ex.code == 1003, str(ex))
