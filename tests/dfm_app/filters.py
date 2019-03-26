import django_mongoengine_filter

from .documents import Person

__all__ = ("PersonFilter",)


class PersonFilter(django_mongoengine_filter.FilterSet):

    profile_type = django_mongoengine_filter.StringFilter()
    ten_fingers = django_mongoengine_filter.MethodFilter(
        action="ten_fingers_filter"
    )
    # agnostic = django_mongoengine_filter.BooleanFilter()
    # gender = django_mongoengine_filter.StringFilter()
    # contract_type = django_mongoengine_filter.StringFilter()
    # type = django_mongoengine_filter.StringFilter()
    # work_think_level = django_mongoengine_filter.StringFilter()

    class Meta:
        model = Person
        fields = ["profile_type", "ten_fingers", "agnostic"]

    def ten_fingers_filter(self, queryset, name, value):
        if value == "yes":
            return queryset.filter(num_fingers=10)
        return queryset
