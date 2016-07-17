#coding:utf-8
'''
Created on 2016年7月17日

@author: lch
'''

from django.shortcuts import render, redirect
from wafuli.models import UserEvent, AdminEvent, AuditLog, TransList, UserWelfare,\
    CouponProject
import datetime
from django.db.models import Sum, Count
from django.core.urlresolvers import reverse
from django.http.response import JsonResponse, Http404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from account.transaction import charge_money, charge_score
from decimal import Decimal
import logging
from account.models import MyUser
from wafuli_admin.models import RecommendRank
from wafuli.data import COUPON_TYPE
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
logger = logging.getLogger('wafuli')

def deliver_coupon(request):
    if request.method == 'GET':
        return render(request, 'deliver_coupon.html', {'type_list':COUPON_TYPE})
    

def get_project_list(request):
    if not request.is_ajax():
        raise Http404
    result={'prolist':{}}
    type = request.GET.get('id', None)
    if not type:
        raise Http404
    pro_list = CouponProject.objects.filter(type=str(type)).only('id','title')
    pro_dic={}
    for x in pro_list:
        pro_dic[str(x.id)] = x.title
    result['prolist'] = pro_dic
    return JsonResponse(result)
@csrf_exempt
def parse_file(request):
    result={'user':'aaaa'}
    return JsonResponse(result)