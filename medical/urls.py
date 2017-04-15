from django.conf.urls import url
from . import views

app_name = 'medical'
urlpatterns = [
    url(r'^drug/$', views.list_drug, name='list_drug'),
    url(r'^drug/add/$', views.add_drug, name='add_drug'),
    url(r'^drug/remove/(?P<drug_id>[0-9]+)/$', views.remove_drug, name='remove_drug'),
    url(r'^diagnosis/create/(?P<patient_id>[0-9]+)/$', views.create_diagnosis, name='create_diagnosis'),
    url(r'^diagnosis/update/(?P<diagnosis_id>[0-9]+)/$', views.update_diagnosis, name='update_diagnosis'),
]
