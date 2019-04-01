#!/usr/bin/env bash
cd tests/
server="0.0.0.0"
port="8000"
if [[ $1 == "--port" ]]
then
    port="$2"
    shift
    shift
    args="$@"
else
    port="8000"
    args="$@"
fi

#./manage.py runserver "$server:$port" --traceback -v 3 "$args"

if [[ $args ]]
then
    ./manage.py runserver "$server:$port" --traceback -v 3 --settings=settings.dev "$args"
else
    ./manage.py runserver "$server:$port" --traceback -v 3 --settings=settings.dev  "$@"
fi
