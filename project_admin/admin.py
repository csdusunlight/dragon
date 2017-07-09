from django.contrib import admin

# Register your models here.
from .models import *
from django.contrib.admin.options import ModelAdmin
class ContactInline(admin.StackedInline):
    model = Contact


class PlatformAdmin(admin.ModelAdmin):
    inlines = [ContactInline, ]

admin.site.register(Project)
admin.site.register(Contact)
admin.site.register(Platform,PlatformAdmin)