#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
    Alignak REST backend client library
    ===================================

    This module is a Python library used for connecting to an Alignak backend.
"""
# Application version and manifest
VERSION = (0, 6, 13)

__application__ = u"Alignak Backend client"
__short_version__ = '.'.join((str(each) for each in VERSION[:2]))
__version__ = '.'.join((str(each) for each in VERSION[:4]))
__author__ = u"Alignak team"
__copyright__ = u"(c) 2015-2016 - %s" % __author__
__license__ = u"GNU Affero General Public License, version 3"
__description__ = u"Alignak backend client library"
__releasenotes__ = u"""Alignak backend client library"""
__doc_url__ = "https://github.com/Alignak-monitoring-contrib/alignak-backend-client"
# Application manifest
manifest = {
    'name': __application__,
    'version': __version__,
    'author': __author__,
    'description': __description__,
    'copyright': __copyright__,
    'license': __license__,
    'release': __releasenotes__,
    'doc': __doc_url__
}
