
from django.conf.urls import url, include
from restapi import views
from wafuli import rest

urlpatterns = [
    url(r'^api-auth/', include('rest_framework.urls',namespace='rest_framework')),
    url(r'^translist/$', views.TranslistList.as_view()),
]
