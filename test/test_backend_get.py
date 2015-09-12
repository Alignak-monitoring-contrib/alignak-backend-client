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
import unittest2
from alignakbackend_api_client.client import Backend

@all_requests
def response_get_simple(url, request):
    headers = {'content-type': 'application/json'}
    content = '{"_updated": "Thu, 01 Jan 1970 00:00:00 GMT", "_links": {"self": ' \
              '{"href": "host/55d113586376e9835e1b2fe6", "title": "Host"}, ' \
              '"collection": {"href": "host", "title": "host"}, ' \
              '"parent": {"href": "/", "title": "home"}}, "host_name": "alix", ' \
              '"_created": "Thu, 01 Jan 1970 00:00:00 GMT", "_id": "55d113586376e9835e1b2fe6", ' \
              '"_etag": "694909e730bf5da80f10ee386eea03d73ab9ec76"}'
    return response(200, content, headers, None, 5, request)

@all_requests
def response_get_all(url, request):
    headers = {'content-type': 'application/json'}
    content = '{}'
    if url.query == 'projection=%7B%22host_name%22:1%7D':
        content = '{"_items": [{"_updated": "Thu, 01 Jan 1970 00:00:00 GMT", "_links": {"self": {"href": "host/55d46cf26376e91e92122256", "title": "Host"}}, "host_name": "server2", "_created": "Thu, 01 Jan 1970 00:00:00 GMT", "_id": "55d46cf26376e91e92122256", "_etag": "f4433b9dfd4fce9b07bc3ad8e64708d7013b9b0b"}, {"_updated": "Thu, 01 Jan 1970 00:00:00 GMT", "_links": {"self": {"href": "host/55d46cf66376e91e92122257", "title": "Host"}}, "host_name": "server3", "_created": "Thu, 01 Jan 1970 00:00:00 GMT", "_id": "55d46cf66376e91e92122257", "_etag": "f9cd8d7f09d8e1343d5c6717aa96cbe20077f1fa"}, {"_updated": "Thu, 01 Jan 1970 00:00:00 GMT", "_links": {"self": {"href": "host/55d46cfa6376e91e92122258", "title": "Host"}}, "host_name": "server4", "_created": "Thu, 01 Jan 1970 00:00:00 GMT", "_id": "55d46cfa6376e91e92122258", "_etag": "928b0e11c389843851984353a77b9b5d0f91c331"}, {"_updated": "Thu, 01 Jan 1970 00:00:00 GMT", "_links": {"self": {"href": "host/55d113586376e9835e1b2fe6", "title": "Host"}}, "host_name": "alix", "_created": "Thu, 01 Jan 1970 00:00:00 GMT", "_id": "55d113586376e9835e1b2fe6", "_etag": "694909e730bf5da80f10ee386eea03d73ab9ec76"}, {"_updated": "Thu, 01 Jan 1970 00:00:00 GMT", "_links": {"self": {"href": "host/55d113616376e9835e1b2fe7", "title": "Host"}}, "host_name": "charnay", "_created": "Thu, 01 Jan 1970 00:00:00 GMT", "_id": "55d113616376e9835e1b2fe7", "_etag": "0f47f7ae688f68e62b412cdf41bd1e20439f15c5"}, {"_updated": "Thu, 01 Jan 1970 00:00:00 GMT", "_links": {"self": {"href": "host/55d113666376e9835e1b2fe8", "title": "Host"}}, "host_name": "localhost", "_created": "Thu, 01 Jan 1970 00:00:00 GMT", "_id": "55d113666376e9835e1b2fe8", "_etag": "5b3c959511085ac1eed5b8c934a4639dd72adc8c"}, {"_updated": "Thu, 01 Jan 1970 00:00:00 GMT", "_links": {"self": {"href": "host/55d46cee6376e91e92122255", "title": "Host"}}, "host_name": "server1", "_created": "Thu, 01 Jan 1970 00:00:00 GMT", "_id": "55d46cee6376e91e92122255", "_etag": "296d463c81e05a813fd16d901445aceea21b4beb"}, {"_updated": "Thu, 01 Jan 1970 00:00:00 GMT", "_links": {"self": {"href": "host/55d46cfe6376e91e92122259", "title": "Host"}}, "host_name": "server5", "_created": "Thu, 01 Jan 1970 00:00:00 GMT", "_id": "55d46cfe6376e91e92122259", "_etag": "0cd36fce7a570b5f6521f5527baac895a1b88856"}, {"_updated": "Thu, 01 Jan 1970 00:00:00 GMT", "_links": {"self": {"href": "host/55d46d016376e91e9212225a", "title": "Host"}}, "host_name": "server6", "_created": "Thu, 01 Jan 1970 00:00:00 GMT", "_id": "55d46d016376e91e9212225a", "_etag": "d0519006726c2fec2134da50bec17d425455a2d8"}, {"_updated": "Thu, 01 Jan 1970 00:00:00 GMT", "_links": {"self": {"href": "host/55d46d056376e91e9212225b", "title": "Host"}}, "host_name": "server7", "_created": "Thu, 01 Jan 1970 00:00:00 GMT", "_id": "55d46d056376e91e9212225b", "_etag": "5adb41be14f654126ed10b6d4c4118512afd1018"}, {"_updated": "Thu, 01 Jan 1970 00:00:00 GMT", "_links": {"self": {"href": "host/55d46d116376e91e9212225c", "title": "Host"}}, "host_name": "server8", "_created": "Thu, 01 Jan 1970 00:00:00 GMT", "_id": "55d46d116376e91e9212225c", "_etag": "b0f232121b3d9c39462e30eb86ac14a1b8359f04"}, {"_updated": "Thu, 01 Jan 1970 00:00:00 GMT", "_links": {"self": {"href": "host/55d46d156376e91e9212225d", "title": "Host"}}, "host_name": "server9", "_created": "Thu, 01 Jan 1970 00:00:00 GMT", "_id": "55d46d156376e91e9212225d", "_etag": "a9cbf4a11b3aad90e513e95cf8fb43d9b19ca703"}, {"_updated": "Thu, 01 Jan 1970 00:00:00 GMT", "_links": {"self": {"href": "host/55d46d196376e91e9212225e", "title": "Host"}}, "host_name": "server10", "_created": "Thu, 01 Jan 1970 00:00:00 GMT", "_id": "55d46d196376e91e9212225e", "_etag": "035606a6809bbe5ab850bffc707e31d5f9f2a92e"}, {"_updated": "Thu, 01 Jan 1970 00:00:00 GMT", "_links": {"self": {"href": "host/55d46d1d6376e91e9212225f", "title": "Host"}}, "host_name": "server11", "_created": "Thu, 01 Jan 1970 00:00:00 GMT", "_id": "55d46d1d6376e91e9212225f", "_etag": "e9fb82a8b31f61f532d494085c11e0a11d091ccc"}, {"_updated": "Thu, 01 Jan 1970 00:00:00 GMT", "_links": {"self": {"href": "host/55d46d206376e91e92122260", "title": "Host"}}, "host_name": "server12", "_created": "Thu, 01 Jan 1970 00:00:00 GMT", "_id": "55d46d206376e91e92122260", "_etag": "908884beef70ab411dcab27f9c90d462cfb7e28d"}, {"_updated": "Thu, 01 Jan 1970 00:00:00 GMT", "_links": {"self": {"href": "host/55d46d236376e91e92122261", "title": "Host"}}, "host_name": "server13", "_created": "Thu, 01 Jan 1970 00:00:00 GMT", "_id": "55d46d236376e91e92122261", "_etag": "afd02f7e58a623394ded8a614616ed2f4d346487"}, {"_updated": "Thu, 01 Jan 1970 00:00:00 GMT", "_links": {"self": {"href": "host/55d46d266376e91e92122262", "title": "Host"}}, "host_name": "server14", "_created": "Thu, 01 Jan 1970 00:00:00 GMT", "_id": "55d46d266376e91e92122262", "_etag": "d11555491b14a4b22ac8f5e67229aced12e716c1"}, {"_updated": "Thu, 01 Jan 1970 00:00:00 GMT", "_links": {"self": {"href": "host/55d46d296376e91e92122263", "title": "Host"}}, "host_name": "server15", "_created": "Thu, 01 Jan 1970 00:00:00 GMT", "_id": "55d46d296376e91e92122263", "_etag": "b797745641f488e7ca3da0c5d51aac31d36facc6"}, {"_updated": "Thu, 01 Jan 1970 00:00:00 GMT", "_links": {"self": {"href": "host/55d46d426376e91e92122264", "title": "Host"}}, "host_name": "server16", "_created": "Thu, 01 Jan 1970 00:00:00 GMT", "_id": "55d46d426376e91e92122264", "_etag": "0e2dac8de36579b7b61a0d0d365a3fa9faccc6db"}, {"_updated": "Thu, 01 Jan 1970 00:00:00 GMT", "_links": {"self": {"href": "host/55d46d456376e91e92122265", "title": "Host"}}, "host_name": "server17", "_created": "Thu, 01 Jan 1970 00:00:00 GMT", "_id": "55d46d456376e91e92122265", "_etag": "884a23470eb052e612df725a54b63064c8ca9fe7"}, {"_updated": "Thu, 01 Jan 1970 00:00:00 GMT", "_links": {"self": {"href": "host/55d46d486376e91e92122266", "title": "Host"}}, "host_name": "server18", "_created": "Thu, 01 Jan 1970 00:00:00 GMT", "_id": "55d46d486376e91e92122266", "_etag": "78662a6072789a6982287d58039bf15c54b5739b"}, {"_updated": "Thu, 01 Jan 1970 00:00:00 GMT", "_links": {"self": {"href": "host/55d46d516376e91e92122267", "title": "Host"}}, "host_name": "server19", "_created": "Thu, 01 Jan 1970 00:00:00 GMT", "_id": "55d46d516376e91e92122267", "_etag": "04f6f13e381fc82ed4018e3484e545ff165934fc"}, {"_updated": "Thu, 01 Jan 1970 00:00:00 GMT", "_links": {"self": {"href": "host/55d46d546376e91e92122268", "title": "Host"}}, "host_name": "server20", "_created": "Thu, 01 Jan 1970 00:00:00 GMT", "_id": "55d46d546376e91e92122268", "_etag": "a00f93873ec96dfaf3e45b851acbc5c82108f90d"}, {"_updated": "Thu, 01 Jan 1970 00:00:00 GMT", "_links": {"self": {"href": "host/55d46d596376e91e92122269", "title": "Host"}}, "host_name": "server21", "_created": "Thu, 01 Jan 1970 00:00:00 GMT", "_id": "55d46d596376e91e92122269", "_etag": "84027fc4a76e8d8d50fe69d0a49bcf34f5dd42f3"}, {"_updated": "Thu, 01 Jan 1970 00:00:00 GMT", "_links": {"self": {"href": "host/55d46d5b6376e91e9212226a", "title": "Host"}}, "host_name": "server22", "_created": "Thu, 01 Jan 1970 00:00:00 GMT", "_id": "55d46d5b6376e91e9212226a", "_etag": "4a4adadb580c94636c8943312a04d20cabc70471"}], "_links": {"self": {"href": "host", "title": "host"}, "last": {"href": "host?page=2", "title": "last page"}, "parent": {"href": "/", "title": "home"}, "next": {"href": "host?page=2", "title": "next page"}}, "_meta": {"max_results": 25, "total": 28, "page": 1}}'
    elif url.query == 'projection=%7B%22host_name%22:1%7D&page=2':
        content = '{"_items": [{"_updated": "Thu, 01 Jan 1970 00:00:00 GMT", "_links": {"self": {"href": "host/55d46d5e6376e91e9212226b", "title": "Host"}}, "host_name": "server23", "_created": "Thu, 01 Jan 1970 00:00:00 GMT", "_id": "55d46d5e6376e91e9212226b", "_etag": "ec85cdca4528ad2657df327b0058cfc68aa7c6fa"}, {"_updated": "Thu, 01 Jan 1970 00:00:00 GMT", "_links": {"self": {"href": "host/55d46d616376e91e9212226c", "title": "Host"}}, "host_name": "server24", "_created": "Thu, 01 Jan 1970 00:00:00 GMT", "_id": "55d46d616376e91e9212226c", "_etag": "cda5b137acfd300f675963bdb6ac8b46b5fe8d59"}, {"_updated": "Thu, 01 Jan 1970 00:00:00 GMT", "_links": {"self": {"href": "host/55d46d646376e91e9212226d", "title": "Host"}}, "host_name": "server25", "_created": "Thu, 01 Jan 1970 00:00:00 GMT", "_id": "55d46d646376e91e9212226d", "_etag": "32fc9289abd81fa345883b44ac117237519f5a91"}, {"_updated": "Thu, 01 Jan 1970 00:00:00 GMT", "_links": {"self": {"href": "host/55d47cfe6376e91e9212226e", "title": "Host"}}, "host_name": "server26", "_created": "Thu, 01 Jan 1970 00:00:00 GMT", "_id": "55d47cfe6376e91e9212226e", "_etag": "bfc5f9da6336d8e8a1c17ae5f228264b2062d565"}, {"_updated": "Thu, 01 Jan 1970 00:00:00 GMT", "_links": {"self": {"href": "host/55d47d016376e91e9212226f", "title": "Host"}}, "host_name": "server27", "_created": "Thu, 01 Jan 1970 00:00:00 GMT", "_id": "55d47d016376e91e9212226f", "_etag": "0a4996bf381d3be0ae61ea0c455a265abe7a9960"}, {"_updated": "Thu, 01 Jan 1970 00:00:00 GMT", "_links": {"self": {"href": "host/55d47d056376e91e92122270", "title": "Host"}}, "host_name": "server28", "_created": "Thu, 01 Jan 1970 00:00:00 GMT", "_id": "55d47d056376e91e92122270", "_etag": "ef89a0be3a45988caeb68e32dd0ae21a7d00b1d8"}, {"_updated": "Thu, 01 Jan 1970 00:00:00 GMT", "_links": {"self": {"href": "host/55d47d086376e91e92122271", "title": "Host"}}, "host_name": "server29", "_created": "Thu, 01 Jan 1970 00:00:00 GMT", "_id": "55d47d086376e91e92122271", "_etag": "81608b4ae41afbb836c7d9cd8650a8fd50587201"}, {"_updated": "Thu, 01 Jan 1970 00:00:00 GMT", "_links": {"self": {"href": "host/55d47d0c6376e91e92122272", "title": "Host"}}, "host_name": "server30", "_created": "Thu, 01 Jan 1970 00:00:00 GMT", "_id": "55d47d0c6376e91e92122272", "_etag": "aa919f8d5afcf0c3d7a638479a59e1eb809c2f10"}, {"_updated": "Thu, 01 Jan 1970 00:00:00 GMT", "_links": {"self": {"href": "host/55d47d0f6376e91e92122273", "title": "Host"}}, "host_name": "server31", "_created": "Thu, 01 Jan 1970 00:00:00 GMT", "_id": "55d47d0f6376e91e92122273", "_etag": "cfe25f480a904d05eae1cbd0a6b0f9cdfa9c6443"}, {"_updated": "Thu, 01 Jan 1970 00:00:00 GMT", "_links": {"self": {"href": "host/55d47d126376e91e92122274", "title": "Host"}}, "host_name": "server32", "_created": "Thu, 01 Jan 1970 00:00:00 GMT", "_id": "55d47d126376e91e92122274", "_etag": "9a27a68d51fbc84b0443a59ee07e26395cad722d"}, {"_updated": "Thu, 01 Jan 1970 00:00:00 GMT", "_links": {"self": {"href": "host/55d47d156376e91e92122275", "title": "Host"}}, "host_name": "server33", "_created": "Thu, 01 Jan 1970 00:00:00 GMT", "_id": "55d47d156376e91e92122275", "_etag": "764407415bb9b87d509d66d6142dcb428dad4ea3"}, {"_updated": "Thu, 01 Jan 1970 00:00:00 GMT", "_links": {"self": {"href": "host/55d47d186376e91e92122276", "title": "Host"}}, "host_name": "server34", "_created": "Thu, 01 Jan 1970 00:00:00 GMT", "_id": "55d47d186376e91e92122276", "_etag": "84ffb5738f819c4a381d9c12784c0e6032cea74c"}, {"_updated": "Thu, 01 Jan 1970 00:00:00 GMT", "_links": {"self": {"href": "host/55d47d1b6376e91e92122277", "title": "Host"}}, "host_name": "server35", "_created": "Thu, 01 Jan 1970 00:00:00 GMT", "_id": "55d47d1b6376e91e92122277", "_etag": "9521ab30c0e565bbf4543c85a22439e816f6830b"}, {"_updated": "Thu, 01 Jan 1970 00:00:00 GMT", "_links": {"self": {"href": "host/55d47d1d6376e91e92122278", "title": "Host"}}, "host_name": "server36", "_created": "Thu, 01 Jan 1970 00:00:00 GMT", "_id": "55d47d1d6376e91e92122278", "_etag": "55af38bd28e1289c91634215006aee785765e662"}, {"_updated": "Thu, 01 Jan 1970 00:00:00 GMT", "_links": {"self": {"href": "host/55d47d206376e91e92122279", "title": "Host"}}, "host_name": "server37", "_created": "Thu, 01 Jan 1970 00:00:00 GMT", "_id": "55d47d206376e91e92122279", "_etag": "225de7e80b085999951d8b86adfe9b01ea683770"}, {"_updated": "Thu, 01 Jan 1970 00:00:00 GMT", "_links": {"self": {"href": "host/55d47d246376e91e9212227a", "title": "Host"}}, "host_name": "server38", "_created": "Thu, 01 Jan 1970 00:00:00 GMT", "_id": "55d47d246376e91e9212227a", "_etag": "720c0f01d2d454d0962c0a17f18e583d69b03c0f"}, {"_updated": "Thu, 01 Jan 1970 00:00:00 GMT", "_links": {"self": {"href": "host/55d47d276376e91e9212227b", "title": "Host"}}, "host_name": "server39", "_created": "Thu, 01 Jan 1970 00:00:00 GMT", "_id": "55d47d276376e91e9212227b", "_etag": "3abe3f2d07499f565019b0826d383521970961b0"}, {"_updated": "Thu, 01 Jan 1970 00:00:00 GMT", "_links": {"self": {"href": "host/55d47d2b6376e91e9212227c", "title": "Host"}}, "host_name": "server40", "_created": "Thu, 01 Jan 1970 00:00:00 GMT", "_id": "55d47d2b6376e91e9212227c", "_etag": "6cdc05a513aeaeba8a89b9ab97cafcdb3b91c5e9"}, {"_updated": "Thu, 01 Jan 1970 00:00:00 GMT", "_links": {"self": {"href": "host/55d47d2e6376e91e9212227d", "title": "Host"}}, "host_name": "server41", "_created": "Thu, 01 Jan 1970 00:00:00 GMT", "_id": "55d47d2e6376e91e9212227d", "_etag": "fe357b1b97523d020ca16c5643051cacc988308e"}, {"_updated": "Thu, 01 Jan 1970 00:00:00 GMT", "_links": {"self": {"href": "host/55d47d316376e91e9212227e", "title": "Host"}}, "host_name": "server42", "_created": "Thu, 01 Jan 1970 00:00:00 GMT", "_id": "55d47d316376e91e9212227e", "_etag": "8cc3200148fef2e053c94a2e6b3d8ea03a7dd613"}, {"_updated": "Thu, 01 Jan 1970 00:00:00 GMT", "_links": {"self": {"href": "host/55d47d346376e91e9212227f", "title": "Host"}}, "host_name": "server43", "_created": "Thu, 01 Jan 1970 00:00:00 GMT", "_id": "55d47d346376e91e9212227f", "_etag": "f0a036e10318450a32a71710c7005fd32982170f"}, {"_updated": "Thu, 01 Jan 1970 00:00:00 GMT", "_links": {"self": {"href": "host/55d47d386376e91e92122280", "title": "Host"}}, "host_name": "server44", "_created": "Thu, 01 Jan 1970 00:00:00 GMT", "_id": "55d47d386376e91e92122280", "_etag": "566d4dd11200b9f20253d7af87141b6790a21d83"}, {"_updated": "Thu, 01 Jan 1970 00:00:00 GMT", "_links": {"self": {"href": "host/55d47d3b6376e91e92122281", "title": "Host"}}, "host_name": "server45", "_created": "Thu, 01 Jan 1970 00:00:00 GMT", "_id": "55d47d3b6376e91e92122281", "_etag": "31871f63eeb39bf959341655509298e7ca18e686"}, {"_updated": "Thu, 01 Jan 1970 00:00:00 GMT", "_links": {"self": {"href": "host/55d47d3e6376e91e92122282", "title": "Host"}}, "host_name": "server46", "_created": "Thu, 01 Jan 1970 00:00:00 GMT", "_id": "55d47d3e6376e91e92122282", "_etag": "0779793b441b124b091442ae4d1ff9b239ee1f72"}, {"_updated": "Thu, 01 Jan 1970 00:00:00 GMT", "_links": {"self": {"href": "host/55d47d416376e91e92122283", "title": "Host"}}, "host_name": "server47", "_created": "Thu, 01 Jan 1970 00:00:00 GMT", "_id": "55d47d416376e91e92122283", "_etag": "7c5b90f1b17355f6314ffd8d2f3cd0a542ac6b66"}], "_links": {"self": {"href": "host?page=2", "title": "host"}, "prev": {"href": "host", "title": "previous page"}, "last": {"href": "host?page=3", "title": "last page"}, "parent": {"href": "/", "title": "home"}, "next": {"href": "host?page=3", "title": "next page"}}, "_meta": {"max_results": 25, "total": 54, "page": 2}}';
    elif url.query == 'projection=%7B%22host_name%22:1%7D&page=3':
        content = '{"_items": [{"_updated": "Thu, 01 Jan 1970 00:00:00 GMT", "_links": {"self": {"href": "host/55d47d446376e91e92122284", "title": "Host"}}, "host_name": "server48", "_created": "Thu, 01 Jan 1970 00:00:00 GMT", "_id": "55d47d446376e91e92122284", "_etag": "6f34c822f611d67381630f3bdf5649a4c3299c89"}, {"_updated": "Thu, 01 Jan 1970 00:00:00 GMT", "_links": {"self": {"href": "host/55d47d466376e91e92122285", "title": "Host"}}, "host_name": "server49", "_created": "Thu, 01 Jan 1970 00:00:00 GMT", "_id": "55d47d466376e91e92122285", "_etag": "7b5b44f5396b123983e032ee1ef34482b0201099"}, {"_updated": "Thu, 01 Jan 1970 00:00:00 GMT", "_links": {"self": {"href": "host/55d47d4a6376e91e92122286", "title": "Host"}}, "host_name": "server50", "_created": "Thu, 01 Jan 1970 00:00:00 GMT", "_id": "55d47d4a6376e91e92122286", "_etag": "23c4ca0c74a16e9e3ada2a03161440afb1ada8c6"}, {"_updated": "Thu, 01 Jan 1970 00:00:00 GMT", "_links": {"self": {"href": "host/55d47d4d6376e91e92122287", "title": "Host"}}, "host_name": "server51", "_created": "Thu, 01 Jan 1970 00:00:00 GMT", "_id": "55d47d4d6376e91e92122287", "_etag": "6d9263cf5917bc9a40495820fd1dac245e9243c7"}], "_links": {"self": {"href": "host?page=3", "title": "host"}, "prev": {"href": "host?page=2", "title": "previous page"}, "parent": {"href": "/", "title": "home"}}, "_meta": {"max_results": 25, "total": 54, "page": 3}}'
    return response(200, content, headers, None, 5, request)


