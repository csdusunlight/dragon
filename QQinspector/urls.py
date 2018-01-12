#coding:utf-8
'''
Created on 20170703

@author: lch
'''

from django.conf.urls import url
from QQinspector import views

urlpatterns = [
    url(r'^upload/$', views.upload, name="upload"),
]
