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
# Create your views here.
logger = logging.getLogger('wafuli')

def deliver_coupon(request):
    user = request.user
    if request.method == 'GET':
        if not ( user.is_authenticated() and user.is_staff):
            return redirect(reverse('admin:login') + "?next=" + reverse('admin_index'))
        else:
            return render(request, 'deliver_coupon.html', {'type_list':COUPON_TYPE})
    elif request.method == 'POST':
        result = {'code':0}
        if not user.has_admin_perms('006'):
            result['code'] = -5
            result['res_msg'] = u'您没有操作权限！'
            return JsonResponse(result)
        coupon_type = request.POST.get('selecttype')
        project_id = request.POST.get('selectproject')
        if coupon_type is None or project_id is None:
            raise Http404
        else:
            project_id = int(project_id)
            coupon_type = str(coupon_type)
        project = CouponProject.objects.get(id=project_id)
        success_count = 0
        fail_list = []
        if coupon_type == '0' or coupon_type == '1':
            select_user = request.POST.get('selectuser')
            if select_user is None:
                raise Http404
            else:
                select_user = str(select_user)
            if select_user == '1':
                for user in MyUser.objects.all():
                    Coupon.objects.create(user=user, project=project)
                    success_count += 1
            elif select_user == '2':
                select_list_str = request.POST.get('users')
                if select_list_str is None:
                    raise Http404
                else:
                    select_list_str = str(select_list_str)
                select_list = select_list_str.strip().split('\n')
                user_set = set([])
                for user in select_list:
                    if user:
                        user_set.add(user)
                for username in user_set:
                    try:
                        user = MyUser.objects.get(username = username)
                        Coupon.objects.create(user=user, project=project)
                    except:
                        fail_list.append(username)
                    else:
                        success_count += 1
        elif coupon_type == '2':
            select_list_str = request.POST.get('codes')
            if select_list_str is None:
                raise Http404
            else:
                select_list_str = str(select_list_str)
            select_list = select_list_str.strip().split('\n')
            code_set = set([])
            for code in select_list:
                if code:
                    code_set.add(code)
            for code in code_set:
                Coupon.objects.create(project=project, exchange_code=code)
                success_count += 1
        result.update({'succ_num':success_count, 'fail_list':fail_list})
        return JsonResponse(result)
        
def get_project_list(request):
    if not request.is_ajax():
        raise Http404
    result={'prolist':{}}
    type = request.GET.get('id', None)
    if not type:
        raise Http404
    pro_list = CouponProject.objects.filter(type=str(type), is_del=False).only('id','title')
    pro_dic={}
    for x in pro_list:
        pro_dic[str(x.id)] = x.title
    result['prolist'] = pro_dic
    return JsonResponse(result)
@csrf_exempt
def parse_file(request):
    res={'code':-9,}
    file = request.FILES.get('file')
    if not file:
        res['code'] = -2
        res['res_msg'] = u'请先选择文件！'
    else:
        try:
            res['list'] = handle_uploaded_file(file)
        except:
            res['code'] = -3
            res['res_msg'] = u'文件格式有误！'
        else:
            res['code'] = 0
    return JsonResponse(res)

def handle_uploaded_file(f):
    ret = []
    with open('./name', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    with open('./name', 'r') as file:
        for line in file:
            ret.append(line.strip())
    return ret