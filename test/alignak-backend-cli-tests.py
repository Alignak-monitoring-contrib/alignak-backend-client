#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Tests for the alignak-backend-cli script
"""

from __future__ import print_function

import os
import shlex
import subprocess
import time

import unittest2

# import alignak_backend_client.backend_client
#
# Set coverage test mode...
os.environ['COVERAGE_PROCESS_START'] = '1'


class TestAlignakBackendCli(unittest2.TestCase):
    """Test class for alignak-backend-cli"""

    @classmethod
    def setUpClass(cls):
        """Prepare the Alignak backend"""
        print("Start alignak backend")

        cls.backend_address = "http://localhost:5000"

        # Set DB name for tests
        os.environ['ALIGNAK_BACKEND_MONGO_DBNAME'] = 'alignak-backend-cli-test'

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
        print("Stop alignak backend")
        cls.pid.kill()

    def test_start_errors(self):
        # pylint: disable=no-self-use
        """ Start CLI without parameters or erroneous parameters"""
        print('test application default start')
        print("Coverage env: %s" % os.environ.get('COV_CORE_SOURCE', 'unknown'))

        fnull = open(os.devnull, 'w')

        print("Launching application without parameters...")
        # from alignak_backend_client.backend_client import main
        # print("Main: %s" % main())
        exit_code = subprocess.call(
            shlex.split('python ../alignak_backend_client/backend_client.py')
        )
        assert exit_code == 64

        print("Launching application with erroneous parameters...")
        exit_code = subprocess.call(
            shlex.split('python ../alignak_backend_client/backend_client.py -Z')
        )
        assert exit_code == 64

    def test_start_help(self):
        # pylint: disable=no-self-use
        """ Start CLI with help parameter"""

        print("Launching application with CLI help...")
        exit_code = subprocess.call(
            shlex.split('python ../alignak_backend_client/backend_client.py -h')
        )
        assert exit_code == 0
