#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author sunq
import json
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

from common.base_cursor import BaseCursor
from common.views import get_url_arg, get_body_arg
from main.model.quick_order import QuickOrderModel
from main.model.quick_order_category import QuickOrderCategory
from main.model.quick_order_goods import QuickOrderGoods
# from .main_pub import *
from main.views.main_pub import add_main_var, response


@login_required
@add_main_var
def quick_order(request, template_name):
    return render_to_response(template_name, context_instance=RequestContext(request))


@login_required
def search_quick_orders(request):
    page = get_url_arg(request, 'cur_page', int, 1)
    per_page = get_url_arg(request, 'per_page', int, 20)
    search_key = get_url_arg(request, 'search_key', str, None)
    total_page, data = QuickOrderModel.search_quick_order(page, per_page, search_key)

    def format(x):
        x.append(QuickOrderGoods.get_goods_simple_str(x[0]))
        return x

    data = list(map(format, data))
    return HttpResponse(json.dumps([data, total_page]))


@login_required
@add_main_var
def edit_quick_order(request, template_name):
    id = get_url_arg(request, 'id', int, 0)
    return render_to_response(template_name, {'id': id}, context_instance=RequestContext(request))


@login_required
def insert_quick_order(request):
    if request.method == 'POST':
        current_user = request.user.id
        id = get_body_arg(request, 'id', int, 0)
        category_id = get_body_arg(request, 'category_id', int, 0)
        icon_url = get_body_arg(request, 'icon_url', str, '')
        quick_order_name = get_body_arg(request, 'quick_order_name', str, '')
        quick_order_desc = get_body_arg(request, 'quick_order_desc', str, '')
        goods = get_body_arg(request, 'goods', 'json_array', '')
        order_style = get_body_arg(request, 'order_style', str, '')
        background_style = get_body_arg(request, 'background_style', str, '')
        is_h5 = get_body_arg(request, 'is_h5', int, 0)
        h5_url = get_body_arg(request, 'h5_url', str, '')
        result = _insert(quick_order_name, quick_order_desc, icon_url, order_style, background_style, current_user,
                         category_id, goods, is_h5, h5_url, id=id)
        if result:
            return response(0, '操作成功')
        else:
            return response(2, '保存失败')
    else:
        return response(1, '非法请求')


def _insert(quick_order_name, quick_order_desc, icon_url, order_style, background_style, current_user, category_id,
            goods, is_h5, h5_url, id=0):
    try:
        with transaction.atomic():
            qm = QuickOrderModel.create_or_get_quick_order(quick_order_name, quick_order_desc, icon_url, order_style,
                                                           background_style, current_user, is_h5, h5_url, id=id)
            qc = QuickOrderCategory.create_or_get(qm.id, category_id, current_user)
            qgs = QuickOrderGoods.create_schedule(goods, current_user, qm.id)

            return True
    except Exception as e:
        return False


@login_required
def update_quick_order(request):
    if request.method == 'GET':
        id = get_url_arg(request, 'id', int, 0)
        if id > 0:
            data = QuickOrderModel.get_update_data(id)
            if data:
                return response(0, u'操作成功', data)
            else:
                return response(2, '资源获取失败')
        else:
            return response(3, '参数错误')
    else:
        return response(1, '非法请求')


@login_required
def delete_quick_order(request):
    id = get_url_arg(request, 'id', int, 0)
    if id > 0:
        result = QuickOrderModel.delete_quick_order(id)
        if result:
            return response(0, "删除成功!")
        else:
            return response(1, "删除失败!")
    else:
        return response(1, "非法参数")


def search_second_category(request):
    page = get_url_arg(request, 'page', int, 1)
    # per_page = get_url_arg(request, 'per_page', int, 1500)
    search_key = get_url_arg(request, 'search_key', str, None)
    total_page, actions = _slice_category_select(search_key, page=page, per_page=10000)
    result = {'total_page': total_page, 'cur_page': page, "actions": actions}
    json_str = json.dumps(result)

    return HttpResponse(json_str)


def _slice_category_select(key, page=1, per_page=10000):
    if key and len(key) > 0:
        categories = r"select `id`,`name` from `cms_navi_category` where `parent_id` =0 and `fatherId`=0 and `type`=1 and (`id` like '%{0}%' or `name` like '%{0}%')".format(
            key)
    else:
        categories = r"select `id`,`name` from `cms_navi_category` where `parent_id` =0 and `fatherId`=0 and `type`=1"

    total_page, result = BaseCursor.get_pageinate(page, per_page, categories)
    return total_page, result


def ajax_quick_order(request):
    page = get_url_arg(request, 'page', int, 1)
    per_page = get_url_arg(request, 'per_page', int, 15)
    id = get_url_arg(request, 'id', int, 0)
    search_key = get_url_arg(request, 'search_key', str, None)
    total_page, quick_orders = _slice_quick_order_select(search_key, id, page, per_page)

    def _format(item):
        x = str(item[0]) + '-' + item[1]
        y = item[2]
        return [x, y]

    quick_orders = list(map(_format, quick_orders))
    result = {'total_page': total_page, 'cur_page': page, "actions": quick_orders}
    json_str = json.dumps(result)
    return HttpResponse(json_str)


def _slice_quick_order_select(key, category_id, page=1, per_page=20):
    if key and len(key) > 0:
        goods = r"select qo.id,qo.cms_quick_desc,qo.cms_quick_name from cms_quick_order_category qoc inner join  cms_quick_order qo on qoc.quick_order_id = qo.id where qoc.category_id={1} and (qo.id like '%{0}%' or qo.cms_quick_name like '%{0}%')".format(
            key, category_id)
    else:
        goods = r"select qo.id,qo.cms_quick_desc,qo.cms_quick_name from cms_quick_order_category qoc inner join  cms_quick_order qo on qoc.quick_order_id = qo.id where qoc.category_id={0}".format(
            category_id)
    total_page, result = BaseCursor.get_pageinate(page, per_page, goods)
    return total_page, result
