from django.conf.urls import url
from . import views

app_name = 'hospital'
urlpatterns = [
    url(r'^log/$', views.logView, name='log'),
    url(r'^statistics/$', views.statisticsView, name='statistics'),
    url(r'^admit/(?P<patient_id>[0-9]+)/$', views.admit_patient, name='admit_patient'),
    url(r'^discharge/(?P<patient_id>[0-9]+)/$', views.discharge_patient, name='discharge_patient'),
]
