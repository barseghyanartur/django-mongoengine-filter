from .filterset import FilterSet
from .filters import *  # noqa

VERSION = (0, 4, 0)

__title__ = "django-mongoengine-filter"
__version__ = ".".join([str(_i) for _i in VERSION])
__author__ = "Artur Barseghyan <artur.barseghyan@gmail.com>"
__copyright__ = "2019-2022 Artur Barseghyan"
__license__ = "GPL 2.0/LGPL 2.1"
