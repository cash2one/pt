# -*- coding: utf-8 -*-
# Author:songroger
# Aug.4.2016
from __future__ import unicode_literals
import json
import traceback
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import Sku
from pttools.pthttp import PtHttpResponse
from django.db import IntegrityError


@require_http_methods(['POST', 'PUT', 'DELETE'])
@csrf_exempt
def synch_skus(request):
    """
    接收商品sku信息接口（开放平台）
    """
    data = {}
    if request.method == "DELETE":
        sku_id = request.GET.get("sid", None)
        goods_id = request.GET.get("gid", None)
        if sku_id and goods_id:
            Sku.objects.filter(sku_id=sku_id, goods_id=goods_id).delete()
            data = {"msg": u"删除成功", "code": 0}
    elif request.method == "POST" or request.method == "PUT":
        data = _add_or_up_sku(request)
        return PtHttpResponse(data)

    return PtHttpResponse(data)


def _add_or_up_sku(request):
    json_string = request.body.decode('utf-8')
    try:
        request_data = json.loads(json_string)
        if request_data:
            # ca_objects = [Sku(**g) for g in request_data]
            for g in request_data:
                sku_id = g.get("sku_id", None)
                goods_id = g.get("goods_id", None)
                sku = Sku.objects.filter(sku_id=sku_id, goods_id=goods_id)
                if sku:
                    sku.update(**g)
                else:
                    Sku.objects.create(**g)
            data = {"msg": u"添加成功", "code": 0}
    except:
        data = {"msg": u"添加失败", "code": 1}
    return data
