#!/usr/bin/env bash
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

pep8 --max-line-length=100 --exclude='*.pyc, *.ini' alignak_backend_client_api/*
pylint --rcfile=.pylintrc alignak_backend_client_api/
pep257 --select=D300 alignak_backend_client_api
cd test
nosetests -xv --process-restartworker --processes=1 --process-timeout=300 --with-coverage --cover-erase --cover-tests --cover-package=alignak_backend_client_api test*.py
coverage combine
coverage report -m
cd ..