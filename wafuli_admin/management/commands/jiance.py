# encoding: utf-8
import os

import datetime
from dragon.settings import MEDIA_ROOT
from dragon.settings import BASE_DIR
from django.core.management.base import BaseCommand
from QQinspector.models import Item, Detail_Statis, QQGroup


class Command(BaseCommand):
    def handle(self, *args, **options):
        pingtai=[]
        all_count = {}
        confpath = os.path.join(BASE_DIR, 'wafuli_admin', 'management', 'commands',"pingtai.txt")
        with open(confpath,'r') as file:
            for line in file:
                item = line.decode('utf-8').strip()
                pingtai.append(item)
        
        today =datetime.date.today().strftime("%Y-%m-%d")
        todaydir = os.path.join(MEDIA_ROOT, 'QQmsgs', today).replace('\\','/')
        print os.listdir(todaydir)
        if not os.path.exists(todaydir):
            return
        files = os.listdir(todaydir)
        for file in files:
            print file
            filename = os.path.join(todaydir, file)
            qqgroup = file.replace('.txt','')
            with open(filename,'r') as file1:
                list1 = file1.read().decode('gbk', 'ignore')
                for items in pingtai:
                    item_list = items.split(',')
                    item = item_list[0]
                    for item_i in item_list:
                        count = list1.count(item_i)
                        if count > 0:
                            if item in all_count:
                                all_count[item]['count'] += count
                                all_count[item]['detail'].update({qqgroup : count})
                            else:
                                all_count[item] = {'count':count, 'detail':{qqgroup : count}} 
        sorted_dict = sorted(all_count.iteritems(), key=lambda x:x[1]['count'], reverse=True) 
        for k,v in sorted_dict:
            item = Item.objects.create(name = k, time = datetime.datetime.now(), count = v['count'])
            detail = v['detail']
            for m,n in detail.items():
                try:
                    qq = QQGroup.objects.get(number=m)
                except:
                    continue
                Detail_Statis.objects.create(item=item, qq=qq, count=n)
        
#         conn = mysql.connector.connect(host='101.200.159.130', user='root', password='Xianjian7', database='test', use_unicode=True)
#         cursor = conn.cursor()
#         for k,v in sorted_dict:
#             cursor.execute('insert into QQinspector_Item ( name, time, count ) values ( %s, now(), %s)' , [k, v['count']])
#         #     conn.commit()
#             detail = v['detail']
#             item_id = cursor.lastrowid
#             print cursor.lastrowid
#             for m,n in detail.items():
#                 cursor.execute('insert into QQinspector_Detail_Statis ( item_id, qq, count ) values ( %s, %s, %s)' , [item_id, m, n])
#                 
#         conn.commit()
#         cursor.close()

