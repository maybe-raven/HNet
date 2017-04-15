from django.conf.urls import url
from . import views

app_name = 'medical'
urlpatterns = [
    url(r'^drug/add/$', views.add_drug, name='add_drug'),
    url(r'^prescriptions/$', views.view_prescriptions, name='view_prescriptions'),
    url(r'^patient/list/$', views.view_patients, name='view_patients'),
]
