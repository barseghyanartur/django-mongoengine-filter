from django.shortcuts import render

from django_mongoengine_filter.views import FilterView

from .documents import Person
from .filters import PersonFilter

__all__ = ("person_list", "PersonListView")


def person_list(request):
    filter = PersonFilter(request.GET, queryset=Person.objects())
    return render(request, "dfm_app/person_list.html", {"objects": filter.qs})
    # return render(request, "dfm_app/person_list.html", {"filter": filter})


class PersonListView(FilterView):

    filterset_class = PersonFilter
    template_name = "dfm_app/person_list.html"
