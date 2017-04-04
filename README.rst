Alignak Backend client
======================

*Python client library and CLI for Alignak Backend*

.. image:: https://travis-ci.org/Alignak-monitoring-contrib/alignak-backend-client.svg?branch=develop
    :target: https://travis-ci.org/Alignak-monitoring-contrib/alignak-backend-client
    :alt: Develop branch build status

.. image:: https://landscape.io/github/Alignak-monitoring-contrib/alignak-backend-client/develop/landscape.svg?style=flat
    :target: https://landscape.io/github/Alignak-monitoring-contrib/alignak-backend-client/develop
    :alt: Development code static analysis

.. image:: https://coveralls.io/repos/Alignak-monitoring-contrib/alignak-backend-client/badge.svg?branch=develop&service=github
    :target: https://coveralls.io/github/Alignak-monitoring-contrib/alignak-backend-client?branch=develop
    :alt: Development code coverage

.. image:: https://readthedocs.org/projects/alignak-backend-client/badge/?version=latest
    :target: http://alignak-backend-client.readthedocs.org/en/latest/?badge=latest
    :alt: Lastest documentation Status

.. image:: https://readthedocs.org/projects/alignak-backend-client/badge/?version=develop
    :target: http://alignak-backend-client.readthedocs.org/en/develop/?badge=develop
    :alt: Development documentation Status

.. image:: https://badge.fury.io/py/alignak_backend.svg
    :target: https://badge.fury.io/py/alignak_backend_client
    :alt: Most recent PyPi version

.. image:: https://img.shields.io/badge/IRC-%23alignak-1e72ff.svg?style=flat
    :target: http://webchat.freenode.net/?channels=%23alignak
    :alt: Join the chat #alignak on freenode.net

.. image:: https://img.shields.io/badge/License-AGPL%20v3-blue.svg
    :target: http://www.gnu.org/licenses/agpl-3.0
    :alt: License AGPL v3


Documentation
-------------

The Backend client class is commented and `an online documentation <http://alignak-backend-client.readthedocs.io/>`_  is automatically built from the source code. Click on this link or on one of the docs badges on this page to browse the documentation.

The `Alignak backend documentation <http://alignak-backend.readthedocs.io/>`_ will also be really helpful to you ;)


Installation
------------

From PyPI
~~~~~~~~~
To install the package from PyPI:
::

   sudo pip install alignak-backend-client


From source files
~~~~~~~~~~~~~~~~~
To install the package from the source files:
::

   git clone https://github.com/Alignak-monitoring-contrib/alignak-backend-client
   cd alignak-backend-client
   sudo pip install .


Release strategy
----------------

Alignak backend and its *satellites* (backend client, and backend import tools) must all have the
same features level. As of it, take care to install the same minor version on your system to
ensure compatibility between all the packages. Use 0.4.x version of Backend import and Backend
client with a 0.4.x version of the Backend.


Bugs, issues and contributing
-----------------------------

Contributions to this project are welcome and encouraged ... `issues in the project repository <https://github.com/alignak-monitoring-contrib/alignak-backend-client/issues>`_ are the common way to raise an information.
