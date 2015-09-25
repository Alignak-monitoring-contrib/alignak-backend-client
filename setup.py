#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

import os
del os.link

setup(
    name = "alignak_backend_client",
    version = "0.1.1",
    # packages = find_packages(),
    # scripts = ['say_hello.py'],

    # Project uses reStructuredText, so ensure that the docutils get
    # installed or upgraded on the target machine
    install_requires = ['requests'],

    # metadata for upload to PyPI
    author = "Frédéric MOHIER",
    author_email = "frederic.mohier@gmail.com",
    description = "Client API for Alignak Backend",
    license = "GPLv3",
    keywords = "alignak monitoring",
    url = "https://github.com/Alignak-monitoring-contrib/alignak-backend-client",   # project home page, if any

    # could also include long_description, download_url, classifiers, etc.
)