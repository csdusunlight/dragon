#coding:utf-8
'''
Created on 20160614

@author: lch
'''
from django.shortcuts import render

from wafuli.models import Advertisement, UserWelfare, UserEvent
import logging
from django.core.urlresolvers import reverse
from django.http.response import JsonResponse, Http404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from wafuli_admin.models import RecommendRank
import datetime
logger = logging.getLogger('wafuli')
def recommend(request, id=None):
    if request.method == "POST":
        if not request.is_ajax():
            logger.warning("Experience refused no-ajax request!!!")
        result = {}
        if not request.user.is_authenticated():
            result['code'] = -1
            result['url'] = reverse('login') + "?next=" + reverse('activity_recommend')
            return JsonResponse(result)
        title = request.POST.get('title', '')
        url = request.POST.get('url', '')
        reason = request.POST.get('reason', '')
        if not (title and url) or len(title)>200 or len(url)>200 or len(reason)>200:
            result['code'] = 3
            result['res_msg'] = u'输入参数长度有误！'
        else:
            try:
                wel = UserWelfare.objects.create(user=request.user, title=title,url=url,reason=reason)
                UserEvent.objects.create(user=request.user, event_type='6', content_object=wel, audit_state='1')
            except Exception as e:
                result['code'] = 2
                result['res_msg'] = u'重复提交或数据有误！'
                logger.error(e)
            else:
                result['code'] = 0
        return JsonResponse(result)
    else:
        adv = Advertisement.objects.filter(location='7',is_hidden=False).first()
        user = request.user
        context = {'adv':adv,}
        if user.is_authenticated():
            if hasattr(user, 'rank_of'):
                context['rank'] = user.rank_of.rank
                context['acc_num'] = user.rank_of.acc_num
            else:
                context['rank'] = '--'
                context['acc_num'] = 0
            today = datetime.date.today()
            first_day = datetime.datetime(today.year, today.month, 1)
            context['total_num'] = UserEvent.objects.filter(user=user, event_type='6', \
                        time__gte=first_day,).count()
        return render(request, 'activity_recommend.html',context)
    
def get_activity_recommend_page(request):
    res={'code':0,}
    user = request.user
    if not ( user.is_authenticated() and user.is_staff):
        res['code'] = -1
        res['url'] = reverse('login') + "?next=" + reverse('activity_recommend')
        return JsonResponse(res)
    page = request.GET.get("page", None)
    size = request.GET.get("size", 5)
    try:
        size = int(size)
    except ValueError:
        size = 5
    if not page or size <= 0:
        raise Http404
    item_list = []
    item_list = UserEvent.objects.filter(user=user,event_type='6')
    
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
        wel = con.content_object
        i = {"title":wel.title,
             "url":wel.url,
             "reason":wel.reason,
             "date":wel.date.strftime("%Y-%m-%d %H:%M"),
             "result":con.get_audit_state_display(),
             }
        data.append(i)
    if data:
        res['code'] = 1
    res["pageCount"] = paginator.num_pages
    res["recordCount"] = item_list.count()
    res["data"] = data
    return JsonResponse(res)

def get_recommend_rank_page(request):
    res={'code':0,}
    user = request.user
    if not ( user.is_authenticated() and user.is_staff):
        res['code'] = -1
        res['url'] = reverse('login') + "?next=" + reverse('activity_recommend')
        return JsonResponse(res)
    page = request.GET.get("page", None)
    size = request.GET.get("size", 3)
    try:
        size = int(size)
    except ValueError:
        size = 3
    if not page or size <= 0:
        raise Http404
    item_list = []
    item_list = RecommendRank.objects.all()[0:12]
    
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
        username = con.user.username
        if len(username) > 4:
            username = username[0:4] + '****'
        else:
            username = username + '****'
        i = {"username":username,
             "num":con.acc_num,
             "rank":con.rank,
             "award":con.award,
             }
        data.append(i)
    if data:
        res['code'] = 1
    res["pageCount"] = paginator.num_pages
    res["recordCount"] = item_list.count()
    res["data"] = data
    return JsonResponse(res)