#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import with_statement

from setuptools import setup, find_packages

import os
import setuptools


# Fix for debian 7 python that raise error on at_exit at the end of setup.py
# (cf http://bugs.python.org/issue15881)
try:
    import multiprocessing
except ImportError:
    pass


# Better to use exec to load the VERSION from alignak/bin/__init__
# so to not have to import the alignak package:
VERSION = "unknown"
ver_file = os.path.join('alignakbackend-api-client',
                        '__init__.py')
with open(ver_file) as fh:
    exec(fh.read())

os.environ['PBR_VERSION'] = VERSION

packages = find_packages()
setuptools.setup(
    setup_requires=['pbr'],
    packages=packages,
    version=VERSION,
    namespace_packages=['alignakbackend-api-client'],
    pbr=True,
)
