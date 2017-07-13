#coding:utf-8
from .models import Project
from project_admin.serializers import ProjectSerializer,\
    ProjectInvestDataSerializer, CompanyBalanceSerializer, PlatformSerializer,\
    ContactSerializer, ProjectStatisSerializer, DayStatisSerializer
# Create your views here.

from rest_framework import generics, permissions
from project_admin.permissions import IsAdminOrReadOnly,\
    CsrfExemptSessionAuthentication
import django_filters
from project_admin.Filters import ProjectFilter, ProjectInvestDateFilter,\
    CompanyBalanceFilter
from django.shortcuts import redirect, render
from django.core.urlresolvers import reverse
from django.http.response import Http404, JsonResponse
from project_admin.Paginations import ProjectPageNumberPagination
from project_admin.models import *
from django.views.decorators.csrf import csrf_exempt
import xlrd
import logging
from django.db import transaction
from account.models import DBlock
from decimal import Decimal
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

def contacts_detail(request):
    admin_user = request.user
    if request.method == "GET":
        if not ( admin_user.is_authenticated() and admin_user.is_staff):
            return redirect(reverse('admin:login') + "?next=" + reverse('admin_finance'))
        return render(request,"contacts_detail.html")
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
    if ncols!=10:
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
                elif j==8:
                    value = value.strip()
                    if value == u"网站":
                        temp.append('site')
                    elif value == u"渠道":
                        temp.append('channel')
                    else:
                        raise Exception(u"必须为网站或渠道。")
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
                source = item[8]
                remark = item[9]
                if not is_futou and mob in db_mobile_list:
                    duplicate_mobile_list.append(mob)
                else:
                    obj = ProjectInvestData(project_id=pid, invest_mobile=mob,settle_amount=settle,
                                    invest_amount=amount,invest_term=term,invest_time=time,
                                    state='1',remark=remark,source=source)
                    investdata_list.append(obj)
        ProjectInvestData.objects.bulk_create(investdata_list)
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
    if ncols!=10:
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
                elif j==8:
                    value = value.strip()
                    if value == u"网站":
                        temp.append('site')
                    elif value == u"渠道":
                        temp.append('channel')
                    else:
                        raise Exception(u"必须为网站或渠道。")
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
                source = item[8]
                remark = item[9]
                if not is_futou and mob in db_mobile_list:
                    duplicate_mobile_list.append(mob)
                else:
                    obj = ProjectInvestData(project_id=pid, invest_mobile=mob,settle_amount=settle,
                                    invest_amount=amount,invest_term=term,invest_time=time,
                                    state='1',remark=remark,source=source)
                    investdata_list.append(obj)
        ProjectInvestData.objects.bulk_create(investdata_list)
    succ_num = len(investdata_list)
    duplic_num2 = len(duplicate_mobile_list)
    duplic_num1 = nrows - succ_num - duplic_num2
    duplic_mobile_list_str = u'，'.join(duplicate_mobile_list)
    ret.update(code=0,sun=succ_num, dup1=duplic_num1, dup2=duplic_num2, anum=nrows-1, dupstr=duplic_mobile_list_str)
    return JsonResponse(ret)

def export_investdata_excel(request):
    user = request.user
    item_list = []
    item_list = ProjectInvestData.objects
    startTime = request.GET.get("startTime", None)
    endTime = request.GET.get("endTime", None)
    startTime2 = request.GET.get("startTime2", None)
    endTime2 = request.GET.get("endTime2", None)
    state = request.GET.get("state",'1')
    if startTime and endTime:
        s = datetime.datetime.strptime(startTime,'%Y-%m-%dT%H:%M')
        e = datetime.datetime.strptime(endTime,'%Y-%m-%dT%H:%M')
        item_list = item_list.filter(time__range=(s,e))
    if startTime2 and endTime2:
        s = datetime.datetime.strptime(startTime2,'%Y-%m-%dT%H:%M')
        e = datetime.datetime.strptime(endTime2,'%Y-%m-%dT%H:%M')
        item_list = item_list.filter(audit_time__range=(s,e))
    username = request.GET.get("username", None)
    if username:
        item_list = item_list.filter(user__username=username)
    mobile = request.GET.get("mobile", None)
    if mobile:
        item_list = item_list.filter(user__mobile=mobile)
    usertype = request.GET.get("usertype",0)
    usertype= int(usertype)
    if usertype == 1:
        item_list = item_list.filter(user__is_channel=False)
    elif usertype == 2:
        item_list = item_list.filter(user__is_channel=True)
        chalevel = request.GET.get("chalevel","")
        print usertype,chalevel
        if chalevel:
            item_list = item_list.filter(user__channel__level=chalevel)
    companyname = request.GET.get("companyname", None)
    if companyname:
        item_list = item_list.filter(finance__company__name__contains=companyname)

    projectname = request.GET.get("projectname", None)
    if projectname:
        item_list = item_list.filter(finance__title__contains=projectname)
    adminname = request.GET.get("adminname", None)
    if adminname:
        item_list = item_list.filter(audited_logs__user__username=adminname)
    task_type = ContentType.objects.get_for_model(Finance)
    item_list = item_list.filter(content_type = task_type.id)
    item_list = item_list.filter(event_type='1', audit_state=state).select_related('user').order_by('time')
    data = []
    for con in item_list:
        project = con.content_object
        project_name=project.title
        mobile_sub=con.invest_account
        invest_time=con.invest_time
        id=con.id
        remark= con.remark
        invest_amount= con.invest_amount
        term=con.invest_term
        user_mobile = con.user.mobile if not con.user.is_channel else con.user.channel.qq_number
        user_type = u"普通用户" if not con.user.is_channel else u"渠道："+ con.user.channel.level
        result = ''
        return_amount = ''
        reason = ''
        if con.audit_state=='0':
            result = u'是'
            if con.translist.exists():
                return_amount = str(con.translist.first().transAmount/100.0)
        elif con.audit_state=='2':
            result = u'否'
            if con.audited_logs.exists():
                reason = con.audited_logs.first().reason
        data.append([id, project_name, invest_time, user_mobile,user_type, mobile_sub, term,
                     invest_amount, remark, result, return_amount, reason])
    w = Workbook()     #创建一个工作簿
    ws = w.add_sheet(u'待审核记录')     #创建一个工作表
    title_row = [u'记录ID',u'项目名称',u'投资日期', u'挖福利账号', u'用户类型', u'注册手机号' ,u'投资期限' ,u'投资金额', u'备注',
                 u'审核通过',u'返现金额',u'拒绝原因']
    for i in range(len(title_row)):
        ws.write(0,i,title_row[i])
    row = len(data)
    style1 = easyxf(num_format_str='YY/MM/DD')
    for i in range(row):
        lis = data[i]
        col = len(lis)
        for j in range(col):
            if j==2:
                ws.write(i+1,j,lis[j],style1)
            else:
                ws.write(i+1,j,lis[j])
    sio = StringIO.StringIO()
    w.save(sio)
    sio.seek(0)
    response = HttpResponse(sio.getvalue(), content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=待审核记录.xls'
    response.write(sio.getvalue())
    return response