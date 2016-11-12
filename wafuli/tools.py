#coding:utf-8
from django.conf import settings
import time,os
import random
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import F
import logging
logger = logging.getLogger('wafuli')
def createUrl():
    tstr = time.strftime('%Y/%m/%d/')
    html_name = str(int(time.time()))+'.html'
    directory = os.path.join(settings.MEDIA_ROOT, 'html',  tstr).replace('\\','/')
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open(os.path.join(directory, html_name), 'w') as html_file:
        pass
    url = os.path.join(settings.MEDIA_URL,'html', tstr, html_name).replace('\\','/')
    return url
def writeHtml(html,url):
    s = len(settings.MEDIA_URL)
    if url==None or len(url)<=s:
        return -1
    url = url[s:]
    url = os.path.join(settings.MEDIA_ROOT,url).replace('\\','/')
    if not os.path.exists(url):
        return -1
    with open(url, 'w') as html_file:
        html = html.encode('utf-8')        
        html_file.write(html)
    return 0
 
def weighted_random(items): 
    total = sum(w for _,w in items) 
    n = random.uniform(0, total)#在饼图扔骰子 
    for x, w in items:#遍历找出骰子所在的区间 
        if n<w: 
            break
        n -= w 
    return x


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

def update_view_count(welfare):
    try:
        welfare.view_count = F('view_count') + 1
        welfare.save(update_fields=['view_count',])
        if hasattr(welfare, 'company'):
            company = welfare.company
            if company:
                company.view_count = F('view_count') + 1
                company.save(update_fields=['view_count',])
    except Exception, e:
        logger.error(e)