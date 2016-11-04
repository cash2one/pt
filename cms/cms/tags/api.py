# -*- coding: utf-8 -*-
# Author:songroger
# Aug.1.2016
from __future__ import unicode_literals
import json
import traceback
from pttools.pthttp import PtHttpResponse
from django.views.decorators.http import require_http_methods, require_safe
from django.contrib.auth.decorators import login_required
from tags.utils import get_tags_list, get_tag, add_tag, up_tag, delete_tag, \
    get_tag_group_list, get_tag_group, add_tag_group, up_tag_group, \
    delete_tag_group, get_tag_goods_list, tag_to_goods, delete_tags, \
    get_tag_group_tags, delete_group_tag, get_third_category_list, \
    tag_to_group, cats_get_goods, get_booking_tag_groups, get_booking_groups, \
    tag_to_booking, delete_tag_booking, set_tag_sort, set_group_sort, \
    get_all_skus


@require_safe
@login_required
def tag_list(request):
    """
    获取标签列表
    """
    page = int(request.GET.get('page', 1))
    limit = int(request.GET.get('limit', 10))
    full = int(request.GET.get('all', 0))
    data = get_tags_list(page, limit, full)
    return PtHttpResponse(data)


@require_http_methods(['GET', 'POST', 'PUT', 'DELETE'])
@login_required
def tag(request):
    data = {}
    if request.method == "GET":
        tid = request.GET.get('id', None)
        if tid:
            data = get_tag(tid)
            return PtHttpResponse(data)
    elif request.method == "POST":
        data = add_tag(request)
        return PtHttpResponse(data)
    elif request.method == "PUT":
        tid = request.GET.get('id', None)
        if tid:
            data = up_tag(request, tid)
            return PtHttpResponse(data)
    elif request.method == "DELETE":
        tid = request.GET.get('id', None)
        if tid:
            data = delete_tag(tid)
            return PtHttpResponse(data)
    return PtHttpResponse(data)


@require_safe
@login_required
def tag_group_list(request):
    """
    获取标签组列表
    """
    page = int(request.GET.get('page', 1))
    limit = int(request.GET.get('limit', 10))
    full = int(request.GET.get('all', 0))
    data = get_tag_group_list(page, limit, full)
    return PtHttpResponse(data)


@require_http_methods(['GET', 'POST', 'PUT', 'DELETE'])
@login_required
def tag_group(request):
    data = {}
    if request.method == "GET":
        gid = request.GET.get('id', None)
        if gid:
            data = get_tag_group(gid)
            return PtHttpResponse(data)
    elif request.method == "POST":
        data = add_tag_group(request)
        return PtHttpResponse(data)
    elif request.method == "PUT":
        gid = request.GET.get('id', None)
        if gid:
            data = up_tag_group(request, gid)
            return PtHttpResponse(data)
    elif request.method == "DELETE":
        gid = request.GET.get('id', None)
        if gid:
            data = delete_tag_group(gid)
            return PtHttpResponse(data)
    return PtHttpResponse(data)


@require_safe
@login_required
def tag_goods_list(request):
    """
    标签商品列表页
    """
    data = {}
    page = int(request.GET.get('page', 1))
    limit = int(request.GET.get('limit', 10))
    tag = request.GET.get('tag', None)
    if tag:
        data = get_tag_goods_list(page, limit, int(tag))
    return PtHttpResponse(data)


@require_http_methods(['POST', 'DELETE'])
@login_required
def tag_goods(request):
    data = {}
    if request.method == "POST":
        json_string = request.body.decode('utf-8')
        try:
            request_data = json.loads(json_string)
            if request_data:
                tag_id = request_data.get('tag_id', None)
                goods_id = request_data.get('goods_id', [])
                data = tag_to_goods(tag_id, goods_id)
                # data = {"msg": u"添加成功", "code": 0}
            else:
                data = {"msg": u"缺少参数", "code": 1}
        except:
            data = {"msg": u"添加失败", "code": 1}
    elif request.method == "DELETE":
        tag_id = request.GET.get('tag_id', None)
        goods_id = request.GET.get('goods_id', None)
        sku_id = request.GET.get('sku_id', None)
        if tag_id and goods_id and sku_id:
            data = delete_tags(tag_id, goods_id, sku_id)
        else:
            data = {"msg": u"缺少参数", "code": 1}

    return PtHttpResponse(data)


@require_safe
@login_required
def tag_group_tags(request):
    data = {}
    page = int(request.GET.get('page', 1))
    limit = int(request.GET.get('limit', 10))
    gid = request.GET.get('gid', None)
    if gid:
        data = get_tag_group_tags(page, limit, gid)
    return PtHttpResponse(data)


