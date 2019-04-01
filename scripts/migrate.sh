#!/usr/bin/env bash
cd tests/
./manage.py migrate --traceback -v 3 --settings=settings.dev  "$@"
