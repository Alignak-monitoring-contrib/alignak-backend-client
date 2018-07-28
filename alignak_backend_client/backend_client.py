#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Copyright (C) 2015-2018: Frédéric Mohier
#
# Alignak Backend Client script is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any later version.
#
# Alignak Backend Client is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE.  See the GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this script.  If not, see <http://www.gnu.org/licenses/>.

"""
alignak-backend-cli command line interface::

    Usage:
        alignak-backend-cli [-h]
        alignak-backend-cli [-V]
        alignak-backend-cli [-v] [-q] [-c] [-l] [-m] [-e] [-i]
                            [-b url] [-u username] [-p password]
                            [-d data]
                            [-f folder]
                            [-T template] [-t type] [<action>] [<item>]

    Options:
        -h, --help                  Show this screen.
        -V, --version               Show application version.
        -v, --verbose               Run in verbose mode (more info to display)
        -q, --quiet                 Run in quiet mode (display nothing)
        -c, --check                 Check only (dry run), do not change the backend.
        -l, --list                  Get an items list
        -b, --backend url           Specify backend URL [default: http://127.0.0.1:5000]
        -u, --username=username     Backend login username [default: admin]
        -p, --password=password     Backend login password [default: admin]
        -d, --data=data             Data for the new item to create [default: none]
        -f, --folder=folder         Folder where to read/write data files [default: none]
        -i, --include-read-data     Do not use only the provided data, but append the one
                                    read from he backend
        -t, --type=host             Type of the provided item [default: host]
        -e, --embedded              Do not embed linked objects
        -m, --model                 Get only the templates
        -T, --template=template     Template to use for the new item

    Exit code:
        0 if required operation succeeded
        1 if backend access is denied (check provided username/password)
        2 if element operation failed (missing template,...)

        64 if command line parameters are not used correctly

    Use cases:
        Display help message:
            alignak-backend-cli (-h | --help)

        Display current version:
            alignak-backend-cli -V
            alignak-backend-cli --version

        Specify backend parameters if they are different from the default
            alignak-backend-cli -b http://127.0.0.1:5000 -u admin -p admin get host_name

    Actions:
        'get' to get an item in the backend
        'list' (shortcut for 'get -l' to get the list of all items of a type
        'add' to add an(some) item(s) in the backend
        'update' to update an(some) item(s) in the backend
        'delete' to delete an item (or all items of a type) in the backend

    Use cases to get data:
        Get an items list from the backend:
            alignak-backend-cli get -l
            Try to get the list of all hosts and copy the JSON dump in a file named
            './alignak-object-list-hosts.json'

            alignak-backend-cli get -l -t user
            Try to get the list of all users and copy the JSON dump in a file named
            './alignak-object-list-users.json'

            alignak-backend-cli get -l -f /tmp -t user
            Try to get the list of all users and copy the JSON dump in a file named
            '/tmp/alignak-object-list-users.json'

            alignak-backend-cli list -t user
            Shortcut for 'alignak-backend-cli get -l -t user'

        Get the hosts templates list from the backend:
            alignak-backend-cli -l -m
            Try to get the list of all hosts templates and copy the JSON dump in a
            file named './alignak-object-list-hosts.json'

        Get an item from the backend:
            alignak-backend-cli get host_name
            Try to get the definition of an host named 'host_name' and copy the JSON dump
            in a file named './alignak-object-dump-host-host_name.json'

            alignak-backend-cli -t user get contact_name
            Try to get the definition of a user (contact) contact named 'contact_name' and
            copy the JSON dump in a file named './alignak-object-dump-contact-contact_name.json'

        Get a service from the backend:
            alignak-backend-cli get -t service host_name/service_name
            Try to get the definition of the service service_name for an host named 'host_name'
            and copy the JSON dump in a file named
            './alignak-object-dump-service-host_name_service_name.json'

    Use cases to add data:
        Add an item to the backend (without templating):
            alignak-backend-cli new_host
            This will add an host named new_host

            alignak-backend-cli -t user new_contact
            This will add a user named new_contact

        Add an item to the backend (with some data):
            alignak-backend-cli --data="/tmp/input_host.json" add new_host
            This will add an host named new_host with the data that are read from the
            JSON file /tmp/input_host.json

            alignak-backend-cli -t user new_contact --data="stdin"
            This will add a user named new_contact with the JSON data read from the
            stdin. You can 'cat file > alignak-backend-cli -t user new_contact --data="stdin"'

        Add an item to the backend based on a template:
            alignak-backend-cli -T host_template add new_host
            This will add an host named new_host with the data existing in the template
            host_template

        Add an item to the backend based on several templates:
            alignak-backend-cli -T "host_template,host_template2" add new_host
            This will add an host named new_host with the data existing in the templates
            host_template and host_template2

    Use cases to update data:
        Update an item into the backend (with some data):
            alignak-backend-cli --data "./update_host.json" update test_host
            This will update an host named test_host with the data that are read from the
            JSON file ./update_host.json

    Use cases to delete data:
        Delete an item from the backend:
            alignak-backend-cli delete test_host
            This will delete the host named test_host

        Delete all items from the backend:
            alignak-backend-cli delete -t retentionservice
            This will delete all the retentionservice items

        Delete all the services of an host from the backend:
            alignak-backend-cli delete -t service test_host/*
            This will delete all the services of the host named test_host

    Hints and tips:
        You can operate on any backend endpoint: user, host, service, graphite, ... see the
        Alignak backend documentation (http://alignak-backend.readthedocs.io/) to get a full
        list of the available endpoints and their data fields.

        For a service specify the name as 'host_name/service_name' to get a service for a
        specific host, else the script will return the first service with the required name

        By default, the script embeds in the provided result all the possible embeddable data.
        As such, when you get a service, you will also get its host, check period, ...
        Unfortunately, the same embedding can not be used when adding or updating an item :(

        Use the -m (--model) option to get the templates lists for the host, service or user
        when you get a list. If not used, the list do not include the templates

        Use the -e (--embedded) option to get the linked objects embedded in the output. For
        an host, as an example, the result will include the linked check period, contacts,
        check command,... If not used, the result will only include the linked objects identifier.

        To get the list of all the services of an host, you can get the service list with
        a wildcard in the host name. For all the services of the host named 'passive-01',
        use 'passive-01/*' as in 'alignak-backend-cli get -l -t service passive-01/*'

        To get all the information for an host, including the services, you can use
        a wildcard in the host name. For all the information of the host named 'passive-01',
        use 'passive-01/*' as in 'alignak-backend-cli get -t host passive-01/*'. Using the -e
        option will include all the related objects of the host and its services in the
        dump file.

        If somehow you need to update an item and post all the data when updating, use the
        `-i` option. This will use the data read from the backend and update this data with
        the one provided in the data file specified in the `-d` option.

        Use the -v option to have more information

"""
from __future__ import print_function

