import django_filters_mongoengine

from .documents import Person

__all__ = ("PersonFilter",)


class PersonFilter(django_filters_mongoengine.FilterSet):

    profile_type = django_filters_mongoengine.StringFilter()
    # gender = django_filters_mongoengine.MethodFilter(method="custom_filter")
    # contract_type = django_filters.CharFilter(method='custom_filter')
    # type = django_filters.CharFilter(method='custom_filter')
    # work_think_level = django_filters.CharFilter(method='custom_filter')

    class Meta:
        model = Person
        fields = ["profile_type"]

    def custom_filter(self, queryset, name, value):
        return queryset.filter(**{name: value})
