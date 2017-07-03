#coding:utf-8
'''
Created on 2017年7月3日

@author: lch
'''
import django_filters
from project_admin.models import Project
class ProjectFilter(django_filters.rest_framework.FilterSet):
    dateft = django_filters.DateFromToRangeFilter(name="time")

    class Meta:
        model = Project
        fields = ['name', 'dateft','state']