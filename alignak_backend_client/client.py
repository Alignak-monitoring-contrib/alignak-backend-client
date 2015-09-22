#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Copyright (C) 2015-2015: AlignakBackend team, see AUTHORS.txt file for contributors
#
# This file is part of AlignakBackend.
#
# AlignakBackend is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# AlignakBackend is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with AlignakBackend.  If not, see <http://www.gnu.org/licenses/>.
"""
This module is a wrapper to get, post, patch, delete in alignak-backend
"""
import traceback
import logging

import json
import requests
from requests import Timeout, HTTPError
from requests.auth import HTTPBasicAuth

log = logging.getLogger(__name__)


class BackendException(Exception):
    """Specific backend exception
    Defined error codes:
    - 1000: general exception, message contains more information
    - 1001: backend access denied
    - 1002: backend connection timeout
    - 1003: backend uncatched HTTPError
    - 1004: backend token not provided on login, user is not yet authorized to log in
    - 1005: If-Match header is required for patching an object
    """
    def __init__(self, code, message, response=None):
        # Call the base class constructor with the parameters it needs
        super(BackendException, self).__init__(message)
        self.code = code
        self.message = message
        self.response = response

    def __str__(self):
        """Exception to String"""
        return "Backend error code %d: %s" % (self.code, self.message)


