#coding:utf-8
from project_admin.serializers import *
# Create your views here.

from rest_framework import generics, permissions
from project_admin.permissions import IsAdminOrReadOnly,\
    CsrfExemptSessionAuthentication
import django_filters
from project_admin.Filters import ProjectFilter, ProjectInvestDateFilter,\
    CompanyBalanceFilter, AccountBillFilter
from django.shortcuts import redirect, render
from django.core.urlresolvers import reverse
from django.http.response import Http404, JsonResponse, HttpResponse
from project_admin.Paginations import ProjectPageNumberPagination
from project_admin.models import *
from django.views.decorators.csrf import csrf_exempt
import xlrd
import logging
from django.db import transaction
from account.models import DBlock
from decimal import Decimal
from xlwt.Workbook import Workbook
from xlwt.Style import easyxf
import StringIO
import traceback
logger = logging.getLogger('wafuli')
class BaseViewMixin(object):
    authentication_classes = (CsrfExemptSessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,IsAdminOrReadOnly)

class ContactList(BaseViewMixin,generics.ListCreateAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    pagination_class = ProjectPageNumberPagination
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_fields = '__all__'
    #     search_fields = ('=name', '=contact')


class ContactDetail(BaseViewMixin,generics.RetrieveUpdateDestroyAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

class PlatformList(BaseViewMixin,generics.ListCreateAPIView):
    queryset = Platform.objects.all()
    serializer_class = PlatformSerializer
    pagination_class = ProjectPageNumberPagination
#     search_fields = ('=name', '=contact')


class PlatformDetail(BaseViewMixin,generics.RetrieveUpdateDestroyAPIView):
    queryset = Platform.objects.all()
    serializer_class = PlatformSerializer

class ProjectList(BaseViewMixin,generics.ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_class = ProjectFilter
    pagination_class = ProjectPageNumberPagination
#     search_fields = ('=name', '=contact')


class ProjectDetail(BaseViewMixin,generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

class ProjectInvestDataList(BaseViewMixin,generics.ListCreateAPIView):
    queryset = ProjectInvestData.objects.all()
    serializer_class = ProjectInvestDataSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
#     filter_fields = ('__all__')
    filter_class = ProjectInvestDateFilter
    pagination_class = ProjectPageNumberPagination
#     search_fields = ('=name', '=contact')


class ProjectInvestDataDetail(BaseViewMixin,generics.RetrieveUpdateDestroyAPIView):
    queryset = ProjectInvestData.objects.all()
    serializer_class = ProjectInvestDataSerializer

class CompanyBalanceList(BaseViewMixin,generics.ListCreateAPIView):
    queryset = CompanyBalance.objects.all()
    serializer_class = CompanyBalanceSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
#     filter_fields = ('__all__')
    filter_class = CompanyBalanceFilter
    pagination_class = ProjectPageNumberPagination
#     search_fields = ('=name', '=contact')


class CompanyBalanceDetail(BaseViewMixin,generics.RetrieveUpdateDestroyAPIView):
    queryset = CompanyBalance.objects.all()
    serializer_class = CompanyBalanceSerializer


class ProjectStatisList(BaseViewMixin,generics.ListCreateAPIView):
    queryset = ProjectStatis.objects.all()
    serializer_class = ProjectStatisSerializer
    pagination_class = ProjectPageNumberPagination
class DayStatisList(BaseViewMixin,generics.ListCreateAPIView):
    queryset = DayStatis.objects.all()
    serializer_class = DayStatisSerializer
    pagination_class = ProjectPageNumberPagination
class AccountList(BaseViewMixin,generics.ListCreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
#     filter_fields = ('__all__')
#     filter_class = ProjectInvestDateFilt
    pagination_class = ProjectPageNumberPagination
class AccountDetail(BaseViewMixin,generics.RetrieveUpdateDestroyAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    
class AccountBillList(BaseViewMixin,generics.ListCreateAPIView):
    queryset = AccountBill.objects.all()
    serializer_class = AccountBillSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
#     filter_fields = ('__all__')
    filter_class = AccountBillFilter
    pagination_class = ProjectPageNumberPagination
class AccountBillDetail(BaseViewMixin,generics.RetrieveUpdateDestroyAPIView):
    queryset = AccountBill.objects.all()
    serializer_class = AccountBillSerializer
class DayAccountStatisList(BaseViewMixin,generics.ListCreateAPIView):
    queryset = DayAccountStatic.objects.all()
    serializer_class = DayAccountStatisSerializer
    pagination_class = ProjectPageNumberPagination
# 立项部分增加
def project_index(request):
    admin_user = request.user
    if request.method == "GET":
        if not ( admin_user.is_authenticated() and admin_user.is_staff):
            return redirect(reverse('admin:login') + "?next=" + reverse('admin_finance'))
        return render(request,"project.html")



def project_data(request):
    admin_user = request.user
    if request.method == "GET":
        if not ( admin_user.is_authenticated() and admin_user.is_staff):
            return redirect(reverse('admin:login') + "?next=" + reverse('admin_finance'))
        return render(request,"project_data.html")

def project_finance(request):
    admin_user = request.user
    if request.method == "GET":
        if not ( admin_user.is_authenticated() and admin_user.is_staff):
            return redirect(reverse('admin:login') + "?next=" + reverse('admin_finance'))
        return render(request,"project_finance.html")



def project_settle(request):
    admin_user = request.user
    if request.method == "GET":
        if not ( admin_user.is_authenticated() and admin_user.is_staff):
            return redirect(reverse('admin:login') + "?next=" + reverse('admin_finance'))
        return render(request,"project_settle.html")

# 立项部分---end


# 综合管理部分修改
def project_detail(request):
    admin_user = request.user
    if request.method == "GET":
        if not ( admin_user.is_authenticated() and admin_user.is_staff):
            return redirect(reverse('admin:login') + "?next=" + reverse('admin_finance'))
        return render(request,"project_detail.html")
def project_status(request):
    admin_user = request.user
    if request.method == "GET":
        if not ( admin_user.is_authenticated() and admin_user.is_staff):
            return redirect(reverse('admin:login') + "?next=" + reverse('admin_finance'))
        return render(request,"project_status.html")

def jiafang_detail(request):
    admin_user = request.user
    if request.method == "GET":
        if not ( admin_user.is_authenticated() and admin_user.is_staff):
            return redirect(reverse('admin:login') + "?next=" + reverse('admin_finance'))
        return render(request,"jiafang_detail.html")

def finance_pandect(request):
    admin_user = request.user
    if request.method == "GET":
        if not ( admin_user.is_authenticated() and admin_user.is_staff):
            return redirect(reverse('admin:login') + "?next=" + reverse('admin_finance'))
        return render(request,"finance_pandect.html")

def account_manage(request):
    admin_user = request.user
    if request.method == "GET":
        if not ( admin_user.is_authenticated() and admin_user.is_staff):
            return redirect(reverse('admin:login') + "?next=" + reverse('admin_finance'))
        return render(request,"account_manage.html")
def account_detail(request):
    admin_user = request.user
    if request.method == "GET":
        if not ( admin_user.is_authenticated() and admin_user.is_staff):
            return redirect(reverse('admin:login') + "?next=" + reverse('admin_finance'))
        return render(request,"account_detail.html")

def contacts_detail(request, id):
    return render(request,"contacts_detail.html",{'platform_id':id})
# 综合管理部分修改----end


@csrf_exempt
def import_projectdata_excel(request):
    admin_user = request.user
    if not ( admin_user.is_authenticated() and admin_user.is_staff):
        raise Http404
    ret = {'code':-1}
    file = request.FILES.get('file')
#     print file.name
    with open('./out.xls', 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    data = xlrd.open_workbook('./out.xls')
    table = data.sheets()[0]
    nrows = table.nrows
    ncols = table.ncols
    if ncols!=8:
        ret['msg'] = u"文件格式与模板不符，请下载最新模板填写！"
        return JsonResponse(ret)
    rtable = {}
    mobile_list = []
    dup={}
    try:
        for i in range(1,nrows):
            temp = []
            for j in range(ncols):
                cell = table.cell(i,j)
                value = cell.value
                if j==0:
                    id = int(value)
                    temp.append(id)
                elif j==2:
                    value = value.strip()
                    if value == u"首投":
                        temp.append(False)
                    elif value == u"复投":
                        temp.append(True)
                    else:
                        raise Exception(u"必须为首投或复投。")
                elif j==3:
                    if(cell.ctype!=3):
                        raise Exception(u"投资日期列格式错误，请修改后重新提交。")
                    else:
                        time = xlrd.xldate.xldate_as_datetime(value, 0)
                        temp.append(time)
                elif j==4:
                    try:
                        mobile = str(int(value)).strip()
                    except Exception,e:
                        raise Exception(u"手机号必须是11位数字，请修改后重新提交。")
                    if len(mobile)==11:
                        temp.append(mobile)
                    else:
                        raise Exception(u"手机号必须是11位数字，请修改后重新提交。")
                elif j==5 or j==7:
                    try:
                        temp.append(Decimal(value))
                    except:
                        raise Exception(u"投资金额必须为数字")
                elif j==6:
                    try:
                        temp.append(int(value))
                    except Exception,e:
                        raise Exception(u"投资标期必须为数字，请修改后重新提交。")
                else:
                    temp.append(value)
            tid = temp[0]
            if not temp[2]:
                if dup.has_key(tid):
                    if temp[4] in dup[tid]:
                        continue
                    else:
                        dup[tid].append(temp[4])
                else:
                    dup[tid] = [temp[4],]

            if rtable.has_key(tid):
                rtable[tid].append(temp)
            else:
                rtable[tid]=[temp,]
    except Exception, e:
        logger.info(unicode(e))
#             traceback.print_exc()
        ret['msg'] = unicode(e)
        return JsonResponse(ret)
    ####开始去重
    investdata_list = []
    duplicate_mobile_list = []
    try:
        with transaction.atomic():
            db_key = DBlock.objects.select_for_update().get(index='investdata')
            print rtable
            for id, values in rtable.items():
                temp = ProjectInvestData.objects.filter(project_id=id).values('invest_mobile')
                db_mobile_list = map(lambda x: x['invest_mobile'], temp)
                for item in values:
                    pid = item[0]
                    time = item[3]
                    mob = item[4]
                    is_futou = item[2]
                    amount = item[5]
                    term = item[6]
                    settle = item[7]
                    source = ''
                    remark = ''
                    if not is_futou and mob in db_mobile_list:
                        duplicate_mobile_list.append(mob)
                    else:
                        obj = ProjectInvestData(project_id=pid, invest_mobile=mob,settle_amount=settle,
                                        invest_amount=amount,invest_term=term,invest_time=time,
                                        state='1',remark=remark,source=source)
                        investdata_list.append(obj)
            ProjectInvestData.objects.bulk_create(investdata_list)
    except Exception, e:
        logger.info(unicode(e))
#             traceback.print_exc()
        ret['msg'] = unicode(e)
        return JsonResponse(ret)
    succ_num = len(investdata_list)
    duplic_num2 = len(duplicate_mobile_list)
    duplic_num1 = nrows - succ_num - duplic_num2
    duplic_mobile_list_str = u'，'.join(duplicate_mobile_list)
    ret.update(code=0,sun=succ_num, dup1=duplic_num1, dup2=duplic_num2, anum=nrows-1, dupstr=duplic_mobile_list_str)
    return JsonResponse(ret)

@csrf_exempt
def import_audit_projectdata_excel(request):
    admin_user = request.user
    if not ( admin_user.is_authenticated() and admin_user.is_staff):
        raise Http404
    ret = {'code':-1}
    file = request.FILES.get('file')
#     print file.name
    with open('./out2.xls', 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    data = xlrd.open_workbook('./out2.xls')
    table = data.sheets()[0]
    nrows = table.nrows
    ncols = table.ncols
    if ncols!=13:
        ret['msg'] = u"文件格式与模板不符，请下载最新模板填写！"
        return JsonResponse(ret)
    rtable = []
    mobile_list = []
    dup={}
    try:
        for i in range(1,nrows):
            temp = []
            duplic = False
            for j in range(ncols):
                cell = table.cell(i,j)
                if j==0:
                    id = int(cell.value)
                    temp.append(id)
                elif j==9:
                    result = cell.value.strip()
                    if result == u"是":
                        result = True
                        temp.append(True)
                    elif result == u"否":
                        result = False
                        temp.append(False)
                    else:
                        raise Exception(u"审核结果必须为是或否。")
                elif j==10:
                    return_amount = 0
                    if cell.value:
                        return_amount = Decimal(cell.value)
                    elif result:
                        raise Exception(u"审核结果为是时，返现金额不能为空或零。")
                    temp.append(return_amount)
                elif j==11:
                    value = cell.value.strip()
                    if value == u"网站":
                        temp.append('site')
                    elif value == u"渠道":
                        temp.append('channel')
                    else:
                        raise Exception(u"必须为网站或渠道。")
                elif j==12:
                    reason = cell.value
                    temp.append(reason)
                else:
                    continue
            rtable.append(temp)
    except Exception, e:
        logger.info(unicode(e))
#             traceback.print_exc()
        ret['msg'] = unicode(e)
        return JsonResponse(ret)
    ####开始去重
        admin_user = request.user
    suc_num = 0
    try:
        for row in rtable:
            id = row[0]
            result = row[1]
            retamount = row[2]
            source = row[3]
            remark = row[4]
            event = ProjectInvestData.objects.get(id=id)
            if event.state != '1':
                continue
            if result:
                amount = retamount
                event.state = '0'
                event.return_amount = retamount
                event.audit_time = datetime.datetime.now()
                event.source = source
                event.remark = remark
                event.save(update_fields=['state', 'return_amount', 'audit_time', 'source', 'remark'])
                suc_num += 1
        ret['code'] = 0
    except Exception as e:
        exstr = traceback.format_exc()
        logger.info(unicode(exstr))
        ret['code'] = 1
        ret['msg'] = unicode(e)
    ret['num'] = suc_num
    return JsonResponse(ret)
def export_investdata_excel(request):
    user = request.user
    item_list = []
    item_list = ProjectInvestData.objects
    is_futou = request.GET.get("is_futou", None)
    if is_futou=="true":
        item_list = item_list.filter(is_futou=True)
    elif is_futou=="false":
        item_list = item_list.filter(is_futou=False)
    state = request.GET.get("state", None)
    if state:
        item_list = item_list.filter(state=state)
    source = request.GET.get("source", None)
    if source:
        item_list = item_list.filter(source=source)
    invest_mobile = request.GET.get("invest_mobile", None)
    if invest_mobile:
        item_list = item_list.filter(invest_mobile=invest_mobile)
    name__contains = request.GET.get("name__contains", None)
    if name__contains:
        item_list = item_list.filter(project__name__contains=name__contains)
    project = request.GET.get("project", None)
    if project:
        item_list = item_list.filter(project_id=project)
    investtime_0 = request.GET.get("investtime_0", None)
    investtime_1 = request.GET.get("investtime_1", None)
    audittime_0 = request.GET.get("audittime_0", None)
    audittime_1 = request.GET.get("audittime_1", None)
    if investtime_0 and investtime_1:
        s = datetime.date.strptime(investtime_0,'%Y-%m-%d')
        e = datetime.date.strptime(investtime_1,'%Y-%m-%d')
        item_list = item_list.filter(invest_time__range=(s,e))
    if audittime_0 and audittime_1:
        s = datetime.datetime.strptime(audittime_0,'%Y-%m-%dT%H:%M')
        e = datetime.datetime.strptime(audittime_1,'%Y-%m-%dT%H:%M')
        item_list = item_list.filter(audit_time__range=(s,e))
  
    item_list = item_list.select_related('project').order_by('invest_time')
    data = []
    for con in item_list:
        project = con.project
        id=con.id
        project_id = project.id
        project_name = project.name
        if con.is_futou:
            is_futou = u"复投"
        else:
            is_futou = u"首投"
        invest_time = con.invest_time
        invest_mobile = con.invest_mobile
        invest_amount = con.invest_amount
        invest_term = con.invest_term
        settle_amount = con.settle_amount
        if con.state=='0':
            result = u'是'
            return_amount = con.return_amount
        else:
            result = u'否'
            return_amount = ''
        source = con.get_source_display()
        remark = con.remark
        data.append([id, project_id, project_name, is_futou, invest_time, invest_mobile, invest_amount, invest_term, settle_amount,
                     result, return_amount, source, remark])
    w = Workbook()     #创建一个工作簿
    ws = w.add_sheet(u'待审核记录')     #创建一个工作表
    title_row = [u'记录ID',u'项目编号',u'项目名称',u'首投/复投',u'投资日期', u'提交手机号',u'投资金额' ,u'投资标期',u'预估消耗', u'审核状态',
                 u'返现金额',u'投资来源',u'备注']
    for i in range(len(title_row)):
        ws.write(0,i,title_row[i])
    row = len(data)
    style1 = easyxf(num_format_str='YY/MM/DD')
    for i in range(row):
        lis = data[i]
        col = len(lis)
        for j in range(col):
            if j==4:
                ws.write(i+1,j,lis[j],style1)
            else:
                ws.write(i+1,j,lis[j])
    sio = StringIO.StringIO()
    w.save(sio)
    sio.seek(0)
    response = HttpResponse(sio.getvalue(), content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=导出表格.xls'
    response.write(sio.getvalue())
    return response

def export_account_bill_excel(request):
    user = request.user
    item_list = []
    item_list = AccountBill.objects.all()
    name = request.GET.get("name", None)
    if name:
        item_list = item_list.filter(account__name=name)
    account = request.GET.get("account", None)
    if account:
        item_list = item_list.filter(account_id=account)
    account_type = request.GET.get("account_type", None)
    if account_type:
        item_list = item_list.filter(account__type=account_type)
    type = request.GET.get("type", None)
    if type:
        item_list = item_list.filter(type=type)
    subtype = request.GET.get("subtype", None)
    if subtype:
        item_list = item_list.filter(subtype=subtype)
    target = request.GET.get("target", None)
    if target:
        item_list = item_list.filter(target=target)
    timeft_0 = request.GET.get("timeft_0", None)
    timeft_1 = request.GET.get("timeft_1", None)
    if timeft_0 and timeft_1:
        s = datetime.date.strptime(timeft_0,'%Y-%m-%dT%H:%M')
        e = datetime.date.strptime(timeft_1,'%Y-%m-%dT%H:%M')
        item_list = item_list.filter(time__range=(s,e))
    data = []
    for con in item_list:
        time = con.time.strftime("%Y-%m-%d %H:%M")
        account_id = con.account_id
        account_type = con.account.get_type_display()
        account_name = con.account.name
        bill_type = con.get_type_display()
        subtype = con.get_subtype_display()
        target = con.target
        amount = con.amount
        balance = con.account.balance
        remark = con.remark
        data.append([time, account_id, account_type, account_name, bill_type, subtype, 
                     target, amount, balance, remark])
    w = Workbook()     #创建一个工作簿
    ws = w.add_sheet(u'账目明细')     #创建一个工作表
    title_row = [u'账单时间',u'账户ID',u'账户类型',u'账户名称',u'账单类型', u'收/支类型',
                 u'交易对象',u'交易金额',u'账户余额',u'备注']
    for i in range(len(title_row)):
        ws.write(0,i,title_row[i])
    row = len(data)
    style1 = easyxf(num_format_str='YY/MM/DD HH:mm')
    for i in range(row):
        lis = data[i]
        col = len(lis)
        for j in range(col):
            if j==0:
                ws.write(i+1,j,lis[j],style1)
            else:
                ws.write(i+1,j,lis[j])
    sio = StringIO.StringIO()
    w.save(sio)
    sio.seek(0)
    response = HttpResponse(sio.getvalue(), content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=导出表格.xls'
    response.write(sio.getvalue())
    return response