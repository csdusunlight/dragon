#coding:utf-8
'''
Created on 2017年3月30日

@author: lch
'''
from django.shortcuts import render
from django.http.response import JsonResponse
from wafuli.models import UserEvent, Finance
from account.models import DBlock
from django.db import transaction
import traceback
import xlrd
import os
from dragon.settings import STATIC_DIR
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

@login_required
@csrf_exempt
def channel(request):
    if request.method == 'POST':
        fid = request.POST.get('fid')
        ret = {'code':-1}
        file = request.FILES.get('userfile')
        filename = os.path.join(STATIC_DIR, 'excel', request.user.mobile + '.xls').replace('\\','/')
        print filename
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
        succ_num = len(userevent_list)
        duplic_num1 = nrows - len(rtable)- 1
        duplic_num2 = duplic_num1 - succ_num
        duplic_mobile_list_str = ','.join(duplicate_mobile_list)
        ret.update(code=0,sun=succ_num, dup1=duplic_num1, dup2=duplic_num2, dupstr=duplic_mobile_list_str)
        return JsonResponse(ret)
    else:
        return render(request, 'account/account_channel.html')