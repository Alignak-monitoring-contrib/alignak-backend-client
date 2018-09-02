#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=fixme

#
# Copyright (C) 2015-2018: AlignakBackend team, see AUTHORS.txt file for contributors
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
import logging
from logging import getLogger

import math
import multiprocessing

from future.moves.urllib.parse import urljoin

import requests
from requests import RequestException
from requests.auth import HTTPBasicAuth
from requests.adapters import HTTPAdapter
# from requests.packages.urllib3 import Retry
from urllib3.util import Retry

logger = getLogger(__name__)
# Check if logger has already handler to prevent override it
if logger.handlers:
    logger.addHandler(logger.handlers)
else:
    logging.basicConfig()
# Set logger level to WARNING, this to allow global application DEBUG logs without being spammed...
logger.setLevel('WARNING')

# Disable default logs for requests and urllib3 libraries ...
getLogger("requests").setLevel('WARNING')
getLogger("urllib3").setLevel('WARNING')

# Define pagination limits according to backend's ones!
BACKEND_PAGINATION_LIMIT = 50
BACKEND_PAGINATION_DEFAULT = 25

# Proxy protocols
PROXY_PROTOCOLS = ['http', 'https']

# Connection error code
BACKEND_ERROR = 1000


class BackendException(Exception):
    """Specific backend exception class.
    This specific exception is raised by the module when an error is encountered.

    It provides an error code, an error message and the backend response.

    Defined error codes:

    - 1000: first stage error, exception raising between the client and the backend when connecting
    - <1000: second stage error. Connection between client and backend is ok,
    but the backend returns errors on
    requests
    """
    # TODO: create a special Exception for managing problems in the session,
    # and another inside the response decoding
    def __init__(self, code, message, response=None):
        # Call the base class constructor with the parameters it needs
        super(BackendException, self).__init__(message)
        self.code = code
        self.message = message
        self.response = response
        logger.error(self.__str__())

    def __str__(self):
        """Exception to String"""
        if self.response and not isinstance(self.response, dict):
            return "BackendException raised with code {0} and message:" \
                   " {1} - {2}".format(self.code, self.message, self.response.content)

        return "BackendException raised with code {0} and message:" \
               " {1} - {2}".format(self.code, self.message, self.response)


