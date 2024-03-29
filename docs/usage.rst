Using django-mongoengine-filter
===============================

django-mongoengine-filter provides a simple way to filter down a queryset based on
parameters a user provides.  Say we have a ``Product`` model and we want to let
our users filter which products they see on a list page.

The model
---------

Let's start with our model:

.. code-block:: python

    from django.db import models

    class Product(models.Model):
        name = models.CharField(max_length=255)
        price = models.DecimalField()
        description = models.TextField()
        release_date = models.DateField()
        manufacturer = models.ForeignKey(Manufacturer)

The filter
----------

We have a number of fields and we want to let our users filter based on the
price or the release_date.  We create a ``FilterSet`` for this:

.. code-block:: python

    import django_mongoengine_filter

    class ProductFilter(django_mongoengine_filter.FilterSet):
        class Meta:
            model = Product
            fields = ['price', 'release_date']


As you can see this uses a very similar API to Django's ``ModelForm``.  Just
like with a ``ModelForm`` we can also override filters, or add new ones using a
declarative syntax:

.. code-block:: python

    import django_filters

    class ProductFilter(django_mongoengine_filter.FilterSet):
        price = django_filters.NumberFilter(lookup_type='lt')
        class Meta:
            model = Product
            fields = ['price', 'release_date']

Filters take a ``lookup_type`` argument which specifies what lookup type to
use with Django's ORM.  So here when a user entered a price it would show all
Products with a price less than that.

**It's quite common to forget to set lookup type for `CharField`s/`TextField`s
and wonder why search for "foo" doesn't return result for "foobar". It's because
default lookup type is exact text, but you probably want `icontains` lookup
field.**

Items in the ``fields`` sequence in the ``Meta`` class may include
"relationship paths" using Django's ``__`` syntax to filter on fields on a
related model:

.. code-block:: python

    class ProductFilter(django_mongoengine_filter.FilterSet):
        class Meta:
            model = Product
            fields = ['manufacturer__country']

Filters also take any arbitrary keyword arguments which get passed onto the
``django.forms.Field`` initializer.  These extra keyword arguments get stored
in ``Filter.extra``, so it's possible to override the initializer of a
``FilterSet`` to add extra ones:

.. code-block:: python

    class ProductFilter(django_mongoengine_filter.FilterSet):
        class Meta:
            model = Product
            fields = ['manufacturer']

        def __init__(self, *args, **kwargs):
            super(ProductFilter, self).__init__(*args, **kwargs)
            self.filters['manufacturer'].extra.update(
                {'empty_label': 'All Manufacturers'})

Like ``django.contrib.admin.ModelAdmin`` does it is possible to override
default filters for all the models fields of the same kind using
``filter_overrides``:

.. code-block:: python

    class ProductFilter(django_mongoengine_filter.FilterSet):
        filter_overrides = {
            models.CharField: {
                'filter_class': django_filters.CharFilter,
                'extra': lambda f: {
                    'lookup_type': 'icontains',
                }
            }
        }

        class Meta:
            model = Product
            fields = ['name']

The view
--------

Now we need to write a view:

.. code-block:: python

    def product_list(request):
        f = ProductFilter(request.GET, queryset=Product.objects)
        return render_to_response('my_app/template.html', {'filter': f})

If a queryset argument isn't provided then all the items in the default manager
of the model will be used.

The URL conf
------------

We need a URL pattern to call the view:

.. code-block:: python

    re_path(r'^list$', views.product_list)

The template
------------

And lastly we need a template:

.. code-block:: html

    {% extends "base.html" %}

    {% block content %}
        <form action="" method="get">
            {{ filter.form.as_p }}
            <input type="submit" />
        </form>
        {% for obj in filter %}
            {{ obj.name }} - ${{ obj.price }}<br />
        {% endfor %}
    {% endblock %}

And that's all there is to it!  The ``form`` attribute contains a normal
Django form, and when we iterate over the ``FilterSet`` we get the objects in
the resulting queryset.

