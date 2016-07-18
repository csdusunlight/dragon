#coding:utf-8
'''
Created on 2016年7月17日

@author: lch
'''

from django.shortcuts import render, redirect
from wafuli.models import UserEvent, AdminEvent, AuditLog, TransList, UserWelfare,\
    CouponProject, Coupon
import datetime
from django.db.models import Sum, Count
from django.core.urlresolvers import reverse
from django.http.response import JsonResponse, Http404, HttpResponseRedirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from account.transaction import charge_money, charge_score
from decimal import Decimal
import logging
from account.models import MyUser
from wafuli_admin.models import RecommendRank
from wafuli.data import COUPON_TYPE
from django.views.decorators.csrf import csrf_exempt
from Canvas import Line
from httplib import HTTPResponse
# Create your views here.
logger = logging.getLogger('wafuli')

def deliver_coupon(request):
    if request.method == 'GET':
        return render(request, 'deliver_coupon.html', {'type_list':COUPON_TYPE})
    elif request.method == 'POST':
        coupon_type = request.POST.get('selecttype')
        project_id = request.POST.get('selectproject')
        project = CouponProject.objects.get(id=project_id)
        if not (coupon_type and project_id):
            raise Http404
        if coupon_type == '0':
            select_user = request.POST.get('selectuser')
            if not select_user:
                raise Http404
            if select_user == '1':
                for i in MyUser.objects.all():
                    Coupon.objects.create(user=i, project=project)
            elif select_user == '2':
                select_list_str = request.POST.get('users')
                select_list_str = select_list_str.strip().split('\n')
                user_set = set([])
                for user in select_list_str:
                    user_set.add(user)
                success_list = []
                
                for user in user_set:
                    
        return HttpResponseRedirect('deliver_coupon')
            
            
        

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
    ret = handle_uploaded_file(request.FILES['file'])
    result={'user':ret}
    return JsonResponse(result)

def handle_uploaded_file(f):
    ret = []
    with open('./name', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    with open('./name', 'r') as file:
        for line in file:
            ret.append(line.strip())
    return ret