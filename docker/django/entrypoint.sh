#!/bin/sh

# Create dirs if necessary
echo "Creating dirs"
./scripts/create_dirs.sh

# Apply database migrations
echo "Apply database migrations"
./tests/manage.py migrate --noinput --settings=settings.docker

# Start server
echo "Starting server"
python ./tests/manage.py runserver 0.0.0.0:8000 --settings=settings.docker --traceback -v 3
