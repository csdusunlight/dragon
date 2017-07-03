#coding:utf-8
'''
Created on 2017年7月3日

@author: lch
'''
from rest_framework import serializers
from .models import Project
class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('uuid', 'name', 'time', 'contact', 'coopway', 'settleway', 'state',
                  'contract_company', 'settle_detail', 'paid_amount', 'consume_amount',
                  'return_amount', 'topay_amount', 'profit')