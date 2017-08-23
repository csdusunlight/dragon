#coding:utf-8
'''
Created on 2017年8月22日

@author: lch
'''
from rest_framework import generics
from wafuli.serializers import MediaProjectSerializer, UserEventSerializer
from wafuli.models import MediaProject, UserEvent
import django_filters
from project_admin.Paginations import ProjectPageNumberPagination
from project_admin.views import BaseViewMixin
class MediaProjectList(generics.ListCreateAPIView):
    queryset = MediaProject.objects.all()
    serializer_class = MediaProjectSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend, )
    filter_fields = ['state',]
    pagination_class = ProjectPageNumberPagination
    
class UserEventList(BaseViewMixin,generics.ListCreateAPIView):
    queryset = UserEvent.objects.all()
    serializer_class = UserEventSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend, )
    filter_fields = ['event_type','audit_state']
    pagination_class = ProjectPageNumberPagination
    
class UserEventDetail(BaseViewMixin,generics.RetrieveUpdateDestroyAPIView):
    queryset = UserEvent.objects.all()
    serializer_class = UserEventSerializer