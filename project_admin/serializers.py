#coding:utf-8
'''
Created on 2017年7月3日

@author: lch
'''
from rest_framework import serializers
from .models import *
class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'
class PlatformSerializer(serializers.ModelSerializer):
#     contacts = serializers.PrimaryKeyRelatedField(many=True, queryset=Contact.objects.all())
    contacts = ContactSerializer(many=True)
    class Meta:
        model = Platform
        fields = ('id', 'name', 'url', 'contacts')
class ProjectSerializer(serializers.ModelSerializer):
    state_des = serializers.CharField(source='get_state_display', read_only=True)
    settleway_des = serializers.CharField(source='get_settleway_display', read_only=True)
    platformname = serializers.CharField(source='platform.name', read_only=True)
    class Meta:
        model = Project
        fields = ('id', 'name', 'platform','platformname','time', 'contact', 'coopway', 'settleway', 'settleway_des', 'state','state_des',
                  'contract_company', 'settle', 'cost', 'consume',
                  'topay_amount', 'profit')
        read_only_fields = ('id', 'profit','topay_amount','settleway_des','consume','state_des', 'time')

class ProjectInvestDataSerializer(serializers.ModelSerializer):
    projectname = serializers.CharField(source='project.name', read_only=True)
#     projectid = serializers.CharField(source='project.id', read_only=True)
    state_des = serializers.CharField(source='get_state_display', read_only=True)
    class Meta:
        model = ProjectInvestData
        fields =('id', 'project', 'projectname', 'is_futou','invest_mobile','invest_time','invest_amount',
                 'invest_term','settle_amount','return_amount','state','state_des','remark')
        read_only_fields = ('id',)

class CompanyBalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyBalance
        fields ='__all__'
        read_only_fields = ('id',)