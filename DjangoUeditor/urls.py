#coding:utf-8
from django.conf.urls import patterns, url

from views import get_ueditor_controller

urlpatterns = patterns('',
    url(r'^controller/$',get_ueditor_controller)
)