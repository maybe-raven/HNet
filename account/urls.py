from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

app_name = 'account'
urlpatterns = [
    url(r'^login/$', auth_views.login, {'template_name': 'account/common/login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'template_name': 'account/common/logout.html'}, name='logout'),
    url(r'^patient/register/$', views.register_patient, name='register_patient'),
    url(r'^administrator/create/$', views.create_administrators, name='create_administrator'),
    url(r'^doctor/create/$', views.register_doctor, name='create_doctor'),
    url(r'^profile/$', views.profile, name='profile'),
]
