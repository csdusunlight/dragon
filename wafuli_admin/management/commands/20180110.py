
#coding:utf-8
'''
Created on 2017年2月19日

@author: lch
'''

from django.core.management.base import BaseCommand
import logging
from wafuli.models import UserEvent, Finance
from django.contrib.contenttypes.models import ContentType
from wafuli_admin.models import Invest_Record
from django.db.models import F
from account.models import MyUser
logger = logging.getLogger("wafuli")
class Command(BaseCommand):
    def handle(self, *args, **options):
        users = MyUser.objects.all()
        for user in users:
            with_total = user.with_total
            amount, level = level_compute(with_total, 0)
            user.with_level = amount
            user.level = level
            user.save()
            
            
            
def level_compute(amount, level):
    if level == 0:
        if amount >= 100000:
            amount -= 100000
            level += 1
            amount, level = level_compute(amount, level)
    elif level == 1:
        if amount >= 500000:
            amount -= 500000
            level += 1
            amount, level = level_compute(amount, level)
    elif level >=2:
        if amount >= 1000000:
            m = int(amount/1000000)
            amount -= 1000000 * m
            level += m
    return amount, level
