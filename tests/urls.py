from django.urls import re_path

from dfm_app.views import person_list, PersonListView

urlpatterns = [
    re_path(r"^persons/$", person_list, name="person_list"),
    re_path(r"^persons-cbv/$", PersonListView.as_view(), name="person_list_cbv"),
]
