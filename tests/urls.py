from django.urls import re_path as url

from dfm_app.views import person_list, PersonListView

urlpatterns = [
    url(r"^persons/$", person_list, name="person_list"),
    url(r"^persons-cbv/$", PersonListView.as_view(), name="person_list_cbv"),
]
