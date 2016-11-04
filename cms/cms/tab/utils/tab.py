# -*- coding: utf-8 -*-
# Author:songroger
# Aug.13.2016
from __future__ import unicode_literals
import json
import traceback
import logging
from ..models import Tabs, TabChannel
from django.core.paginator import Paginator
from ..settings import TAB_PARAMETERS
from pttools.pthttp import check_parameter
from pttools.ptformat import ptlog


log = logging.getLogger("main.app")

__all__ = ["get_tab_list", "add_or_up_tab", "delete_tab"]


def get_tab_list(page, limit, channel_id):
    data = {}
    tc = TabChannel.objects.filter(channel_id=channel_id)

    p = Paginator(tc, limit)
    if page > p.num_pages:
        return data
    tcs = p.page(page)
    data['tabs'] = [
        dict(channel_id=t.channel_id,
             id=t.tc.id,
             un_check_name=t.tc.un_check_name,
             check_name=t.tc.check_name,
             un_check_style=t.tc.un_check_style,
             check_style=t.tc.check_style,
             un_check_icon=t.tc.un_check_icon,
             check_icon=t.tc.check_icon,
             action_id=t.tc.action_id,
             dot_key=t.tc.dot_key,
             sort=t.tc.sort
             ) for t in tcs]

    data["total"] = p.count
    data['page'] = page
    data["totalpage"] = p.num_pages
    data["hasNext"] = tcs.has_next()
    return data


def add_or_up_tab(request, channel_id, tab_id):
    data = {}
    json_string = request.body.decode('utf-8')
    try:
        request_data = json.loads(json_string)
        if request_data:
            must_result = check_parameter(request_data, TAB_PARAMETERS)
            if must_result.get("code") == 1:
                return must_result
            tab = Tabs.objects.filter(id=tab_id)
            if tab:
                tab.update(**request_data)
            else:
                dot_key = request_data.get("dot_key")
                is_dot_key_exists = TabChannel.objects.filter(
                    channel_id=channel_id, tc__dot_key=dot_key).exists()
                if is_dot_key_exists:
                    return {"msg": u"已经有同名打点Tab栏", "code": 1}
                tabs = Tabs.objects.create(**request_data)
                TabChannel.objects.create(channel_id=channel_id, tc=tabs)
            return {"msg": u"操作成功", "code": 0}
        data = {"msg": u"缺少参数", "code": 1}
    except:
        ptlog()
        data = {"msg": u"操作失败", "code": 1}

    return data


def delete_tab(channel_id, tab_id):
    data = {}
    try:
        tabs = Tabs.objects.filter(id=tab_id)
        for t in tabs:
            TabChannel.objects.filter(channel_id=channel_id, tc=t).delete()
        tabs.delete()
        data = {"msg": u"操作成功", "code": 0}
    except:
        ptlog()
        {"msg": u"操作失败", "code": 0}
    return data
