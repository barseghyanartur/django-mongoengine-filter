from dfm_app.views import PersonListView, person_list
from django.urls import re_path

urlpatterns = [
    re_path(r"^persons/$", person_list, name="person_list"),
    re_path(
        r"^persons-cbv/$", PersonListView.as_view(), name="person_list_cbv"
    ),
]
