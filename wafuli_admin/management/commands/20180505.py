
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
from public.pinyin import PinYin
logger = logging.getLogger("wafuli")
from wafuli.models import Company
class Command(BaseCommand):
    def handle(self, *args, **options):
        pinyin = PinYin()
        pinyin.load_word()
        a=Company.objects.all()
        for i in a:
            i.pinyin=pinyin.hanzi2pinyin_split(string=i.name, split="")[0]
            i.save(update_fields=['pinyin'])

            
            
