#!/usr/bin/env bash
echo "code_style.in"
pip-compile requirements/code_style.in "$@"

echo "common.in"
pip-compile requirements/common.in "$@"

echo "debug.in"
pip-compile requirements/debug.in "$@"

echo "dev.in"
pip-compile requirements/dev.in "$@"

echo "django_2_2.in"
pip-compile requirements/django_2_2.in "$@"

echo "django_3_0.in"
pip-compile requirements/django_3_0.in "$@"

echo "django_3_1.in"
pip-compile requirements/django_3_1.in "$@"

echo "django_3_2.in"
pip-compile requirements/django_3_2.in "$@"

echo "django_4_0.in"
pip-compile requirements/django_4_0.in "$@"

echo "django_4_1.in"
pip-compile requirements/django_4_1.in "$@"

echo "docs.in"
pip-compile requirements/docs.in "$@"

echo "documentation.in"
pip-compile requirements/documentation.in "$@"

echo "test.in"
pip-compile requirements/test.in "$@"

echo "testing.in"
pip-compile requirements/testing.in "$@"
