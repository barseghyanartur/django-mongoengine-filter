from django.conf.urls import url

from dfm_app.views import person_list

urlpatterns = [url(r"^persons/$", person_list, name="person_list")]
