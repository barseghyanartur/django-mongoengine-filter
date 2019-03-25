Django Filter MonogoEngine
==========================
django-mongoengine-filter is a reusable Django application for allowing users
to filter `mongoengine querysets`_ dynamically.

Full documentation on `read the docs`_.

.. image:: https://img.shields.io/pypi/v/django-mongoengine-filter.svg
   :target: https://pypi.python.org/pypi/django-mongoengine-filter
   :alt: PyPI Version

Requirements
------------

* Python 3.5+
* Django 2.1+

Installation
------------

Install using pip:

.. code-block:: sh

    pip install django-mongoengine-filter

Or latest development version from repository:

.. code-block:: sh

    pip install https://github.com/barseghyanartur/django-mongoengine-filter/archive/master.zip

Usage
-----
**Sample document**

.. code-block:: python

    from mongoengine import fields, document
    from .constants import PROFILE_TYPES, PROFILE_TYPE_FREE, GENDERS, GENDER_MALE

    __all__ = ("Person",)


    class Person(document.Document):

        name = fields.StringField(
            required=True,
            max_length=255,
            default="Robot",
            verbose_name="Name"
        )
        age = fields.IntField(required=True, verbose_name="Age")
        num_fingers = fields.IntField(
            required=False,
            verbose_name="Number of fingers"
        )
        profile_type = fields.StringField(
            required=False,
            blank=False,
            null=False,
            choices=PROFILE_TYPES,
            default=PROFILE_TYPE_FREE,
        )
        gender = fields.StringField(
            required=False,
            blank=False,
            null=False,
            choices=GENDERS,
            default=GENDER_MALE
        )

        def __str__(self):
            return self.name

**Sample filter**

.. code-block:: python

    import django_filters_mongoengine

    class PersonFilter(django_filters_mongoengine.FilterSet):

        profile_type = django_filters_mongoengine.StringFilter()
        ten_fingers = django_filters_mongoengine.MethodFilter(
            action="ten_fingers_filter"
        )

        class Meta:
            model = Person
            fields = ["profile_type", "ten_fingers"]

        def ten_fingers_filter(self, queryset, name, value):
            if value == 'yes':
                return queryset.filter(num_fingers=10)
            return queryset

**Sample view**

.. code-block:: python

    def person_list(request):
        filter = PersonFilter(request.GET, queryset=Person.objects())
        return render(request, "dfm_app/person_list.html", {"objects": filter.qs})

**Sample requests**


- GET /persons/
- GET /persons/?profile_type=free&gender=male
- GET /persons/?profile_type=free&gender=female
- GET /persons/?profile_type=member&gender=female
- GET /persons/?ten_fingers=yes

**Read more**

.. _`mongoengine querysets`: http://mongoengine-odm.readthedocs.org/apireference.html#module-mongoengine.queryset
.. _`read the docs`: https://django-filter.readthedocs.org/en/latest/

Development
===========

Testing
-------

To run tests in your working environment type:

.. code-block:: sh

    ./runtests.py

To test with all supported Python versions type:

.. code-block:: sh

    tox

Running MongoDB
---------------

The easiest way is to run it via Docker:

.. code-block:: sh

    docker pull mongo:latest
    docker run -p 27017:27017 mongo:latest

Writing documentation
---------------------
Keep the following hierarchy.

.. code-block:: text

    =====
    title
    =====

    header
    ======

    sub-header
    ----------

    sub-sub-header
    ~~~~~~~~~~~~~~

    sub-sub-sub-header
    ^^^^^^^^^^^^^^^^^^

    sub-sub-sub-sub-header
    ++++++++++++++++++++++

    sub-sub-sub-sub-sub-header
    **************************

License
=======
GPL 2.0/LGPL 2.1

Support
=======
For any issues contact me at the e-mail given in the `Author`_ section.

Author
======
Artur Barseghyan <artur.barseghyan@gmail.com>
