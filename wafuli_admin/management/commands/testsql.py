
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
logger = logging.getLogger("wafuli")
class Command(BaseCommand):
    def handle(self, *args, **options):
        from django.db import connection, transaction
        cursor = connection.cursor()
    
        # 数据修改操作——提交要求
        cursor.execute("select b.is_channel,  a.audit_state,  \
            sum(invest_amount) as sum, count(*) as count from wafuli_userevent a join account_myuser b\
             on a.user_id=b.id group by a.audit_state, b.is_channel")
#         transaction.commit_unless_managed()
    
        # 数据检索操作,不需要提交
#         cursor.execute("SELECT foo FROM bar WHERE baz = %s", [self.baz])
        row = cursor.fetchall()
        print row
#         return row
