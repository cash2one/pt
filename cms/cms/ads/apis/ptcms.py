# -*- coding: utf-8 -*-
# Author:songroger
# Aug.29.2016
from __future__ import unicode_literals
from pttools.pthttp import PtHttpResponse
from django.views.decorators.http import require_http_methods, require_safe
from django.contrib.auth.decorators import login_required
from ads.utils import get_cover_ads_list, add_or_up_cover_ads, delete_ads


@require_safe
@login_required
def cover_ads_list(request):
    """
    获取cover ads列表
    """
    data = {}
    page = int(request.GET.get('page', 1))
    limit = int(request.GET.get('limit', 10))
    channel_id = int(request.GET.get('channel', 0))
    if channel_id:
        data = get_cover_ads_list(page, limit, channel_id)
    return PtHttpResponse(data)


@require_http_methods(['POST', 'PUT', 'DELETE'])
@login_required
def cover_ads(request):
    data = {}
    channel_id = int(request.GET.get('channel', 0))
    ads_id = int(request.GET.get('aid', 0))
    if request.method == "POST":
        if channel_id:
            data = add_or_up_cover_ads(request, channel_id, 0)
        else:
            data = {"msg": u"缺少参数channel", "code": 1}
    elif request.method == "PUT":
        if channel_id and ads_id:
            data = add_or_up_cover_ads(request, channel_id, ads_id)
        else:
            data = {"msg": u"缺少参数channel或aid", "code": 1}
    elif request.method == "DELETE":
        if channel_id and ads_id:
            data = delete_ads(channel_id, ads_id)
        else:
            data = {"msg": u"缺少参数channel或aid", "code": 1}
    return PtHttpResponse(data)
