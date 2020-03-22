# flake8: noqa
from __future__ import absolute_import
from .filterset import FilterSet
from .filters import *

VERSION = (0, 3, 5)

__title__ = "django-mongoengine-filter"
__version__ = ".".join([str(_i) for _i in VERSION])
__author__ = "Artur Barseghyan <artur.barseghyan@gmail.com>"
__copyright__ = "2019-2020 Artur Barseghyan"
__license__ = "GPL 2.0/LGPL 2.1"
