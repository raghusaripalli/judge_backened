from django.conf.urls import url, include
from django.contrib import admin
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token

from .Views_Judge import *
from .Views_User import *
from .Views_Contest import *
from .Views_Problems import *

urlpatterns = [
    url(r'^token-auth/', obtain_jwt_token),
    url(r'^token-refresh/', refresh_jwt_token),
    url(r'^token-verify/', verify_jwt_token),


    url(r'^NestedUser/$', NestedUserList.as_view()),
    url(r'^NestedUser/(?P<pk>[0-9]+)/$', NestedUserDetail.as_view()),
    url(r'^users/$',UserList.as_view()),
    url(r'^users/(?P<pk>[0-9]+)/$',UserDetail.as_view()),
    url(r'^profile/$',ProfileDetail.as_view()),

    url(r'^submit/$',SubmitCode.as_view()),
    url(r'^contests/$',ContestList.as_view()),
    url(r'^contests/(?P<pk>[0-9]+)/$',ContestDetail.as_view()),

    url(r'^contests/(?P<contestid>[0-9]+)/problems/$',ContestProblemsList.as_view()),
    url(r'^contests/(?P<contestid>[0-9]+)/problems/(?P<problemid>[0-9]+)/$',ContestProblemsDetail.as_view())
]
urlpatterns += [
    url(r'^auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
]