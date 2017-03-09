#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Copyright (C) 2015-2016: AlignakBackend team, see AUTHORS.txt file for contributors
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
    Alignak REST backend client library
    ===================================

    This module is a Python library used for connecting to an Alignak backend.

    The `Backend` class implements the necessary methods to establish a connection
    and interact with the backend REST API.

    Backend interaction will necessarily start with a `login` and end with a `logout`. In
    between, using the `get`, `post`, `patch` and `delete` functions will allow to manipulate
    the backend elements.

    The Alignak backend data model is `documented here <http://alignak-backend.readthedocs.io/>`_.
"""
import json
import traceback
import logging
from logging import getLogger, WARNING

import math
import multiprocessing

from future.moves.urllib.parse import urljoin

import requests
from requests import Timeout, HTTPError
from requests import ConnectionError as RequestsConnectionError
from requests.auth import HTTPBasicAuth


logger = getLogger(__name__)
# Check if logger has already handler to prevent override it
if logger.handlers:
    logger.addHandler(logger.handlers)
else:
    logging.basicConfig()
# Set logger level to WARNING, this to allow global application DEBUG logs without being spammed...
logger.setLevel(WARNING)

# Disable default logs for requests and urllib3 libraries ...
getLogger("requests").setLevel(WARNING)
getLogger("urllib3").setLevel(WARNING)

# Define pagination limits according to backend's ones!
BACKEND_PAGINATION_LIMIT = 50
BACKEND_PAGINATION_DEFAULT = 25


class BackendException(Exception):
    """Specific backend exception class.
    This specific exception is raised by the module when an error is encountered.

    It provides an error code, an error message and the backend response.

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
    Backend client class to communicate with an Alignak backend

    Provide the backend endpoint URL to initialize the client (eg. http://127.0.0.1:5000)

    """
    def __init__(self, endpoint, processes=1):
        """
        Initialize a client connection

        :param endpoint: root endpoint (API URL)
        :type endpoint: str
        """
        self.connected = False
        self.authenticated = False
        self.processes = processes
        if endpoint.endswith('/'):  # pragma: no cover - test url is complying ...
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
        logger.debug("request backend authentication for: %s, generate: %s", username, generate)

        if not username or not password:
            raise BackendException(1001, "Missing mandatory parameters")

        self.authenticated = False
        self.token = None

        try:
            headers = {'Content-Type': 'application/json'}
            params = {u'username': username, u'password': password}
            if generate == 'force':
                params['action'] = 'generate'

            response = requests.post(
                urljoin(self.url_endpoint_root, 'login'),
                json=params,
                headers=headers
            )
            if response.status_code == 401:
                logger.debug("authentication refused: %s", response.content)
                return False
            response.raise_for_status()
        except Timeout as e:  # pragma: no cover - need specific backend tests
            logger.error("Backend connection timeout, error: %s", str(e))
            raise BackendException(1002, "Backend connection timeout")
        except HTTPError as e:  # pragma: no cover - need specific backend tests
            logger.error("Backend HTTP error, error: %s", str(e))
            raise BackendException(1003, "Backend HTTPError: %s / %s" % (type(e), str(e)))
        except RequestsConnectionError as e:
            logger.error("Backend connection error, error: %s", str(e))
            raise BackendException(1000, "Backend connection error")
        except Exception as e:  # pragma: no cover - security ...
            logger.error("Backend connection exception, error: %s / %s", type(e), str(e))
            raise BackendException(1000, "Backend is not available")

        resp = response.json()
        logger.debug("authentication response: %s", resp)

        if '_status' in resp:  # pragma: no cover - need specific backend tests
            # Considering an information is returned if a _status field is present ...
            logger.debug("backend status: %s", resp['_status'])

        if '_error' in resp:  # pragma: no cover - need specific backend tests
            # Considering a problem occured is an _error field is present ...
            error = resp['_error']
            logger.error(
                "authentication, error: %s, %s",
                error['code'], error['message']
            )
            raise BackendException(error['code'], error['message'])

        else:
            if 'token' in resp:
                self.token = resp['token']
                self.authenticated = True
                logger.debug("user authenticated: %s", username)
                return True
            elif generate == 'force':  # pragma: no cover - need specific backend tests
                logger.error("Token generation required but none provided.")
                raise BackendException(1004, "Token not provided")
            elif generate == 'disabled':  # pragma: no cover - need specific backend tests
                logger.error("Token disabled ... to be implemented!")
                return False
            elif generate == 'enabled':  # pragma: no cover - need specific backend tests
                logger.warning("Token enabled, but none provided, require new token generation")
                return self.login(username, password, 'force')

            return False  # pragma: no cover - unreachable ...

    def logout(self):
        """
        Logout from the backend

        :return: return True if logout is successfull, otherwise False
        :rtype: bool
        """
        if not self.token or not self.authenticated:
            logger.warning("Unnecessary logout ...")
            return True

        logger.debug("request backend logout")

        try:
            response = requests.post(
                urljoin(self.url_endpoint_root, 'logout'),
                auth=HTTPBasicAuth(self.token, '')
            )
            response.raise_for_status()
        except Timeout as e:  # pragma: no cover - need specific backend tests
            logger.error("Backend connection timeout, error: %s", str(e))
            raise BackendException(1002, "Backend connection timeout")
        except HTTPError as e:  # pragma: no cover - need specific backend tests
            logger.error("Backend HTTP error, error: %s", str(e))
            raise BackendException(1003, "Backend HTTPError: %s / %s" % (type(e), str(e)))
        except RequestsConnectionError as e:  # pragma: no cover - need specific backend tests
            logger.error("Backend connection error, error: %s", str(e))
            raise BackendException(1000, "Backend connection error")
        except Exception as e:  # pragma: no cover - security ...
            logger.error("Backend connection exception, error: %s / %s", type(e), str(e))
            raise BackendException(1000, "Backend exception: %s / %s" % (type(e), str(e)))

        self.authenticated = False
        self.token = None

        return True

    def get_domains(self):
        """
        Connect to alignak backend and retrieve all available child endpoints of root

        If connection is successful, returns a list of all the resources available in the backend:
        Each resource is identified with its title and provides its endpoint relative to backend
        root endpoint.::

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
            logger.error("Authentication is required for getting an object.")
            raise BackendException(1001, "Access denied, please login before trying to get")

        logger.debug("trying to get domains from backend: %s", self.url_endpoint_root)

        resp = self.get('')
        logger.debug("received domains data: %s", resp)
        if "_links" in resp:
            _links = resp["_links"]
            if "child" in _links:
                return _links["child"]

        return {}  # pragma: no cover - should never occur!

    def get(self, endpoint, params=None):
        """
        Get items or item in alignak backend

        If an error occurs, a BackendExcehi spea1ption is raised.

        This method builds a response that always contains: _items and _status::

            {
                u'_items': [
                    ...
                ],
                u'_status': u'OK'
            }

        :param endpoint: endpoint (API URL) relative from root endpoint
        :type endpoint: str
        :param params: list of parameters for the backend API
        :type params: list
        :return: list of properties when query item | list of items when get many items
        :rtype: list
        """
        if not self.token:
            logger.error("Authentication is required for getting an object.")
            raise BackendException(1001, "Access denied, please login before trying to get")

        try:
            logger.debug(
                "get, endpoint: %s, parameters: %s",
                urljoin(self.url_endpoint_root, endpoint),
                params
            )
            response = requests.get(
                urljoin(self.url_endpoint_root, endpoint),
                params=params,
                auth=HTTPBasicAuth(self.token, '')
            )
            logger.debug("get, response: %s", response)
            response.raise_for_status()

        except RequestsConnectionError as e:
            logger.error("Backend connection error, error: %s", str(e))
            raise BackendException(1000, "Backend connection error")

        except HTTPError as e:  # pragma: no cover - need specific backend tests
            if e.response.status_code == 404:
                raise BackendException(404, 'Not found')

            logger.error("Backend HTTP error, error: %s", str(e))
            raise BackendException(1003, "Backend HTTPError: %s / %s" % (type(e), str(e)))
        resp = response.json()
        if '_status' in resp:  # pragma: no cover - need specific backend tests
            # Considering an information is returned if a _status field is present ...
            logger.debug("backend status: %s", resp['_status'])
        else:
            resp['_status'] = 'OK'

        if '_error' in resp:  # pragma: no cover - need specific backend tests
            # Considering a problem occured is an _error field is present ...
            error = resp['_error']
            error['message'] = "Url: %s. Message: %s" % (endpoint, error['message'])
            logger.error("backend error: %s, %s", error['code'], error['message'])
            raise BackendException(error['code'], error['message'])

        # logger.debug("get, endpoint: %s, response: %s", endpoint, resp)

        return resp

    def get_all(self, endpoint, params=None):
        """
        Get all items in the specified endpoint of alignak backend

        If an error occurs, a BackendException is raised.

        If the max_results parameter is not specified in parameters, it is set to
        BACKEND_PAGINATION_LIMIT (backend maximum value) to limit requests number.

        This method builds a response that always contains: _items and _status::

            {
                u'_items': [
                    ...
                ],
                u'_status': u'OK'
            }

        :param endpoint: endpoint (API URL) relative from root endpoint
        :type endpoint: str
        :param params: list of parameters for the backend API
        :type params: list
        :return: list of properties when query item | list of items when get many items
        :rtype: list
        """
        if not self.token:
            logger.error("Authentication is required for getting an object.")
            raise BackendException(1001, "Access denied, please login before trying to get")

        logger.debug("get_all, endpoint: %s, parameters: %s", endpoint, params)

        # Set max results at maximum value supported by the backend to limit requests number
        if not params:
            params = {'max_results': BACKEND_PAGINATION_LIMIT}
        elif params and 'max_results' not in params:
            params['max_results'] = BACKEND_PAGINATION_LIMIT

        # Get first page
        last_page = False
        items = []
        if self.processes == 1:
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

                if 'next' in resp['_links']:
                    # Go to next page ...
                    params['page'] = int(resp['_meta']['page']) + 1
                    params['max_results'] = int(resp['_meta']['max_results'])
                else:
                    last_page = True
                items.extend(resp['_items'])
        else:
            def get_pages(endpoint, params, pages, out_q):
                """
                Function to get pages loaded by multiprocesses

                :param endpoint: endpoint to get data
                :type endpoint: string
                :param params: parameters for get request
                :type params: dict
                :param pages: range of pages to get
                :type pages: list
                :param out_q: Queue object
                :type out_q: object
                :return: None
                """
                multi_items = []
                for page in pages:
                    params['page'] = page
                    resp = self.get(endpoint, params)
                    multi_items.extend(resp['_items'])
                out_q.put(multi_items)

            # Get first page
            resp = self.get(endpoint, params)
            number_pages = int(math.ceil(
                float(resp['_meta']['total']) / float(resp['_meta']['max_results'])))

            out_q = multiprocessing.Queue()
            chunksize = int(math.ceil(number_pages / float(self.processes)))
            procs = []
            for i in range(self.processes):
                begin = i * chunksize
                end = begin + chunksize
                if end > number_pages:
                    end = number_pages
                begin += 1
                end += 1
                p = multiprocessing.Process(target=get_pages,
                                            args=(endpoint, params, range(begin, end), out_q))
                procs.append(p)
                p.start()

            # Collect all results into a single result dict. We know how many dicts
            # with results to expect.
            for i in range(self.processes):
                items.extend(out_q.get())

            # Wait for all worker processes to finish
            for p in procs:
                p.join()

        return {
            '_items': items,
            '_status': 'OK'
        }

    def post(self, endpoint, data, files=None, headers=None):
        """
        Create a new item

        :param endpoint: endpoint (API URL)
        :type endpoint: str
        :param data: properties of item to create
        :type data: dict
        :param headers: headers (example: Content-Type)
        :type headers: dict
        :return: response (creation information)
        :rtype: dict
        """
        if not self.token:
            logger.error("Authentication is required for adding an object.")
            raise BackendException(1001, "Access denied, please login before trying to post")

        if not headers:
            headers = {'Content-Type': 'application/json'}
            if isinstance(data, dict):
                data = json.dumps(data)

        logger.debug("post, endpoint: %s", urljoin(self.url_endpoint_root, endpoint))
        logger.debug("post, headers: %s", headers)
        logger.debug("post, data: %s = %s", type(data), data)
        logger.debug("post, files: %s", files)
        try:
            if not files:
                response = requests.post(
                    urljoin(self.url_endpoint_root, endpoint),
                    data=data,
                    files=files,
                    headers=headers,
                    auth=HTTPBasicAuth(self.token, '')
                )
                resp = response.json()
            else:
                # Posting files is not yet used, but reserved for future use...
                response = requests.post(
                    urljoin(self.url_endpoint_root, endpoint),
                    data=data,
                    files=files,
                    auth=HTTPBasicAuth(self.token, '')
                )
                resp = json.loads(response.content)
            logger.debug("post, response: %s", resp)
        except ValueError as e:  # pragma: no cover - should never happen now...
            logger.error("Exception, error: %s", str(e))
            logger.error("traceback: %s", traceback.format_exc())
            raise BackendException(1003, "Exception: %s" % (str(e)))

        except RequestsConnectionError as e:
            logger.error("Backend connection error, error: %s", str(e))
            raise BackendException(1000, "Backend connection error")

        except Exception as e:  # pragma: no cover - should never happen now...
            logger.error("Exception, error: %s", str(e))
            logger.error("traceback: %s", traceback.format_exc())
            # resp = response
            logger.error(
                "Response is not JSON formatted: %d / %s", response.status_code, response.content
            )
            raise BackendException(
                1003, "Response is not JSON formatted: %s" % (response.content), response
            )

        if '_status' in resp:
            # Considering an information is returned if a _status field is present ...
            logger.debug("backend status: %s", resp['_status'])

        if '_error' in resp:  # pragma: no cover - need specific backend tests
            # Considering a problem occured is an _error field is present ...
            error = resp['_error']
            logger.error("backend error: %s, %s", error['code'], error['message'])
            if '_issues' in resp:
                for issue in resp['_issues']:
                    logger.error(" - issue: %s: %s", issue, resp['_issues'][issue])
            raise BackendException(error['code'], error['message'], resp)

        return resp

    def patch(self, endpoint, data, headers=None, inception=False):
        """
        Method to update an item

        The headers must include an If-Match containing the object _etag.
            headers = {'If-Match': contact_etag}

        The data dictionary contain the fields that must be modified.

        If the patching fails because the _etag object do not match with the provided one, a
        BackendException is raised with code = 412.

        If inception is True, this method makes e new get request on the endpoint to refresh the
        _etag and then a new patch is called.

        If an HTTP 412 error occurs, a BackendException is raised. This exception is:
        - code: 412
        - message: response content
        - response: backend response

        All other HTTP error raises a BackendException.
        If some _issues are provided by the backend, this exception is:
        - code: HTTP error code
        - message: response content
        - response: JSON encoded backend response (including '_issues' dictionary ...)

        If no _issues are provided and an _error is signaled by the backend, this exception is:
        - code: backend error code
        - message: backend error message
        - response: JSON encoded backend response

        :param endpoint: endpoint (API URL)
        :type endpoint: str
        :param data: properties of item to update
        :type data: dict
        :param headers: headers (example: Content-Type). 'If-Match' required
        :type headers: dict
        :param inception: if True tries to get the last _etag
        :type inception: bool
        :return: dictionary containing patch response from the backend
        :rtype: dict
        """
        if not self.token:
            logger.error("Authentication is required for patching an object.")
            raise BackendException(1001, "Access denied, please login before trying to patch")

        if not headers:
            logger.error("Header If-Match is required for patching an object.")
            raise BackendException(1005, "Header If-Match required for patching an object")

        logger.debug("patch, endpoint: %s", urljoin(self.url_endpoint_root, endpoint))
        logger.debug("patch, headers: %s", headers)
        logger.debug("patch, data: %s", data)
        try:
            response = requests.patch(
                urljoin(self.url_endpoint_root, endpoint),
                json=data,
                headers=headers,
                auth=HTTPBasicAuth(self.token, '')
            )
        except RequestsConnectionError as e:
            logger.error("Backend connection error, error: %s", str(e))
            raise BackendException(1000, "Backend connection error")

        except Exception as e:  # pragma: no cover - should never happen now...
            logger.error("Exception, error: %s", str(e))
            logger.error("traceback: %s", traceback.format_exc())
            raise BackendException(
                1003, "Exception error: %s" % (str(e)), response
            )

        logger.debug("patch, response: %s", response)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 412:
            # 412 means Precondition failed, but confirm ...
            if inception:
                # update etag and retry to patch
                resp = self.get(endpoint)
                headers['If-Match'] = resp['_etag']
                return self.patch(
                    endpoint,
                    data=data, headers=headers, inception=False
                )
            else:
                raise BackendException(412, response.content, response)
        else:  # pragma: no cover - should never occur
            logger.error(
                "Patching failed, response is: %d / %s",
                response.status_code, response.content
            )
            resp = response.json()
            if '_status' in resp:
                # Considering an information is returned if a _status field is present ...
                logger.debug("backend status: %s", resp['_status'])

            if '_issues' in resp:
                for issue in resp['_issues']:
                    logger.error(" - issue: %s: %s", issue, resp['_issues'][issue])
                raise BackendException(response.status_code, response.content, resp)

            if '_error' in resp:  # pragma: no cover - need specific backend tests
                # Considering a problem occured if an _error field is present ...
                error = resp['_error']
                logger.error("backend error: %s, %s", error['code'], error['message'])
                raise BackendException(error['code'], error['message'], resp)

            return response.json()

    def delete(self, endpoint, headers):
        """
        Method to delete an item or all items

        headers['If-Match'] must contain the _etag identifier of the element to delete

        :param endpoint: endpoint (API URL)
        :type endpoint: str
        :param headers: headers (example: Content-Type)
        :type headers: dict
        :return: response (deletion information)
        :rtype: dict
        """
        if not self.token:
            logger.error("Authentication is required for deleting an object.")
            raise BackendException(1001, "Access denied, please login before trying to delete")

        logger.debug("delete, endpoint: %s", urljoin(self.url_endpoint_root, endpoint))
        logger.debug("delete, headers: %s", headers)
        try:
            response = requests.delete(
                urljoin(self.url_endpoint_root, endpoint),
                headers=headers,
                auth=HTTPBasicAuth(self.token, '')
            )
            logger.debug("delete, response: %s", response)
            if response.status_code != 204:  # pragma: no cover - should not happen ...
                response.raise_for_status()

            response = {"_status": "OK"}
            return response
        except Timeout as e:  # pragma: no cover - need specific backend tests
            logger.error("Backend connection timeout, error: %s", str(e))
            raise BackendException(1002, "Backend connection timeout")
        except HTTPError as e:  # pragma: no cover - need specific backend tests
            logger.error("Backend HTTP error, error: %s", str(e))
            raise BackendException(1003, "Backend HTTPError: %s / %s" % (type(e), str(e)))
        except Exception as e:  # pragma: no cover - security ...
            logger.error("Backend connection exception, error: %s / %s", type(e), str(e))
            raise BackendException(1000, "Backend exception: %s / %s" % (type(e), str(e)))
