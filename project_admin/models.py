#coding:utf-8
from django.db import models
from django.utils import timezone
from wafuli.data import AUDIT_STATE
import time,datetime
# Create your models here.
PROJECT_STATE=(
    ('prepare', u"未开始"),
    ('start', u"正在进行"),
    ('pause', u"暂停"),
    ('finish', u"已结束"),
)
SETTLE_STATE=(
    ('advance', u"预付款"),
    ('later', u"后付款"),
    ('daily', u"日结"),
)
class Platform(models.Model):
    name = models.CharField(u"平台名称", max_length=20)
    url = models.CharField(u"网站域名", max_length=100)
    def __unicode__(self):
        return self.name
class Contact(models.Model):
    platform = models.ForeignKey(Platform, verbose_name=u"合作平台", related_name='contacts')
    name = models.CharField(u"姓名", max_length=50)
    mobile = models.CharField(u"手机号", max_length=50)
    qq = models.CharField(u"QQ号", max_length=50)
    weixin = models.CharField(u"微信号", max_length=50)
    invoicecompany = models.CharField(u"开票公司", max_length=50)
    invoiceid = models.CharField(u"开票税号", max_length=50)
    address = models.CharField(u"联系地址", max_length=50)
    remark = models.CharField(u"备注", max_length=50)
    def __unicode__(self):
        return self.name
def get_today():
    return datetime.date.today()
class Project(models.Model):
    name = models.CharField(u"项目名称", max_length=50)
    platform = models.ForeignKey(Platform, verbose_name=u"甲方名称", related_name='projects')
    time = models.DateField(u"立项日期", default=get_today)
    contact = models.CharField(u"商务对接人", max_length=10)
    coopway = models.CharField(u"合作方式", max_length=10)
    settleway = models.CharField(u"结算方式", max_length=10, choices=SETTLE_STATE)
    contract_company = models.CharField(u"签约公司", max_length=30)
    settle_detail = models.CharField(u"结算详情", max_length=30)
    state = models.CharField(u"项目状态", max_length=10, choices=PROJECT_STATE)
    settle = models.DecimalField(u"结算费用", max_digits=10, decimal_places=2, default=0)
    consume = models.DecimalField(u"消耗总额", max_digits=10, decimal_places=2, default=0)
    cost = models.DecimalField(u"项目成本", max_digits=10, decimal_places=2, default=0)
    def consume_minus_paid(self):
        return self.consume - self.settle
    topay_amount = property(consume_minus_paid)
#     return_amount = models.DecimalField(u"返现总额", max_digits=10, decimal_places=2, default=0)
    def paid_minus_cost(self):
        return self.settle-self.cost
    profit = property(paid_minus_cost)
    def __unicode__(self):
        return str(self.id) + ' ' + self.name
    def save(self, force_insert=False, force_update=False, using=None, 
        update_fields=None):
        if self.state != 'finish':
            self.cost = self.settle
        return models.Model.save(self, force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)

class ProjectInvestData(models.Model):
    project = models.ForeignKey(Project, verbose_name=u"项目", related_name='project_data')
    is_futou = models.BooleanField(u"是否复投", default=False)
    invest_mobile = models.CharField(u"投资手机号", max_length=13)
    invest_time = models.DateField(u"投资时间")
    invest_amount = models.DecimalField(u"投资金额", max_digits=10, decimal_places=2)
    invest_term = models.CharField(u"投资标期", max_length=13)
    settle_amount = models.DecimalField(u"结算金额", max_digits=10, decimal_places=2)
    return_amount = models.DecimalField(u"返现金额", max_digits=10, decimal_places=2)
    state = models.CharField(u"审核状态", max_length=10, choices=AUDIT_STATE)
    remark = models.CharField(u"备注", max_length=100)
    def __unicode__(self):
        return self.project.name + self.invest_mobile

class CompanyBalance(models.Model):
    company = models.CharField(u"公司", max_length=20, unique=True)
    date = models.DateField(u"日期")
    income = models.DecimalField(u"收支", max_digits=10, decimal_places=2)
    balance = models.DecimalField(u"余额", max_digits=10, decimal_places=2)
    remark = models.CharField(u"摘要", max_length=100)
    def __unicode__(self):
        return self.project.name + str(self.date)


