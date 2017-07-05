#coding:utf-8
'''
Created on 2017年7月3日

@author: lch
'''
from rest_framework import serializers
from .models import *
class ProjectSerializer(serializers.ModelSerializer):
    state_des = serializers.CharField(source='get_state_display', read_only=True)
    settleway_des = serializers.CharField(source='get_settleway_display', read_only=True)
    class Meta:
        model = Project
        fields = ('uuid', 'name', 'time', 'contact', 'coopway', 'settleway', 'settleway_des', 'state','state_des',
                  'contract_company', 'settle_detail', 'paid_amount', 'consume_amount',
                  'return_amount', 'topay_amount', 'profit')
#         read_only_fields = ('uuid',)

class ProjectInvestDataSerializer(serializers.ModelSerializer):
    projectname = serializers.CharField(source='project.name', read_only=True)
    projectuuid = serializers.CharField(source='project.uuid', read_only=True)
    state_des = serializers.CharField(source='get_state_display', read_only=True)
    class Meta:
        model = ProjectInvestData
        fields =('id', 'project', 'projectname', 'projectuuid','invest_mobile','invest_time','invest_amount',
                 'invest_term','settle_amount','return_amount','state','state_des','remark')
        read_only_fields = ('id',)

class CompanyBalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyBalance
        fields =('company', 'date','income','expenditure','remark')
        read_only_fields = ('id',)