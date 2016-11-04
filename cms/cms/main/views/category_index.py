#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author sunq
import json

from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

from common.views import get_url_arg, get_body_arg
from main.model.adbeans import Adbeans
from main.model.category_index import CategoryIndex
from main.model.category_index_ads import CategoryIndexAds
from main.model.category_index_quick_order import CategoryIndexQuickOrder
from main.model.category_index_recommended import CategoryIndexRecommended
from main.views.main_pub import add_main_var, response


@login_required
@add_main_var
def category_index(request, template_name):
    return render_to_response(template_name, context_instance=RequestContext(request))


@login_required
def search_category_index(request):
    page = get_url_arg(request, 'cur_page', int, 1)
    per_page = get_url_arg(request, 'per_page', int, 20)
    search_key = get_url_arg(request, 'search_key', str, None)
    total_page, data = CategoryIndex.search_category_index(page, per_page, search_key)

    def _format(item):
        if item[-1] == '*':
            item[-1] = '不限(全国)'
        return item

    data = list(map(_format, data))
    return HttpResponse(json.dumps([data, total_page]))


@login_required
@add_main_var
def edit_category_index(request, template_name):
    id = get_url_arg(request, 'id', int, 0)
    return render_to_response(template_name, {'id': id}, context_instance=RequestContext(request))


@login_required
def delete_category_index(request):
    id = get_url_arg(request, 'id', int, 0)
    if id > 0:
        result = CategoryIndex.delete_category_index(id)
        if result:
            return response(0, "删除成功!")
        else:
            return response(1, "删除失败!")
    else:
        return response(1, "非法参数")


@login_required
def insert_category_index(request):
    if request.method == 'POST':
        current_user = request.user.id
        id = get_body_arg(request, 'id', int, 0)

        category_id = get_body_arg(request, 'category_id', int, 0)
        is_need_all = get_body_arg(request, 'is_need_all', int, 0)
        category_city = get_body_arg(request, 'city', str, '*')
        banners = get_body_arg(request, 'banners', 'json_array', [])
        quick_orders = get_body_arg(request, 'quick_orders', 'json_array', [])
        recommended_goods = get_body_arg(request, 'recommended_goods', 'json_array', [])
        result = _insert(category_id, is_need_all, category_city, banners, quick_orders, recommended_goods,
                         current_user, id=id)
        if result:
            return response(0, '操作成功')
        else:
            return response(2, '保存失败')

    else:
        return response(1, '非法请求')


@login_required
def update_category_index(request):
    if request.method == 'GET':
        id = get_url_arg(request, 'id', int, 0)
        if id > 0:
            data = CategoryIndex.get_update_data(id)
            if data:
                return response(0, '操作成功', data)
            else:
                return response(2, '资源获取失败')
        else:
            return response(3, '参数错误')
    else:
        return response(1, '非法请求')


def _insert(category_id, is_need_all, category_city, banners, quick_orders, recommended_goods,
            current_user, id=0):
    try:
        with transaction.atomic():
            ads = Adbeans.create_schedule(banners)
            ad_ids = [ad.id for ad in ads]
            category_index = CategoryIndex.create_or_update(category_id, category_city, is_need_all, current_user,
                                                            id=id)
            rel_ads = CategoryIndexAds.create_schedule(category_index.id, ad_ids, current_user)
            rel_qos = CategoryIndexQuickOrder.create_schedule(category_index.id, quick_orders, current_user)
            recommendeds = CategoryIndexRecommended.create_schedule(category_index.id, recommended_goods, current_user)
        return True
    except Exception as e:
        return False
