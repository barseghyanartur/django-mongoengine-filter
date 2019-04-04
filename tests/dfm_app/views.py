from django.shortcuts import render

from django_mongoengine_filter.views import FilterView

from .documents import Person
from .filters import PersonFilter

__all__ = (
    "person_list",
    "PersonListView",
)


def person_list(request):
    """Sample function-based view."""
    filter_obj = PersonFilter(request.GET, queryset=Person.objects)
    return render(
        request,
        "dfm_app/person_list.html",
        {"object_list": filter_obj.qs}
    )


class PersonListView(FilterView):
    """Sample class-based view."""

    filterset_class = PersonFilter
    template_name = "dfm_app/person_list.html"
