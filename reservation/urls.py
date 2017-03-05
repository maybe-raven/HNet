from django.conf.urls import url
from . import views

app_name = 'reservation'
urlpatterns = [

    url(r'^calendar/$', views.calendar, name='calendar_now'),
    url(r'^calendar/(?P<month>[0-9]{1,2})/(?P<year>[0-9]{4})/$', views.calendar, name='calendar'),
    url(r'^overview/$', views.overview, name='overview'),
    url(r'^detail/(?P<appointment_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^create/$', views.create_appointment, name='create'),
    url(r'^create/done$', views.create_appointment_done, name='create_done'),
    url(r'^edit/(?P<appointment_id>[0-9]+)/$', views.edit_appointment, name='edit'),
    url(r'^cancel/(?P<appointment_id>[0-9]+)/$', views.cancel_appointment, name='cancel'),
]