class Backend(object):
    """
    Backend class to communicate with alignak-backend
    """
    def __init__(self, endpoint):
        """
        Alignak backend

        :param endpoint: root endpoint (API URL)
        :type endpoint: str
        """
        self.connected = False
        self.authenticated = False
        if endpoint.endswith('/'):
            self.url_endpoint_root = endpoint[0:-1]
        else:
            self.url_endpoint_root = endpoint
        self.token = None

    def login(self, username, password, generate='enabled'):
        """
        Log into the backend and get the token

        generate parameter may have following values:
        - enabled: require current token (default)
        - force: force new token generation
        - disabled

        if login is:
        - accepted, returns True
        - refused, returns False

        In case of any error, raises a BackendException

        :param username: login name
        :type username: str
        :param password: password
        :type password: str
        :param generate: Can have these values: enabled | force | disabled
        :type generate: str
        :return: return True if authentication is successfull, otherwise False
        :rtype: bool
        """
        log.info("request backend authentication for: %s, generate: %s", username, generate)

        if not username or not password:
            raise BackendException(1001, "Missing mandatory parameters")

        self.authenticated = False
        self.token = None

        try:
            headers = {'Content-Type': 'application/json'}
            params = {'username': username, 'password': password}
            if generate == 'force':
                params['action'] = 'generate'

            response = requests.post(
                '/'.join([self.url_endpoint_root, 'login']),
                json=params,
                headers=headers
            )
            if response.status_code == 401:
                return False
            response.raise_for_status()
        except Timeout as e:  # pragma: no cover - need specific backend tests
            log.error("Backend connection timeout, error: %s", str(e))
            raise BackendException(1002, "Backend connection timeout")
        except HTTPError as e:  # pragma: no cover - need specific backend tests
            log.error("Backend HTTP error, error: %s", str(e))
            raise BackendException(1003, "Backend HTTPError: %s / %s" % (type(e), str(e)))
        except Exception as e:  # pragma: no cover - security ...
            log.error("Backend connection exception, error: %s / %s", type(e), str(e))
            raise BackendException(1000, "Backend exception: %s / %s" % (type(e), str(e)))

        resp = response.json()
        log.debug("authentication response: %s", resp)

        if '_status' in resp:  # pragma: no cover - need specific backend tests
            # Considering an information is returned if a _status field is present ...
            log.warning("backend status: %s", resp['_status'])

        if '_error' in resp:  # pragma: no cover - need specific backend tests
            # Considering a problem occured is an _error field is present ...
            error = resp['_error']
            log.error(
                "authentication, error: %s, %s",
                error['code'], error['message']
            )
            raise BackendException(error['code'], error['message'])

        else:
            if 'token' in resp:
                self.token = resp['token']
                self.authenticated = True
                log.info("user authenticated: %s", username)
                return True
            elif generate == 'force':  # pragma: no cover - need specific backend tests
                log.error("Token generation required but none provided.")
                raise BackendException(1004, "Token not provided")
            elif generate == 'disabled':  # pragma: no cover - need specific backend tests
                log.error("Token disabled ... to be implemented!")
                return False
            elif generate == 'enabled':  # pragma: no cover - need specific backend tests
                log.warning("Token enabled, but none provided, require new token generation")
                return self.login(username, password, 'force')

            return False  # pragma: no cover - unreachable ...

    def logout(self):
        """
        Logout from the backend

        :return: return True if logout is successfull, otherwise False
        :rtype: bool
        """
        if not self.token or not self.authenticated:
            log.warning("Unnecessary logout ...")
            return True

        log.info("request backend logout")

        try:
            response = requests.post(
                '/'.join([self.url_endpoint_root, 'logout']),
                auth=HTTPBasicAuth(self.token, '')
            )
            response.raise_for_status()
        except Timeout as e:  # pragma: no cover - need specific backend tests
            log.error("Backend connection timeout, error: %s", str(e))
            raise BackendException(1002, "Backend connection timeout")
        except HTTPError as e:  # pragma: no cover - need specific backend tests
            log.error("Backend HTTP error, error: %s", str(e))
            raise BackendException(1003, "Backend HTTPError: %s / %s" % (type(e), str(e)))
        except Exception as e:  # pragma: no cover - security ...
            log.error("Backend connection exception, error: %s / %s", type(e), str(e))
            raise BackendException(1000, "Backend exception: %s / %s" % (type(e), str(e)))

        self.authenticated = False
        self.token = None

        return True

    def get_domains(self):
        """
        Connect to alignak backend and retrieve all available child endpoints of root

        If connection is successfull, returns a list of all the resources available in the backend:
        Each resource is identified with its title and provides its endpoint relative to backend
        root endpoint.
            [
                {u'href': u'loghost', u'title': u'loghost'},
                {u'href': u'escalation', u'title': u'escalation'},
                ...
            ]

        If an error occurs a BackendException is raised.

        If an exception occurs, it is raised to caller.

        :return: list of available resources
        :rtype: list
        """
        if not self.token:
            log.error("Authentication is required for getting an object.")
            raise BackendException(1001, "Access denied, please login before trying to get")

        log.debug("trying to get domains from backend: %s", self.url_endpoint_root)

        resp = self.get('')
        log.debug("received domains data: %s", resp)
        if "_links" in resp:
            _links = resp["_links"]
            if "child" in _links:
                return _links["child"]

        return {}  # pragma: no cover - should never occur!

    def get(self, endpoint, params=None):
        """
        Get items or item in alignak backend

        If an error occurs, a BackendException is raised.

        :param endpoint: endpoint (API URL) relative from root endpoint
        :type endpoint: str
        :param params: list of parameters for the backend API
        :type params: list
        :return: list of properties when query item | list of items when get many items
        :rtype: list
        """
        if not self.token:
            log.error("Authentication is required for getting an object.")
            raise BackendException(1001, "Access denied, please login before trying to get")

        log.debug("get, endpoint: %s, parameters: %s", endpoint, params)

        response = requests.get(
            '/'.join([self.url_endpoint_root, endpoint]),
            params=params,
            auth=HTTPBasicAuth(self.token, '')
        )
        resp = response.json()
        if '_status' in resp:  # pragma: no cover - need specific backend tests
            # Considering an information is returned if a _status field is present ...
            log.warning("backend status: %s", resp['_status'])

        if '_error' in resp:  # pragma: no cover - need specific backend tests
            # Considering a problem occured is an _error field is present ...
            error = resp['_error']
            log.error("backend error: %s, %s", error['code'], error['message'])
            raise BackendException(error['code'], error['message'])

        log.debug("get, endpoint: %s, response: %s", endpoint, resp)

        return resp

    def get_all(self, endpoint, params=None):
        """
        Get all items in the specified endpoint of alignak backend

        If an error occurs, a BackendException is raised.

        If the max_results parameter is not specified in parameters, it is set to 200
        (backend maximum value) to limit requests number.

        :param endpoint: endpoint (API URL) relative from root endpoint
        :type endpoint: str
        :param params: list of parameters for the backend API
        :type params: list
        :return: list of properties when query item | list of items when get many items
        :rtype: list
        """
        if not self.token:
            log.error("Authentication is required for getting an object.")
            raise BackendException(1001, "Access denied, please login before trying to get")

        log.debug("get_all, endpoint: %s, parameters: %s", endpoint, params)

        # Set max results at maximum value supported by the backend to limit requests number
        if not params:
            params = {'max_results': 200}
        elif params and 'max_results' not in params:
            params['max_results'] = 200

        # Get first page
        last_page = False
        items = []
        while not last_page:
            # Get elements ...
            resp = self.get(endpoint, params)
            # Response contains:
            # _items:
            # ...
            # _links:
            #  self, parent, prev, last, next
            # _meta:
            # - max_results, total, page

            page_number = int(resp['_meta']['page'])
            max_results = int(resp['_meta']['max_results'])

            if 'next' in resp['_links']:
                # Go to next page ...
                params['page'] = page_number + 1
                params['max_results'] = max_results
            else:
                last_page = True
            items.extend(resp['_items'])

        return items

    def post(self, endpoint, data, headers=None):
        """
        Create a new item

        :param endpoint: endpoint (API URL)
        :type endpoint: str
        :param data: properties of item to create
        :type data:str
        :param headers: headers (example: Content-Type)
        :type headers: dict
        :return: response (creation information)
        :rtype: dict
        """
        if not self.token:
            log.error("Authentication is required for deleting an object.")
            raise BackendException(1001, "Access denied, please login before trying to post")

        if not headers:
            headers = {'Content-Type': 'application/json'}

        response = requests.post(
            '/'.join([self.url_endpoint_root, endpoint]),
            json=data,
            headers=headers,
            auth=HTTPBasicAuth(self.token, '')
        )
        resp = response.json()
        if '_status' in resp:
            # Considering an information is returned if a _status field is present ...
            log.warning("backend status: %s", resp['_status'])

        if '_error' in resp:  # pragma: no cover - need specific backend tests
            # Considering a problem occured is an _error field is present ...
            error = resp['_error']
            log.error("backend error: %s, %s", error['code'], error['message'])
            if '_issues' in resp:
                for issue in resp['_issues']:
                    log.error(" - issue: %s: %s", issue, resp['_issues'][issue])
            raise BackendException(error['code'], error['message'], resp)

        return resp

    def patch(self, endpoint, data, headers=None, inception=False):
        """
        Method to update an item

        :param endpoint: endpoint (API URL)
        :type endpoint: str
        :param data: properties of item to update
        :type data:str
        :param headers: headers (example: Content-Type). 'If-Match' required
        :type headers: dict
        :param inception: if True tries to get the last _etag
        :type inception: bool
        :return: dictionary with response of update fields
        :rtype: dict
        """
        if not self.token:
            log.error("Authentication is required for deleting an object.")
            raise BackendException(1001, "Access denied, please login before trying to patch")

        if not headers:
            log.error("Header If-Match is required for patching an object.")
            raise BackendException(1005, "Header If-Match required for patching an object")

        response = requests.patch(
            '/'.join([self.url_endpoint_root, endpoint]),
            json=data,
            headers=headers,
            auth=HTTPBasicAuth(self.token, '')
        )
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 412:
            # 412 means Precondition failed
            if 'Client and server etags don' in response.content:
                # update etag + retry
                if inception:
                    resp = self.get(endpoint)
                    headers['If-Match'] = resp['_etag']
                    return self.patch(
                        endpoint,
                        data=data, headers=headers, inception=False
                    )
                else:
                    raise BackendException(412, response.content)
        else:  # pragma: no cover - should never occur
            return response.json()

    def delete(self, endpoint, headers):
        """
        Method to delete an item or all items

        headers['If-Match'] must contain the _etag identifier of the element to delete

        :param endpoint: endpoint (API URL)
        :type endpoint: str
        :param headers: headers (example: Content-Type)
        :type headers: dict
        :return: response (creation information)
        :rtype: dict
        """
        if not self.token:
            log.error("Authentication is required for deleting an object.")
            raise BackendException(1001, "Access denied, please login before trying to delete")

        try:
            response = requests.delete(
                '/'.join([self.url_endpoint_root, endpoint]),
                headers=headers,
                auth=HTTPBasicAuth(self.token, '')
            )
            if response.status_code != 204:
                response.raise_for_status()
        except Timeout as e:  # pragma: no cover - need specific backend tests
            log.error("Backend connection timeout, error: %s", str(e))
            raise BackendException(1002, "Backend connection timeout")
        except HTTPError as e:  # pragma: no cover - need specific backend tests
            log.error("Backend HTTP error, error: %s", str(e))
            raise BackendException(1003, "Backend HTTPError: %s / %s" % (type(e), str(e)))
        except Exception as e:  # pragma: no cover - security ...
            log.error("Backend connection exception, error: %s / %s", type(e), str(e))
            raise BackendException(1000, "Backend exception: %s / %s" % (type(e), str(e)))

        return {}