class TestBackendGet(unittest2.TestCase):

    def test_get_single(self):
        """
        Get single data (get on object to get properties)

        :return: None
        """

        backend = Backend()

        with HTTMock(response_get_simple):
            resp = backend.method_get('http://alignakbackend.local/host/55d113586376e9835e1b2fe6?projection={"host_name":1}')

        self.assertEqual({u'_updated': u'Thu, 01 Jan 1970 00:00:00 GMT', u'_links': {u'self': {u'href': u'host/55d113586376e9835e1b2fe6', u'title': u'Host'}, u'parent': {u'href': u'/', u'title': u'home'}, u'collection': {u'href': u'host', u'title': u'host'}}, u'host_name': u'alix', u'_created': u'Thu, 01 Jan 1970 00:00:00 GMT', u'_id': u'55d113586376e9835e1b2fe6', u'_etag': u'694909e730bf5da80f10ee386eea03d73ab9ec76'}, resp)

    def test_get_all(self):
        """
        Test to get all data (like all hosts). It manage the pagination

        :return: none
        """

        backend = Backend()

        with HTTMock(response_get_all):
            resp = backend.method_get('http://alignakbackend.local/host?projection={"host_name":1}')

        self.assertEqual([{u'_updated': u'Thu, 01 Jan 1970 00:00:00 GMT', u'_links': {u'self': {u'href': u'host/55d46cf26376e91e92122256', u'title': u'Host'}}, u'host_name': u'server2', u'_created': u'Thu, 01 Jan 1970 00:00:00 GMT', u'_id': u'55d46cf26376e91e92122256', u'_etag': u'f4433b9dfd4fce9b07bc3ad8e64708d7013b9b0b'},
                          {u'_updated': u'Thu, 01 Jan 1970 00:00:00 GMT', u'_links': {u'self': {u'href': u'host/55d46cf66376e91e92122257', u'title': u'Host'}}, u'host_name': u'server3', u'_created': u'Thu, 01 Jan 1970 00:00:00 GMT', u'_id': u'55d46cf66376e91e92122257', u'_etag': u'f9cd8d7f09d8e1343d5c6717aa96cbe20077f1fa'},
                          {u'_updated': u'Thu, 01 Jan 1970 00:00:00 GMT', u'_links': {u'self': {u'href': u'host/55d46cfa6376e91e92122258', u'title': u'Host'}}, u'host_name': u'server4', u'_created': u'Thu, 01 Jan 1970 00:00:00 GMT', u'_id': u'55d46cfa6376e91e92122258', u'_etag': u'928b0e11c389843851984353a77b9b5d0f91c331'},
                          {u'_updated': u'Thu, 01 Jan 1970 00:00:00 GMT', u'_links': {u'self': {u'href': u'host/55d113586376e9835e1b2fe6', u'title': u'Host'}}, u'host_name': u'alix', u'_created': u'Thu, 01 Jan 1970 00:00:00 GMT', u'_id': u'55d113586376e9835e1b2fe6', u'_etag': u'694909e730bf5da80f10ee386eea03d73ab9ec76'},
                          {u'_updated': u'Thu, 01 Jan 1970 00:00:00 GMT', u'_links': {u'self': {u'href': u'host/55d113616376e9835e1b2fe7', u'title': u'Host'}}, u'host_name': u'charnay', u'_created': u'Thu, 01 Jan 1970 00:00:00 GMT', u'_id': u'55d113616376e9835e1b2fe7', u'_etag': u'0f47f7ae688f68e62b412cdf41bd1e20439f15c5'},
                          {u'_updated': u'Thu, 01 Jan 1970 00:00:00 GMT', u'_links': {u'self': {u'href': u'host/55d113666376e9835e1b2fe8', u'title': u'Host'}}, u'host_name': u'localhost', u'_created': u'Thu, 01 Jan 1970 00:00:00 GMT', u'_id': u'55d113666376e9835e1b2fe8', u'_etag': u'5b3c959511085ac1eed5b8c934a4639dd72adc8c'},
                          {u'_updated': u'Thu, 01 Jan 1970 00:00:00 GMT', u'_links': {u'self': {u'href': u'host/55d46cee6376e91e92122255', u'title': u'Host'}}, u'host_name': u'server1', u'_created': u'Thu, 01 Jan 1970 00:00:00 GMT', u'_id': u'55d46cee6376e91e92122255', u'_etag': u'296d463c81e05a813fd16d901445aceea21b4beb'},
                          {u'_updated': u'Thu, 01 Jan 1970 00:00:00 GMT', u'_links': {u'self': {u'href': u'host/55d46cfe6376e91e92122259', u'title': u'Host'}}, u'host_name': u'server5', u'_created': u'Thu, 01 Jan 1970 00:00:00 GMT', u'_id': u'55d46cfe6376e91e92122259', u'_etag': u'0cd36fce7a570b5f6521f5527baac895a1b88856'},
                          {u'_updated': u'Thu, 01 Jan 1970 00:00:00 GMT', u'_links': {u'self': {u'href': u'host/55d46d016376e91e9212225a', u'title': u'Host'}}, u'host_name': u'server6', u'_created': u'Thu, 01 Jan 1970 00:00:00 GMT', u'_id': u'55d46d016376e91e9212225a', u'_etag': u'd0519006726c2fec2134da50bec17d425455a2d8'},
                          {u'_updated': u'Thu, 01 Jan 1970 00:00:00 GMT', u'_links': {u'self': {u'href': u'host/55d46d056376e91e9212225b', u'title': u'Host'}}, u'host_name': u'server7', u'_created': u'Thu, 01 Jan 1970 00:00:00 GMT', u'_id': u'55d46d056376e91e9212225b', u'_etag': u'5adb41be14f654126ed10b6d4c4118512afd1018'},
                          {u'_updated': u'Thu, 01 Jan 1970 00:00:00 GMT', u'_links': {u'self': {u'href': u'host/55d46d116376e91e9212225c', u'title': u'Host'}}, u'host_name': u'server8', u'_created': u'Thu, 01 Jan 1970 00:00:00 GMT', u'_id': u'55d46d116376e91e9212225c', u'_etag': u'b0f232121b3d9c39462e30eb86ac14a1b8359f04'},
                          {u'_updated': u'Thu, 01 Jan 1970 00:00:00 GMT', u'_links': {u'self': {u'href': u'host/55d46d156376e91e9212225d', u'title': u'Host'}}, u'host_name': u'server9', u'_created': u'Thu, 01 Jan 1970 00:00:00 GMT', u'_id': u'55d46d156376e91e9212225d', u'_etag': u'a9cbf4a11b3aad90e513e95cf8fb43d9b19ca703'},
                          {u'_updated': u'Thu, 01 Jan 1970 00:00:00 GMT', u'_links': {u'self': {u'href': u'host/55d46d196376e91e9212225e', u'title': u'Host'}}, u'host_name': u'server10', u'_created': u'Thu, 01 Jan 1970 00:00:00 GMT', u'_id': u'55d46d196376e91e9212225e', u'_etag': u'035606a6809bbe5ab850bffc707e31d5f9f2a92e'},
                          {u'_updated': u'Thu, 01 Jan 1970 00:00:00 GMT', u'_links': {u'self': {u'href': u'host/55d46d1d6376e91e9212225f', u'title': u'Host'}}, u'host_name': u'server11', u'_created': u'Thu, 01 Jan 1970 00:00:00 GMT', u'_id': u'55d46d1d6376e91e9212225f', u'_etag': u'e9fb82a8b31f61f532d494085c11e0a11d091ccc'},
                          {u'_updated': u'Thu, 01 Jan 1970 00:00:00 GMT', u'_links': {u'self': {u'href': u'host/55d46d206376e91e92122260', u'title': u'Host'}}, u'host_name': u'server12', u'_created': u'Thu, 01 Jan 1970 00:00:00 GMT', u'_id': u'55d46d206376e91e92122260', u'_etag': u'908884beef70ab411dcab27f9c90d462cfb7e28d'},
                          {u'_updated': u'Thu, 01 Jan 1970 00:00:00 GMT', u'_links': {u'self': {u'href': u'host/55d46d236376e91e92122261', u'title': u'Host'}}, u'host_name': u'server13', u'_created': u'Thu, 01 Jan 1970 00:00:00 GMT', u'_id': u'55d46d236376e91e92122261', u'_etag': u'afd02f7e58a623394ded8a614616ed2f4d346487'},
                          {u'_updated': u'Thu, 01 Jan 1970 00:00:00 GMT', u'_links': {u'self': {u'href': u'host/55d46d266376e91e92122262', u'title': u'Host'}}, u'host_name': u'server14', u'_created': u'Thu, 01 Jan 1970 00:00:00 GMT', u'_id': u'55d46d266376e91e92122262', u'_etag': u'd11555491b14a4b22ac8f5e67229aced12e716c1'},
                          {u'_updated': u'Thu, 01 Jan 1970 00:00:00 GMT', u'_links': {u'self': {u'href': u'host/55d46d296376e91e92122263', u'title': u'Host'}}, u'host_name': u'server15', u'_created': u'Thu, 01 Jan 1970 00:00:00 GMT', u'_id': u'55d46d296376e91e92122263', u'_etag': u'b797745641f488e7ca3da0c5d51aac31d36facc6'},
                          {u'_updated': u'Thu, 01 Jan 1970 00:00:00 GMT', u'_links': {u'self': {u'href': u'host/55d46d426376e91e92122264', u'title': u'Host'}}, u'host_name': u'server16', u'_created': u'Thu, 01 Jan 1970 00:00:00 GMT', u'_id': u'55d46d426376e91e92122264', u'_etag': u'0e2dac8de36579b7b61a0d0d365a3fa9faccc6db'},
                          {u'_updated': u'Thu, 01 Jan 1970 00:00:00 GMT', u'_links': {u'self': {u'href': u'host/55d46d456376e91e92122265', u'title': u'Host'}}, u'host_name': u'server17', u'_created': u'Thu, 01 Jan 1970 00:00:00 GMT', u'_id': u'55d46d456376e91e92122265', u'_etag': u'884a23470eb052e612df725a54b63064c8ca9fe7'},
                          {u'_updated': u'Thu, 01 Jan 1970 00:00:00 GMT', u'_links': {u'self': {u'href': u'host/55d46d486376e91e92122266', u'title': u'Host'}}, u'host_name': u'server18', u'_created': u'Thu, 01 Jan 1970 00:00:00 GMT', u'_id': u'55d46d486376e91e92122266', u'_etag': u'78662a6072789a6982287d58039bf15c54b5739b'},
                          {u'_updated': u'Thu, 01 Jan 1970 00:00:00 GMT', u'_links': {u'self': {u'href': u'host/55d46d516376e91e92122267', u'title': u'Host'}}, u'host_name': u'server19', u'_created': u'Thu, 01 Jan 1970 00:00:00 GMT', u'_id': u'55d46d516376e91e92122267', u'_etag': u'04f6f13e381fc82ed4018e3484e545ff165934fc'},
                          {u'_updated': u'Thu, 01 Jan 1970 00:00:00 GMT', u'_links': {u'self': {u'href': u'host/55d46d546376e91e92122268', u'title': u'Host'}}, u'host_name': u'server20', u'_created': u'Thu, 01 Jan 1970 00:00:00 GMT', u'_id': u'55d46d546376e91e92122268', u'_etag': u'a00f93873ec96dfaf3e45b851acbc5c82108f90d'},
                          {u'_updated': u'Thu, 01 Jan 1970 00:00:00 GMT', u'_links': {u'self': {u'href': u'host/55d46d596376e91e92122269', u'title': u'Host'}}, u'host_name': u'server21', u'_created': u'Thu, 01 Jan 1970 00:00:00 GMT', u'_id': u'55d46d596376e91e92122269', u'_etag': u'84027fc4a76e8d8d50fe69d0a49bcf34f5dd42f3'},
                          {u'_updated': u'Thu, 01 Jan 1970 00:00:00 GMT', u'_links': {u'self': {u'href': u'host/55d46d5b6376e91e9212226a', u'title': u'Host'}}, u'host_name': u'server22', u'_created': u'Thu, 01 Jan 1970 00:00:00 GMT', u'_id': u'55d46d5b6376e91e9212226a', u'_etag': u'4a4adadb580c94636c8943312a04d20cabc70471'},
                          {u'_updated': u'Thu, 01 Jan 1970 00:00:00 GMT', u'_links': {u'self': {u'href': u'host/55d46d5e6376e91e9212226b', u'title': u'Host'}}, u'host_name': u'server23', u'_created': u'Thu, 01 Jan 1970 00:00:00 GMT', u'_id': u'55d46d5e6376e91e9212226b', u'_etag': u'ec85cdca4528ad2657df327b0058cfc68aa7c6fa'},
                          {u'_updated': u'Thu, 01 Jan 1970 00:00:00 GMT', u'_links': {u'self': {u'href': u'host/55d46d616376e91e9212226c', u'title': u'Host'}}, u'host_name': u'server24', u'_created': u'Thu, 01 Jan 1970 00:00:00 GMT', u'_id': u'55d46d616376e91e9212226c', u'_etag': u'cda5b137acfd300f675963bdb6ac8b46b5fe8d59'},
                          {u'_updated': u'Thu, 01 Jan 1970 00:00:00 GMT', u'_links': {u'self': {u'href': u'host/55d46d646376e91e9212226d', u'title': u'Host'}}, u'host_name': u'server25', u'_created': u'Thu, 01 Jan 1970 00:00:00 GMT', u'_id': u'55d46d646376e91e9212226d', u'_etag': u'32fc9289abd81fa345883b44ac117237519f5a91'},
                          {u'_updated': u'Thu, 01 Jan 1970 00:00:00 GMT', u'_links': {u'self': {u'href': u'host/55d47cfe6376e91e9212226e', u'title': u'Host'}}, u'host_name': u'server26', u'_created': u'Thu, 01 Jan 1970 00:00:00 GMT', u'_id': u'55d47cfe6376e91e9212226e', u'_etag': u'bfc5f9da6336d8e8a1c17ae5f228264b2062d565'},
                          {u'_updated': u'Thu, 01 Jan 1970 00:00:00 GMT', u'_links': {u'self': {u'href': u'host/55d47d016376e91e9212226f', u'title': u'Host'}}, u'host_name': u'server27', u'_created': u'Thu, 01 Jan 1970 00:00:00 GMT', u'_id': u'55d47d016376e91e9212226f', u'_etag': u'0a4996bf381d3be0ae61ea0c455a265abe7a9960'},
                          {u'_updated': u'Thu, 01 Jan 1970 00:00:00 GMT', u'_links': {u'self': {u'href': u'host/55d47d056376e91e92122270', u'title': u'Host'}}, u'host_name': u'server28', u'_created': u'Thu, 01 Jan 1970 00:00:00 GMT', u'_id': u'55d47d056376e91e92122270', u'_etag': u'ef89a0be3a45988caeb68e32dd0ae21a7d00b1d8'},
                          {u'_updated': u'Thu, 01 Jan 1970 00:00:00 GMT', u'_links': {u'self': {u'href': u'host/55d47d086376e91e92122271', u'title': u'Host'}}, u'host_name': u'server29', u'_created': u'Thu, 01 Jan 1970 00:00:00 GMT', u'_id': u'55d47d086376e91e92122271', u'_etag': u'81608b4ae41afbb836c7d9cd8650a8fd50587201'},
                          {u'_updated': u'Thu, 01 Jan 1970 00:00:00 GMT', u'_links': {u'self': {u'href': u'host/55d47d0c6376e91e92122272', u'title': u'Host'}}, u'host_name': u'server30', u'_created': u'Thu, 01 Jan 1970 00:00:00 GMT', u'_id': u'55d47d0c6376e91e92122272', u'_etag': u'aa919f8d5afcf0c3d7a638479a59e1eb809c2f10'},
                          {u'_updated': u'Thu, 01 Jan 1970 00:00:00 GMT', u'_links': {u'self': {u'href': u'host/55d47d0f6376e91e92122273', u'title': u'Host'}}, u'host_name': u'server31', u'_created': u'Thu, 01 Jan 1970 00:00:00 GMT', u'_id': u'55d47d0f6376e91e92122273', u'_etag': u'cfe25f480a904d05eae1cbd0a6b0f9cdfa9c6443'},
                          {u'_updated': u'Thu, 01 Jan 1970 00:00:00 GMT', u'_links': {u'self': {u'href': u'host/55d47d126376e91e92122274', u'title': u'Host'}}, u'host_name': u'server32', u'_created': u'Thu, 01 Jan 1970 00:00:00 GMT', u'_id': u'55d47d126376e91e92122274', u'_etag': u'9a27a68d51fbc84b0443a59ee07e26395cad722d'},
                          {u'_updated': u'Thu, 01 Jan 1970 00:00:00 GMT', u'_links': {u'self': {u'href': u'host/55d47d156376e91e92122275', u'title': u'Host'}}, u'host_name': u'server33', u'_created': u'Thu, 01 Jan 1970 00:00:00 GMT', u'_id': u'55d47d156376e91e92122275', u'_etag': u'764407415bb9b87d509d66d6142dcb428dad4ea3'},
                          {u'_updated': u'Thu, 01 Jan 1970 00:00:00 GMT', u'_links': {u'self': {u'href': u'host/55d47d186376e91e92122276', u'title': u'Host'}}, u'host_name': u'server34', u'_created': u'Thu, 01 Jan 1970 00:00:00 GMT', u'_id': u'55d47d186376e91e92122276', u'_etag': u'84ffb5738f819c4a381d9c12784c0e6032cea74c'},
                          {u'_updated': u'Thu, 01 Jan 1970 00:00:00 GMT', u'_links': {u'self': {u'href': u'host/55d47d1b6376e91e92122277', u'title': u'Host'}}, u'host_name': u'server35', u'_created': u'Thu, 01 Jan 1970 00:00:00 GMT', u'_id': u'55d47d1b6376e91e92122277', u'_etag': u'9521ab30c0e565bbf4543c85a22439e816f6830b'},
                          {u'_updated': u'Thu, 01 Jan 1970 00:00:00 GMT', u'_links': {u'self': {u'href': u'host/55d47d1d6376e91e92122278', u'title': u'Host'}}, u'host_name': u'server36', u'_created': u'Thu, 01 Jan 1970 00:00:00 GMT', u'_id': u'55d47d1d6376e91e92122278', u'_etag': u'55af38bd28e1289c91634215006aee785765e662'},
                          {u'_updated': u'Thu, 01 Jan 1970 00:00:00 GMT', u'_links': {u'self': {u'href': u'host/55d47d206376e91e92122279', u'title': u'Host'}}, u'host_name': u'server37', u'_created': u'Thu, 01 Jan 1970 00:00:00 GMT', u'_id': u'55d47d206376e91e92122279', u'_etag': u'225de7e80b085999951d8b86adfe9b01ea683770'},
                          {u'_updated': u'Thu, 01 Jan 1970 00:00:00 GMT', u'_links': {u'self': {u'href': u'host/55d47d246376e91e9212227a', u'title': u'Host'}}, u'host_name': u'server38', u'_created': u'Thu, 01 Jan 1970 00:00:00 GMT', u'_id': u'55d47d246376e91e9212227a', u'_etag': u'720c0f01d2d454d0962c0a17f18e583d69b03c0f'},
                          {u'_updated': u'Thu, 01 Jan 1970 00:00:00 GMT', u'_links': {u'self': {u'href': u'host/55d47d276376e91e9212227b', u'title': u'Host'}}, u'host_name': u'server39', u'_created': u'Thu, 01 Jan 1970 00:00:00 GMT', u'_id': u'55d47d276376e91e9212227b', u'_etag': u'3abe3f2d07499f565019b0826d383521970961b0'},
                          {u'_updated': u'Thu, 01 Jan 1970 00:00:00 GMT', u'_links': {u'self': {u'href': u'host/55d47d2b6376e91e9212227c', u'title': u'Host'}}, u'host_name': u'server40', u'_created': u'Thu, 01 Jan 1970 00:00:00 GMT', u'_id': u'55d47d2b6376e91e9212227c', u'_etag': u'6cdc05a513aeaeba8a89b9ab97cafcdb3b91c5e9'},
                          {u'_updated': u'Thu, 01 Jan 1970 00:00:00 GMT', u'_links': {u'self': {u'href': u'host/55d47d2e6376e91e9212227d', u'title': u'Host'}}, u'host_name': u'server41', u'_created': u'Thu, 01 Jan 1970 00:00:00 GMT', u'_id': u'55d47d2e6376e91e9212227d', u'_etag': u'fe357b1b97523d020ca16c5643051cacc988308e'},
                          {u'_updated': u'Thu, 01 Jan 1970 00:00:00 GMT', u'_links': {u'self': {u'href': u'host/55d47d316376e91e9212227e', u'title': u'Host'}}, u'host_name': u'server42', u'_created': u'Thu, 01 Jan 1970 00:00:00 GMT', u'_id': u'55d47d316376e91e9212227e', u'_etag': u'8cc3200148fef2e053c94a2e6b3d8ea03a7dd613'},
                          {u'_updated': u'Thu, 01 Jan 1970 00:00:00 GMT', u'_links': {u'self': {u'href': u'host/55d47d346376e91e9212227f', u'title': u'Host'}}, u'host_name': u'server43', u'_created': u'Thu, 01 Jan 1970 00:00:00 GMT', u'_id': u'55d47d346376e91e9212227f', u'_etag': u'f0a036e10318450a32a71710c7005fd32982170f'},
                          {u'_updated': u'Thu, 01 Jan 1970 00:00:00 GMT', u'_links': {u'self': {u'href': u'host/55d47d386376e91e92122280', u'title': u'Host'}}, u'host_name': u'server44', u'_created': u'Thu, 01 Jan 1970 00:00:00 GMT', u'_id': u'55d47d386376e91e92122280', u'_etag': u'566d4dd11200b9f20253d7af87141b6790a21d83'},
                          {u'_updated': u'Thu, 01 Jan 1970 00:00:00 GMT', u'_links': {u'self': {u'href': u'host/55d47d3b6376e91e92122281', u'title': u'Host'}}, u'host_name': u'server45', u'_created': u'Thu, 01 Jan 1970 00:00:00 GMT', u'_id': u'55d47d3b6376e91e92122281', u'_etag': u'31871f63eeb39bf959341655509298e7ca18e686'},
                          {u'_updated': u'Thu, 01 Jan 1970 00:00:00 GMT', u'_links': {u'self': {u'href': u'host/55d47d3e6376e91e92122282', u'title': u'Host'}}, u'host_name': u'server46', u'_created': u'Thu, 01 Jan 1970 00:00:00 GMT', u'_id': u'55d47d3e6376e91e92122282', u'_etag': u'0779793b441b124b091442ae4d1ff9b239ee1f72'},
                          {u'_updated': u'Thu, 01 Jan 1970 00:00:00 GMT', u'_links': {u'self': {u'href': u'host/55d47d416376e91e92122283', u'title': u'Host'}}, u'host_name': u'server47', u'_created': u'Thu, 01 Jan 1970 00:00:00 GMT', u'_id': u'55d47d416376e91e92122283', u'_etag': u'7c5b90f1b17355f6314ffd8d2f3cd0a542ac6b66'},
                          {u'_updated': u'Thu, 01 Jan 1970 00:00:00 GMT', u'_links': {u'self': {u'href': u'host/55d47d446376e91e92122284', u'title': u'Host'}}, u'host_name': u'server48', u'_created': u'Thu, 01 Jan 1970 00:00:00 GMT', u'_id': u'55d47d446376e91e92122284', u'_etag': u'6f34c822f611d67381630f3bdf5649a4c3299c89'},
                          {u'_updated': u'Thu, 01 Jan 1970 00:00:00 GMT', u'_links': {u'self': {u'href': u'host/55d47d466376e91e92122285', u'title': u'Host'}}, u'host_name': u'server49', u'_created': u'Thu, 01 Jan 1970 00:00:00 GMT', u'_id': u'55d47d466376e91e92122285', u'_etag': u'7b5b44f5396b123983e032ee1ef34482b0201099'},
                          {u'_updated': u'Thu, 01 Jan 1970 00:00:00 GMT', u'_links': {u'self': {u'href': u'host/55d47d4a6376e91e92122286', u'title': u'Host'}}, u'host_name': u'server50', u'_created': u'Thu, 01 Jan 1970 00:00:00 GMT', u'_id': u'55d47d4a6376e91e92122286', u'_etag': u'23c4ca0c74a16e9e3ada2a03161440afb1ada8c6'},
                          {u'_updated': u'Thu, 01 Jan 1970 00:00:00 GMT', u'_links': {u'self': {u'href': u'host/55d47d4d6376e91e92122287', u'title': u'Host'}}, u'host_name': u'server51', u'_created': u'Thu, 01 Jan 1970 00:00:00 GMT', u'_id': u'55d47d4d6376e91e92122287', u'_etag': u'6d9263cf5917bc9a40495820fd1dac245e9243c7'}
                          ],
                          resp)

