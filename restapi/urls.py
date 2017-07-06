"""Judge URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token

from .views import *

urlpatterns = [
    url(r'^token-auth/', obtain_jwt_token),
    url(r'^token-refresh/', refresh_jwt_token),
    url(r'^token-verify/', verify_jwt_token),


    url(r'^NestedUser/$', NestedUserList.as_view()),
    url(r'^NestedUser/(?P<pk>[0-9]+)/$', NestedUserDetail.as_view()),
    url(r'^users/$',UserList.as_view()),
    url(r'^users/(?P<pk>[0-9]+)/$',UserDetail.as_view()),
    url(r'^profile/$',ProfileDetail.as_view()),


    # url(r'^submit/$',SubmitCode.as_view())
]
urlpatterns += [
    url(r'^auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
]