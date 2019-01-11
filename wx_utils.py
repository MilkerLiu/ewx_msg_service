# coding: utf-8
import os, json

from config.models import *


# 企业微信配置
def corpid():
    cfg = ConfigModel.objects.filter(key=CONFIG_EWX_CORP_ID).first()
    if cfg:
        return cfg.value
    else:
        return ""


def corpsecret():
    cfg = ConfigModel.objects.filter(key=CONFIG_EWX_CORP_SECRET).first()
    if cfg:
        return cfg.value
    else:
        return ""


get_token_url = "https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=%s&corpsecret=%s"
send_group_msg_url = "https://qyapi.weixin.qq.com/cgi-bin/appchat/send?access_token=%s"
create_group_url = 'https://qyapi.weixin.qq.com/cgi-bin/appchat/create?access_token=%s'
get_group_url = 'https://qyapi.weixin.qq.com/cgi-bin/appchat/get?access_token=%s&chatid=%s'


def request(url, body=None):
    if body:
        body_data = json.dumps(body)
        cmd = 'curl -H "Content-Type:application/json" -X POST --data \'%s\' "%s"' % (body_data, url)
    else:
        cmd = 'curl "%s"' % url
    res = os.popen(cmd)
    result = res.read()
    res.close()
    return json.loads(result)


def get_token():
    """
    获取企业微信消息服务的Token
    :return:
    """
    url = get_token_url % (corpid(), corpsecret())
    body = request(url)
    return body['access_token']


def create_group(group):
   """
   创建群组
   :param token:
   :return:
   """
   url = create_group_url % get_token()
   res = request(url, group)
   return res


def get_group(chatid):
    """
    获取群组
    :param chatid:
    :return:
    """
    url = get_group_url % (get_token(), chatid)
    res = request(url)
    return res


def send_group_msg(data):
    """
    发送群组消息
    :param data:
    :return:
    """
    url = send_group_msg_url % get_token()
    res = request(url, data)
    return res