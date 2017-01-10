#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

from importlib import import_module

try:
    from setuptools import setup, find_packages
except:
    sys.exit("Error: missing python-setuptools library")

try:
    from alignak.version import VERSION
    __alignak_version__ = VERSION
except:
    __alignak_version__ = 'x.y.z'

from alignak_backend_client import __application__, __version__, __copyright__
from alignak_backend_client import __releasenotes__, __license__, __doc_url__
from alignak_backend_client import __name__ as __pkg_name__

package = import_module('alignak_backend_client')

setup(
    name=__pkg_name__,
    version=__version__,

    license=__license__,

    # metadata for upload to PyPI
    author="Frédéric MOHIER",
    author_email="frederic.mohier@gmail.com",
    keywords="alignak monitoring backend",
    url="https://github.com/Alignak-monitoring-contrib/alignak-backend-client",
    description=package.__doc__.strip(),
    long_description=open('README.rst').read(),

    zip_safe=False,

    packages=find_packages(),
    include_package_data=True,

    install_requires=['requests', 'future'],

    entry_points={
        'console_scripts': [
            'alignak-backend-cli = alignak_backend_client.backend_client:main'
        ],
    },
    classifiers = [
        'Development Status :: 5 - Production/Stable',
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
