#!/usr/bin/env bash

black django_mongoengine_filter/ --line-length 80
black tests/ --line-length 80
black setup.py --line-length 80
black runtests.py --line-length 80
black docs/ --line-length 80
