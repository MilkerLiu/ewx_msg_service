# coding: utf-8
import os, json

# 企业微信配置
corpid          = 'ww1a533286d8aca221'
corpsecret      = 'SSaM6w5xBFBNEvONs5LuXdw6sXfgKA6J1YpYa3bd3X8'

get_token_url       = "https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=%s&corpsecret=%s"
send_group_msg_url  = "https://qyapi.weixin.qq.com/cgi-bin/appchat/send?access_token=%s"
create_group_url    = 'https://qyapi.weixin.qq.com/cgi-bin/appchat/create?access_token=%s'
get_group           = 'https://qyapi.weixin.qq.com/cgi-bin/appchat/get?access_token=%s&chatid=%s'

def get_token():
    """
    获取企业微信消息服务的Token
    :return:
    """
    url = get_token_url % (corpid, corpsecret)
    res = os.popen('curl "%s"' % url)
    result = res.read()
    res.close()
    body = json.loads(result)
    return body['access_token']


def create_group(group):
   """
   创建群组
   :param token:
   :return:
   """
   url = create_group_url % get_token()
   msg = json.dumps(group)
   cmd = 'curl -H "Content-Type:application/json" -X POST --data \'%s\' "%s"' % (msg, url)
   os.system(cmd)


def get_group(chatid):
    """
    获取群组
    :param chatid:
    :return:
    """
    url = get_token_url % (get_token(), chatid)
    res = os.popen('curl "%s"' % url)
    result = res.read()
    res.close()
    body = json.loads(result)
    if body['code'] == 0:
        return body['chat_info']
    else:
        return None


def send_group_msg(data):
   url = send_group_msg_url % get_token()
   msg = json.dumps(data)
   cmd = 'curl -H "Content-Type:application/json" -X POST --data \'%s\' "%s"' % (msg, url)
   os.system(cmd)