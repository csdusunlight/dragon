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
SETTLE_STATE=(
    ('advance', u"预付款"),
    ('later', u"后付款"),
    ('daily', u"日结"),
)   
class Project(models.Model):
    uuid = models.CharField(u"项目编号", max_length=20, primary_key=True)
    name = models.CharField(u"项目名称", max_length=50)
    time = models.DateField(u"立项日期", default=timezone.now)
    contact = models.CharField(u"商务对接人", max_length=10)
    coopway = models.CharField(u"合作方式", max_length=10)
    settleway = models.CharField(u"结算方式", max_length=10, choices=SETTLE_STATE)
    contract_company = models.CharField(u"签约公司", max_length=30)
    settle_detail = models.CharField(u"结算详情", max_length=30)
    state = models.CharField(u"项目状态", max_length=10, choices=PROJECT_STATE)
    paid_amount = models.DecimalField(u"付款总额", max_digits=10, decimal_places=2, default=0)
    consume_amount = models.DecimalField(u"消耗总额", max_digits=10, decimal_places=2, default=0)
    def consume_minus_paid(self):
        return self.consume_amount - self.paid_amount
    topay_amount = property(consume_minus_paid)
    return_amount = models.DecimalField(u"返现总额", max_digits=10, decimal_places=2, default=0)
    def paid_minus_return(self):
        return self.paid_amount-self.return_amount
    profit = property(paid_minus_return)
    def __unicode__(self):
        return self.uuid + ' ' + self.name
class ProjectInvestData(models.Model):
    project = models.ForeignKey(Project, verbose_name=u"项目id", related_name='project_data')
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
    income = models.DecimalField(u"收入", max_digits=10, decimal_places=2)
    expenditure = models.DecimalField(u"支出", max_digits=10, decimal_places=2)
    remark = models.CharField(u"摘要", max_length=100)
    def __unicode__(self):
        return self.project.name + str(self.date)