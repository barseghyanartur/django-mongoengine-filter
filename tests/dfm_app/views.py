from django.shortcuts import render

from .documents import Person
from .filters import PersonFilter

__all__ = ("person_list",)


def person_list(request):
    filter = PersonFilter(request.GET, queryset=Person.objects())
    return render(request, "dfm_app/person_list.html", {"objects": filter.qs})
    # return render(request, "dfm_app/person_list.html", {"filter": filter})
