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
    
# Register your models here.
admin.site.register(Item, ItemAdmin)
admin.site.register(QQGroup)
admin.site.register(Detail_Statis, DetailAdmin)