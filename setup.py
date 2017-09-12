#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from importlib import import_module

try:
    from setuptools import setup, find_packages
except:
    sys.exit("Error: missing python-setuptools library")

from alignak_backend_client import __version__, __author__, __author_email__
from alignak_backend_client import __license__, __git_url__, __classifiers__
from alignak_backend_client import __name__ as __pkg_name__

package = import_module('alignak_backend_client')

setup(
    name=__pkg_name__,
    version=__version__,

    license=__license__,

    # metadata for upload to PyPI
    author=__author__,
    author_email=__author_email__,
    keywords="alignak monitoring backend",
    url=__git_url__,
    description=package.__doc__.strip(),
    long_description=open('README.rst').read(),

    classifiers = __classifiers__,

    zip_safe=False,

    packages=find_packages(),

    # Where to install distributed files
    # data_files = [],

    # Dependencies (if some) ...
    install_requires=['requests', 'future'],

    entry_points={
        'console_scripts': [
            'alignak-backend-cli = alignak_backend_client.backend_client:main'
        ],
    },
)
