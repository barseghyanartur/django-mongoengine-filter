Django Filter MonogoEngine
===========================

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

Or from repository directly:

.. code-block:: sh

    pip install https://github.com/barseghyanartur/django-mongoengine-filter/archive/master.zip

Usage
-----

.. code-block:: python

    import django_filters_mongoengine

    class ProductFilter(django_filters_mongoengine.FilterSet):
        class Meta:
            model = Product
            fields = ['name', 'price', 'manufacturer']

And then in your view you could do:

.. code-block:: python

    def product_list(request):
        filter = ProductFilter(request.GET, queryset=Product.objects.all())
        return render_to_response('my_app/template.html', {'filter': filter})

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
