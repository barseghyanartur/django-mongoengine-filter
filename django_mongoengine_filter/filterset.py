from __future__ import unicode_literals

from collections import OrderedDict
from copy import deepcopy

import mongoengine
import six
from django import forms
from django.core.validators import EMPTY_VALUES
from django.db import models
from django.db.models.constants import LOOKUP_SEP
from django.utils.text import capfirst
from django.utils.translation import gettext as _
from mongoengine.errors import LookUpError
from mongoengine.fields import EmbeddedDocumentField, ListField

from .filters import (  # DateFilter,; TimeFilter,
    BooleanFilter,
    ChoiceFilter,
    DateTimeFilter,
    Filter,
    ModelChoiceFilter,
    ModelMultipleChoiceFilter,
    NumberFilter,
    StringFilter,
)

ORDER_BY_FIELD = "o"

__all__ = (
    "BaseFilterSet",
    "FILTER_FOR_DBFIELD_DEFAULTS",
    "filters_for_model",
    "FilterSet",
    "filterset_factory",
    "FilterSetMetaclass",
    "FilterSetOptions",
    "get_declared_filters",
    "get_model_field",
    "ORDER_BY_FIELD",
)


def get_declared_filters(bases, attrs, with_base_filters=True):
    filters = []
    for filter_name, obj in list(attrs.items()):
        if isinstance(obj, Filter):
            obj = attrs.pop(filter_name)
            if getattr(obj, "name", None) is None:
                obj.name = filter_name
            filters.append((filter_name, obj))
    filters.sort(key=lambda x: x[1].creation_counter)

    if with_base_filters:
        for base in bases[::-1]:
            if hasattr(base, "base_filters"):
                filters = list(base.base_filters.items()) + filters
    else:
        for base in bases[::-1]:
            if hasattr(base, "declared_filters"):
                filters = list(base.declared_filters.items()) + filters

    return OrderedDict(filters)


def get_model_field(model, f):
    parts = f.split(LOOKUP_SEP)
    member = None
    if len(parts) == 1:
        try:
            return model._lookup_field(f)[0]
        except LookUpError:
            return None
    for part in parts[:-1]:
        try:
            member = model._lookup_field(part)[0].lookup_member(parts[-1])
        except LookUpError:
            return None
        if isinstance(member, (EmbeddedDocumentField, ListField)):
            model = member
    return member


def filters_for_model(
    model,
    fields=None,
    exclude=None,
    filter_for_field=None,
    filter_for_reverse_field=None,
):
    field_dict = OrderedDict()
    opts = model._meta
    if fields is None:
        fields = [
            f.name
            for f in sorted(opts.fields + opts.many_to_many)
            if not isinstance(f, models.AutoField)
        ]
    for f in fields:
        field = get_model_field(model, f)
        if field is None:
            field_dict[f] = None
            continue
        if isinstance(fields, dict):
            # Create a filter for each lookup type.
            for lookup_type in fields[f]:
                filter_ = filter_for_field(field, f, lookup_type)
                if filter_:
                    filter_name = f
                    # Don't add "exact" to filter names
                    if lookup_type != "exact":
                        filter_name = f + LOOKUP_SEP + lookup_type
                    field_dict[filter_name] = filter_
        else:
            filter_ = filter_for_field(field, f)
            if filter_:
                field_dict[f] = filter_
    return field_dict


class FilterSetOptions:
    def __init__(self, options=None):
        self.model = getattr(options, "model", None)
        self.fields = getattr(options, "fields", None)
        self.exclude = getattr(options, "exclude", None)
        self.order_by = getattr(options, "order_by", False)
        self.form = getattr(options, "form", forms.Form)


class FilterSetMetaclass(type):
    def __new__(cls, name, bases, attrs):
        try:
            parents = [b for b in bases if issubclass(b, FilterSet)]
        except NameError:
            # We are defining FilterSet itself here
            parents = None
        declared_filters = get_declared_filters(bases, attrs, False)
        new_class = super(FilterSetMetaclass, cls).__new__(
            cls, name, bases, attrs
        )

        if not parents:
            return new_class

        opts = new_class._meta = FilterSetOptions(
            getattr(new_class, "Meta", None)
        )
        if opts.model:
            filters = filters_for_model(
                opts.model,
                opts.fields,
                opts.exclude,
                new_class.filter_for_field,
                new_class.filter_for_reverse_field,
            )
            filters.update(declared_filters)
        else:
            filters = declared_filters

        if None in filters.values():
            raise TypeError(
                "Meta.fields contains a field that isn't defined "
                "on this FilterSet"
            )

        new_class.declared_filters = declared_filters
        new_class.base_filters = filters
        return new_class


FILTER_FOR_DBFIELD_DEFAULTS = {
    mongoengine.UUIDField: {"filter_class": NumberFilter},
    mongoengine.StringField: {"filter_class": StringFilter},
    mongoengine.BooleanField: {"filter_class": BooleanFilter},
    mongoengine.DateTimeField: {"filter_class": DateTimeFilter},
    mongoengine.DecimalField: {"filter_class": NumberFilter},
    mongoengine.IntField: {"filter_class": NumberFilter},
    mongoengine.FloatField: {"filter_class": NumberFilter},
    mongoengine.EmailField: {"filter_class": StringFilter},
    mongoengine.URLField: {"filter_class": StringFilter},
}


