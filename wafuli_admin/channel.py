#coding:utf-8
'''
Created on 2017年3月27日

@author: lch
'''

import xlrd
from xlwt import *
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import datetime
from django.http.response import JsonResponse, Http404
import traceback
from django.contrib.auth.decorators import login_required
from django.db import transaction
from wafuli.models import UserEvent, Finance
from account.models import DBlock, Channel, MyUser
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

@login_required
@csrf_exempt
def parse_excel(request):
    if request.method == 'GET':
        return render(request,'upload_excel.html')
    else:
        fid = request.POST.get('fid')
        ret = {'code':-1}
        file = request.FILES.get('file')
        filename = './' + str(request.user.mobile) + '.xls'
        with open(filename, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        data = xlrd.open_workbook(filename)
        table = data.sheets()[0]
        nrows = table.nrows
        ncols = table.ncols
        if ncols!=5:
            ret['msg'] = u"文件格式与模板不符，请下载最新模板填写！"
            return ret
        rtable = []
        mobile_list = []
        try:
            for i in range(1,nrows):
                temp = []
                duplic = False
                for j in range(ncols):
                    cell = table.cell(i,j)
                    if j==0:
                        if(cell.ctype!=3):
                            raise Exception(u"投资日期列格式错误，请修改后重新提交。")
                        else:
                            time = xlrd.xldate.xldate_as_datetime(cell.value, 0)
                            temp.append(time)
                    elif j==1:
                        try:
                            mobile = str(int(cell.value)).strip()
                        except Exception,e:
                            raise Exception(u"手机号必须是11位数字，请修改后重新提交。")
                        if len(mobile)==11:
                            temp.append(mobile)
                        else:
                            raise Exception(u"手机号必须是11位数字，请修改后重新提交。")
                        if mobile in mobile_list:
                            duplic = True
                            break;
                        else:
                            mobile_list.append(mobile)
                    elif j==2:
                        term = unicode(cell.value).strip()
                        temp.append(term)
                    elif j==3:
                        amount = cell.value
                        try:
                            if float(amount) == int(amount):
                                amount = int(amount)
                            else:
                                amount = float(amount)
                        except:
                            raise Exception(u"投资金额必须为数字")
                        temp.append(amount)
                    else:
                        remark = cell.value
                        temp.append(remark)
                if duplic:
                    duplic = False
                else:
                    rtable.append(temp)
        except Exception, e:
            traceback.print_exc()
            ret['msg'] = unicode(e)
        
        finance = Finance.objects.first()
        print rtable,mobile_list
        ####开始去重
        with transaction.atomic():
            db_key = DBlock.objects.select_for_update().get(index='event_key')
            temp = UserEvent.objects.filter(event_type='1').exclude(audit_state='2').values('invest_account')
            db_mobile_list = map(lambda x: str(x['invest_account']), temp)
            userevent_list = []
            duplicate_mobile_list = []
            for i in range(len(mobile_list)):
                mob = mobile_list[i]
                if mob in db_mobile_list:
                    duplicate_mobile_list.append(mob)
                else:
                    item = rtable[i]
                    obj = UserEvent(user=request.user, event_type='1',invest_account=mob,
                                    invest_amount=item[3],invest_term=item[2],time=item[0],
                                    audit_state='1',remark=item[4],content_object=finance)
                    userevent_list.append(obj)
            UserEvent.objects.bulk_create(userevent_list)
        print len(userevent_list), len(rtable), nrows-1
#         for item in rtable:
            
#         w = Workbook()     #创建一个工作簿
#         ws = w.add_sheet('hello') 
#         style1 = easyxf(num_format_str='YY/MM/DD')
#         for i in range(len(rtable)):
#             row = rtable[i]
#             for j in range(len(row)):
#                 c = row[j]
#                 if j==0:
#                     ws.write(i,j,c,style1)
#                 else:
#                     ws.write(i,j,c)
#         w.save('out.xls') 
        return JsonResponse(ret)
#         style0 = xlwt.easyxf('font: name Times New Roman, color-index red, bold on', num_format_str='#,##0.00')
#         style1 = xlwt.easyxf(num_format_str='D-MMM-YY')

                
def get_admin_channel_page(request):
    res={'code':0,}
    user = request.user
    if not ( user.is_authenticated() and user.is_staff):
        res['code'] = -1
        res['url'] = reverse('admin:login') + "?next=" + reverse('admin_channel')
        return JsonResponse(res)
    page = request.GET.get("page", None)
    size = request.GET.get("size", 10)
    state = request.GET.get("state",'0')
    
    try:
        size = int(size)
    except ValueError:
        size = 10

    if not page or size <= 0:
        raise Http404
    item_list = []

    item_list = Channel.objects.all()
    startTime = request.GET.get("startTime", None)
    endTime = request.GET.get("endTime", None)
    if startTime and endTime:
        s = datetime.datetime.strptime(startTime,'%Y-%m-%dT%H:%M')
        e = datetime.datetime.strptime(endTime,'%Y-%m-%dT%H:%M')
        item_list = item_list.filter(join_time__range=(s,e))
        
    qq_number = request.GET.get("qq", None)
    if qq_number:
        item_list = item_list.filter(qq_number=qq_number)
    
    mobile = request.GET.get("mobile", None)
    if mobile:
        item_list = item_list.filter(user__mobile=mobile)
        
    paginator = Paginator(item_list, size)
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
    # If page is not an integer, deliver first page.
        contacts = paginator.page(1)
    except EmptyPage:
    # If page is out of range (e.g. 9999), deliver last page of results.
        contacts = paginator.page(paginator.num_pages)
    data = []
    for con in contacts:
        recent_login_time = u'无'
        if con.user.this_login_time:
            recent_login_time = con.user.this_login_time.strftime("%Y-%m-%d %H:%M")
        i = {"username":con.user.username,
             "mobile":con.user.mobile,
             "zhifubao":con.user.zhifubao,
             "zhifubao_name":con.user.zhifubao_name,
             "join_time":con.join_time.strftime("%Y-%m-%d %H:%M"),
             'recent_login_time':recent_login_time,
             "balance":con.user.balance/100.0,
             "id":con.user.id,
             "qq":con.qq_number
             }
        data.append(i)
    if data:
        res['code'] = 1
    res["pageCount"] = paginator.num_pages
    res["recordCount"] = item_list.count()
    res["data"] = data
    return JsonResponse(res)
