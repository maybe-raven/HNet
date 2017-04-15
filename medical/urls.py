from django.conf.urls import url
from . import views

app_name = 'medical'
urlpatterns = [
    url('^drug/add/$', views.add_drug, name='add_drug'),
    url(r'^drug/remove/(?P<drug_id>[0-9]+)/$', views.remove_drug, name='remove_drug'),
]
