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

    def test_start_00_errors(self):
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
        exit_code = subprocess.call(
            shlex.split('python ../alignak_backend_client/backend_client.py -t realm unknown_action')
        )
        assert exit_code == 64
        exit_code = subprocess.call(
            shlex.split('python ../alignak_backend_client/backend_client.py -b http://mybackend -t realm list')
        )
        assert exit_code == 1
        exit_code = subprocess.call(
            shlex.split('python ../alignak_backend_client/backend_client.py -b http://127.0.0.1:5000 -u fake -p faka -t realm list')
        )
        assert exit_code == 1

    def test_start_00_help(self):
        # pylint: disable=no-self-use
        """ Start CLI with help parameter"""

        print("Launching application with CLI help...")
        exit_code = subprocess.call(
            shlex.split('python ../alignak_backend_client/backend_client.py -h')
        )
        assert exit_code == 0

    def test_start_00_quiet_verbose(self):
        # pylint: disable=no-self-use
        """ Start CLI with quiet/verbose mode"""

        # Quiet mode
        exit_code = subprocess.call(shlex.split(
            'python ../alignak_backend_client/backend_client.py -f "/tmp" -t realm -q list'
        ))
        assert exit_code == 0
        # Verbosemode
        exit_code = subprocess.call(shlex.split(
            'python ../alignak_backend_client/backend_client.py -f "/tmp" -t realm -v list'
        ))
        assert exit_code == 0

    def test_start_01_get_default(self):
        # pylint: disable=no-self-use
        """ CLI to get default backend objects"""

        # work_dir = os.path.abspath(os.path.dirname(__file__))
        work_dir = '/tmp'
        files = ['alignak-object-list-realms.json',
                 'alignak-object-list-commands.json',
                 'alignak-object-list-timeperiods.json',
                 'alignak-object-list-usergroups.json',
                 'alignak-object-list-hostgroups.json',
                 'alignak-object-list-servicegroups.json',
                 'alignak-model-list-users.json',
                 'alignak-model-list-hosts.json',
                 'alignak-model-list-services.json',
                 'alignak-object-list-users.json',
                 'alignak-object-list-hosts.json',
                 'alignak-object-list-services.json']

        for filename in files:
            if os.path.exists(os.path.join(work_dir, filename)):
                os.remove(os.path.join(work_dir, filename))

        print("Getting the backend default elements...")
        exit_code = subprocess.call(shlex.split(
            'python ../alignak_backend_client/backend_client.py -f "%s" -t realm list' % work_dir
        ))
        assert exit_code == 0
        exit_code = subprocess.call(shlex.split(
            'python ../alignak_backend_client/backend_client.py -f "%s" -t command list' % work_dir
        ))
        assert exit_code == 0
        exit_code = subprocess.call(shlex.split(
            'python ../alignak_backend_client/backend_client.py -f "%s" -t timeperiod list' % work_dir
        ))
        assert exit_code == 0
        exit_code = subprocess.call(shlex.split(
            'python ../alignak_backend_client/backend_client.py -f "%s" -t usergroup list' % work_dir
        ))
        assert exit_code == 0
        exit_code = subprocess.call(shlex.split(
            'python ../alignak_backend_client/backend_client.py -f "%s" -t hostgroup list' % work_dir
        ))
        assert exit_code == 0
        exit_code = subprocess.call(shlex.split(
            'python ../alignak_backend_client/backend_client.py -f "%s" -t servicegroup list' % work_dir
        ))
        assert exit_code == 0
        exit_code = subprocess.call(shlex.split(
            'python ../alignak_backend_client/backend_client.py -f "%s" -t user -m list' % work_dir
        ))
        assert exit_code == 0
        exit_code = subprocess.call(shlex.split(
            'python ../alignak_backend_client/backend_client.py -f "%s" -t host -m list' % work_dir
        ))
        assert exit_code == 0
        exit_code = subprocess.call(shlex.split(
            'python ../alignak_backend_client/backend_client.py -f "%s" -t service -m list' % work_dir
        ))
        assert exit_code == 0
        exit_code = subprocess.call(shlex.split(
            'python ../alignak_backend_client/backend_client.py -f "%s" -t user list' % work_dir
        ))
        assert exit_code == 0
        exit_code = subprocess.call(shlex.split(
            'python ../alignak_backend_client/backend_client.py -f "%s" -t host list' % work_dir
        ))
        assert exit_code == 0
        exit_code = subprocess.call(shlex.split(
            'python ../alignak_backend_client/backend_client.py -f "%s" -t service list' % work_dir
        ))
        assert exit_code == 0
        for filename in files:
            print("Exists %s?" % filename)
            assert os.path.exists(os.path.join(work_dir, filename))

    def test_start_02_create(self):
        # pylint: disable=no-self-use
        """ CLI to create backend objects"""

        work_dir = os.path.abspath(os.path.dirname(__file__))
        work_dir = os.path.join(work_dir, 'json')

        print("Creating backend elements...")
        # Create commands
        exit_code = subprocess.call(shlex.split(
            'python ../alignak_backend_client/backend_client.py -f "%s" -t command -d checks-pack-commands.json add' % work_dir
        ))
        assert exit_code == 0

        # Create templates
        exit_code = subprocess.call(shlex.split(
            'python ../alignak_backend_client/backend_client.py -f "%s" -t user -d checks-pack-users-templates.json add' % work_dir
        ))
        assert exit_code == 0
        exit_code = subprocess.call(shlex.split(
            'python ../alignak_backend_client/backend_client.py -f "%s" -t host -d checks-pack-hosts-templates.json add' % work_dir
        ))
        assert exit_code == 0
        exit_code = subprocess.call(shlex.split(
            'python ../alignak_backend_client/backend_client.py -f "%s" -t service -d checks-pack-services-templates.json add' % work_dir
        ))
        assert exit_code == 0

        # Create a realm
        # First, dry-run ... it will not create!
        exit_code = subprocess.call(shlex.split(
            'python ../alignak_backend_client/backend_client.py -t realm -c add test_realm'
        ))
        assert exit_code == 0
        # Then we create :)
        exit_code = subprocess.call(shlex.split(
            'python ../alignak_backend_client/backend_client.py -t realm add test_realm'
        ))
        assert exit_code == 0
        # Already exists!
        exit_code = subprocess.call(shlex.split(
            'python ../alignak_backend_client/backend_client.py -t realm add test_realm'
        ))
        assert exit_code == 2

        # Create hosts
        # First, dry-run ... it will not create!
        exit_code = subprocess.call(shlex.split(
            'python ../alignak_backend_client/backend_client.py -f "%s" -t host -c add host_without_template' % work_dir
        ))
        assert exit_code == 0
        # Then we create :)
        exit_code = subprocess.call(shlex.split(
            'python ../alignak_backend_client/backend_client.py -f "%s" -t host add host_without_template' % work_dir
        ))
        assert exit_code == 0
        # Already exists!
        exit_code = subprocess.call(shlex.split(
            'python ../alignak_backend_client/backend_client.py -f "%s" -t host add host_without_template' % work_dir
        ))
        assert exit_code == 2
        exit_code = subprocess.call(shlex.split(
            'python ../alignak_backend_client/backend_client.py -f "%s" -t host -T windows-passive-host add host_test' % work_dir
        ))
        assert exit_code == 0
        exit_code = subprocess.call(shlex.split(
            'python ../alignak_backend_client/backend_client.py -f "%s" -t host -d example_host_data.json add host_test_2' % work_dir
        ))
        assert exit_code == 0
        exit_code = subprocess.call(shlex.split(
            'python ../alignak_backend_client/backend_client.py -f "%s" -t host -d example_host_from_template.json add host_test_3' % work_dir
        ))
        assert exit_code == 0

        # Get hosts and services lists
        # All the hosts (implicit default value)
        exit_code = subprocess.call(shlex.split(
            'python ../alignak_backend_client/backend_client.py -f "%s" list' % work_dir
        ))
        assert exit_code == 0
        # All the hosts
        exit_code = subprocess.call(shlex.split(
            'python ../alignak_backend_client/backend_client.py -f "%s" -t host list' % work_dir
        ))
        assert exit_code == 0
        # Embed the linked resources
        exit_code = subprocess.call(shlex.split(
            'python ../alignak_backend_client/backend_client.py -f "%s" -t host -e list' % work_dir
        ))
        assert exit_code == 0
        # A specific host
        exit_code = subprocess.call(shlex.split(
            'python ../alignak_backend_client/backend_client.py -f "%s" -t host get host_test' % work_dir
        ))
        assert exit_code == 0
        exit_code = subprocess.call(shlex.split(
            'python ../alignak_backend_client/backend_client.py -f "%s" -t host -e get host_test' % work_dir
        ))
        assert exit_code == 0
        # A specific host and its services in the same output
        exit_code = subprocess.call(shlex.split(
            'python ../alignak_backend_client/backend_client.py -f "%s" -t host get host_test/*' % work_dir
        ))
        assert exit_code == 0
        exit_code = subprocess.call(shlex.split(
            'python ../alignak_backend_client/backend_client.py -f "%s" -t host -e get host_test/*' % work_dir
        ))
        assert exit_code == 0
        # A specific host service
        exit_code = subprocess.call(shlex.split(
            'python ../alignak_backend_client/backend_client.py -f "%s" -t service get host_test/nsca_services' % work_dir
        ))
        assert exit_code == 0
        # All the services
        exit_code = subprocess.call(shlex.split(
            'python ../alignak_backend_client/backend_client.py -f "%s" -t service list' % work_dir
        ))
        assert exit_code == 0
        # The services of the host host_test
        exit_code = subprocess.call(shlex.split(
            'python ../alignak_backend_client/backend_client.py -f "%s" -t service list host_test/*' % work_dir
        ))
        assert exit_code == 0
        # The services of an unknown host
        exit_code = subprocess.call(shlex.split(
            'python ../alignak_backend_client/backend_client.py -f "%s" -t service list host_unknown/*' % work_dir
        ))
        assert exit_code == 2
        # A specific service of the host host_test
        exit_code = subprocess.call(shlex.split(
            'python ../alignak_backend_client/backend_client.py -f "%s" -t service list host_test/nsca_cpu' % work_dir
        ))
        assert exit_code == 0

    def test_start_02_create_nrpe(self):
        # pylint: disable=no-self-use
        """ CLI to create backend objects - several services with the same name"""

        work_dir = os.path.abspath(os.path.dirname(__file__))
        work_dir = os.path.join(work_dir, 'json/nrpe')

        print("Creating backend elements...")
        # Create commands
        exit_code = subprocess.call(shlex.split(
            'python ../alignak_backend_client/backend_client.py -f "%s" -t command -d commands.json add' % work_dir
        ))
        assert exit_code == 0

        # Create templates
        exit_code = subprocess.call(shlex.split(
            'python ../alignak_backend_client/backend_client.py -f "%s" -t host -d hosts-templates.json add' % work_dir
        ))
        assert exit_code == 0
        exit_code = subprocess.call(shlex.split(
            'python ../alignak_backend_client/backend_client.py -f "%s" -t service -d services-templates.json add' % work_dir
        ))
        assert exit_code == 0

    def test_start_03_get_elements(self):
        # pylint: disable=no-self-use
        """ CLI to get default backend objects"""

        # work_dir = os.path.abspath(os.path.dirname(__file__))
        work_dir = '/tmp'
        files = ['alignak-object-list-realms.json',
                 'alignak-object-list-commands.json',
                 'alignak-object-list-timeperiods.json',
                 'alignak-object-list-usergroups.json',
                 'alignak-object-list-hostgroups.json',
                 'alignak-object-list-servicegroups.json',
                 'alignak-model-list-users.json',
                 'alignak-model-list-hosts.json',
                 'alignak-model-list-services.json',
                 'alignak-object-list-users.json',
                 'alignak-object-list-hosts.json',
                 'alignak-object-list-services.json']

        for filename in files:
            if os.path.exists(os.path.join(work_dir, filename)):
                os.remove(os.path.join(work_dir, filename))

        print("Getting the backend default elements...")
        exit_code = subprocess.call(shlex.split(
            'python ../alignak_backend_client/backend_client.py -f "%s" -t realm list' % work_dir
        ))
        assert exit_code == 0
        exit_code = subprocess.call(shlex.split(
            'python ../alignak_backend_client/backend_client.py -f "%s" -t command list' % work_dir
        ))
        assert exit_code == 0
        exit_code = subprocess.call(shlex.split(
            'python ../alignak_backend_client/backend_client.py -f "%s" -t timeperiod list' % work_dir
        ))
        assert exit_code == 0
        exit_code = subprocess.call(shlex.split(
            'python ../alignak_backend_client/backend_client.py -f "%s" -t usergroup list' % work_dir
        ))
        assert exit_code == 0
        exit_code = subprocess.call(shlex.split(
            'python ../alignak_backend_client/backend_client.py -f "%s" -t hostgroup list' % work_dir
        ))
        assert exit_code == 0
        exit_code = subprocess.call(shlex.split(
            'python ../alignak_backend_client/backend_client.py -f "%s" -t servicegroup list' % work_dir
        ))
        assert exit_code == 0
        exit_code = subprocess.call(shlex.split(
            'python ../alignak_backend_client/backend_client.py -f "%s" -t user -m list' % work_dir
        ))
        assert exit_code == 0
        exit_code = subprocess.call(shlex.split(
            'python ../alignak_backend_client/backend_client.py -f "%s" -t host -m list' % work_dir
        ))
        assert exit_code == 0
        exit_code = subprocess.call(shlex.split(
            'python ../alignak_backend_client/backend_client.py -f "%s" -t service -m list' % work_dir
        ))
        assert exit_code == 0
        exit_code = subprocess.call(shlex.split(
            'python ../alignak_backend_client/backend_client.py -f "%s" -t user list' % work_dir
        ))
        assert exit_code == 0
        exit_code = subprocess.call(shlex.split(
            'python ../alignak_backend_client/backend_client.py -f "%s" -t host list' % work_dir
        ))
        assert exit_code == 0
        exit_code = subprocess.call(shlex.split(
            'python ../alignak_backend_client/backend_client.py -f "%s" -t service list' % work_dir
        ))
        assert exit_code == 0
        for filename in files:
            print("Exists %s?" % filename)
            assert os.path.exists(os.path.join(work_dir, filename))

    def test_start_04_update(self):
        # pylint: disable=no-self-use
        """ CLI to create backend objects"""

        work_dir = os.path.abspath(os.path.dirname(__file__))
        work_dir = os.path.join(work_dir, 'json')

        print("Updating backend elements...")
        # Unknown data file
        # First, dry-run ... it will not update!
        exit_code = subprocess.call(shlex.split(
            'python ../alignak_backend_client/backend_client.py -f "%s" -t host -d unknown.json -c update host_test' % work_dir
        ))
        assert exit_code == 2
        # Then we update
        exit_code = subprocess.call(shlex.split(
            'python ../alignak_backend_client/backend_client.py -f "%s" -t host -d unknown.json update host_test' % work_dir
        ))
        assert exit_code == 2

        # Update an host
        #  First, dry-run ... it will not update!
        exit_code = subprocess.call(shlex.split(
            'python ../alignak_backend_client/backend_client.py -f "%s" -t host -d example_host_livestate.json -c update host_test' % work_dir
        ))
        assert exit_code == 0
        # Then we update
        exit_code = subprocess.call(shlex.split(
            'python ../alignak_backend_client/backend_client.py -f "%s" -t host -d example_host_livestate.json update host_test' % work_dir
        ))
        assert exit_code == 0
        # And again...
        exit_code = subprocess.call(shlex.split(
            'python ../alignak_backend_client/backend_client.py -f "%s" -t host -d example_host_livestate.json update host_test' % work_dir
        ))
        assert exit_code == 0
        # And again... re-using read data
        exit_code = subprocess.call(shlex.split(
            'python ../alignak_backend_client/backend_client.py -f "%s" -t host -d example_host_livestate.json update -i host_test' % work_dir
        ))
        assert exit_code == 0

        # Update a service
        #  First, dry-run ... it will not update!
        exit_code = subprocess.call(shlex.split(
            'python ../alignak_backend_client/backend_client.py -f "%s" -t service -d example_service_livestate.json -c update host_test/nsca_cpu' % work_dir
        ))
        assert exit_code == 0
        exit_code = subprocess.call(shlex.split(
            'python ../alignak_backend_client/backend_client.py -f "%s" -t service -d example_service_livestate.json update host_test/nsca_cpu' % work_dir
        ))
        assert exit_code == 0
        exit_code = subprocess.call(shlex.split(
            'python ../alignak_backend_client/backend_client.py -f "%s" -t service -d example_service_livestate.json update -i host_test/nsca_cpu' % work_dir
        ))
        assert exit_code == 0

        # Get hosts and services lists
        exit_code = subprocess.call(shlex.split(
            'python ../alignak_backend_client/backend_client.py -f "%s" -c -t host list' % work_dir
        ))
        assert exit_code == 0
        exit_code = subprocess.call(shlex.split(
            'python ../alignak_backend_client/backend_client.py -f "%s" -t host list' % work_dir
        ))
        assert exit_code == 0
        exit_code = subprocess.call(shlex.split(
            'python ../alignak_backend_client/backend_client.py -f "%s" -c -t service list' % work_dir
        ))
        assert exit_code == 0
        exit_code = subprocess.call(shlex.split(
            'python ../alignak_backend_client/backend_client.py -f "%s" -t service list' % work_dir
        ))
        assert exit_code == 0
        exit_code = subprocess.call(shlex.split(
            'python ../alignak_backend_client/backend_client.py -f "%s" -c -t service list host_test/*' % work_dir
        ))
        assert exit_code == 0
        exit_code = subprocess.call(shlex.split(
            'python ../alignak_backend_client/backend_client.py -f "%s" -t service list host_test/*' % work_dir
        ))
        assert exit_code == 0

    def test_start_05_delete(self):
        # pylint: disable=no-self-use
        """ CLI to delete backend objects"""

        work_dir = os.path.abspath(os.path.dirname(__file__))
        work_dir = os.path.join(work_dir, 'json')

        print("Deleting backend elements...")
        # Delete all host services
        # First, dry-run ... it will not delete!
        exit_code = subprocess.call(shlex.split(
            'python ../alignak_backend_client/backend_client.py -t service delete -c host_test/*'
        ))
        assert exit_code == 0
        # Then we delete
        exit_code = subprocess.call(shlex.split(
            'python ../alignak_backend_client/backend_client.py -t service delete host_test/*'
        ))
        assert exit_code == 0
        # Delete host
        exit_code = subprocess.call(shlex.split(
            'python ../alignak_backend_client/backend_client.py -t host delete host_test'
        ))
        assert exit_code == 0

        # Delete a service of an host
        # First, dry-run ... it will not delete!
        exit_code = subprocess.call(shlex.split(
            'python ../alignak_backend_client/backend_client.py -t service delete -c host_test_2/nsca_services'
        ))
        assert exit_code == 0

        # Delete an unknown service of an host
        # First, dry-run ...
        exit_code = subprocess.call(shlex.split(
            'python ../alignak_backend_client/backend_client.py -t service delete -c host_test_2/unknown_service'
        ))
        assert exit_code == 2
        # Then real request
        exit_code = subprocess.call(shlex.split(
            'python ../alignak_backend_client/backend_client.py -t service delete host_test_2/unknown_service'
        ))
        assert exit_code == 2

        # Delete all users
        exit_code = subprocess.call(shlex.split(
            'python ../alignak_backend_client/backend_client.py -t user delete'
        ))
        assert exit_code == 0

        # Get hosts and services lists
        exit_code = subprocess.call(shlex.split(
            'python ../alignak_backend_client/backend_client.py -f "%s" -t host list' % work_dir
        ))
        assert exit_code == 0
        exit_code = subprocess.call(shlex.split(
            'python ../alignak_backend_client/backend_client.py -f "%s" -t service list' % work_dir
        ))
        assert exit_code == 0