class Backend(object):  # pylint: disable=useless-object-inheritance
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
        self.processes = processes
        if endpoint.endswith('/'):  # pragma: no cover - test url is complying ...
            self.url_endpoint_root = endpoint[0:-1]
        else:
            self.url_endpoint_root = endpoint

        self.session = requests.Session()
        self.session.header = {'Content-Type': 'application/json'}

        # Needed for retrying requests (104 - Connection reset by peer for example)
        methods = ['POST', 'HEAD', 'GET', 'PUT', 'DELETE', 'PATCH']
        http_retry = Retry(total=5, connect=5, read=5, backoff_factor=0.1,
                           method_whitelist=methods)
        https_retry = Retry(total=5, connect=5, read=5, backoff_factor=0.1,
                            method_whitelist=methods)
        http_adapter = HTTPAdapter(max_retries=http_retry)
        https_adapter = HTTPAdapter(max_retries=https_retry)
        self.session.mount('http://', http_adapter)
        self.session.mount('https://', https_adapter)

        self.authenticated = False
        self._token = None
        self.proxies = None

        self.timeout = None  # TODO: Add this option in config file

    def get_url(self, endpoint):
        """
        Returns the formated full URL endpoint
        :param endpoint: str. the relative endpoint to access
        :return: str
        """
        return urljoin(self.url_endpoint_root, endpoint)

    def get_response(self, method, endpoint, headers=None, json=None, params=None, data=None):
        # pylint: disable=too-many-arguments
        """
        Returns the response from the requested endpoint with the requested method
        :param method: str. one of the methods accepted by Requests ('POST', 'GET', ...)
        :param endpoint: str. the relative endpoint to access
        :param params: (optional) Dictionary or bytes to be sent in the query string
        for the :class:`Request`.
        :param data: (optional) Dictionary, bytes, or file-like object to send in the body
        of the :class:`Request`.
        :param json: (optional) json to send in the body of the :class:`Request`.
        :param headers: (optional) Dictionary of HTTP Headers to send with the :class:`Request`.
        :return: Requests.response
        """
        logger.debug("Parameters for get_response:")
        logger.debug("\t - endpoint: %s", endpoint)
        logger.debug("\t - method: %s", method)
        logger.debug("\t - headers: %s", headers)
        logger.debug("\t - json: %s", json)
        logger.debug("\t - params: %s", params)
        logger.debug("\t - data: %s", data)

        url = self.get_url(endpoint)

        # First stage. Errors are connection errors (timeout, no session, ...)
        try:
            response = self.session.request(method=method, url=url, headers=headers, json=json,
                                            params=params, data=data, proxies=self.proxies,
                                            timeout=self.timeout)
            logger.debug("response headers: %s", response.headers)
            logger.debug("response content: %s", response.content)
        except RequestException as e:
            response = {"_status": "ERR",
                        "_error": {"message": e, "code": BACKEND_ERROR},
                        "_issues": {"message": e, "code": BACKEND_ERROR}}
            raise BackendException(code=BACKEND_ERROR,
                                   message=e,
                                   response=response)
        else:
            return response

    @staticmethod
    def decode(response):
        """
        Decodes and returns the response as JSON (dict) or raise BackendException
        :param response: requests.response object
        :return: dict
        """

        # Second stage. Errors are backend errors (bad login, bad url, ...)
        try:
            response.raise_for_status()
        except requests.HTTPError as e:
            raise BackendException(code=response.status_code,
                                   message=e,
                                   response=response)
        else:
            resp_json = response.json()
            # Catch errors not sent in a HTTP error
            error = resp_json.get('_error', None)
            if error:
                raise BackendException(code=error['code'],
                                       message=error['message'],
                                       response=response)
            return resp_json

    def set_token(self, token):
        """
        Set token in authentification for next requests
        :param token: str. token to set in auth. If None, reinit auth
        """
        if token:
            auth = HTTPBasicAuth(token, '')
            self._token = token
            self.authenticated = True  # TODO: Remove this parameter
            self.session.auth = auth
            logger.debug("Using session token: %s", token)
        else:
            self._token = None
            self.authenticated = False
            self.session.auth = None
            logger.debug("Session token/auth reinitialised")

    def get_token(self):
        """Get the stored backend token"""
        return self._token

    token = property(get_token, set_token)

    def login(self, username, password, generate='enabled', proxies=None):
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
        :param proxies: dict of proxy (http and / or https)
        :type proxies: dict
        :return: return True if authentication is successfull, otherwise False
        :rtype: bool
        """
        logger.debug("login for: %s with generate: %s", username, generate)

        if not username or not password:
            raise BackendException(BACKEND_ERROR, "Missing mandatory parameters")

        if proxies:
            for key in proxies.keys():
                try:
                    assert key in PROXY_PROTOCOLS
                except AssertionError:
                    raise BackendException(BACKEND_ERROR, "Wrong proxy protocol ", key)
        self.proxies = proxies

        endpoint = 'login'
        json = {u'username': username, u'password': password}
        if generate == 'force':
            json['action'] = 'generate'
            logger.debug("Asking for generating new token")

        response = self.get_response(method='POST', endpoint=endpoint, json=json)
        if response.status_code == 401:
            logger.error("Backend refused login with params %s", json)
            self.set_token(token=None)
            return False

        resp = self.decode(response=response)

        if 'token' in resp:
            self.set_token(token=resp['token'])
            return True
        if generate == 'force':  # pragma: no cover - need specific backend tests
            self.set_token(token=None)
            raise BackendException(BACKEND_ERROR, "Token not provided")
        if generate == 'disabled':  # pragma: no cover - need specific backend tests
            logger.error("Token disabled ... to be implemented!")
            return False
        if generate == 'enabled':  # pragma: no cover - need specific backend tests
            logger.warning("Token enabled, but none provided, require new token generation")
            return self.login(username, password, 'force')

        return False  # pragma: no cover - unreachable ...

    def logout(self):
        """
        Logout from the backend

        :return: return True if logout is successfull, otherwise False
        :rtype: bool
        """
        logger.debug("request backend logout")
        if not self.authenticated:
            logger.warning("Unnecessary logout ...")
            return True

        endpoint = 'logout'

        _ = self.get_response(method='POST', endpoint=endpoint)

        self.session.close()
        self.set_token(token=None)

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

        resp = self.get('')
        if "_links" in resp:
            _links = resp["_links"]
            if "child" in _links:
                return _links["child"]

        return {}  # pragma: no cover - should never occur!

    def get(self, endpoint, params=None):
        """
        Get items or item in alignak backend

        If an error occurs, a BackendException is raised.

        This method builds a response as a dictionary that always contains: _items and _status::

            {
                u'_items': [
                    ...
                ],
                u'_status': u'OK'
            }

        :param endpoint: endpoint (API URL) relative from root endpoint
        :type endpoint: str
        :param params: parameters for the backend API
        :type params: dict
        :return: dictionary as specified upper
        :rtype: dict
        """
        response = self.get_response(method='GET', endpoint=endpoint, params=params)

        resp = self.decode(response=response)
        if '_status' not in resp:  # pragma: no cover - need specific backend tests
            resp['_status'] = 'OK'  # TODO: Sure??

        return resp

    def get_all(self, endpoint, params=None):
        # pylint: disable=too-many-locals
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
        :type params: dict
        :return: dict of properties
        :rtype: dict
        """
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
                resp = self.get(endpoint=endpoint, params=params)
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
                :type out_q: multiprocessing.Queue
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
        # pylint: disable=unused-argument
        """
        Create a new item

        :param endpoint: endpoint (API URL)
        :type endpoint: str
        :param data: properties of item to create
        :type data: dict
        :param files: Not used. To be implemented
        :type files: None
        :param headers: headers (example: Content-Type)
        :type headers: dict
        :return: response (creation information)
        :rtype: dict
        """
        # We let Requests encode data to json
        response = self.get_response(method='POST', endpoint=endpoint, json=data, headers=headers)

        resp = self.decode(response=response)

        # TODO: Add files support (cf. Requests - post-a-multipart-encoded-file)
        # try:
        #     if not files:
        #         response = requests.post(
        #             urljoin(self.url_endpoint_root, endpoint),
        #             data=data,
        #             files=files,
        #             headers=headers,
        #             auth=HTTPBasicAuth(self.token, '')
        #         )
        #         resp = response.json()
        #     else:
        #         # Posting files is not yet used, but reserved for future use...
        #         response = requests.post(
        #             urljoin(self.url_endpoint_root, endpoint),
        #             data=data,
        #             files=files,
        #             auth=HTTPBasicAuth(self.token, '')
        #         )
        #         resp = json.loads(response.content)

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
        if not headers:
            raise BackendException(BACKEND_ERROR, "Header If-Match required for patching an object")

        response = self.get_response(method='PATCH', endpoint=endpoint, json=data, headers=headers)

        if response.status_code == 200:
            return self.decode(response=response)

        if response.status_code == 412:
            # 412 means Precondition failed, but confirm ...
            if inception:
                # update etag and retry to patch
                resp = self.get(endpoint)
                headers = {'If-Match': resp['_etag']}
                return self.patch(endpoint, data=data, headers=headers, inception=False)

            raise BackendException(response.status_code, response.content)
        else:  # pragma: no cover - should never occur
            raise BackendException(response.status_code, response.content)

    def put(self, endpoint, data, headers=None, inception=False):
        """
        Method to replace an item

        The headers must include an If-Match containing the object _etag.
            headers = {'If-Match': contact_etag}

        The data dictionary contain all fields.

        If the puting fails because the _etag object do not match with the provided one, a
        BackendException is raised with code = 412.

        If inception is True, this method makes a new get request on the endpoint to refresh the
        _etag and then a new put is called.

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
        :return: dictionary containing put response from the backend
        :rtype: dict
        """
        if not headers:
            raise BackendException(BACKEND_ERROR, "Header If-Match required for puting an object")

        response = self.get_response(method='PUT', endpoint=endpoint, json=data, headers=headers)

        if response.status_code == 200:
            return self.decode(response=response)

        if response.status_code == 412:
            # 412 means Precondition failed, but confirm ...
            if inception:
                # update etag and retry to patch
                resp = self.get(endpoint)
                headers = {'If-Match': resp['_etag']}
                return self.patch(endpoint, data=data, headers=headers, inception=False)

            raise BackendException(response.status_code, response.content)
        else:  # pragma: no cover - should never occur
            raise BackendException(response.status_code, response.content)

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
        response = self.get_response(method='DELETE', endpoint=endpoint, headers=headers)

        logger.debug("delete, response: %s", response)
        if response.status_code != 204:  # pragma: no cover - should not happen ...
            resp = self.decode(response=response)

        resp = {"_status": "OK"}
        return resp
