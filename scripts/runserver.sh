#!/usr/bin/env bash
cd tests/
./manage.py migrate "$server:$port" --traceback -v 3 --settings=settings.dev  "$@"
