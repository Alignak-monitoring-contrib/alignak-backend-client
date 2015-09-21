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
from requests import Timeout
from requests.auth import HTTPBasicAuth

log = logging.getLogger(__name__)


class BackendException(Exception):
    """Specific backend exception"""
    def __init__(self, code, message):
        # Call the base class constructor with the parameters it needs
        super(BackendException, self).__init__(message)
        self.code = code
        self.message = message

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
        self.url_endpoint_root = endpoint
        self.token = None

    def login(self, username, password, generate='enabled'):
        """
        Log into the backend and get the token

        :param username: login name
        :type username: str
        :param password: password
        :type password: str
        :param generate: Can have these values: enabled | force | disabled
        :type generate: str
        :return: return True if authentication is successfull, otherwise False
        :rtype: bool
        """
        log.info(
            "request backend authentication for: %s, generate: %s",
            username, generate
        )

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
                ''.join([self.url_endpoint_root, 'login']),
                json=params,
                headers=headers
            )
            response.raise_for_status()
        except Timeout as e:
            log.error("Backend connection timeout, error: %s", str(e))
            raise BackendException(1002, "Backend connection timeout")
        except Exception as e:
            log.error("Backend connection exception, error: %s / %s", type(e), str(e))
            raise BackendException(1003, "Backend connection exception")

        resp = response.json()
        log.info(
            "authentication response: %s",
            resp
        )

        if '_status' in resp:
            # Considering an information is returned if a _status field is present ...
            log.warning("backend status: %s", resp['_status'])

        if '_error' in resp:
            # Considering a problem occured is an _error field is present ...
            error = resp['_error']
            log.error(
                "authentication, error: %s, %s",
                error['code'], error['message']
            )

            raise BackendException(error['code'], error['message'])

        else:
            if 'token' not in resp:  # pragma: no cover
                log.error("User authentication failed")
                raise BackendException(1003, "User authentication failed")

            if 'token' in resp:
                self.token = resp['token']
                self.authenticated = True
                log.info(
                    "user authenticated: %s, token: %s", username, self.token
                )
                return True
            elif generate == 'force':
                return False
            elif generate == 'disabled':
                return False
            elif generate == 'enabled':
                return self.login(username, password, 'force')
            return False

    def method_get(self, endpoint, allpages=True):
        """
        Get items or item in alignak backend

        :param endpoint: endpoint (API URL)
        :type endpoint: str
        :param allpages: if True get all pages, otherwise only the first page
        :type allpages: bool
        :return: list of properties when query item | list of items when get many items
        :rtype: list
        """
        if not self.token:
            return {}
        params = {'auth': HTTPBasicAuth(self.token, '')}
        response = requests.get(endpoint, params)
        resp = response.json()
        if '_items' in resp:
            items = resp['_items']
            if not allpages:
                return items
            if 'next' in resp['_links']:
                # It has pagination, so get items of all pages
                page_number = resp['_links']['next']['href'].split('page=')
                separator = '?'
                if '?page=' in endpoint:
                    endpoint_plit = endpoint.split('?page=')
                    endpoint = endpoint_plit[0]
                elif '?' in endpoint:
                    separator = '&'
                    if '&page=' in endpoint:
                        endpoint_plit = endpoint.split('&page=')
                        endpoint = endpoint_plit[0]
                next_response = self.method_get(separator.join(
                    [endpoint, ''.join(['page=', page_number[1]])]))
                items.extend(next_response)
            return items
        return resp

    def method_post(self, endpoint, data_json, headers):
        """
        Create a new item

        :param endpoint: endpoint (API URL)
        :type endpoint: str
        :param data_json: properties of item to create
        :type data_json:str
        :param headers: headers (example: Content-Type)
        :type headers: dict
        :return: response (creation information)
        :rtype: dict
        """
        if not self.token:
            return {}
        params = {'auth': HTTPBasicAuth(self.token, '')}
        params['headers'] = headers
        response = requests.post(endpoint, data_json, params)
        return response.json()

    def method_patch(self, endpoint, data_json, headers, stop_inception=False):
        """
        Method to update an item

        :param endpoint: endpoint (API URL)
        :type endpoint: str
        :param data_json: properties of item to update
        :type data_json:str
        :param headers: headers (example: Content-Type). 'If-Match' required
        :type headers: dict
        :param stop_inception: if false try to get the right etag
        :type stop_inception: bool
        :return: dictionary with response of update fields
        :rtype: dict
        """
        if not self.token:
            return {}
        params = {'auth': HTTPBasicAuth(self.token, '')}
        params['headers'] = headers
        response = requests.patch(endpoint, data_json, params)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 412:
            # 412 means Precondition failed
            # print(response.content)
            if 'Client and server etags don' in response.content:
                # update etag + retry
                if stop_inception:
                    return '{}'
                resp = self.method_get(endpoint)
                headers['If-Match'] = resp['_etag']
                return self.method_patch(endpoint, data_json, headers, True)
        else:
            # print("%s: %s for %s" % (response.status_code, response.content, endpoint))
            return response.json()

    def method_delete(self, endpoint):
        """
        Method to delete an item or all items

        :param endpoint: endpoint (API URL)
        :type endpoint: str
        :return: None
        """
        if not self.token:
            return {}
        params = {'auth': HTTPBasicAuth(self.token, '')}
        requests.delete(endpoint, params)
