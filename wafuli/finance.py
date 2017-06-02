#coding:utf-8
from django.shortcuts import render
from django.http.response import Http404
from wafuli.models import Finance, Advertisement
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.http import JsonResponse
from django.db.models import F,Q
import logging
from wafuli.tools import update_view_count
from django.contrib.auth.decorators import login_required
logger = logging.getLogger('wafuli')
from .tools import listing
import re


def finance(request, id=None):
    if id is None:
        ad_list = Advertisement.objects.filter(Q(location='0')|Q(location='4'),is_hidden=False)[0:8]
        context = {'ad_list':ad_list}
        return render(request, 'finance.html',context)
    else:
        id = int(id)
        news = None
        try:
            news = Finance.objects.get(id=id)
        except Finance.DoesNotExist:
            raise Http404(u"该页面不存在")
        update_view_count(news)
        scheme = news.scheme
        table = []
        str_rows = scheme.split('|')
        for str_row in str_rows:
            row = str_row.split('#')
            table.append(row);
        other_wel_list = Finance.objects.filter(state='1', level__in=['normal','all']).order_by('-view_count')[0:10]
        context = {
                   'news':news,
                   'type':'Finance',
                   'other_wel_list':other_wel_list,
                   'table':table,
        }
        return render(request, 'detail-finance.html', context)

def get_finance_page(request):
    res={'code':0,}
    page = request.GET.get("page", None)
    size = request.GET.get("size", 8)
    company_name = request.GET.get("company_name", 0)
    company_background = request.GET.get("company_background", 0)
    invest_account = request.GET.get("invest_account", 0)
    project_type = request.GET.get("project_type", 0)
    project_status = request.GET.get("project_status", 0)


    try:
        size = int(size)
    except ValueError:
        size = 9
    if not page or size <= 0:
        raise Http404
    item_list = Finance.objects.filter(level__in=['normal','all'])

    company_name = str(company_name)
    company_item = company_name.split('$')
    company_background = str(company_background)
    invest_account = str(invest_account)
    project_type = str(project_type)
    project_status = str(project_status)

    if company_name != '0':  #全部
        item_list = item_list.filter(company__in=company_item)
    # if company_background != '0':  #全部
    #     item_list = item_list.filter(background=company_background)
    if company_background == '1':
        item_list = item_list.filter(background__contains=u'民营系')
    if company_background == '2':
        item_list = item_list.filter(background__contains=u'国资系')
    if company_background == '3':
        item_list = item_list.filter(background__contains=u'上市系')
    if invest_account != '0':
        item_list = item_list.filter(marks__name=invest_account)
    if project_type == '0':
        item_list = item_list.filter(f_type__in=["1","2"])
    if project_type != '0':
        item_list = item_list.filter(f_type=project_type)
    if project_status == '0':
        item_list = item_list.filter(state__in=["1","2"])
    if project_status != '0':
        item_list = item_list.filter(state=project_status)

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
        marks = con.marks.all();
        str_marks = ''
        for mark in marks:
            str_marks += '<span>' + mark.name + '</span>'
        i = {"title":con.title,
             "interest":con.interest,
             "amount":con.amount_to_invest,
             "time":con.investTime,
             "revenue":con.revenue,
             "benefit":con.benefit,
             "url":con.url,
             "img_url":con.pic.url,
             "is_new":'new' if con.is_new() else '',
             "marks":str_marks
        }
        data.append(i)
    if data:
        res['code'] = 1
    res["pageCount"] = paginator.num_pages
    res["recordCount"] = item_list.count()
    res["data"] = data
    return JsonResponse(res)