Other Meta options
------------------

Ordering using ``order_by``
~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can allow the user to control ordering by providing the
``order_by`` argument in the Filter's Meta class.  ``order_by`` can be either a
``list`` or ``tuple`` of field names, in which case those are the options, or
it can be a ``bool`` which, if True, indicates that all fields that
the user can filter on can also be sorted on. An example or ordering using a list:

.. code-block:: python

    import django_filters

    class ProductFilter(django_filters.FilterSet):

        price = django_filters.NumberFilter(lookup_type='lt')

        class Meta:
            model = Product
            fields = ['price', 'release_date']
            order_by = ['price']

If you want to control the display of items in ``order_by``, you can set it to
a list or tuple of 2-tuples in the format ``(field_name, display_name)``.
This lets you override the displayed names for your ordering fields:

.. code-block:: python

    order_by = (
        ('name', 'Company Name'),
        ('average_rating', 'Stars'),
    )

Note that the default query parameter name used for ordering is ``o``.  You
can override this by setting an ``order_by_field`` attribute on the
``FilterSet`` class to the string value you would like to use.

Custom Forms using ``form``
~~~~~~~~~~~~~~~~~~~~~~~~~~~

The inner ``Meta`` class also takes an optional ``form`` argument.  This is a
form class from which ``FilterSet.form`` will subclass.  This works similar to
the ``form`` option on a ``ModelAdmin.``

Non-Meta options
----------------

Note that these options do not go in the Meta class, they are specified directly
in your FilterSet class.

``strict``
~~~~~~~~~~

The ``strict`` option controls whether results are returned when an invalid
value is specified by the user for any filter field. By default, ``strict`` is
set to ``True`` meaning that an empty queryset is returned if any field contains
an invalid value. You can loosen this behavior by setting ``strict`` to
``False`` which will effectively ignore a filter field if its value is invalid.

Overriding ``FilterSet`` methods
--------------------------------

``get_ordering_field()``
~~~~~~~~~~~~~~~~~~~~~~~~

If you want to use a custom widget, or in any other way override the ordering
field you can override the ``get_ordering_field()`` method on a ``FilterSet``.
This method just needs to return a Form Field.

Ordering on multiple fields, or other complex orderings can be achieved by
overriding the ``Filterset.get_order_by()`` method. This is passed the selected
``order_by`` value, and is expected to return an iterable of values to pass to
``QuerySet.order_by``. For example, to sort a ``User`` table by last name, then
first name:

.. code-block:: python

    class UserFilter(django_filters.FilterSet):
        class Meta:
            order_by = (
                ('username', 'Username'),
                ('last_name', 'Last Name')
            )

        def get_order_by(self, order_value):
            if order_value == 'last_name':
                return ['last_name', 'first_name']
            return super(UserFilter, self).get_order_by(order_value)

Generic View
------------

In addition to the above usage there is also a class-based generic view
included in django-filter, which lives at ``django_filters.views.FilterView``.
You must provide either a ``model`` or ``filterset_class`` argument, similar to
``ListView`` in Django itself:

.. code-block:: python

    # urls.py
    from django.urls import re_path
    from django_filters.views import FilterView
    from myapp.models import Product

    urlpatterns = [
        re_path(r'^list/$', FilterView.as_view(model=Product)),
    ]

You must provide a template at ``<app>/<model>_filter.html`` which gets the
context parameter ``filter``.  Additionally, the context will contain
``object_list`` which holds the filtered queryset.

A legacy functional generic view is still included in django-filter, although
its use is deprecated.  It can be found at
``django_filters.views.object_filter``.  You must provide the same arguments
to it as the class based view:

.. code-block:: python

    # urls.py
    from django.urls import re_path
    from myapp.models import Product

    urlpatterns = [
        re_path(r'^list/$', 'django_filters.views.object_filter', {'model': Product}),
    ]

The needed template and its context variables will also be the same as the
class-based view above.
