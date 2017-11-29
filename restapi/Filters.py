#coding:utf-8
'''
Created on 2017年8月23日

@author: lch
'''
import django_filters
from wafuli.models import TransList, UserEvent
from account.models import MyUser
#         
class TranslistFilter(django_filters.rest_framework.FilterSet):
    trans_date = django_filters.DateFromToRangeFilter(name="time")
    user_mobile = django_filters.CharFilter('user', lookup_expr='mobile')
    user_name = django_filters.CharFilter('user', lookup_expr='username')
    reason_contains = django_filters.CharFilter('reason', lookup_expr='contains')
    class Meta:
        model = TransList
        fields = ['user_mobile', 'user_name', 'reason_contains', 'trans_date', 'transType']
        
# class UserEventFilter(django_filters.rest_framework.FilterSet):
#     investtime = django_filters.DateFromToRangeFilter(name="invest_date")
#     submittime = django_filters.DateFromToRangeFilter(name="submit_time")
#     audittime = django_filters.DateFromToRangeFilter(name="audit_time")
#     project_title_contains = django_filters.CharFilter(name="project", lookup_expr='title__contains')
#     user_mobile = django_filters.CharFilter(name="user", lookup_expr='mobile')
#     user_level = django_filters.CharFilter(name="user", lookup_expr='level')
#     zhifubao_contains = django_filters.CharFilter(name="zhifubao", lookup_expr='contains')
#     project_channel_contains = django_filters.CharFilter(name="project", lookup_expr='channel__contains')
#     class Meta:
#         model = UserEvent
#         exclude = ['invest_image', 'invest_time', 'audit_time']