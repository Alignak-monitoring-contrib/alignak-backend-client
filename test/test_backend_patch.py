#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Copyright (C) 2015-2015: Alignak team, see AUTHORS.txt file for contributors
#
# This file is part of Alignak.
#
# Alignak is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Alignak is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with Alignak.  If not, see <http://www.gnu.org/licenses/>.

from httmock import all_requests, response, HTTMock
import ujson
import unittest2
from alignak.modules.mod_alignakbackendsched.alignakbackend import Backend

@all_requests
def response_patch(url, request):
    headers = {'content-type': 'application/json'}
    if request.method == 'PATCH':
        if request.headers['If-Match'] == '27f88f9749259b53ccaf48331074fa54d092e1cc':
            content = '{"_updated": "Wed, 19 Aug 2015 07:59:51 GMT", "_links": {"self": {"href": "livehost/55d113976376e9835e1b2feb", "title": "Livehost"}}, "_created": "Sun, 16 Aug 2015 22:49:59 GMT", "_status": "OK", "_id": "55d113976376e9835e1b2feb", "_etag": "fff582e398e47bce29e7317f25eb5068aaac3c4a"}'
            return response(200, content, headers, None, 5, request)
        else:
            content = '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">\n<title>412 Precondition Failed</title>\n<h1>Precondition Failed</h1>\n<p>Client and server etags don\'t match</p>\n'
            return response(412, content, headers, None, 5, request)
    elif request.method == 'GET':
        content = '{"_updated": "Wed, 19 Aug 2015 07:59:51 GMT", "last_state_change": 1439818531, "acknowledged": false, "last_check": 1439789562, "long_output": null, "state": "UP", "_links": {"self": {"href": "livehost/55d113976376e9835e1b2feb", "title": "Livehost"}, "collection": {"href": "livehost", "title": "livehost"}, "parent": {"href": "/", "title": "home"}}, "host_name": "55d113586376e9835e1b2fe6", "_created": "Sun, 16 Aug 2015 22:49:59 GMT", "services": null, "output": "[Errno 2] No such file or directory", "_id": "55d113976376e9835e1b2feb", "_etag": "27f88f9749259b53ccaf48331074fa54d092e1cc"}'
        return response(200, content, headers, None, 5, request)

@all_requests
def response_patch_notok(url, request):
    headers = {'content-type': 'application/json'}
    if request.method == 'PATCH':
        if request.headers['If-Match'] == '27f88f9749259b53ccaf48331074fa54d092e1cc':
            content = '{"_updated": "Wed, 19 Aug 2015 07:59:51 GMT", "_links": {"self": {"href": "livehost/55d113976376e9835e1b2feb", "title": "Livehost"}}, "_created": "Sun, 16 Aug 2015 22:49:59 GMT", "_status": "OK", "_id": "55d113976376e9835e1b2feb", "_etag": "fff582e398e47bce29e7317f25eb5068aaac3c4a"}'
            return response(200, content, headers, None, 5, request)
        else:
            content = '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">\n<title>412 Precondition Failed</title>\n<h1>Precondition Failed</h1>\n<p>Client and server etags don\'t match</p>\n'
            return response(412, content, headers, None, 5, request)
    elif request.method == 'GET':
        content = '{"_updated": "Wed, 19 Aug 2015 07:59:51 GMT", "last_state_change": 1439818531, "acknowledged": false, "last_check": 1439789562, "long_output": null, "state": "UP", "_links": {"self": {"href": "livehost/55d113976376e9835e1b2feb", "title": "Livehost"}, "collection": {"href": "livehost", "title": "livehost"}, "parent": {"href": "/", "title": "home"}}, "host_name": "55d113586376e9835e1b2fe6", "_created": "Sun, 16 Aug 2015 22:49:59 GMT", "services": null, "output": "[Errno 2] No such file or directory", "_id": "55d113976376e9835e1b2feb", "_etag": "27f88f9749259b53ccaf48331074fa54d092e1ce"}'
        return response(200, content, headers, None, 5, request)


class TestBackendPatch(unittest2.TestCase):

    def test_patch_works(self):
        headers = {
            'Content-Type': 'application/json',
            'If-Match': '27f88f9749259b53ccaf48331074fa54d092e1cc'
        }
        data = {'state': 'UP'}

        backend = Backend()

        with HTTMock(response_patch):
            resp = backend.method_patch('http://alignakbackend.local/livehost/55d113976376e9835e1b2feb', ujson.dumps(data), headers)

        self.assertEqual({"_updated": "Wed, 19 Aug 2015 07:59:51 GMT", "_links": {"self": {"href": "livehost/55d113976376e9835e1b2feb", "title": "Livehost"}}, "_created": "Sun, 16 Aug 2015 22:49:59 GMT", "_status": "OK", "_id": "55d113976376e9835e1b2feb", "_etag": "fff582e398e47bce29e7317f25eb5068aaac3c4a"}, resp)

    def test_patch_etag_notok_ok(self):
        """
        Test Patch method with _etag not ok + 1 retry _etag ok

        :return: None
        """

        headers = {
            'Content-Type': 'application/json',
            'If-Match': '27f88f9749259b53ccaf48331074fa54d092e1cd'
        }
        data = {'state': 'UP'}

        backend = Backend()

        with HTTMock(response_patch):
            resp = backend.method_patch('http://alignakbackend.local/livehost/55d113976376e9835e1b2feb', ujson.dumps(data), headers)

        self.assertEqual({"_updated": "Wed, 19 Aug 2015 07:59:51 GMT", "_links": {"self": {"href": "livehost/55d113976376e9835e1b2feb", "title": "Livehost"}}, "_created": "Sun, 16 Aug 2015 22:49:59 GMT", "_status": "OK", "_id": "55d113976376e9835e1b2feb", "_etag": "fff582e398e47bce29e7317f25eb5068aaac3c4a"}, resp)

    def test_patch_etag_notok_notok(self):
        """
        Test Patch method with _etag not ok + 1 retry _etag not ok

        :return: None
        """

        headers = {
            'Content-Type': 'application/json',
            'If-Match': '27f88f9749259b53ccaf48331074fa54d092e1cd'
        }
        data = {'state': 'UP'}

        backend = Backend()

        with HTTMock(response_patch_notok):
            resp = backend.method_patch('http://alignakbackend.local/livehost/55d113976376e9835e1b2feb', ujson.dumps(data), headers)

        self.assertEqual('{}', resp)

