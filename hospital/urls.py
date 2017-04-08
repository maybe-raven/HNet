from django.conf.urls import url
from . import views

app_name = 'hospital'
urlpatterns = [
    url(r'^log/$', views.logView, name='log'),
]