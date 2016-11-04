# -*- coding: utf-8 -*-
# Author:songroger
# Jul.6.2016
from __future__ import unicode_literals
from config.utils import get_pcard_goods_list, get_pcard_goods, \
    delete_pcard_goods, add_pcard_goods, get_common_goods
from pttools.pthttp import PtHttpResponse
from django.views.decorators.http import require_http_methods, require_safe
from django.contrib.auth.decorators import login_required


@require_safe
@login_required
def pcard_goods_list(request):
    """
    获取套餐卡商品列表
    """
    page = int(request.GET.get('page', 1))
    limit = int(request.GET.get('limit', 10))
    data = get_pcard_goods_list(page, limit)
    return PtHttpResponse(data)


@require_http_methods(['GET', 'POST', 'PUT', 'DELETE'])
@login_required
def pcard_goods(request):
    """
    获取套餐卡商品
    """
    data = {}
    if request.method == "GET":
        cid = request.GET.get('id', None)
        data = get_pcard_goods(cid)
        return PtHttpResponse(data)
    elif request.method == "POST":
        data = add_pcard_goods(request)
        return PtHttpResponse(data)
    elif request.method == "DELETE":
        pid = request.GET.get('pid', None)
        gid = request.GET.get('gid', None)
        if pid and gid:
            data = delete_pcard_goods(pid, gid)
            return PtHttpResponse(data)
        data = {"msg": u"缺少参数", "code": 1}
    return PtHttpResponse(data)


@require_safe
@login_required
def pcard_common_goods(request):
    """
    获取可添加到套餐卡商品列表
    """
    # page = int(request.GET.get('page', 1))
    # limit = int(request.GET.get('limit', 10))
    data = get_common_goods()
    return PtHttpResponse(data)
