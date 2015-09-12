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

import requests


class Backend(object):
    """
    Backend class to communicate with alignak-backend
    """

    def method_get(self, endpoint):
        """
        Get items or item in alignak backend

        :param endpoint: endpoint (API URL)
        :type endpoint: str
        :return: list of properties when query item | list of items when get many items
        :rtype: list
        """
        response = requests.get(endpoint)
        resp = response.json()
        if '_items' in resp:
            items = resp['_items']
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

    @classmethod
    def method_post(cls, endpoint, data_json, headers):
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
        response = requests.post(endpoint, data_json, headers=headers)
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
        response = requests.patch(endpoint, data_json, headers=headers)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 412:
            # 412 means Precondition failed
            #logger.error(response.content)
            if 'Client and server etags don' in response.content:
                # update etag + retry
                if stop_inception:
                    return '{}'
                resp = self.method_get(endpoint)
                headers['If-Match'] = resp['_etag']
                return self.method_patch(endpoint, data_json, headers, True)
        else:
            #logger.error("%s: %s for %s" % (response.status_code, response.content, endpoint))
            return response.json()

    @classmethod
    def method_delete(cls, endpoint):
        """
        Method to delete an item or all items

        :param endpoint: endpoint (API URL)
        :type endpoint: str
        :return: None
        """
        requests.delete(endpoint)
