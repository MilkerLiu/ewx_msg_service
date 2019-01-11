# coding:utf-8

from django.contrib import admin
import ewx_msg_service.settings
from .models import *


@admin.register(ConfigModel)
class ConfigModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'key', 'value']

    def save_model(self, request, obj, form, change):
        super(ConfigModelAdmin, self).save_model(request, obj, form, change)
        if obj.key == CONFIG_SITE_NAME:
            admin.site.site_header = obj.value
            admin.site.site_title =  obj.value