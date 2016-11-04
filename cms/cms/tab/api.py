# -*- coding: utf-8 -*-
# Author:songroger
# Aug.13.2016
from __future__ import unicode_literals
import json
import traceback
from pttools.pthttp import PtHttpResponse
from django.views.decorators.http import require_http_methods, require_safe
from django.contrib.auth.decorators import login_required
from tab.utils import get_tab_list, add_or_up_tab, delete_tab
from main.views.main_pub import get_actions_select


@require_safe
@login_required
def tab_list(request):
    """
    获取tab列表
    """
    data = {}
    page = int(request.GET.get('page', 1))
    limit = int(request.GET.get('limit', 10))
    channel_id = int(request.GET.get('channel', 0))
    if channel_id:
        data = get_tab_list(page, limit, channel_id)
    return PtHttpResponse(data)


@require_http_methods(['POST', 'PUT', 'DELETE'])
@login_required
def tab(request):
    data = {}
    channel_id = int(request.GET.get('channel', 0))
    tab_id = int(request.GET.get('tid', 0))
    if request.method == "POST":
        if channel_id:
            data = add_or_up_tab(request, channel_id, tab_id)
        else:
            data = {"msg": u"缺少参数channel", "code": 1}
    elif request.method == "PUT":
        if channel_id and tab_id:
            data = add_or_up_tab(request, channel_id, tab_id)
        else:
            data = {"msg": u"缺少参数channel或tid", "code": 1}
    elif request.method == "DELETE":
        if channel_id and tab_id:
            data = delete_tab(channel_id, tab_id)
        else:
            data = {"msg": u"缺少参数channel或tid", "code": 1}
    return PtHttpResponse(data)


@require_safe
@login_required
def actions_list(request):
    actions = get_actions_select()
    return PtHttpResponse(json.loads(actions), dump=True)
    # actions = _get_actions()
    # return PtHttpResponse(actions)


# def _get_actions():
#     from main.models import CmsActions
#     actions = CmsActions.objects.all()
#     data = [dict(id=a.id, name=a.memo) for a in actions]
#     return data
