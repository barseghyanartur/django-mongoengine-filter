import django_filters_mongoengine

from .documents import Person

__all__ = ("PersonFilter",)


class PersonFilter(django_filters_mongoengine.FilterSet):

    profile_type = django_filters_mongoengine.StringFilter()
    ten_fingers = django_filters_mongoengine.MethodFilter(
        action="ten_fingers_filter"
    )
    # gender = django_filters_mongoengine.StringFilter()
    # contract_type = django_filters_mongoengine.StringFilter()
    # type = django_filters_mongoengine.StringFilter()
    # work_think_level = django_filters_mongoengine.StringFilter()

    class Meta:
        model = Person
        fields = ["profile_type", "ten_fingers"]

    def ten_fingers_filter(self, queryset, name, value):
        if value == 'yes':
            return queryset.filter(num_fingers=10)
        return queryset
