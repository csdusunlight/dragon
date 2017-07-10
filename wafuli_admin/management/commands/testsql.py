
#coding:utf-8
'''
Created on 2017年4月12日

@author: lch
'''
import logging
from wafuli.models import *
import time as ttime
from django.core.management.base import BaseCommand
from django.db.models import Sum,F
from account.models import MyUser, Channel
from django.conf import settings
from decimal import Decimal
from django.core.urlresolvers import reverse
from django.db.models import F
from wafuli_admin.models import RecommendRank, DayStatis
from project_admin.models import ProjectStatis
logger = logging.getLogger("wafuli")
class Command(BaseCommand):
    def handle(self, *args, **options):
        from django.db import connection, transaction
        cursor = connection.cursor()
        cursor.execute("select a.project_id, a.source, sum(a.settle_amount) as sumofsettle, \
                            sum(a.return_amount) as sumofret from project_admin_projectinvestdata a \
                            group by a.project_id, a.source")
        # 数据修改操作——提交要求
#         cursor.execute("select b.is_channel,  a.audit_state,  \
#             sum(invest_amount) as sum, count(*) as count from wafuli_userevent a join account_myuser b\
#              on a.user_id=b.id group by a.audit_state, b.is_channel")
#         transaction.commit_unless_managed()
    
        # 数据检索操作,不需要提交
#         cursor.execute("SELECT foo FROM bar WHERE baz = %s", [self.baz])
        row = cursor.fetchall()
        print row
        project_dic = {}
        for item in row:
            id = item[0]
            source = item[1]
            consume = item[2]
            ret = item[3]
            attr = {}
            if project_dic.has_key(id):
                attr = project_dic[id]
            else:
                project_dic[id] = attr
            if source == 'site':
                attr['site_consume'] = consume
                attr['site_return'] = ret
            elif source == 'channel':
                attr['channel_consume'] = consume
                attr['channel_return'] = ret
        print project_dic        
        for id, kwarg in project_dic.items():
            ProjectStatis.objects.update_or_create(project_id=id, defaults=kwarg)
#         return row
