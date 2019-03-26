from django.conf.urls import url

from dfm_app.views import person_list, PersonListView

urlpatterns = [
    url(r"^persons/$", person_list, name="person_list"),
    url(r"^persons-cbv/$", person_list, name="person_list_cbv"),
]
