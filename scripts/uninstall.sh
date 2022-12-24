#!/usr/bin/env bash
pip uninstall django-mongoengine-filter -y
rm build -rf
rm dist -rf
rm -rf django_mongoengine_filter.egg-info
rm -rf django-mongoengine-filter.egg-info
rm builddocs.zip
rm builddocs/ -rf
