#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
This test test multiprocess for get items in backend
"""

from __future__ import print_function
import os
import time
import shlex
import subprocess
import unittest2
from alignak_backend_client.client import Backend


class test_multiprocess(unittest2.TestCase):
    """
    test multiprocess to get items in backend
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

        :return: None
        """
        print("")
        print("stop alignak backend")

        cls.pid.kill()
        time.sleep(1)

    def test_multiprocess(self):
        """
        Test multiprocess get right all elements

        :return: None
        """
        print('')
        print('test creation')

        print('Create client API for URL:', self.backend_address)
        backend = Backend(self.backend_address, 8)
        backend.login('admin', 'admin')

        items = backend.get('realm')
        realm_id = items['_items'][0]['_id']

        # add 2000 commands
        backend.delete("command", {})
        data = {'command_line': 'check_ping', '_realm': realm_id}
        for i in range(1, 2001):
            data['name'] = "cmd %d" % i
            backend.post('command', data)

        # get without multiprocess
        backend_yannsolo = Backend(self.backend_address)
        backend_yannsolo.login('admin', 'admin')
        start_time = time.time()
        resp = backend_yannsolo.get_all('command', {'max_results': 20})
        threads_1 = time.time() - start_time
        self.assertEqual(len(resp['_items']), 2002, "Number of commands in non multiprocess mode")

        # get with multiprocess (8 processes)
        start_time = time.time()
        resp = backend.get_all('command', {'max_results': 20})
        threads_8 = time.time() - start_time
        self.assertEqual(len(resp['_items']), 2002, "Number of commands in multiprocess mode")
        ids = []
        for dat in resp['_items']:
            ids.append(dat['_id'])
        self.assertEqual(len(ids), 2002, "Number of id")
        # remove duplicates
        ids_final = set(ids)
        self.assertEqual(len(ids_final), 2002, "Number of id unique")

        print(threads_1)
        print(threads_8)

        # threads_8 must be better than 2 time more faster
        # Disable on travis because have only 1 cpu
        # self.assertGreater(threads_1 * 1000 * 0.5, threads_8 * 1000)
