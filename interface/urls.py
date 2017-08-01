from django.conf.urls import url, include
from django.contrib import admin
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token

from .views import *
from django.contrib.auth import views
from .forms import LoginForm

urlpatterns = [
    url(r'^$', home, name='home'),
    url(r'^login/$', views.login,{'template_name': 'login.html', 'authentication_form': LoginForm, 'redirect_authenticated_user': True},name="loginn"),
    url(r'^logout/$', views.logout, {'next_page': '/login'}, name="logoutt"),
    url(r'^register/$', register_user, name="registerr"),
]
