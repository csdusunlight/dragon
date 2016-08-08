#coding:utf-8
'''
Created on 2016年8月1日

@author: lch
'''
from django.shortcuts import render
from django.http.response import Http404
from wafuli.models import Welfare, Advertisement, Press, Hongbao, Baoyou, CouponProject
from django.core.urlresolvers import reverse
from django.http import JsonResponse
from django.db.models import Q
import logging
from wafuli_admin.models import RecommendRank
from account.models import MyUser
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import re
logger = logging.getLogger('wafuli')

def welfare(request, id=None, page=None, type=None):
    full_path = str(request.get_full_path())
    path_split = re.split('list-page\d+',full_path)
    page_dic = {}
    page_dic['pre_path'] = path_split[0]
    page_dic['suf_path'] = path_split[1]
    if not id:
        if not page:
            page = 1
        wel_list = Welfare.objects.filter(is_del=False)
        state = request.GET.get('state', '1')
        if state:
            state = str(state)
            wel_list = wel_list.filter(state=state)
        if type:
            type = str(type)
            if type == 'hb':
                wel_list = wel_list.filter(type="hongbao")
            elif type == 'yhq':
                wel_list = wel_list.filter(type="youhuiquan")
            elif type == 'by':
                wel_list = wel_list.filter(type="baoyou")
        wel_list, page_num = listing(wel_list, 1, int(page))
        print wel_list
        page_list = []
        if page_num < 10:
            page_list = range(1,10)
        elif page
        ad_list = Advertisement.objects.filter(Q(location='0')|Q(location='2'),is_hidden=False)[0:8]
        strategy_list = Press.objects.filter(type='2')[0:10]
        context = {'wel_list':wel_list,'ad_list':ad_list,'strategy_list':strategy_list}
        ranks = RecommendRank.objects.all()[0:6]
        for i in range(len(ranks)):
            key = 'rank'+str(i+1)
            username = ranks[i].user.username
            if len(username) > 4:
                username = username[0:4] + '****'
            else:
                username = username + '****'
            acc_num = ranks[i].acc_num
            context.update({key:{'username':username,'acc_num':str(acc_num)+u'条'}})
        return render(request, 'zeroWelfare.html', context)
    elif id:
        id = int(id)
        try:
            wel = Welfare.objects.get(id=id)
        except Welfare.DoesNotExist:
            raise Http404(u"该页面不存在")
        template = 'detail-common.html'
        if wel.type == "youhuiquan":
            template = 'detail-youhuiquan.html'
        return render(request, template,{'news':wel,'type':'Welfare'})
    
def exp_welfare_common(request):
    if not request.is_ajax():
        logger.warning("Experience refused no-ajax request!!!")
        raise Http404
    result = {}
    if not request.user.is_authenticated():
        url = reverse('login') + '?next=' + request.META['HTTP_REFERER']
        result['url'] = url
        result['code'] = '0'
        return JsonResponse(result)
    wel_id = request.GET.get('id', None)
    if not wel_id:
        logger.error("wel_id is missing!!!")
        raise Http404
    wel = Welfare.objects.get(id=wel_id)
    if wel.type == "hongbao":
        wel = wel.hongbao
    elif wel.type == "baoyou":
        wel = wel.baoyou
    if wel.isonMobile:
        result['url'] = wel.exp_code.url
    else:
        result['url'] = wel.exp_url
    result['code'] = '1'
    return JsonResponse(result)

def listing(con_list, num, page):
    paginator = Paginator(con_list, num) # Show 2 contacts per page
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
    # If page is not an integer, deliver first page.
        contacts = paginator.page(1)
    except EmptyPage:
    # If page is out of range (e.g. 9999), deliver last page of results.
        contacts = paginator.page(paginator.num_pages)
    return contacts, paginator.num_pages