#coding:utf-8
'''
Created on 2016年8月29日

@author: lch
'''
import logging
from wafuli.models import Welfare, UserTask, Coupon, CouponProject
from django.core.management.base import BaseCommand
from account.models import MyUser, UserToken
from django.db.models import F, Sum, Count
import datetime
import time
from project_admin.models import ProjectInvestData, DayStatis

logger = logging.getLogger("wafuli")
class Command(BaseCommand):
    def handle(self, *args, **options):
        logger.info("******Day-task is beginning*********")
        begin_time = time.time()
        usertasks = UserTask.objects.all()
        for usertask in usertasks:
            task = usertask.task
            task.left_num = F("left_num")+1
            task.save(update_fields=['left_num'])
            usertask.delete()
            
        projects = CouponProject.objects.filter(endtime__lte=datetime.date.today()).order_by()
        for project in projects:
            if project.ctype == '2':
                project.coupons.all().delete()
            else:
                project.coupons.filter(is_used=False).delete()
                
        UserToken.objects.filter(expire__lt = time.time()*1000).delete()
        
        today = datetime.date.today()
        for i in range(7):
            day = today - datetime.timedelta(days=i)
            update_fields = {}
            update_fields['invest_count'] = ProjectInvestData.objects.filter(invest_time=day).count()
            statdic = ProjectInvestData.objects.filter(invest_time=day).aggregate(invest_sum=Sum('invest_amount'),
                   consume_sum=Sum('settle_amount'))
            update_fields['ret_count'] = ProjectInvestData.objects.filter(invest_time=day, state='0').count()
            statdic_pass = ProjectInvestData.objects.filter(invest_time=day, state='0').aggregate(
                   ret_invest_sum=Sum('invest_amount'), ret_sum=Sum('return_amount'))
            update_fields.update(statdic)
            update_fields.update(statdic_pass)
            obj, created = DayStatis.objects.update_or_create(date=day, defaults=update_fields)
        
        end_time = time.time()
        logger.info("******Day-task is finished, time:%s*********",end_time-begin_time)