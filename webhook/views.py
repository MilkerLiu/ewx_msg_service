# coding: utf-8

from django.http import JsonResponse
from webhook.models import GitlabHook
from wx_utils import *
#
import sys
sys.setdefaultencoding('utf-8')


def index(request):
    return JsonResponse({"code": 0})


def hook(request):
    key = request.GET.get('key')
    hook = GitlabHook.objects.filter(key=key).first()
    if not hook:
        return JsonResponse({"code": 101, "msg": "未找到hook对象"})
    if not hook.group:
        return JsonResponse({"code": 102, "msg": "hook对象无群组记录,无法发送消息"})
    data = json.loads(request.body)

    object_kind = request.body.get('object_kind', None)
    if object_kind == 'push':
        return hook_by_push_event(hook, data)
    elif object_kind == 'merge_request':
        return hook_by_merge_request(hook, data)


def hook_by_push_event(hook, data):
    ref = data['ref']
    cfg_branch = hook.ref_branch.replace('*', '')
    if cfg_branch not in ref:
        return JsonResponse({"code": 103, "msg": "分支不匹配"})
    msgs = data['commits']
    content = '**%s:**\n' % hook.msg_title
    content += '> 代码提交: %s' % ref
    for msg in msgs:
        text = msg["message"]
        if not text.startswith('Merge branch'):
            url = msg["url"]
            author = msg['author']['name']
            line = "- [%s:%s](%s)\n" % (text, author, url)
            content += line

    send_group_msg({
        "chatid": hook.group.chatid,
        "msgtype": 'markdown',
        "safe": 0,
        "markdown": {
            "content": content
        }
    })
    return JsonResponse({"code": 0, "msg": "success"})


def hook_by_merge_request(hook, data):
    action = data['action']
    if action != 'merged':
        return JsonResponse({"code": 104, "msg": "非合并"})

    object_attributes = data['object_attributes']
    target_branch = object_attributes['target_branch']
    source_branch = object_attributes['source_branch']

    cfg_branch = hook.ref_branch.replace('*', '')
    if cfg_branch not in target_branch:
        return JsonResponse({"code": 103, "msg": "分支不匹配"})

    content = '**%s:**\n' % hook.msg_title
    content += '> 代码合并: %s -> %s' % (source_branch, target_branch)
    content += '> 操作人: %s' % data['user']['name']

    commit = data['last_commit']
    line = "- [%s:%s](%s)\n" % (commit['author']['name'], commit['message'], commit['url'])
    content += line

    send_group_msg({
        "chatid": hook.group.chatid,
        "msgtype": 'markdown',
        "safe": 0,
        "markdown": {
            "content": content
        }
    })
    return JsonResponse({"code": 0, "msg": "success"})


def send_msg(request):
    """
    发送消息
    :param request:
    :return:
    """
    res = send_group_msg(request.body)
    return JsonResponse(res)