#coding: utf-8

from django import forms
from django.contrib import admin
from webhook.models import *
from wx_utils import *
import ewx_msg_service.settings


class WXGroupForm(forms.ModelForm):
    chatid = forms.CharField(help_text='群组的标识ID, 请使用英文字母', label='群组标识')
    name = forms.CharField(help_text='群组的名称, 创建的微信群的名称', label='群组名称')
    owner = forms.CharField(help_text='群主的名字, 例如: LiuWenHua', label='群主')
    userlist = forms.CharField(help_text='初始群成员, 必须大于两人, 用 , 分割, 例如: LiuWenHua,WangLei', label='群成员')

    class Meta:
        model = WXGroup
        fields = "__all__"


@admin.register(WXGroup)
class WXGroupAdmin(admin.ModelAdmin):

    form = WXGroupForm

    list_display = ['chatid', 'name', 'owner']

    def save_model(self, request, obj, form, change):
        is_create = obj.id is None
        super(WXGroupAdmin, self).save_model(request, obj, form, change)
        if is_create:
            res = get_group(obj.chatid)
            if res.get('errcode', 0) == 0:
                return
            group = {
                'chatid': obj.chatid,
                'name': obj.name,
                'owner': obj.owner,
                'userlist': obj.userlist.split(',')
            }
            create_group(group)
            send_group_msg({
                "chatid": obj.chatid,
                "msgtype": 'text',
                "safe": 0,
                "text": {
                    "content": "群组已创建"
                }
            })


class GitlabHookForm(forms.ModelForm):
    key = forms.CharField(label='标识', help_text='Hook的标识, 例如: ios_release, 则在 gitlab内填入: http://{{domain}}/hook?key=ios_release ')
    name = forms.CharField(label=u'名称', help_text='可识别的名称')
    ref_branch = forms.CharField(label=u'关联的分支', help_text='关联分支, 例如: master, release/*, feature/*')
    msg_title = forms.CharField(label=u'消息标题', help_text=u'消息发送时展示的标题')

    class Meta:
        model = WXGroup
        fields = "__all__"


@admin.register(GitlabHook)
class GitlabHookAdmin(admin.ModelAdmin):
    form = GitlabHookForm

    list_display = ['key', 'name', 'group', 'ref_branch']


@admin.register(WXChatMessage)
class WXChatMessageAdmin(admin.ModelAdmin):

    def save_model(self, request, obj, form, change):
        is_create = obj.id is None
        super(WXChatMessageAdmin, self).save_model(request, obj, form, change)
        msg = obj.msg_dict()
        if is_create and msg:
            send_group_msg(msg)