class BaseFilterSet:
    filter_overrides = {}
    order_by_field = ORDER_BY_FIELD
    strict = True

    def __init__(
        self,
        data=None,
        queryset=None,
        *,
        request=None,
        prefix=None,
        strict=None,
    ):
        self.is_bound = data is not None
        self.data = data or {}
        if queryset is None:
            queryset = self._meta.model.objects
        self.queryset = queryset
        self.request = request
        self.form_prefix = prefix
        if strict is not None:
            self.strict = strict

        self.filters = deepcopy(self.base_filters)
        # propagate the model being used through the filters
        for filter_ in self.filters.values():
            filter_.model = self._meta.model

        # Apply the parent to the filters, this will allow the filters to
        # access the filterset
        for filter_key, filter_ in six.iteritems(self.filters):
            filter_.parent = self

    def __iter__(self):
        for obj in self.qs:
            yield obj

    def __len__(self):
        return len(self.qs)

    def __getitem__(self, key):
        return self.qs[key]

    @property
    def qs(self):
        if not hasattr(self, "_qs"):
            valid = self.is_bound and self.form.is_valid()

            if self.strict and self.is_bound and not valid:
                self._qs = self.queryset.none()
                return self._qs

            # start with all the results and filter from there
            qs = self.queryset.all()
            for name, filter_ in six.iteritems(self.filters):
                value = None
                if valid:
                    value = self.form.cleaned_data[name]
                else:
                    raw_value = self.form[name].value()
                    try:
                        value = self.form.fields[name].clean(raw_value)
                    except forms.ValidationError:
                        # for invalid values either:
                        # strictly "apply" filter yielding no results
                        # and get out of here
                        if self.strict:
                            self._qs = self.queryset.none()
                            return self._qs
                        else:  # or ignore this filter altogether
                            pass

                if value is not None:  # valid & clean data
                    qs = filter_.filter(qs, value)

            if self._meta.order_by:
                order_field = self.form.fields[self.order_by_field]
                data = self.form[self.order_by_field].data
                ordered_value = None
                try:
                    ordered_value = order_field.clean(data)
                except forms.ValidationError:
                    pass

                if ordered_value in EMPTY_VALUES and self.strict:
                    ordered_value = self.form.fields[
                        self.order_by_field
                    ].choices[0][0]

                if ordered_value:
                    qs = qs.order_by(*self.get_order_by(ordered_value))

            self._qs = qs

        return self._qs

    def count(self):
        return self.qs.count()

    @property
    def form(self):
        if not hasattr(self, "_form"):
            fields = OrderedDict(
                [
                    (name, filter_.field)
                    for name, filter_ in six.iteritems(self.filters)
                ]
            )
            fields[self.order_by_field] = self.ordering_field
            Form = type(
                str("%sForm" % self.__class__.__name__),
                (self._meta.form,),
                fields,
            )
            if self.is_bound:
                self._form = Form(self.data, prefix=self.form_prefix)
            else:
                self._form = Form(prefix=self.form_prefix)
        return self._form

    def get_ordering_field(self):
        if self._meta.order_by:
            if isinstance(self._meta.order_by, (list, tuple)):
                if isinstance(self._meta.order_by[0], (list, tuple)):
                    # e.g. (('field', 'Display name'), ...)
                    choices = [(f[0], f[1]) for f in self._meta.order_by]
                else:
                    choices = [
                        (
                            f,
                            _("%s (descending)" % capfirst(f[1:]))
                            if f[0] == "-"
                            else capfirst(f),
                        )
                        for f in self._meta.order_by
                    ]
            else:
                # add asc and desc field names
                # use the filter's label if provided
                choices = []
                for f, fltr in self.filters.items():
                    choices.extend(
                        [
                            (fltr.name or f, fltr.label or capfirst(f)),
                            (
                                "-%s" % (fltr.name or f),
                                _(
                                    "%s (descending)"
                                    % (fltr.label or capfirst(f))
                                ),
                            ),
                        ]
                    )
            return forms.ChoiceField(
                label="Ordering", required=False, choices=choices
            )

    @property
    def ordering_field(self):
        if not hasattr(self, "_ordering_field"):
            self._ordering_field = self.get_ordering_field()
        return self._ordering_field

    def get_order_by(self, order_choice):
        return [order_choice]

    @classmethod
    def filter_for_field(cls, f, name, lookup_type="exact"):
        filter_for_field = dict(FILTER_FOR_DBFIELD_DEFAULTS)
        filter_for_field.update(cls.filter_overrides)
        default = {
            "name": name,
            "label": capfirst(
                f.verbose_name if getattr(f, "verbose_name", None) else f.name
            ),
            "lookup_type": lookup_type,
        }

        if f.choices:
            default["choices"] = f.choices
            return ChoiceFilter(**default)

        data = filter_for_field.get(f.__class__)
        if data is None:
            # could be a derived field, inspect parents
            for class_ in f.__class__.mro():
                # skip if class_ is models.Field or object
                # 1st item in mro() is original class
                if class_ in (f.__class__, models.Field, object):
                    continue
                data = filter_for_field.get(class_)
                if data:
                    break
            if data is None:
                return
        filter_class = data.get("filter_class")
        default.update(data.get("extra", lambda f: {})(f))
        if filter_class is not None:
            return filter_class(**default)

    @classmethod
    def filter_for_reverse_field(cls, f, name):
        rel = f.field.rel
        queryset = f.model.objects
        default = {
            "name": name,
            "label": capfirst(rel.related_name),
            "queryset": queryset,
        }
        if rel.multiple:
            return ModelMultipleChoiceFilter(**default)
        else:
            return ModelChoiceFilter(**default)


class FilterSet(six.with_metaclass(FilterSetMetaclass, BaseFilterSet)):
    pass


def filterset_factory(model):
    meta = type(str("Meta"), (object,), {"model": model})
    filterset = type(
        str("%sFilterSet" % model._meta.object_name),
        (FilterSet,),
        {"Meta": meta},
    )
    return filterset
