#coding:utf-8
'''
Created on 2017年7月3日

@author: lch
'''
import django_filters
from project_admin.models import Project
class ProjectFilter(django_filters.rest_framework.FilterSet):
    dateft = django_filters.DateFromToRangeFilter(name="time")
    name__contains = django_filters.CharFilter(name="name", lookup_expr='contains')
    class Meta:
        model = Project
        fields = ['uuid', 'name__contains', 'dateft','state', 'contact', 'coopway', 'settleway',
                  'contract_company']