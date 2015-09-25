#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

import os
del os.link

import alignak_backend_client

setup(
    name="alignak_backend_client",
    version=alignak_backend_client.__version__,

    # metadata for upload to PyPI
    author="Frédéric MOHIER",
    author_email="frederic.mohier@gmail.com",
    keywords="alignak monitoring",
    url="https://github.com/Alignak-monitoring-contrib/alignak-backend-client",
    description="Client API for Alignak Backend",
    long_description=open('README.rst').read(),

    packages = ['alignak_backend_client'],

    install_requires=['requests'],

    classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Topic :: System :: Monitoring',
        'Topic :: System :: Systems Administration'
    ]
)