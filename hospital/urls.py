from django.conf.urls import url
from . import views

app_name = 'hospital'
urlpatterns = [
    url(r'^log/$', views.logView, name='log'),
    url(r'^discharge/(?P<treatmentsession_id>[0-9]+)/$', views.discharge_patient, name='discharge_patient'),
]