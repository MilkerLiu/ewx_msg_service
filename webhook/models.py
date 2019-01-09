# coding: utf-8

from django.db import models
import json


class WXGroup(models.Model):
    chatid = models.CharField(u'ChatId', max_length=100, null=False)
    name = models.CharField(u'名称', max_length=100)
    owner = models.CharField(u'群主', max_length=100)
    userlist = models.CharField(u'群成员', max_length=200)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'微信群'
        verbose_name_plural = verbose_name


class GitlabHook(models.Model):
    key = models.CharField(u'标识', max_length=100, null=False)
    name = models.CharField(u'名称', max_length=100)
    group = models.ForeignKey(WXGroup, verbose_name=u'收消息的群')
    ref_branch = models.CharField(u'关联的分支', max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'GitLabHook'
        verbose_name_plural = verbose_name


class WXChatMessage(models.Model):
    group = models.ForeignKey(WXGroup, verbose_name=u'收消息的群')
    MSG_TYPE = (
        ('text', '文本消息'),
        ('textcard', '卡片消息'),
        ('markdown', 'markdown消息')
    )
    msgtype = models.CharField(u'消息类型', choices=MSG_TYPE, default='text', max_length=20)
    text_content = models.TextField(u'文本-消息内容', null=True, blank=True)
    markdown_content = models.TextField(u'Markdown-消息内容', null=True, blank=True)
    textcard_content = models.TextField(u'卡片消息-消息内容', null=True, blank=True)

    def __str__(self):
        return self.msgtype

    class Meta:
        verbose_name = u'消息'
        verbose_name_plural = verbose_name

    def msg_dict(self):
        if not self.group:
            return None
        data = {
            "chatid": self.group.chatid,
            "msgtype": self.msgtype,
            "safe": 0
        }
        if self.msgtype == 'text':
            data["text"] = {
                "content": self.text_content
            }
        elif self.msgtype == 'textcard':
            data["textcard"] = json.loads(self.textcard_content)
        elif self.msgtype == 'markdown':
            data["markdown"] = {
                "content": self.markdown_content
            }
        return data
