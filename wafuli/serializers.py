#coding:utf-8
'''
Created on 2017年8月10日

@author: lch
'''
from rest_framework import serializers
from .models import Hongbao
class HongbaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hongbao
        fields = '__all__'