#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'putao'
__mtime__ = '2015/8/28'
"""
from __future__ import unicode_literals
import time

from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from cms.settings import CMS_CHECK_ON, INSTALL_TYPE
from common.base_cursor import BaseCursor
from common.const import AuthCodeName, CmsModule, CheckOpType, CheckStatu
# from .main_pub import *
# from main.forms import *
from main.forms import GoodsForm
from main.models import CmsNaviCategory, CmsCheck, CmsGoods, get_valid_time, get_city_str
from main.views.interface_category import sync_search
import json
from django.core.urlresolvers import reverse
from common.const import MainConst
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from common.views import get_table_paginator, search_key, get_check_status_str, filter_none, get_url_arg
from main.views.main_pub import add_main_var, format_form, get_actions_select, get_scenes, get_city_group, \
    get_city_list, \
    get_categories

import logging

log = logging.getLogger('config.app')


@login_required
@add_main_var
def goods(request, template_name):
    return render_to_response(template_name, context_instance=RequestContext(request))


# 新增商品,把表单数据保存到数据库中,
@login_required
@permission_required(u'%s.%s' % (AuthCodeName.APP_LABEL, AuthCodeName.CONFIG), raise_exception=True)
@add_main_var
def new_goods(request, template_name):
    if request.method == "POST":
        second_category = request.POST.get("second_category")
        if second_category:
            second_category = CmsNaviCategory.objects.get(id=second_category)
            if second_category.fatherid == 0:
                request.POST["category"] = request.POST["second_category"]
                request.POST['second_category'] = None
            else:
                request.POST["category"] = second_category.fatherid
        new_second_category = request.POST.get("new_second_category")
        if new_second_category:
            new_second_category = CmsNaviCategory.objects.get(id=new_second_category)
            if new_second_category.fatherid == 0:
                request.POST["new_category"] = request.POST["new_second_category"]
                request.POST['new_second_category'] = None
            else:
                request.POST["new_category"] = new_second_category.fatherid
        form = GoodsForm(request.POST)
        if form.is_valid():
            oGoods = form.save()
            if CMS_CHECK_ON:
                CmsCheck(module=CmsModule.MAIN_GOODS,
                         table_name='CmsGoods',
                         data_id=oGoods.id,
                         op_type=CheckOpType.NEW,
                         alter_person=request.user.username,
                         alter_date=time.strftime("%Y-%m-%d %X", time.localtime())).save()
            return HttpResponseRedirect(reverse('goods'))
    else:
        form = GoodsForm()
    errors, fields = format_form(form)
    if 'second_category' in fields.keys() and fields['second_category'] == '""':
        fields['second_category'] = fields['category']
    if 'new_second_category' in fields.keys() and fields['new_second_category'] == '""':
        fields['new_second_category'] = fields['new_category']
    scenes = get_scenes()
    actions = get_actions_select()
    citygroups = get_city_group()
    cities = get_city_list()
    categories = get_categories()
    return render_to_response(template_name, {
        "scenes": scenes,
        "actions": actions,
        "citygroups": citygroups,
        "categories": categories,
        "cities": cities,
        "fields": fields,
        "errors": errors
    }, context_instance=RequestContext(request))

@csrf_exempt
def sync_all_goods_to_search(request):
    response = ""
    goods = CmsGoods.objects.filter(parent_id=-1,goods_id__gt=0)
    if goods:
        for g in goods:
            data = {}
            # cate_fields = ['category', 'second_category', 'new_second_category',
            #                'new_category', 'valid_time', 'min_version', 'max_version', 'recommend_icon',
            #                'recommend_reason', 'sort', 'mark', 'tag1', 'tag1_style', 'tag2', 'tag2_style', 'tag3',
            #                'tag3_style',
            #                'recommend_goodsId', 'recommend_goods_reason', 'search_keyword']
            data['category'] = g.category
            data['second_category'] = g.second_category
            data['new_second_category'] = g.new_second_category
            data['new_category'] = g.new_category
            data['valid_time'] = g.valid_time
            data['min_version'] = g.min_version
            data['recommend_icon'] = g.recommend_icon
            data['recommend_reason'] = g.recommend_reason
            data['sort'] = g.sort
            data['mark'] = g.mark
            data['tag1'] = g.tag1
            data['tag1_style'] = g.tag1_style
            data['tag2'] = g.tag2
            data['tag2_style'] = g.tag2_style
            data['tag3'] = g.tag3
            data['tag3_style'] = g.tag3_style
            data['recommend_goodsId'] = g.recommend_goodsId
            data['recommend_goods_reason'] = g.recommend_goods_reason
            data['search_keyword'] = g.search_keyword
            data['citysJson'] = g.citysJson
            data['serviceRangeJson'] = g.serviceRangeJson
            data['card_type'] = g.card_type
            data['service_times'] = g.service_times
            data['card_minutes'] = g.card_minutes
            data['serviceRangeGraph'] = g.serviceRangeGraph
            data['card_icon'] = g.card_icon
            data['operation_tag'] = data['mark']
            op_tag = []
            if data['tag1'] and data['tag1_style']:
                op_tag.append({'tag': data['tag1'], 'tag_style': data['tag1_style']})

            if data['tag2'] and data['tag2_style']:
                op_tag.append({'tag': data['tag2'], 'tag_style': data['tag2_style']})

            if data['tag3'] and data['tag3_style']:
                op_tag.append({'tag': data['tag3'], 'tag_style': data['tag3_style']})
            data['op_tag'] = op_tag
            content = sync_search(g.goods_id, data)
            response = response + content + "--->" + str(g.goods_id) + "\r\n"
    return HttpResponse(response)


# 编辑修改商品
# 返回 场景对象列表，动作对象列表，带有数据库数据的表单对象。
@login_required
@permission_required(u'%s.%s' % (AuthCodeName.APP_LABEL, AuthCodeName.CONFIG), raise_exception=True)
@add_main_var
def edit_goods(request, template_name):
    id = request.GET.get("id")
    all_goods = CmsGoods.objects.filter(parent_id=-1, goods_id__gt=0)
    if request.method == "POST":
        second_category = request.POST.get("second_category")
        if second_category:
            second_category = CmsNaviCategory.objects.get(id=second_category)
            if second_category.fatherid == 0:
                request.POST["category"] = request.POST["second_category"]
                request.POST['second_category'] = None
            else:
                request.POST["category"] = second_category.fatherid
        new_second_category = request.POST.get("new_second_category")
        if new_second_category:
            new_second_category = CmsNaviCategory.objects.get(id=new_second_category)
            if new_second_category.fatherid == 0:
                request.POST["new_category"] = request.POST["new_second_category"]
                request.POST['new_second_category'] = None
            else:
                request.POST["new_category"] = new_second_category.fatherid
        goods = CmsGoods.objects.get(id=id)
        request.POST['is_support_cart'] = goods.is_support_cart
        request.POST['sort'] = goods.sort
        request.POST['citysJson'] = goods.citysJson
        request.POST['serviceRangeJson'] = goods.serviceRangeJson
        request.POST['card_type'] = goods.card_type
        request.POST['service_times'] = goods.service_times
        request.POST['card_minutes'] = goods.card_minutes
        request.POST['serviceRangeGraph'] = goods.serviceRangeGraph
        #V 4.5添加字段
        request.POST['sale_status'] = goods.sale_status
        request.POST['is_select_count'] = goods.is_select_count
        request.POST['min_buy_count'] = goods.min_buy_count
        request.POST['max_buy_count'] = goods.max_buy_count
        request.POST['c_time'] = goods.c_time
        request.POST['card_support_length'] = goods.card_support_length
        request.POST['service_length'] = goods.service_length
        #V 4.5添加字段完毕
        # request.POST['recommend_goodsId'] = str(goods.recommend_goodsId)
        # log.info('recommend_goodsId:'+request.POST.get('recommend_goodsId'))
        form = GoodsForm(request.POST, instance=goods)
        if form.is_valid():
            form.save()
            data = {}
            cate_fields = ['category', 'second_category', 'new_second_category',
                           'new_category', 'valid_time', 'min_version', 'max_version', 'recommend_icon',
                           'recommend_reason', 'sort', 'mark', 'tag1', 'tag1_style', 'tag2', 'tag2_style', 'tag3',
                           'tag3_style',
                           'recommend_goodsId', 'recommend_goods_reason', 'search_keyword']
            for field in cate_fields:
                if request.POST.get(field):
                    data[field] = request.POST.get(field)
            data['min_version'] = request.POST.get('min_version')
            data['max_version'] = request.POST.get('max_version')
            data['recommend_icon'] = request.POST.get('recommend_icon')
            data['recommend_reason'] = request.POST.get('recommend_reason')
            data['sort'] = request.POST.get('sort')
            data['mark'] = request.POST.get('mark')
            data['tag1'] = request.POST.get('tag1')
            data['tag1_style'] = request.POST.get('tag1_style')
            data['tag2'] = request.POST.get('tag2')
            data['tag2_style'] = request.POST.get('tag2_style')
            data['tag3'] = request.POST.get('tag3')
            data['tag3_style'] = request.POST.get('tag3_style')
            data['recommend_goodsId'] = request.POST.get('recommend_goodsId')
            data['recommend_goods_reason'] = request.POST.get('recommend_goods_reason')
            data['citysJson'] = goods.citysJson
            data['serviceRangeJson'] = goods.serviceRangeJson
            data['card_type'] = goods.card_type
            data['service_times'] = goods.service_times
            data['card_minutes'] = goods.card_minutes
            data['serviceRangeGraph'] = goods.serviceRangeGraph
            data['card_icon'] = goods.card_icon

            # 更新同一goods_id的商品
            if data:
                CmsGoods.objects.filter(~Q(id=id), goods_id=goods.goods_id).update(**data)
                if INSTALL_TYPE == 2 or INSTALL_TYPE == 3:
                    # 同步至搜索
                    data['operation_tag'] = data['mark']
                    op_tag = []
                    if data['tag1'] and data['tag1_style']:
                        op_tag.append({'tag': data['tag1'], 'tag_style': data['tag1_style']})

                    if data['tag2'] and data['tag2_style']:
                        op_tag.append({'tag': data['tag2'], 'tag_style': data['tag2_style']})

                    if data['tag3'] and data['tag3_style']:
                        op_tag.append({'tag': data['tag3'], 'tag_style': data['tag3_style']})
                    data['op_tag'] = op_tag
                    sync_search(goods.goods_id, data)
            if CMS_CHECK_ON:
                CmsCheck(module=CmsModule.MAIN_GOODS,
                         table_name='CmsGoods',
                         data_id=id,
                         op_type=CheckOpType.EDIT,
                         alter_person=request.user.username,
                         alter_date=time.strftime("%Y-%m-%d %X", time.localtime())).save()
            return HttpResponseRedirect(reverse('goods'))
    else:
        goods = CmsGoods.objects.get(id=id)
        form = GoodsForm(instance=goods)
    errors, fields = format_form(form)
    if 'second_category' in fields.keys() and fields['second_category'] == '""':
        fields['second_category'] = fields['category']
    if 'new_second_category' in fields.keys() and fields['new_second_category'] == '""':
        fields['new_second_category'] = fields['new_category']
    scenes = get_scenes()
    actions = get_actions_select()
    citygroups = get_city_group()
    cities = get_city_list()
    categories = get_categories()
    return render_to_response(template_name, {
        "scenes": scenes,
        "actions": actions,
        "categories": categories,
        "citygroups": citygroups,
        "cities": cities,
        "id": id,
        "fields": fields,
        "errors": errors,
        "all_goods": all_goods
    }, context_instance=RequestContext(request))


# 查询商品列表（搜索商品，分页查看），返回总页码和对象列表
# 版本2
@login_required
def search_goods(request):
    per_page = request.GET.get("per_page")
    if not per_page:
        per_page = MainConst.PER_PAGE
    cur_page = request.GET.get("cur_page")
    if not cur_page:
        cur_page = 1
    key = request.GET.get("key")
    objs = CmsGoods.objects.filter(parent_id=-1).order_by("-sort")
    goods = []
    all_category = CmsNaviCategory.objects.all()
    for obj in objs:
        new_category = ""
        new_second_category = ""
        if obj.new_category:
            try:
                for cate in all_category:
                    if obj.new_category == cate.id:
                        new_category = cate.name
                        break
            except:
                log.error(str(obj.new_second_category) + " is not query by cms_navi_category")
        if obj.new_second_category:
            try:
                for sec_cate in all_category:
                    if obj.new_second_category == sec_cate.id:
                        new_second_category = sec_cate.name
            except:
                log.error(str(obj.new_second_category) + " is not query by cms_navi_category")
        status_str, status_int = get_check_status_str("CmsGoods", obj.id)
        goods.append([
            new_category,
            new_second_category,
            obj.name,
            obj.small_icon_url,
            obj.icon_url,
            obj.goods_id,
            obj.cp_name,
            obj.desc,
            obj.search_keyword,
            get_valid_time(obj.valid_time),
            get_city_str(obj.city),
            status_str,
            obj.is_support_cart,
            obj.min_version,
            obj.max_version,
            obj.recommend_icon,
            obj.recommend_reason,
            obj.sort,
            status_int,
            obj.id
        ])
    result = search_key(goods, key, [1, 10, 11])
    result, num_pages = get_table_paginator(result, per_page, cur_page)
    filter_none(result)
    return HttpResponse(json.dumps([list(result), num_pages]))


# 更改商品排序
@login_required
def exchange_sort(request):
    goods_id = request.POST.get("goods_id")
    sort = request.POST.get("sort")
    log.error("goods_id:" + goods_id + " sort:" + sort)
    data = {}
    data['sort'] = sort
    CmsGoods.objects.filter(goods_id=goods_id).update(**data)
    return HttpResponse(0)


# 删除商品
@login_required
@permission_required(u'%s.%s' % (AuthCodeName.APP_LABEL, AuthCodeName.CONFIG), raise_exception=True)
def del_goods(request):
    id = request.POST.get('id')
    goods = CmsGoods.objects.get(id=id)
    if CMS_CHECK_ON:
        check = CmsCheck(
            module=CmsModule.MAIN_GOODS,
            table_name="CmsGoods",
            data_id=id,
            op_type=CheckOpType.DELETE,
            status=CheckStatu.WAIT_SUBMIT,
            is_show=1,
            alter_person=request.user.username,
            alter_date=time.strftime("%Y-%m-%d %X", time.localtime()))
        check.save()
    goods.delete()
    return HttpResponse(0)


def ajax_goods(request):
    page = get_url_arg(request, 'page', int, 1)
    #per_page = get_url_arg(request, 'per_page', int, 15)
    per_page = 5000
    category_id = get_url_arg(request, 'id', int, 0)
    search_key = get_url_arg(request, 'search_key', str, None)
    total_page, actions = _slice_goods_select(search_key, category_id, page=page, per_page=per_page)

    def _format(item):
        new_item = []
        if (item[3]) == '*':
            item[3] = u'不限(全国)'
        new_item.append(item[0])
        new_item.append('-'.join(item[1:]))
        return new_item

    actions = list(map(_format, actions))
    result = {'total_page': total_page, 'cur_page': page, "actions": actions}
    json_str = json.dumps(result)
    return HttpResponse(json_str)


def ajax_desc_goods(request):
    page = get_url_arg(request, 'page', int, 1)
    #per_page = get_url_arg(request, 'per_page', int, 15)
    per_page = 5000
    category_id = get_url_arg(request, 'id', int, 0)
    search_key = get_url_arg(request, 'search_key', str, None)
    total_page, actions = _slice_goods_desc_select(search_key, category_id, page=page, per_page=per_page)
    result = {'total_page': total_page, 'cur_page': page, "actions": actions}
    json_str = json.dumps(result)
    return HttpResponse(json_str)


def _slice_goods_select(key, category_id, page=1, per_page=15):
    if key and len(key) > 0:
        goods = r"select `goods_id`,`cp_name`,`name`,`city` from `view_cms_goods_formal` where `parent_id`=-1 and `new_category`={1} and  (`id` like '%{0}%' or `name` like '%{0}%' or `city` like '%{0}%' or `cp_name` like '%{0}%')".format(
            key, category_id)
    else:
        goods = r"select `goods_id`,`cp_name`,`name`,`city` from `view_cms_goods_formal` where `parent_id`=-1 and `new_category`={0}".format(
            category_id)
    # print(goods)
    total_page, result = BaseCursor.get_pageinate(page, per_page, goods)
    return total_page, result


def _slice_goods_desc_select(key, category_id, page=1, per_page=15):
    if key and len(key) > 0:
        goods = r"select `goods_id`,CONCAT(name,'-',cp_name) from `view_cms_goods_formal` where `parent_id`=-1 and `new_category`={1} and  (`id` like '%{0}%' or `name` like '%{0}%' or `desc` like '%{0}%' )".format(
            key, category_id)
    else:
        goods = r"select `goods_id`,CONCAT(name,'-',cp_name) from `view_cms_goods_formal` where `parent_id`=-1 and `new_category`={0}".format(
            category_id)
    total_page, result = BaseCursor.get_pageinate(page, per_page, goods)
    return total_page, result
