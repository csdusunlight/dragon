#coding:utf-8
'''
Created on 2017年7月3日

@author: lch
'''
import django_filters
from project_admin.models import Project, ProjectInvestData, ProjectBalance
class ProjectFilter(django_filters.rest_framework.FilterSet):
    dateft = django_filters.DateFromToRangeFilter(name="time")
    name__contains = django_filters.CharFilter(name="name", lookup_expr='contains')
    class Meta:
        model = Project
        fields = ['uuid', 'name__contains', 'dateft','state', 'contact', 'coopway', 'settleway',
                  'contract_company']

class ProjectInvestDateFilter(django_filters.rest_framework.FilterSet):
    dateft = django_filters.DateFromToRangeFilter(name="invest_time")
    name__contains = django_filters.CharFilter(name="project", lookup_expr='name__contains')
    class Meta:
        model = ProjectInvestData
        fields = ['invest_time', 'project', 'name__contains', 'dateft','state', 'invest_mobile']

class ProjectBalanceFilter(django_filters.rest_framework.FilterSet):
    dateft = django_filters.DateFromToRangeFilter(name="date")
    name__contains = django_filters.CharFilter(name="project", lookup_expr='name__contains')
    class Meta:
        model = ProjectBalance
        fields = ['project', 'date', 'name__contains', 'dateft',]