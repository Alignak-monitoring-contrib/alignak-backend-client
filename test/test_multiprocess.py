#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import time
import shlex
import unittest2
import subprocess

pid = None
backend_address = "http://localhost:5000"

def setup_module(module):
    print ("")
    print ("start alignak backend")

    # Set test mode for applications backend
    os.environ['TEST_ALIGNAK_BACKEND'] = '1'
    os.environ['TEST_ALIGNAK_BACKEND_DB'] = 'alignak-backend'

    # Delete used mongo DBs
    exit_code = subprocess.call(
        shlex.split('mongo %s --eval "db.dropDatabase()"' % os.environ['TEST_ALIGNAK_BACKEND_DB'])
    )
    assert exit_code == 0

    global pid
    global backend_address
    pid = subprocess.Popen(['uwsgi', '-w', 'alignakbackend:app', '--socket', '0.0.0.0:5000', '--protocol=http', '--enable-threads', '-p', '8'])
    #pid = subprocess.Popen(['alignak_backend'])
    time.sleep(3)
    # backend = Backend(backend_address)
    # backend.login("admin", "admin", "force")

def teardown_module(module):
    print ("")
    print ("stop alignak backend")

    global pid
    pid.kill()

from alignak_backend_client.client import Backend, BackendException

class test_multiprocess(unittest2.TestCase):

    # @classmethod
    # def setUpClass(cls):

    # @classmethod
    # def tearDownClass(cls):

    def test_multiprocess(self):
        global backend_address

        print ''
        print 'test creation'

        print 'Create client API for URL:', backend_address
        backend = Backend(backend_address, 8)
        backend.login('admin', 'admin')

        items = backend.get('realm')
        realm_id = items['_items'][0]['_id']

        # add 700 commands
        backend.delete("command", {})
        data = {'command_line': 'check_ping', '_realm': realm_id}
        for i in xrange(1, 2001):
            data['name'] = "cmd %d" % i
            backend.post('command', data)

        # get without multiprocess
        backend_yannsolo = Backend(backend_address)
        backend_yannsolo.login('admin', 'admin')
        start_time = time.time()
        resp = backend_yannsolo.get_all('command', {'max_results': 20})
        threads_1 = time.time() - start_time
        self.assertEqual(len(resp['_items']), 2000, "Number of commands in non multiprocess mode")

        # get with multiprocess (8 processes)
        start_time = time.time()
        resp = backend.get_all('command', {'max_results': 20})
        threads_8 = time.time() - start_time
        self.assertEqual(len(resp['_items']), 2000, "Number of commands in multiprocess mode")
        ids = []
        for dat in resp['_items']:
            ids.append(dat['_id'])
        self.assertEqual(len(ids), 2000, "Number of id")
        # remove doubles
        ids_final = set(ids)
        self.assertEqual(len(ids_final), 2000, "Number of id unique")

        # threads_8 must be better than 2 time more faster
        # Disable on travis because have only 1 cpu
        #self.assertGreater(threads_1 * 1000 * 0.5, threads_8 * 1000)