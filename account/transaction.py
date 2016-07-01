'''
Created on 20160318

@author: lch
'''
#type_add = '0'
#type_min = '1'
from wafuli.models import TransList, ScoreTranlist
from account.models import MyUser
import logging
from decimal import Decimal
logger = logging.getLogger('wafuli')
def charge_money(user, type, amount, reason):
    if not (isinstance(user, MyUser) and reason) or type !='0' and type != '1':
        return -1
    try:
        amount = Decimal(amount)
    except:
        return None
    trans = TransList(user=user, transType=type)
    trans.initAmount = user.balance
    trans.transAmount = amount
    trans.reason = reason
    if type == '0':
        user.balance += amount
        user.accu_income += amount
    elif user.balance < amount - Decimal(0.001):
        logger.info('I:The account balance is not enough!')
        return None
    else:
        user.balance -= amount
    try:
        trans.save()
    except:
        logger.critical('Saving trans object is failed!!!')
        return None
    try:
        user.save(update_fields=['accu_income','balance'])
        return trans
    except:
        logger.critical('Saving User Info is failed!!!')
        trans.delete()
        return None

def correct_money(user, type, amount, reason):
    pass

def charge_score(user, type, amount, reason):
    if not (isinstance(user, MyUser) and reason) or type !='0' and type != '1':
        return None
    try:
        amount = int(amount)
    except:
        return None
    trans = ScoreTranlist(user=user, transType=type)
    trans.initAmount = user.scores
    trans.transAmount = amount
    trans.reason = reason
    if type == '0':
        user.scores += amount
        user.accu_scores += amount
    elif user.scores < amount:
        logger.info('I:The account scores is not enough!')
        return None
    else:
        user.scores -= amount
    try:
        trans.save()
    except:
        return None
    try:
        user.save(update_fields=['scores','accu_scores'])
        return trans
    except:
        trans.delete()
        return None

def correct_score(user, type, amount):
    pass