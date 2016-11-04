#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'putao'
__mtime__ = '2015/8/28'
"""
import time

from cms.settings import CMS_CHECK_ON
from common.const import CmsModule, CheckOpType, CheckStatu
import json
from django.core.urlresolvers import reverse
from common.const import MainConst
# from .main_pub import *
# from main.forms import *
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from common.const import AuthCodeName
from common.views import get_table_paginator, get_check_status_str, search_key, make_timestamp, timestamp2str
from main.forms import CouponsForm
from main.models import CmsCoupon, get_valid_time, get_city_str, CmsCheck
from main.views.main_pub import add_main_var, get_city_list, format_form, get_city_group, get_scenes


# 优惠券列表


@login_required
@add_main_var
def coupons(request, template_name):
    return render_to_response(template_name, context_instance=RequestContext(request))


# 列表（搜索，分页查看），返回总页码和对象列表
@login_required
def search_coupons(request):
    per_page = request.GET.get("per_page")
    if not per_page:
        per_page = MainConst.PER_PAGE
    cur_page = request.GET.get("cur_page")
    if not cur_page:
        cur_page = 1
    objs = CmsCoupon.objects.filter(parent_id=-1)
    coupons = []
    for obj in objs:
        status_str, status_int = get_check_status_str("CmsCoupon", obj.id)
        coupons.append([
            obj.name,
            obj.url,
            obj.coupon_id,
            get_valid_time(obj.valid_time),
            get_city_str(obj.city),
            status_str,
            status_int,
            obj.id
        ])
    key = request.GET.get("key")
    coupons_lst = search_key(coupons, key, [1, 6, 7])
    result, num_pages = get_table_paginator(coupons_lst, per_page, cur_page)
    return HttpResponse(json.dumps([list(result), num_pages]))


# 新增优惠券
@login_required
@permission_required(u'%s.%s' % (AuthCodeName.APP_LABEL, AuthCodeName.CONFIG), raise_exception=True)
@add_main_var
def new_coupons(request, template_name):
    """
    新建优惠券
    url :{% url 'new_coupons' %}
    :请求方式: Get
    :请求参数：无
    :返回数据：scenes 场景列表 citygroups 城市分组列表，cities 所有城市(列表)
    :[[id,name],[id,name],....]

    :请求方式：Post
    :请求参数：数据库字段(input name)
    """
    if request.method == "POST":
        form = CouponsForm(request.POST)
        form.data['start'] = make_timestamp(form.data['start'])
        form.data['end'] = make_timestamp(form.data['end'])
        if form.is_valid():
            oCoupons = form.save()
            if CMS_CHECK_ON:
                CmsCheck(module=CmsModule.MAIN_COUPON,
                         table_name='CmsCoupon',
                         data_id=oCoupons.id,
                         op_type=CheckOpType.NEW,
                         alter_person=request.user.username,
                         alter_date=time.strftime("%Y-%m-%d %X", time.localtime())).save()
            return HttpResponseRedirect(reverse("coupons"))
    else:
        form = CouponsForm()
    errors, fields = format_form(form)
    if 'start' in fields.keys():
        fields['start'] = json.dumps(timestamp2str(fields['start']))
    if 'end' in fields.keys():
        fields['end'] = json.dumps(timestamp2str(fields['end']))
    scenes = get_scenes()
    citygroups = get_city_group()
    cities = get_city_list()
    return render_to_response(template_name, {
        "scenes": scenes,
        "citygroups": citygroups,
        "cities": cities,
        "errors": errors,
        "fields": fields
    }, context_instance=RequestContext(request))


# 编辑优惠券
@login_required
@permission_required(u'%s.%s' % (AuthCodeName.APP_LABEL, AuthCodeName.CONFIG), raise_exception=True)
@add_main_var
def edit_coupons(request, template_name):
    """
    编辑优惠券
    url :{% url 'edit_coupons' %}？id={{ id }}
    :请求方式: Get
    :请求参数：id(优惠券id)
    :返回数据：scenes 场景列表 citygroups 城市分组列表，cities 所有城市(列表)
    :[[id,name],[id,name],....]

    :请求方式：Post
    :请求参数：数据库字段(input name)
    """
    id = request.GET.get("id")
    oCmsCoupon = CmsCoupon.objects.get(id=id)
    if request.method == "POST":
        form = CouponsForm(request.POST, instance=oCmsCoupon)
        form.data['start'] = make_timestamp(form.data['start'])
        form.data['end'] = make_timestamp(form.data['end'])
        if form.is_valid():
            form.save()
            if CMS_CHECK_ON:
                CmsCheck(module=CmsModule.MAIN_COUPON,
                         table_name='CmsCoupon',
                         data_id=id,
                         op_type=CheckOpType.EDIT,
                         alter_person=request.user.username,
                         alter_date=time.strftime("%Y-%m-%d %X", time.localtime())).save()
            return HttpResponseRedirect(reverse("coupons"))
    else:
        form = CouponsForm(instance=oCmsCoupon)
    errors, fields = format_form(form)
    if 'start' in fields.keys():
        fields['start'] = json.dumps(timestamp2str(fields['start']))
    if 'end' in fields.keys():
        fields['end'] = json.dumps(timestamp2str(fields['end']))
    scenes = get_scenes()
    citygroups = get_city_group()
    cities = get_city_list()
    return render_to_response(template_name, {
        "scenes": scenes,
        "citygroups": citygroups,
        "cities": cities,
        "errors": errors,
        "fields": fields,
        "id": id
    }, context_instance=RequestContext(request))


# 删除优惠券
@login_required
@permission_required(u'%s.%s' % (AuthCodeName.APP_LABEL, AuthCodeName.CONFIG), raise_exception=True)
def delete_coupons(request):
    id = request.POST.get('id')
    coupon = CmsCoupon.objects.get(id=id)
    if CMS_CHECK_ON:
        check = CmsCheck(
            module=CmsModule.MAIN_COUPON,
            table_name="CmsCoupon",
            data_id=id,
            op_type=CheckOpType.DELETE,
            status=CheckStatu.WAIT_SUBMIT,
            is_show=1,
            alter_person=request.user.username,
            alter_date=time.strftime("%Y-%m-%d %X", time.localtime()))
        check.save()
    coupon.delete()
    return HttpResponse(0)
