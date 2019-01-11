# coding: utf-8
from django.db import models

# 站点名字
CONFIG_SITE_NAME = 'cfg_site_name'
# 企业微信
CONFIG_EWX_CORP_ID = 'cfg_ewx_corp_id'
CONFIG_EWX_CORP_SECRET = 'cfg_ewx_corp_secret'


class ConfigModel(models.Model):
    name = models.CharField(u'名称', max_length=100)
    key = models.CharField(u'键', max_length=100)
    value = models.CharField(u'值', max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'配置'
        verbose_name_plural = verbose_name