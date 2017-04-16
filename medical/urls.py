from django.conf.urls import url
from . import views

app_name = 'medical'
urlpatterns = [
    url('^drug/add/$', views.add_drug, name='add_drug'),
    url('^drug/update/S', views.update_drug, name='update_drug')
]
