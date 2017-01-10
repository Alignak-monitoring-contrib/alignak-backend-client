#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Copyright (C) 2015-2016: Frédéric Mohier
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
        alignak-backend-cli [-v] [-c] [-l]
                            [-b=url] [-u=username] [-p=password]
                            [-d=data]
                            [-T=template] [-t=type] [<action>] [<item>]

    Options:
        -h, --help                  Show this screen.
        -V, --version               Show application version.
        -v, --verbose               Run in verbose mode (more info to display)
        -c, --check                 Check only (dry run), do not change the backend.
        -l, --list                  Get an items list
        -b, --backend url           Specify backend URL [default: http://127.0.0.1:5000]
        -u, --username=username     Backend login username [default: admin]
        -p, --password=password     Backend login password [default: admin]
        -d, --data=data             Data for the new item to create [default: none]
        -t, --type=host             Type of the provided item [default: host]
        -T, --template=template     Template to use for the new item

    Use cases:
        Display help message:
            backend_client (-h | --help)

        Display current version:
            backend_client -V
            backend_client --version

        Get an items list from the backend:
            backend_client -l
            Try to get the list of all hosts and copy the JSON dump in a file named
            '/tmp/alignak-object-list-hosts'

            backend_client -l -t user
            Try to get the list of all users and copy the JSON dump in a file named
            '/tmp/alignak-object-list-users'

        Get an item from the backend:
            backend_client get host_name
            Try to get the definition of an host named 'host_name' and copy the JSON dump
            in a file named '/tmp/alignak-object-dump-host-host_name'

            backend_client -t user get contact_name
            Try to get the definition of a user (contact) contact named 'contact_name' and
            copy the JSON dump in a file named '/tmp/alignak-object-dump-contact-contact_name'

        Add an item to the backend (without templating):
            backend_client new_host
            This will add an host named new_host

            backend_client -t user new_contact
            This will add a user named new_contact

        Add an item to the backend (with some data):
            backend_client --data="/tmp/input_host.json" add new_host
            This will add an host named new_host with the data that are read from the
            JSON file /tmp/input_host.json

            backend_client -t user new_contact --data="stdin"
            This will add a user named new_contact with the JSON data read from the
            stdin. You can 'cat file > backend_client -t user new_contact --data="stdin"'

        Add an item to the backend based on a template:
            backend_client -T host_template add new_host
            This will add an host named new_host with the data existing in the template
            host_template

        Update an item into the backend (with some data):
            backend_client --data="/tmp/update_host.json" update test_host
            This will update an host named test_host with the data that are read from the
            JSON file /tmp/update_host.json

        Specify you backend parameters if they are different from the default
            backend_client -b=http://127.0.0.1:5000 -u=admin -p=admin get host_name

        Exit code:
            0 if required operation succeeded
            1 if backend access is denied (check provided username/password)
            2 if element creation failed (missing template,...)

            64 if command line parameters are not used correctly
"""
from __future__ import print_function

import os
import sys
import json
import tempfile
import logging

from alignak_backend_client.client import Backend, BackendException

from docopt import docopt, DocoptExit

# Configure logger
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)8s - %(message)s')
# Name the logger to get the backend client logs
logger = logging.getLogger('alignak_backend_client.client')

__version__ = "0.4.1"


class BackendUpdate(object):
    """
    Class to interface the Alignak backend to make some operations
    """
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
        'host': {
            '_realm': 1, '_templates': 1,
            'check_command': 1, 'snapshot_command': 1, 'event_handler': 1,
            'check_period': 1, 'notification_period': 1,
            'snapshot_period': 1, 'maintenance_period': 1,
            'parents': 1, 'hostgroups': 1, 'users': 1, 'usergroups': 1
        },
        'service': {
            '_realm': 1,
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
        }
    }

    def __init__(self):
        self.logged_in = False

        # Get command line parameters
        args = None
        try:
            args = docopt(__doc__, version=__version__)
        except DocoptExit as exp:
            print("Command line parsing error:\n%s." % (exp))
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~")
            print("Exiting with error code: 64")
            exit(64)

        logger.debug("Test")
        # Verbose
        self.verbose = False
        if '--verbose' in args and args['--verbose']:
            logger.setLevel('DEBUG')
            self.verbose = True

        # Dry-run mode?
        self.dry_run = args['--check']
        logger.info("Dry-run mode (check only): %s", self.dry_run)

        # Backend URL
        self.backend = None
        self.backend_url = args['--backend']
        logger.info("Backend URL: %s", self.backend_url)

        # Backend authentication
        self.username = args['--username']
        self.password = args['--password']
        logger.info("Backend login with credentials: %s/%s", self.username, self.password)

        # Get a list
        self.list = args['--list']
        logger.info("Get a list: %s", self.list)

        # Get the item type
        self.item_type = args['--type']
        logger.info("Item type: %s", self.item_type)

        # Get the action to execute
        self.action = args['<action>']
        if self.action is None:
            self.action = 'get'
        logger.info("Action to execute: %s", self.action)
        if self.action not in ['add', 'update', 'get', 'delete']:
            print("Action '%s' is not authorized." % (self.action))
            exit(64)

        # Get the targeted item
        self.item = args['<item>']
        logger.info("Targeted item name: %s", self.item)

        # Get the template to use
        self.template = args['--template']
        logger.info("Using the template: %s", self.template)

        if self.list and not self.item_type:
            self.item_type = self.item
            logger.info("Item type (computed): %s", self.item_type)

        # Get the targeted item
        self.data = args['--data']
        logger.info("Item data provided: %s", self.data)

    def initialize(self):
        # pylint: disable=attribute-defined-outside-init
        """
        Login on backend with username and password

        :return: None
        """
        try:
            logger.info("Authenticating...")
            # Backend authentication with token generation
            # headers = {'Content-Type': 'application/json'}
            # payload = {'username': self.username, 'password': self.password, 'action': 'generate'}
            self.backend = Backend(self.backend_url)
            self.backend.login(self.username, self.password)
        except BackendException as e:
            print("Backend exception: %s" % str(e))

        if self.backend.token is None:
            print("Access denied!")
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~")
            print("Exiting with error code: 1")
            exit(1)

        logger.info("Authenticated.")

        # Default realm
        self.realm_all = ''
        self.default_realm = ''
        realms = self.backend.get_all('realm')
        for r in realms['_items']:
            if r['name'] == 'All' and r['_level'] == 0:
                self.realm_all = r['_id']
                logger.info("Found realm 'All': %s", self.realm_all)

        # Default timeperiods
        self.tp_always = None
        self.tp_never = None
        timeperiods = self.backend.get_all('timeperiod')
        for tp in timeperiods['_items']:
            if tp['name'] == '24x7':
                self.tp_always = tp['_id']
                logger.info("Found TP '24x7': %s", self.tp_always)
            if tp['name'].lower() == 'none' or tp['name'].lower() == 'none':
                self.tp_never = tp['_id']
                logger.info("Found TP 'Never': %s", self.tp_never)

        if self.verbose:
            users = self.backend.get_all('user')
            self.users_names = sorted([user['name'] for user in users['_items']])
            logger.info("Existing users: %s", ','.join(self.users_names))

            hosts = self.backend.get_all('host')
            self.hosts_names = sorted([host['name'] for host in hosts['_items']])
            logger.info("Existing hosts: %s", ','.join(self.hosts_names))

            params = {'where': json.dumps({'_is_template': True})}
            templates = self.backend.get_all('host', params=params)
            self.host_templates_names = sorted([template['name']
                                                for template in templates['_items']])
            logger.info("Existing host templates: %s", ','.join(self.hosts_names))

            params = {'where': json.dumps({'_is_template': True})}
            templates = self.backend.get_all('host', params=params)
            self.service_templates_names = sorted([template['name']
                                                   for template in templates['_items']])
            logger.info("Existing service templates: %s", ','.join(self.service_templates_names))

    def get_resource_list(self, resource_name):
        # pylint: disable=too-many-locals, too-many-nested-blocks
        """Get a specific resource list"""
        try:
            logger.info("Trying to get %s list", resource_name)

            params = {}
            if resource_name in self.embedded_resources:
                params.update({'embedded': json.dumps(self.embedded_resources[resource_name])})

            rsp = self.backend.get_all(resource_name, params=params)
            if len(rsp['_items']) > 0 and rsp['_status'] == 'OK':
                response = rsp['_items']

                logger.info("-> found %ss", resource_name)

                # Exists in the backend, we got the element
                if not self.dry_run:
                    logger.info("-> dumping %ss list", resource_name)
                    for item in response:
                        # Filter fields prefixed with an _ (internal backend fields)
                        for field in item.keys():
                            if field.startswith('_'):
                                if field not in ['_realm', '_sub_realm']:
                                    item.pop(field)
                                    continue

                            # Filter fields prefixed with an _ in embedded items
                            if resource_name in self.embedded_resources and \
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
                                    for embedded_field in embedded_item.keys():
                                        if embedded_field.startswith('_'):
                                            embedded_item.pop(embedded_field)

                        dump = json.dumps(response, indent=4,
                                          separators=(',', ': '), sort_keys=True)
                        if self.verbose:
                            print(dump)
                        try:
                            temp_d = tempfile.gettempdir()
                            path = os.path.join(temp_d, 'alignak-object-list-%ss.json'
                                                % (resource_name))
                            dfile = open(path, "wb")
                            dfile.write(dump)
                            dfile.close()
                        except (OSError, IndexError) as exp:
                            logger.exception("Error when writing the list dump file %s : %s",
                                             path, str(exp))

                    logger.info("-> dumped %ss list", resource_name)
                else:
                    logger.info("Dry-run mode: should have dumped an %s list", resource_name)

                return True
            else:
                logger.warning("-> %s list is empty", resource_name)
                return False

        except BackendException as e:
            print("Get error for '%s' list" % (resource_name))
            logger.exception(e)
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~")
            print("Exiting with error code: 5")
            return False

    def get_resource(self, resource_name, name):
        # pylint: disable=too-many-locals, too-many-nested-blocks
        """Get a specific resource by name"""
        try:
            logger.info("Trying to get %s: '%s'", resource_name, name)

            params = {'where': json.dumps({'name': name})}
            if resource_name in self.embedded_resources:
                params.update({'embedded': json.dumps(self.embedded_resources[resource_name])})

            response = self.backend.get(resource_name, params=params)
            if len(response['_items']) > 0:
                response = response['_items'][0]

                logger.info("-> found %s '%s': %s", resource_name, name, response['_id'])

                # Exists in the backend, we got the element
                if not self.dry_run:
                    logger.info("-> dumping %s: %s", resource_name, name)
                    # Filter fields prefixed with an _ (internal backend fields)
                    for field in response.keys():
                        if field.startswith('_'):
                            response.pop(field)
                            continue

                        # Filter fields prefixed with an _ in embedded items
                        if resource_name in self.embedded_resources and \
                                field in self.embedded_resources[resource_name]:
                            # Embedded items may be a list or a simple dictionary,
                            # always make it a list
                            embedded_items = response[field]
                            if not isinstance(response[field], list):
                                embedded_items = [response[field]]
                            # Filter fields in each embedded item
                            for embedded_item in embedded_items:
                                for embedded_field in embedded_item.keys():
                                    if embedded_field.startswith('_'):
                                        embedded_item.pop(embedded_field)

                    dump = json.dumps(response, indent=4,
                                      separators=(',', ': '), sort_keys=True)
                    print(dump)
                    try:
                        temp_d = tempfile.gettempdir()
                        path = os.path.join(temp_d, 'alignak-object-dump-%s-%s.json' %
                                            (resource_name, name))
                        dfile = open(path, "wb")
                        dfile.write(dump)
                        dfile.close()
                    except (OSError, IndexError) as exp:
                        logger.exception("Error when writing the dump file %s : %s", path, str(exp))

                    logger.info("-> dumped %s: %s", resource_name, name)
                else:
                    logger.info("Dry-run mode: should have dumped an %s '%s'",
                                resource_name, name)

                return True
            else:
                logger.warning("-> %s '%s' not found", resource_name, name)
                return False

        except BackendException as e:
            print("Get error for  '%s' : %s" % (resource_name, name))
            logger.exception(e)
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~")
            print("Exiting with error code: 5")
            return False

    def delete_resource(self, resource_name, name):
        """Delete a specific resource by name"""
        try:
            logger.info("Trying to get %s: '%s'", resource_name, name)

            params = {'where': json.dumps({'name': name})}
            response = self.backend.get(resource_name, params=params)
            if len(response['_items']) > 0:
                response = response['_items'][0]

                logger.info("-> found %s '%s': %s", resource_name, name, response['_id'])

                # Exists in the backend, we must delete the element...
                if not self.dry_run:
                    headers = {
                        'Content-Type': 'application/json',
                        'If-Match': response['_etag']
                    }
                    logger.info("-> deleting %s: %s", resource_name, name)
                    self.backend.delete(resource_name + '/' + response['_id'], headers)
                    logger.info("-> deleted %s: %s", resource_name, name)
                else:
                    response = {'_id': '_fake', '_etag': '_fake'}
                    logger.info("Dry-run mode: should have deleted an %s '%s'",
                                resource_name, name)
                logger.info("-> deleted: '%s': %s",
                            resource_name, response['_id'])

                return True
            else:
                logger.warning("-> %s template '%s' not found", resource_name, name)
                return False

        except BackendException as e:
            print("Deletion error for  '%s' : %s" % (resource_name, name))
            logger.exception(e)
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~")
            print("Exiting with error code: 5")
            return False

        return True

    def create_update_resource(self, resource_name, name, update=False):
        # pylint: disable=too-many-return-statements
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
        if self.data != 'none':
            try:
                if self.data == 'stdin':
                    inf = sys.stdin
                else:
                    inf = open(self.data)

                print(inf)
                json_data = json.load(inf)
                logger.info("Got provided data: %s", json_data)
                if inf is not sys.stdin:
                    inf.close()
            except IOError as e:
                logger.exception("Error reading data file: %s", e)
                return False
            except ValueError as e:
                logger.exception("Error malformed data file: %s", e)
                return False

        try:
            logger.info("Trying to get %s: '%s'", resource_name, name)

            params = {'where': json.dumps({'name': name})}
            response = self.backend.get(resource_name, params=params)
            if len(response['_items']) > 0:
                response = response['_items'][0]

                logger.info("-> found %s '%s': %s", resource_name, name, response['_id'])

                if not update:
                    logger.warning("-> %s should be updated and not created: %s",
                                   resource_name, name)
                    return False

                # Item data updated with provided information if some
                headers = {
                    'Content-Type': 'application/json',
                    'If-Match': response['_etag']
                }
                item_data = response
                if json_data is not None:
                    item_data.update(json_data)

                for field in item_data.copy():
                    logger.debug("Field: %s = %s", field, item_data[field])
                    # Filter Eve extra fields
                    if field in ['_created', '_updated', '_etag', '_links', '_status']:
                        item_data.pop(field)
                        continue
                    # Manage potential object link fields
                    if field in ['realm', 'command', 'timeperiod', 'host', 'grafana']:
                        try:
                            int(item_data[field])
                        except ValueError:
                            # Not an integer, consider an item name
                            params = {'where': json.dumps({'name': item_data[field]})}
                            response = self.backend.get(field, params=params)
                            if len(response['_items']) > 0:
                                response = response['_items'][0]
                                logger.info("Replaced %s = %s with found item _id",
                                            field, item_data[field])
                                item_data[field] = response['_id']
                        continue

                if '_realm' not in item_data:
                    item_data.update({'_realm': self.realm_all})

                # Exists in the backend, we should update if required...
                if not self.dry_run:
                    response = self.backend.patch(
                        resource_name + '/' + response['_id'], item_data,
                        headers=headers, inception=True
                    )
                else:
                    response = {'_id': '_fake', '_etag': '_fake'}
                    logger.info("Dry-run mode: should have updated an %s '%s' with %s",
                                resource_name, name, item_data)

                logger.info("-> updated: '%s': %s, with %s",
                            resource_name, response['_id'], item_data)

                return True
            else:
                logger.info("-> %s '%s' not existing, it can be created.", resource_name, name)

                host_template = None
                if self.template is not None:
                    logger.info("Trying to find the %s template: %s", resource_name, self.template)

                    params = {'where': json.dumps({'name': self.template, '_is_template': True})}
                    response = self.backend.get(resource_name, params=params)
                    if len(response['_items']) > 0:
                        host_template = response['_items'][0]

                        logger.info("-> %s template '%s': %s",
                                    resource_name, self.template, host_template['_id'])
                    else:
                        print("-> %s template '%s' not found" % (resource_name, self.template))
                        return False

                # Host data and template information if templating is required
                item_data = {
                    'name': name,
                }
                if host_template is not None:
                    item_data.update({'_templates': [host_template['_id']],
                                      '_templates_with_services': True})
                if json_data is not None:
                    item_data.update(json_data)

                for field in item_data.copy():
                    logger.debug("Field: %s = %s", field, item_data[field])
                    # Filter Eve extra fields
                    if field in ['_created', '_updated', '_etag', '_links', '_status']:
                        item_data.pop(field)
                        continue
                    # Manage potential object link fields
                    if field in ['realm', 'command', 'timeperiod', 'grafana']:
                        try:
                            int(item_data[field])
                        except ValueError:
                            # Not an integer, consider an item name
                            params = {'where': json.dumps({'name': item_data[field]})}
                            response = self.backend.get(field, params=params)
                            if len(response['_items']) > 0:
                                response = response['_items'][0]
                                logger.info("Replaced %s = %s with found item _id",
                                            field, item_data[field])
                                item_data[field] = response['_id']
                        continue

                if '_realm' not in item_data:
                    item_data.update({'_realm': self.realm_all})

                if not self.dry_run:
                    logger.info("-> trying to create the %s: %s, with: %s",
                                resource_name, name, item_data)
                    response = self.backend.post(resource_name, item_data, headers=None)
                else:
                    response = {'_id': '_fake', '_etag': '_fake'}
                    logger.info("Dry-run mode: should have created an %s '%s' with %s",
                                resource_name, name, item_data)
                logger.info("-> created: '%s': %s, with %s",
                            resource_name, response['_id'], item_data)

                return True
        except BackendException as e:
            print("Creation error for  '%s' : %s", resource_name, name)
            logger.exception(e)
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~")
            print("Exiting with error code: 5")
            return False


def main():
    """
    Main function
    """
    bc = BackendUpdate()
    bc.initialize()
    logger.debug("backend_client, version: %s", __version__)
    logger.debug("~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

    success = False
    if bc.item_type and bc.action == 'get':
        if bc.list:
            success = bc.get_resource_list(bc.item_type)
        else:
            success = bc.get_resource(bc.item_type, bc.item)

    if bc.item and bc.action in ['add', 'update']:
        success = bc.create_update_resource(bc.item_type, bc.item, bc.action == 'update')

    if bc.item and bc.action == 'delete':
        success = bc.delete_resource(bc.item_type, bc.item)

    if not success:
        logger.error("%s '%s' %s failed", bc.item_type, bc.item, bc.action)
        if not bc.verbose:
            logger.warning("Set verbose mode to have more information (-v)")
        exit(2)

    exit(0)


if __name__ == "__main__":  # pragma: no cover
    main()