import os
import sys
import json
import logging

from docopt import docopt, DocoptExit

from alignak_backend_client.client import Backend, BackendException

# Configure logger
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)8s - %(message)s')
# Name the logger to get the backend client logs
logger = logging.getLogger('alignak_backend_client.client')
logger.setLevel('INFO')

# Use the same version as the main alignak backend
__version__ = "1.3.0"


class BackendUpdate(object):  # pylint: disable=useless-object-inheritance
    """Class to interface the Alignak backend to make some operations"""
    embedded_resources = {
        'realm': {
            '_parent': 1,
        },
        'command': {
            '_realm': 1,
        },
        'timeperiod': {
            '_realm': 1,
        },
        'usergroup': {
            '_realm': 1, '_parent': 1,
        },
        'hostgroup': {
            '_realm': 1, '_parent': 1, 'hostgroups': 1, 'hosts': 1
        },
        'servicegroup': {
            '_realm': 1, '_parent': 1, 'hostgroups': 1, 'hosts': 1
        },
        'user': {
            '_realm': 1,
            'host_notification_period': 1, 'host_notification_commands': 1,
            'service_notification_period': 1, 'service_notification_commands': 1
        },
        'userrestrictrole': {
            '_realm': 1, 'user': 1
        },
        'host': {
            '_realm': 1, '_templates': 1,
            'check_command': 1, 'snapshot_command': 1, 'event_handler': 1,
            'check_period': 1, 'notification_period': 1,
            'snapshot_period': 1, 'maintenance_period': 1,
            'parents': 1, 'hostgroups': 1, 'users': 1, 'usergroups': 1
        },
        'service': {
            '_realm': 1, '_templates': 1,
            'host': 1,
            'check_command': 1, 'snapshot_command': 1, 'event_handler': 1,
            'check_period': 1, 'notification_period': 1,
            'snapshot_period': 1, 'maintenance_period': 1,
            'service_dependencies': 1, 'servicegroups': 1, 'users': 1, 'usergroups': 1
        },
        'hostdependency': {
            '_realm': 1,
            'hosts': 1, 'hostgroups': 1,
            'dependent_hosts': 1, 'dependent_hostgroups': 1,
            'dependency_period': 1
        },
        'servicedependency': {
            '_realm': 1,
            'hosts': 1, 'hostgroups': 1,
            'dependent_hosts': 1, 'dependent_hostgroups': 1,
            'services': 1, 'dependent_services': 1,
            'dependency_period': 1
        },
        'hostescalation': {
            '_realm': 1,
            'hosts': 1, 'hostgroups': 1,
            'users': 1, 'usergroups': 1,
            'escalation_period': 1
        },
        'serviceescalation': {
            '_realm': 1,
            'services': 1,
            'hosts': 1, 'hostgroups': 1,
            'users': 1, 'usergroups': 1,
            'escalation_period': 1
        },
        'graphite': {
            'grafana': 1, 'statsd': 1
        },
        'influxdb': {
            'grafana': 1, 'statsd': 1
        }
    }

    def __init__(self):
        self.logged_in = False
        self.logged_in_user = None

        # Get command line parameters
        args = None
        try:
            args = docopt(__doc__, version=__version__)
        except DocoptExit as exp:
            print("Command line parsing error:\n%s." % (exp))
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~")
            print("Exiting with error code: 64")
            exit(64)

        # Verbose mode
        self.verbose = False
        if args['--verbose']:
            logger.setLevel('DEBUG')
            self.verbose = True

        # Quiet mode
        self.quiet = False
        if args['--quiet']:
            logger.setLevel('NOTSET')
            self.quiet = True

        # Dry-run mode?
        self.dry_run = args['--check']
        logger.debug("Dry-run mode (check only): %s", self.dry_run)

        # Backend URL
        self.backend = None
        self.backend_url = args['--backend']
        logger.debug("Backend URL: %s", self.backend_url)

        # Backend authentication
        self.username = args['--username']
        self.password = args['--password']
        logger.debug("Backend login with credentials: %s/%s", self.username, self.password)

        # Get a list
        self.list = args['--list']
        logger.debug("Get a list: %s", self.list)

        # Get the objects templates in the list
        self.model = args['--model']
        logger.debug("Get the templates: %s", self.model)

        # Get the item type
        self.item_type = args['--type']
        logger.debug("Item type: %s", self.item_type)

        # Get the action to execute
        self.action = args['<action>']
        if self.action is None:
            self.action = 'get'
        logger.debug("Action to execute: %s", self.action)
        if self.action not in ['add', 'update', 'get', 'list', 'delete']:
            print("Action '%s' is not authorized." % (self.action))
            exit(64)

        # Get the targeted item
        self.item = args['<item>']
        if self.item == 'None':
            self.item = None
        logger.debug("Targeted item name: %s", self.item)

        # Get the template to use
        # pylint: disable=no-member
        self.templates = args['--template']
        logger.debug("Using the template(s): %s", self.templates)
        if self.templates:
            if ',' in self.templates:
                self.templates = self.templates.split(',')
            else:
                self.templates = [self.templates]

        if self.list and not self.item_type:
            self.item_type = self.item
            logger.debug("Item type (computed): %s", self.item_type)

        # Embedded mode
        self.embedded = args['--embedded']
        logger.debug("Embedded mode: %s", self.embedded)

        # Get the data files folder
        self.folder = None
        if args['--folder'] != 'none':
            self.folder = args['--folder']
        logger.debug("Data files folder: %s", self.folder)

        # Get the associated data file
        self.data = None
        if args['--data'] != 'none':
            self.data = args['--data']
        logger.debug("Item data provided: %s", self.data)
        self.include_read_data = args['--include-read-data']
        logger.debug("Use backend read data: %s", self.include_read_data)

    def initialize(self):
        # pylint: disable=attribute-defined-outside-init
        """Login on backend with username and password

        :return: None
        """
        try:
            logger.info("Authenticating...")
            self.backend = Backend(self.backend_url)
            self.backend.login(self.username, self.password)
        except BackendException as exp:  # pragma: no cover, should never happen
            logger.exception("Exception: %s", exp)
            logger.error("Response: %s", exp.response)

        if self.backend.token is None:
            print("Access denied!")
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~")
            print("Exiting with error code: 1")
            exit(1)

        logger.info("Authenticated.")

        # Logged-in user and default realm
        users = self.backend.get_all('user', {'where': json.dumps({'name': self.username})})
        self.logged_in_user = users['_items'][0]
        self.default_realm = self.logged_in_user['_realm']

        # Main realm
        self.realm_all = None
        realms = self.backend.get_all('realm')
        for r in realms['_items']:
            if r['name'] == 'All' and r['_level'] == 0:
                self.realm_all = r['_id']
                logger.info("Found realm 'All': %s", self.realm_all)
            if r['_id'] == self.default_realm:
                logger.info("Found logged-in user realm: %s", r['name'])

        # Default timeperiods
        self.tp_always = None
        self.tp_never = None
        timeperiods = self.backend.get_all('timeperiod')
        for tp in timeperiods['_items']:
            if tp['name'] == '24x7':
                self.tp_always = tp['_id']
                logger.info("Found TP '24x7': %s", self.tp_always)
            if tp['name'].lower() == 'none' or tp['name'].lower() == 'never':
                self.tp_never = tp['_id']
                logger.info("Found TP 'Never': %s", self.tp_never)

    def file_dump(self, data, filename):  # pylint: disable=no-self-use
        """
        Dump the data to a JSON formatted file
        :param data: data to be dumped
        :param filename: name of the file to use. Only the file name, not the full path!
        :return: dumped file absolute file name
        """
        dump = json.dumps(data, indent=4,
                          separators=(',', ': '), sort_keys=True)
        path = os.path.join(self.folder or os.getcwd(), filename)
        try:
            dfile = open(path, "wt")
            dfile.write(dump)
            dfile.close()
            return path
        except (OSError, IndexError) as exp:  # pragma: no cover, should never happen
            logger.exception("Error when writing the list dump file %s : %s", path, str(exp))
        return None

    def get_resource_list(self, resource_name, name=''):
        # pylint: disable=too-many-locals, too-many-nested-blocks
        """Get a specific resource list

        If name is not None, it may be a request to get the list of the services of an host.
        """
        try:
            logger.info("Trying to get %s list", resource_name)

            params = {}
            if resource_name in ['host', 'service', 'user']:
                params = {'where': json.dumps({'_is_template': self.model})}

            if resource_name == 'service' and name and '/' in name:
                splitted_name = name.split('/')

                # Get host from name
                response2 = self.backend.get(
                    'host', params={'where': json.dumps({'name': splitted_name[0],
                                                         '_is_template': self.model})})
                if response2['_items']:
                    host = response2['_items'][0]
                    logger.info("Got host '%s' for the service '%s'",
                                splitted_name[0], splitted_name[1])
                else:
                    logger.warning("Not found host '%s'!", splitted_name[0])
                    return False

                params = {'where': json.dumps({'host': host['_id']})}

            if self.embedded and resource_name in self.embedded_resources:
                params.update({'embedded': json.dumps(self.embedded_resources[resource_name])})

            rsp = self.backend.get_all(resource_name, params=params)
            if rsp['_items'] and rsp['_status'] == 'OK':
                response = rsp['_items']

                logger.info("-> found %ss", resource_name)

                # Exists in the backend, we got the element
                if not self.dry_run:
                    logger.info("-> dumping %ss list", resource_name)
                    for item in response:
                        # Filter fields prefixed with an _ (internal backend fields)
                        for field in list(item):
                            if field in ['_created', '_updated', '_etag', '_links', '_status']:
                                item.pop(field)
                                continue

                            # Filter fields prefixed with an _ in embedded items
                            if self.embedded and resource_name in self.embedded_resources and \
                                    field in self.embedded_resources[resource_name]:
                                # Embedded items may be a list or a simple dictionary,
                                # always make it a list
                                embedded_items = item[field]
                                if not isinstance(item[field], list):
                                    embedded_items = [item[field]]
                                # Filter fields in each embedded item
                                for embedded_item in embedded_items:
                                    if not embedded_item:
                                        continue
                                    for embedded_field in list(embedded_item):
                                        if embedded_field.startswith('_'):
                                            embedded_item.pop(embedded_field)

                    filename = self.file_dump(response, 'alignak-%s-list-%ss.json'
                                              % ('model' if self.model else 'object',
                                                 resource_name))
                    if filename:
                        logger.info("-> dumped %ss list to %s", resource_name, filename)
                else:
                    logger.info("Dry-run mode: should have dumped an %s list", resource_name)

                return True
            else:
                logger.warning("-> %s list is empty", resource_name)
                if not self.dry_run:
                    logger.info("-> dumping %ss list", resource_name)
                    filename = self.file_dump([], 'alignak-%s-list-%ss.json'
                                              % ('model' if self.model else 'object',
                                                 resource_name))
                    if filename:
                        logger.info("-> dumped %ss list to %s", resource_name, filename)

                return True

        except BackendException as exp:  # pragma: no cover, should never happen
            logger.exception("Exception: %s", exp)
            logger.error("Response: %s", exp.response)
            print("Get error for '%s' list" % (resource_name))
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~")
            print("Exiting with error code: 5")
            return False

    def get_resource(self, resource_name, name):
        # pylint: disable=too-many-locals, too-many-nested-blocks
        """Get a specific resource by name"""
        try:
            logger.info("Trying to get %s: '%s'", resource_name, name)

            services_list = False
            if resource_name == 'host' and '/' in name:
                splitted_name = name.split('/')
                services_list = True
                name = splitted_name[0]

            params = {'where': json.dumps({'name': name})}

            if resource_name in ['host', 'service', 'user']:
                params = {'where': json.dumps({'name': name, '_is_template': self.model})}

            if resource_name == 'service' and '/' in name:
                splitted_name = name.split('/')
                # new_name = splitted_name[0] + '_' + splitted_name[1]
                # name = splitted_name[1]

                # Get host from name
                response2 = self.backend.get(
                    'host', params={'where': json.dumps({'name': splitted_name[0]})})
                if response2['_items']:
                    host = response2['_items'][0]
                    logger.info("Got host '%s' for the service '%s'",
                                splitted_name[0], splitted_name[1])
                else:
                    logger.warning("Not found host '%s'!", splitted_name[0])
                    return False

                params = {'where': json.dumps({'name': splitted_name[1],
                                               'host': host['_id'],
                                               '_is_template': self.model})}

            if self.embedded and resource_name in self.embedded_resources:
                params.update({'embedded': json.dumps(self.embedded_resources[resource_name])})

            response = self.backend.get(resource_name, params=params)
            if response['_items']:
                response = response['_items'][0]

                logger.info("-> found %s '%s': %s", resource_name, name, response['_id'])

                if services_list:
                    # Get services for the host
                    params = {'where': json.dumps({'host': response['_id']})}
                    if self.embedded and 'service' in self.embedded_resources:
                        params.update(
                            {'embedded': json.dumps(self.embedded_resources['service'])})

                    response2 = self.backend.get('service', params=params)
                    if response2['_items']:
                        response['_services'] = response2['_items']
                        logger.info("Got %d services for host '%s'",
                                    len(response2['_items']), splitted_name[0])
                    else:
                        logger.warning("Not found host '%s'!", splitted_name[0])
                        return False

                # Exists in the backend, we got the element
                if not self.dry_run:
                    logger.info("-> dumping %s: %s", resource_name, name)
                    # Filter fields prefixed with an _ (internal backend fields)
                    for field in list(response):
                        if field in ['_created', '_updated', '_etag', '_links', '_status']:
                            response.pop(field)
                            continue

                        # Filter fields prefixed with an _ in embedded items
                        if self.embedded and resource_name in self.embedded_resources and \
                                field in self.embedded_resources[resource_name]:
                            logger.info("-> embedded %s", field)
                            # Embedded items may be a list or a simple dictionary,
                            # always make it a list
                            embedded_items = response[field]
                            if not isinstance(response[field], list):
                                embedded_items = [response[field]]
                            # Filter fields in each embedded item
                            for embedded_item in embedded_items:
                                if not embedded_item:
                                    continue
                                for embedded_field in list(embedded_item):
                                    if embedded_field.startswith('_'):
                                        embedded_item.pop(embedded_field)

                    dump = json.dumps(response, indent=4,
                                      separators=(',', ': '), sort_keys=True)
                    if not self.quiet:
                        print(dump)

                    if resource_name == 'service' and '/' in name:
                        name = splitted_name[0] + '_' + splitted_name[1]
                    filename = self.file_dump(response,
                                              'alignak-object-dump-%s-%s.json'
                                              % (resource_name, name))
                    if filename:
                        logger.info("-> dumped %s '%s' to %s", resource_name, name, filename)

                    logger.info("-> dumped %s: %s", resource_name, name)
                else:
                    if resource_name == 'service' and '/' in name:
                        name = splitted_name[0] + '_' + splitted_name[1]
                    logger.info("Dry-run mode: should have dumped an %s '%s'",
                                resource_name, name)

                return True
            else:
                logger.warning("-> %s '%s' not found", resource_name, name)
                return False

        except BackendException as exp:  # pragma: no cover, should never happen
            logger.exception("Exception: %s", exp)
            logger.error("Response: %s", exp.response)
            print("Get error for  '%s' : %s" % (resource_name, name))
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~")
            print("Exiting with error code: 5")
            return False

    def delete_resource(self, resource_name, name):
        """Delete a specific resource by name"""
        try:
            logger.info("Trying to get %s: '%s'", resource_name, name)

            if name is None:
                # No name is defined, delete all the resources...
                if not self.dry_run:
                    headers = {
                        'Content-Type': 'application/json'
                    }
                    logger.info("-> deleting all %s", resource_name)
                    self.backend.delete(resource_name, headers)
                    logger.info("-> deleted all %s", resource_name)
                else:
                    response = {'_id': '_fake', '_etag': '_fake'}
                    logger.info("Dry-run mode: should have deleted all %s", resource_name)
            else:
                params = {'where': json.dumps({'name': name})}
                if resource_name in ['host', 'service', 'user']:
                    params = {'where': json.dumps({'name': name, '_is_template': self.model})}
                if resource_name == 'service' and '/' in name:
                    splitted_name = name.split('/')
                    name = splitted_name[0] + '_' + splitted_name[1]

                    # Get host from name
                    response2 = self.backend.get(
                        'host', params={'where': json.dumps({'name': splitted_name[0]})})
                    if response2['_items']:
                        host = response2['_items'][0]
                        logger.info("Got host '%s' for the service '%s'",
                                    splitted_name[0], splitted_name[1])
                    else:
                        logger.warning("Not found host '%s'!", splitted_name[0])
                        return False

                    if splitted_name[1] == '*':
                        params = {'where': json.dumps({'host': host['_id']})}
                    else:
                        params = {'where': json.dumps({'name': splitted_name[1],
                                                       'host': host['_id']})}

                response = self.backend.get_all(resource_name, params=params)
                if response['_items']:
                    logger.info("-> found %d matching %s", len(response['_items']), resource_name)
                    for item in response['_items']:
                        logger.info("-> found %s '%s': %s", resource_name, name, item['name'])

                        # Exists in the backend, we must delete the element...
                        if not self.dry_run:
                            headers = {
                                'Content-Type': 'application/json',
                                'If-Match': item['_etag']
                            }
                            logger.info("-> deleting %s: %s", resource_name, item['name'])
                            self.backend.delete(resource_name + '/' + item['_id'], headers)
                            logger.info("-> deleted %s: %s", resource_name, item['name'])
                        else:
                            response = {'_id': '_fake', '_etag': '_fake'}
                            logger.info("Dry-run mode: should have deleted an %s '%s'",
                                        resource_name, name)
                        logger.info("-> deleted: '%s': %s",
                                    resource_name, item['_id'])
                else:
                    logger.warning("-> %s item '%s' not found", resource_name, name)
                    return False
        except BackendException as exp:  # pragma: no cover, should never happen
            logger.exception("Exception: %s", exp)
            logger.error("Response: %s", exp.response)
            print("Deletion error for  '%s' : %s" % (resource_name, name))
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~")
            print("Exiting with error code: 5")
            return False

        return True

    def create_update_resource(self, resource_name, name, update=False):
        # pylint: disable=too-many-return-statements, too-many-locals
        # pylint: disable=too-many-nested-blocks
        """Create or update a specific resource

        :param resource_name: backend resource endpoint (eg. host, user, ...)
        :param name: name of the resource to create/update
        :param update: True to update an existing resource, else will try to create
        :return:
        """
        if self.data is None:
            self.data = {}

        # If some data are provided, try to get them
        json_data = None
        if self.data:
            try:
                # Data may be provided on the command line or from a file
                if self.data == 'stdin':
                    input_file = sys.stdin
                else:
                    path = os.path.join(self.folder or os.getcwd(), self.data)
                    input_file = open(path)

                json_data = json.load(input_file)
                logger.info("Got provided data: %s", json_data)
                if input_file is not sys.stdin:
                    input_file.close()
            except IOError:
                logger.error("Error reading data file: %s", path)
                return False
            except ValueError:
                logger.error("Error malformed data file: %s", path)
                return False

        if name is None and json_data is None:
            logger.error("-> can not add/update a %s without a name and/or data!", resource_name)
            return False

        # Manage provided templates
        used_templates = []
        if self.templates is not None:
            logger.info("Searching the %s template(s): %s",
                        resource_name, self.templates)
            for template in self.templates:
                response = self.backend.get(
                    resource_name, params={'where': json.dumps({'name': template,
                                                                '_is_template': True})})
                if response['_items']:
                    used_templates.append(response['_items'][0]['_id'])

                    logger.info("-> found %s template '%s': %s",
                                resource_name, template, response['_items'][0]['_id'])
                else:
                    logger.error("-> %s required template not found '%s'", resource_name, template)
                    return False

        try:
            if json_data is None:
                json_data = {'name': name}

            if not isinstance(json_data, list):
                json_data = [json_data]

            logger.info("Got %d %ss", len(json_data), resource_name)
            count = 0
            for json_item in json_data:
                logger.info("-> json item: %s", json_item)
                if resource_name not in ['history', 'userrestrictrole', 'logcheckresult'] \
                        and name is None and ('name' not in json_item or not json_item['name']):
                    logger.warning("-> unnamed '%s'!", resource_name)
                    continue

                # Manage resource name
                item_name = name
                if 'name' in json_item:
                    item_name = json_item['name']

                # Got the item name
                params = {'name': item_name}

                if resource_name == 'service' and 'host' in json_item:
                    # Get host from name
                    host_search = {'name': json_item['host']}
                    if '_is_template' in json_item:
                        host_search.update({'_is_template': json_item['_is_template']})
                    logger.info("Host search: %s", host_search)
                    resp_host = self.backend.get(
                        'host', params={'where': json.dumps(host_search)})
                    if resp_host['_items']:
                        host = resp_host['_items'][0]
                        logger.info("Got host '%s' for the service '%s'", host['name'], item_name)
                    else:
                        logger.warning("Host not found: '%s' for the service: %s!",
                                       json_item['host'], item_name)
                        continue

                    params = {'name': item_name, 'host': host['_id']}

                if resource_name == 'service' and '/' in item_name:
                    splitted_name = item_name.split('/')

                    # Get host from name
                    host_search = {'name': splitted_name[0]}
                    if '_is_template' in json_item:
                        host_search.update({'_is_template': json_item['_is_template']})
                    resp_host = self.backend.get(
                        'host', params={'where': json.dumps(host_search)})
                    if resp_host['_items']:
                        host = resp_host['_items'][0]
                        logger.info("Got host '%s' for the service '%s'",
                                    splitted_name[0], splitted_name[1])
                    else:
                        logger.warning("Host not found: '%s' for the service: %s!",
                                       splitted_name[0], item_name)
                        continue

                    item_name = splitted_name[1]
                    params = {'name': item_name, 'host': host['_id']}

                if '_is_template' in json_item:
                    params.update({'_is_template': json_item['_is_template']})

                params = {'where': json.dumps(params)}

                if name:
                    logger.info("Trying to get %s: '%s', params: %s",
                                resource_name, item_name, params)
                    response = self.backend.get(resource_name, params=params)
                    if response['_items']:
                        found_item = response['_items'][0]
                        found_id = found_item['_id']
                        found_etag = found_item['_etag']
                        logger.info("-> found %s '%s': %s", resource_name, item_name, found_id)

                        if not update:
                            logger.warning("-> '%s' %s cannot be created because it already "
                                           "exists!", resource_name, item_name)
                            continue
                    else:
                        if update:
                            logger.warning("-> '%s' %s cannot be updated because it does not "
                                           "exist!", resource_name, item_name)
                            continue

                # Item data updated with provided information if some

                # Data to update
                item_data = {}
                if self.include_read_data:
                    # Include read data if required
                    item_data = found_item

                # Json provided data update existing data
                item_data.update(json_item)
                # Name is also updated (eg. for a service...)
                item_data['name'] = item_name
                # Template information if templating is required
                if used_templates:
                    item_data.update({'_templates': used_templates,
                                      '_templates_with_services': True})

                for field in item_data.copy():
                    logger.debug("Field: %s = %s", field, item_data[field])
                    # Filter Eve extra fields
                    if field in ['_created', '_updated', '_etag', '_links', '_status']:
                        item_data.pop(field)
                        continue
                    # Filter specific backend inner computed fields
                    # pylint: disable=fixme
                    # todo: list to be completed!
                    if field in ['_overall_state_id']:
                        item_data.pop(field)
                        continue

                    # Manage potential object link fields
                    if field not in ['realm', '_realm', '_templates',
                                     'command', 'host', 'service',
                                     'escalation_period', 'maintenance_period',
                                     'snapshot_period', 'check_period', 'dependency_period',
                                     'notification_period', 'host_notification_period',
                                     'escalation_period', 'service_notification_period',
                                     'host_notification_commands', 'service_notification_commands',
                                     'service_dependencies', 'users', 'usergroups',
                                     'check_command', 'event_handler', 'grafana', 'statsd']:
                        continue

                    field_values = item_data[field]
                    if not isinstance(item_data[field], list):
                        field_values = [item_data[field]]

                    found = None
                    for value in field_values:
                        logger.debug(" - %s, single value: %s", field, value)
                        try:
                            int(value, 16)
                            logger.debug(" - %s, uuid value: %s", field, value)

                            if not isinstance(item_data[field], list):
                                found = value
                            else:
                                if found is None:
                                    found = []
                                found.append(value)
                        except TypeError:
                            pass
                        except ValueError:
                            # Not an integer, consider an item name
                            field_params = {'where': json.dumps({'name': value})}
                            logger.debug(" - %s, params: %s", field, field_params)
                            if field in ['escalation_period', 'maintenance_period',
                                         'snapshot_period', 'check_period',
                                         'dependency_period', 'notification_period',
                                         'host_notification_period',
                                         'service_notification_period']:
                                response2 = self.backend.get('timeperiod', params=field_params)
                            elif field in ['_realm']:
                                response2 = self.backend.get('realm', params=field_params)
                            elif field in ['service_dependencies']:
                                response2 = self.backend.get('service', params=field_params)
                            elif field in ['users']:
                                response2 = self.backend.get('user', params=field_params)
                            elif field in ['usergroups']:
                                response2 = self.backend.get('usergroup', params=field_params)
                            elif field in ['check_command', 'event_handler',
                                           'service_notification_commands',
                                           'host_notification_commands']:
                                response2 = self.backend.get('command', params=field_params)
                            elif field in ['_templates']:
                                field_params = {'where': json.dumps({'name': value,
                                                                     '_is_template': True})}
                                response2 = self.backend.get(resource_name, params=field_params)
                            else:
                                response2 = self.backend.get(field, params=field_params)

                            if response2['_items']:
                                response2 = response2['_items'][0]
                                logger.info("Replaced %s = %s with found item _id",
                                            field, value)
                                if not isinstance(item_data[field], list):
                                    found = response2['_id']
                                else:
                                    if found is None:
                                        found = []
                                    found.append(response2['_id'])

                    if found is None:
                        logger.warning("Not found %s = %s, removing field!", field, field_values)
                        item_data.pop(field)
                    else:
                        item_data[field] = found

                if resource_name not in ['realm'] and '_realm' not in item_data:
                    logger.info("add default realm to the data")
                    item_data.update({'_realm': self.default_realm})

                if resource_name in ['realm'] and '_realm' not in item_data:
                    logger.info("add parent realm to the data")
                    item_data.update({'_parent': self.default_realm})

                if '_id' in item_data:
                    item_data.pop('_id')

                if not update:
                    # Trying to create a new element
                    if not item_data['name']:
                        item_data.pop('name')
                    logger.info("-> trying to create the %s: %s.", resource_name, item_name)
                    logger.debug("-> with: %s.", item_data)
                    if not self.dry_run:
                        try:
                            response = self.backend.post(resource_name, item_data, headers=None)
                        except BackendException as exp:
                            self.item = item_name
                            logger.error("Exception: %s", exp)
                            # logger.error("Response: %s", exp.response)
                            continue
                    else:
                        response = {'_status': 'OK', '_id': '_fake', '_etag': '_fake'}
                else:
                    if not name:
                        logger.warning("-> can not update '%s' with no name!", resource_name)
                        continue

                    # Trying to update an element
                    logger.info("-> trying to update the %s: %s.", resource_name, item_name)
                    logger.debug("-> with: %s.", item_data)
                    if not self.dry_run:
                        try:
                            headers = {'Content-Type': 'application/json', 'If-Match': found_etag}
                            response = self.backend.patch(resource_name + '/' + found_id,
                                                          item_data, headers=headers,
                                                          inception=True)
                        except BackendException as exp:
                            self.item = item_name
                            logger.exception("Exception: %s", exp)
                            # logger.error("Response: %s", exp.response)
                            continue
                    else:
                        response = {'_status': 'OK', '_id': '_fake', '_etag': '_fake'}

                if response['_status'] == 'ERR':
                    logger.warning("Response: %s", response)
                    return False

                if not update:
                    # Created a new element
                    if not self.dry_run:
                        logger.info("-> created: '%s': %s", resource_name, response['_id'])
                    else:
                        logger.info("Dry-run mode: should have created an %s '%s'",
                                    resource_name, name)
                else:
                    # Updated an element
                    if not self.dry_run:
                        logger.info("-> updated: '%s': %s", resource_name, response['_id'])
                    else:
                        logger.info("Dry-run mode: should have updated an %s '%s'",
                                    resource_name, name)
                count = count + 1

        except BackendException as exp:  # pragma: no cover, should never happen
            logger.exception("Exception: %s", exp)
            logger.error("Response: %s", exp.response)
            print("Creation/update error for  '%s' : %s" % (resource_name, name))
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~")
            print("Exiting with error code: 5")
            return False

        if count == len(json_data):
            return True
        return False


def main():
    """
    Main function
    """
    bc = BackendUpdate()
    bc.initialize()
    logger.info("backend_client, version: %s", __version__)
    logger.debug("~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

    success = False
    if bc.item_type and bc.action == 'list':
        success = bc.get_resource_list(bc.item_type, bc.item)

    if bc.item_type and bc.action == 'get':
        if bc.list:
            success = bc.get_resource_list(bc.item_type, bc.item)
        else:
            if not bc.item:
                logger.error("Can not %s a %s with no name!", bc.action, bc.item_type)
                logger.error("Perharps you missed some parameters, run 'alignak-backend-cli -h'")
                exit(64)
            success = bc.get_resource(bc.item_type, bc.item)

    if bc.action in ['add', 'update']:
        success = bc.create_update_resource(bc.item_type, bc.item, bc.action == 'update')

    if bc.action == 'delete':
        success = bc.delete_resource(bc.item_type, bc.item)

    if not success:
        logger.error("%s '%s' %s failed", bc.item_type, bc.item, bc.action)
        if not bc.verbose:
            logger.warning("Set verbose mode to have more information (-v)")
        exit(2)

    exit(0)


if __name__ == "__main__":  # pragma: no cover
    main()
