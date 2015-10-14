#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
del os.link

try:
    from setuptools import setup, find_packages
except:
    sys.exit("Error: missing python-setuptools library")

try:
    python_version = sys.version_info
except:
    python_version = (1, 5)
if python_version < (2, 7):
    sys.exit("This application requires a minimum Python 2.7.x, sorry!")
elif python_version >= (3,):
    sys.exit("This application is not yet compatible with Python 3.x, sorry!")

import alignak_backend_client

setup(
    name="Alignak_backend_client",
    version=alignak_backend_client.__version__,

    # metadata for upload to PyPI
    author="Frédéric MOHIER",
    author_email="frederic.mohier@gmail.com",
    keywords="alignak monitoring",
    url="https://github.com/Alignak-monitoring-contrib/alignak-backend-client",
    description="Client API for Alignak Backend",
    long_description=open('README.rst').read(),

    zip_safe=False,

    packages=find_packages(),
    include_package_data=True,

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