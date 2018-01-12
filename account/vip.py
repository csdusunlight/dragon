#coding:utf-8
'''
Created on 2017年4月23日

@author: lch
'''
from account.transaction import charge_money
from wafuli.models import Message
from wafuli_admin.models import UserStatis
from django.db.models import F
from django.db import transaction
VIP_BONUS = {
    0:{'finance':0, 'task':0, 'money':2000,},
    1:{'finance':0.01, 'task':0.10, 'money':5000,},
    2:{'finance':0.02, 'task':0.15, 'money':10000,},
    3:{'finance':0.03, 'task':0.16, 'money':20000,},
    4:{'finance':0.04, 'task':0.18, 'money':80000,},
    5:{'finance':0.05, 'task':0.20, 'money':120000,},
}
VIP_AMOUNT = {0:0, 1:100000, 2:100000, 3:1000000, 4:5000000, 5:10000000,}
def get_vip_bonus(user, amount, type):
    if user.is_channel:
        return
    else:
        level = user.level
        cash = amount*VIP_BONUS[level][type]
        translist = charge_money(user, '0', cash, u'vip奖励')
def vip_judge(user, with_amount):
    obj, created = UserStatis.objects.get_or_create(user=user)
    obj.week_statis = F('week_statis') + with_amount
    obj.month_statis = F('month_statis') + with_amount
    obj.save(update_fields=['week_statis', 'month_statis'])
    if user.is_channel:
        return
    level = user.level
    total = user.with_total
    ntotal = user.with_total + with_amount
    user.with_total = ntotal
    keys = sorted(VIP_AMOUNT.keys())
    for key in keys:
        value = VIP_AMOUNT[key]
        if ntotal >= value and total < value:
            if key > level:
                user.level = key
                charge_money(user, '0', VIP_BONUS[key]['money'], u'VIP升级奖励')
                msg_content = u'恭喜您的会员等级提升为VIP' + str(key) + u'！'
                Message.objects.create(user=user, content=msg_content, title=u"会员升级")
    user.save(update_fields=['level', 'with_total'])

def vip_process(user, with_amount):
    obj, created = UserStatis.objects.get_or_create(user=user)
    obj.week_statis = F('week_statis') + with_amount
    obj.month_statis = F('month_statis') + with_amount
    obj.save(update_fields=['week_statis', 'month_statis'])
    level = user.level
    total = user.with_total + with_amount
    allamount = user.with_level + with_amount
    amount, newlevel = level_compute(allamount, level)
    award = 0
    for i in range(level, newlevel):
        level = i + 1
        if level == 1:
            award += 2000
        elif level == 2:
            award += 5000
        elif level >= 3 and level < 13:
            award += 10000 + 1000*(level-3)
        elif level >= 13:
            award += 20000
    charge_money(user, '0', award, u'账户等级提升奖励')
    if award > 0:
        msg_content = u'恭喜您的会员等级提升为Lv' + str(newlevel) + u'！'
        Message.objects.create(user=user, content=msg_content, title=u"会员升级")
    user.level = newlevel
    user.with_total = F('with_total') + with_amount
    user.with_level = amount
    user.save(update_fields=['level', 'with_total', 'with_level'])
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

if __name__ == '__main__':
    print level_compute(5600000, 0)