@require_http_methods(['POST', 'DELETE'])
@login_required
def manage_tag_group_tags(request):
    data = {}
    if request.method == "POST":
        json_string = request.body.decode('utf-8')
        try:
            request_data = json.loads(json_string)
            if request_data:
                tag_group_id = request_data.get('tag_group_id', None)
                tags_id = request_data.get('tags_id', [])
                data = tag_to_group(tag_group_id, tags_id)
                # data = {"msg": u"添加成功", "code": 0}
            else:
                data = {"msg": u"缺少参数", "code": 1}
        except:
            data = {"msg": u"添加失败", "code": 1}
    elif request.method == "DELETE":
        group_id = request.GET.get('group_id', None)
        tag_id = request.GET.get('tag_id', None)
        if group_id and tag_id:
            data = delete_group_tag(group_id, tag_id)
        else:
            data = {"msg": u"缺少参数", "code": 1}

    return PtHttpResponse(data)


@require_http_methods('POST')
@login_required
def third_category_list(request):
    """
    三级分类列表
    @para: cat_ids:二级分类ID列表
    @return 三级分类名称列表
    """
    data = {}
    json_string = request.body.decode('utf-8')
    try:
        request_data = json.loads(json_string)
        if request_data:
            cat_ids = request_data.get('cat_ids', [])
            data = get_third_category_list(cat_ids)
    except:
        data = {"msg": u"获取数据错误", "code": 1}
    return PtHttpResponse(data)


@require_http_methods('POST')
@login_required
def cats_to_get_goods_list(request):
    """
    根据二级和三级分类列表取商品列表
    @para: thd_cat_ids:三级分类ID列表 sec_cat_ids：二级分类ID
    @return 商品列表
    """
    data = {}
    json_string = request.body.decode('utf-8')
    try:
        request_data = json.loads(json_string)
        if request_data:
            thd_cat_ids = request_data.get('cat_ids', [])
            tid = request_data.get('tid', 0)
            sec_cat_ids = request_data.get('sec_cat_ids', [])
            data = cats_get_goods(tid, thd_cat_ids, sec_cat_ids)
    except:
        data = {"msg": u"获取数据错误", "code": 1}
    return PtHttpResponse(data)


@require_safe
@login_required
def booking_tag_groups(request):
    """
    快捷预约标签组列表页
    """
    page = int(request.GET.get('page', 1))
    limit = int(request.GET.get('limit', 10))
    data = get_booking_tag_groups(page, limit)
    return PtHttpResponse(data)


@require_safe
@login_required
def booking_groups(request):
    """
    快捷入口所有标签组列表
    """
    data = {}
    page = int(request.GET.get('page', 1))
    limit = int(request.GET.get('limit', 10))
    bid = request.GET.get('bid', None)
    if bid:
        data = get_booking_groups(page, limit, bid)
    return PtHttpResponse(data)


@require_http_methods(['POST', 'DELETE'])
@login_required
def tag_booking(request):
    data = {}
    if request.method == "POST":
        json_string = request.body.decode('utf-8')
        try:
            request_data = json.loads(json_string)
            if request_data:
                bid = request_data.get('bid', None)
                gids = request_data.get('gids', [])
                data = tag_to_booking(bid, gids)
                # data = {"msg": u"添加成功", "code": 0}
            else:
                data = {"msg": u"缺少参数", "code": 1}
        except:
            data = {"msg": u"添加失败", "code": 1}
    elif request.method == "DELETE":
        bid = request.GET.get('bid', None)
        gid = request.GET.get('gid', None)
        if bid and gid:
            data = delete_tag_booking(bid, gid)
        else:
            data = {"msg": u"缺少参数", "code": 1}

    return PtHttpResponse(data)


@require_http_methods('PUT')
@login_required
def tag_sort(request):
    data = {}
    json_string = request.body.decode('utf-8')
    try:
        request_data = json.loads(json_string)
        if request_data:
            tid = request_data.get('tid', None)
            gid = request_data.get('gid', None)
            sort = request_data.get('sort', None)
            data = set_tag_sort(tid, gid, sort)
        else:
            data = {"msg": u"缺少参数", "code": 1}
    except:
        data = {"msg": u"修改失败", "code": 1}
    return PtHttpResponse(data)


@require_http_methods('PUT')
@login_required
def group_sort(request):
    data = {}
    json_string = request.body.decode('utf-8')
    try:
        request_data = json.loads(json_string)
        if request_data:
            bid = request_data.get('bid', None)
            gid = request_data.get('gid', None)
            sort = request_data.get('sort', None)
            data = set_group_sort(bid, gid, sort)
        else:
            data = {"msg": u"缺少参数", "code": 1}
    except:
        data = {"msg": u"修改失败", "code": 1}
    return PtHttpResponse(data)


@require_safe
@login_required
def all_skus(request):
    """
    全部商品sku列表
    """
    # page = int(request.GET.get('page', 1))
    # limit = int(request.GET.get('limit', 10))
    data = get_all_skus()
    return PtHttpResponse(data)
