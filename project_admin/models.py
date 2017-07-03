#coding:utf-8
from django.db import models
from django.utils import timezone
from wafuli.data import AUDIT_STATE

# Create your models here.
PROJECT_STATE=(
    ('prepare', u"未开始"),
    ('start', u"正在进行"),
    ('pause', u"暂停"),
    ('finish', u"已结束"),
)   
class Project(models.Model):
    uuid = models.CharField(u"项目编号", max_length=20, primary_key=True)
    name = models.CharField(u"项目名称", max_length=50)
    time = models.DateField(u"立项日期", default=timezone.now)
    contact = models.CharField(u"商务对接人", max_length=10)
    coopway = models.CharField(u"合作方式", max_length=10)
    settleway = models.CharField(u"结算方式", max_length=10)
    contract_company = models.CharField(u"签约公司", max_length=30)
    settle_detail = models.CharField(u"结算详情", max_length=30)
    state = models.CharField(u"项目状态", max_length=10, choices=PROJECT_STATE)
    paid_amount = models.FloatField(u"付款总额")
    consume_amount = models.FloatField(u"消耗总额")
    def consume_minus_paid(self):
        return self.consume_amount - self.paid_amount
    topay_amount = property(consume_minus_paid)
    return_amount = models.FloatField(u"返现总额",default=0)
    def paid_minus_return(self):
        return self.paid_amount-self.return_amount
    profit = property(paid_minus_return)
    def __unicode__(self):
        return self.uuid + ' ' + self.name
class Project_InvestData(models.Model):
    project = models.ForeignKey(Project, verbose_name=u"项目id", related_name='project_data')
    invest_mobile = models.CharField(u"投资手机号", max_length=13)
    invest_time = models.DateTimeField(u"投资时间")
    invest_amount = models.IntegerField(u"投资金额")
    invest_term = models.CharField(u"投资标期", max_length=13)
    settle_amount = models.FloatField(u"结算金额")
    state = models.CharField(u"审核状态", max_length=10, choices=AUDIT_STATE)
    remark = models.CharField(u"备注", max_length=100)
    def __unicode__(self):
        return self.project.name + self.invest_mobile

class Project_Balance(models.Model):
    project = models.ForeignKey(Project, verbose_name=u"项目id", related_name='project_balance')
    date = models.DateField(u"日期")
    income = models.FloatField(u"收入")
    expenditure = models.FloatField(u"支出")
    remark = models.CharField(u"摘要", max_length=100)
    def __unicode__(self):
        return self.project.name + str(self.date)