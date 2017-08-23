#coding:utf-8
'''
Created on 2017年8月10日

@author: lch
'''
from rest_framework import serializers
from .models import Hongbao, MediaProject
from wafuli.models import UserEvent
class HongbaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hongbao
        fields = '__all__'
class MediaProjectSerializer(serializers.ModelSerializer):
    state_des = serializers.CharField(source='get_state_display', read_only=True)
    class Meta:
        model = MediaProject
        fields = ['id', 'title', 'pub_date', 'state', 'is_vip_bonus', 'is_multisub_allowed',
                  'is_need_screenshot', 'attention', 'state_des']
        read_only_fields = ('id', 'pub_date')

class UserEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserEvent
        fields = '__all__'