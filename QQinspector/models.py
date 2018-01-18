#coding:utf-8
from django.db import models
from django.db.models.fields import CharField, URLField, DateTimeField,\
    PositiveIntegerField
from django.db.models.fields.related import ForeignKey

# Create your models here.
class QQGroup(models.Model):
    number = CharField(u"QQ群号", max_length=15, primary_key=True)
    doc_url = URLField(u"项目清单地址", max_length=200, blank=True)
    def __unicode__(self):
        return self.number
    class Meta:
        verbose_name_plural = u"QQ群"
        verbose_name = u"QQ群"
    
class Item(models.Model):
    name = CharField(u"平台名称", max_length=15)
    time = DateTimeField(u"统计时间", auto_now_add=True)
    count = PositiveIntegerField(u"出现次数")
    class Meta:
        ordering = ['-time']
        verbose_name_plural = u"统计结果"
        verbose_name = u"统计结果"
    
class Detail_Statis(models.Model):
    item = ForeignKey(Item, verbose_name=u"对应条目")
    qq = ForeignKey(QQGroup, verbose_name=u"QQ群号")
    count = PositiveIntegerField(u"出现次数")
    def __unicode__(self):
        return self.item.name
    class Meta:
        ordering = ['-item__time']
        verbose_name_plural = u"统计明细"
        verbose_name = u"统计明细"