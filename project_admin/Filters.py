#coding:utf-8
'''
Created on 2017年7月3日

@author: lch
'''
import django_filters
from project_admin.models import Project, ProjectInvestData, CompanyBalance
class ProjectFilter(django_filters.rest_framework.FilterSet):
    startDate = django_filters.DateFromToRangeFilter(name="time")
    finishdate = django_filters.DateFromToRangeFilter(name="finish_time")
    name__contains = django_filters.CharFilter(name="name", lookup_expr='contains')
    platformname__contains = django_filters.CharFilter(name="platform", lookup_expr='name__contains')
    class Meta:
        model = Project
        fields = ['id', 'platformname__contains', 'name__contains', 'startDate','state', 'contact', 'coopway', 'settleway',
                  'contract_company','finishdate']

class ProjectInvestDateFilter(django_filters.rest_framework.FilterSet):
    investtime = django_filters.DateFromToRangeFilter(name="invest_time")
    audittime = django_filters.DateTimeFromToRangeFilter(name="audit_time")
    name__contains = django_filters.CharFilter(name="project", lookup_expr='name__contains')
    class Meta:
        model = ProjectInvestData
        fields = ['is_futou', 'invest_time', 'project', 'name__contains', 'investtime','state', 'invest_mobile', 'audittime', 'source']

class CompanyBalanceFilter(django_filters.rest_framework.FilterSet):
    dateft = django_filters.DateFromToRangeFilter(name="date")
    name__contains = django_filters.CharFilter(name="project", lookup_expr='name__contains')
    class Meta:
        model = CompanyBalance
        fields = ['company', 'date', 'name__contains', 'dateft',]