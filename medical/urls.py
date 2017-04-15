from django.conf.urls import url
from . import views

app_name = 'medical'
urlpatterns = [
    url('^drug/add/$', views.add_drug, name='add_drug'),
    url('^prescription/add/$', views.add_prescription, name='add_prescription'),
    url('^prescription/remove/$', views.remove_prescription, name='remove_prescription'),
]
