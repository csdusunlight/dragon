'''
Created on 20160608

@author: lch
'''
import logging
from wafuli_admin.models import UserStatis
from django.core.management.base import BaseCommand
logger = logging.getLogger("wafuli")
class Command(BaseCommand):
    def handle(self, *args, **options):
        logger.info("******MonthTask is beginning*********")
        UserStatis.objects.update(month_statis=0)
        logger.info("******MonthTask is finished*********")