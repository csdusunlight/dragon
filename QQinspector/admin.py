from django.contrib import admin
from QQinspector.models import *

class ItemAdmin(admin.ModelAdmin):
#     raw_id_fields = ['name','count']
    search_fields = ()
    list_display = ('name', 'count','time')
class DetailAdmin(admin.ModelAdmin):
    raw_id_fields = ['item','qq']
    search_fields = ()
    list_display = ('__unicode__','qq', 'count')
class QQGroupAdmin(admin.ModelAdmin):
#     raw_id_fields = ['name','count']
    search_fields = ()
    list_display = ('number', 'name','doc_url')
# Register your models here.
admin.site.register(Item, ItemAdmin)
admin.site.register(QQGroup, QQGroupAdmin)
admin.site.register(Detail_Statis, DetailAdmin)