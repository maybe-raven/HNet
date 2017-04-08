from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

app_name = 'account'
urlpatterns = [
    url(r'^login/$', auth_views.login, {'template_name': 'account/login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'template_name': 'account/logout.html'}, name='logout'),
    url(r'^register/$', views.register, name='register'),
    url(r'^register/done/$', views.register_done, name='register_done'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^patient/$', views.patient, name='patient'),
]
