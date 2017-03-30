#coding:utf-8
'''
Created on 2017年3月30日

@author: lch
'''
from django.shortcuts import render
def channel(request):
    return render(request, 'account/account_channel.html')