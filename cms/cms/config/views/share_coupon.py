#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'putao'
__mtime__ = '1/11/2016'
"""

# from config.views.config_pub import *
from common.views import filter_none, make_timestamp, timestamp2str
from config.forms import CmsShareCouponForm
from common.const import AuthCodeName, get_nav_text, product_types, get_2array_value
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required, permission_required
import json
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

from main.models import CmsChannels, CmsShareCoupon, timestamp2str_space, get_city_str, getCVT, CmsViewShareCoupon
from main.views.main_pub import add_main_var, get_city_list, get_city_group, format_form, get_actions_select


# 要支持按照城市筛选
@login_required
@add_main_var
def share_coupon(request, template_name):
    t = request.GET.get("t")
    if not t:
        t = "1"
    v = request.GET.get("v")
    c = request.GET.get("c")
    channel = CmsChannels.objects.get(channel_no=c, app_version__app_version=v, app_version__type_id=t).id
    return render_to_response(template_name, {
        "text": get_nav_text(t),
        "t": t,
        "v": v,
        "c": c,
        "channel": channel
    }, context_instance=RequestContext(request))


def search(request):
    channel = request.GET.get("channel")
    coupons = CmsShareCoupon.objects.filter(cmsviewsharecoupon__channel__id=channel)
    result = []
    for coupon in coupons:
        status_str, status_int = "", 1
        valid_time = []
        if coupon.start_time:
            valid_time.append("开始时间：" + timestamp2str_space(coupon.start_time))
        if coupon.end_time:
            valid_time.append("结束时间：" + timestamp2str_space(coupon.end_time))
        if valid_time:
            valid_time = "<br/>".join(valid_time)
        else:
            valid_time = "不限"
        item = [
            get_2array_value(product_types, coupon.product_type),
            "无限制" if coupon.times_limit == -1 else coupon.times_limit,
            valid_time,
            get_city_str(coupon.city),
            status_str,
            status_int,
            coupon.id
        ]
        result.append(item)
    filter_none(result)
    return HttpResponse(json.dumps(result))


@login_required
@permission_required(u'%s.%s' % (AuthCodeName.APP_LABEL, AuthCodeName.CONFIG), raise_exception=True)
@add_main_var
def new(request, template_name):
    channel_id = request.GET.get('channel')
    c, v, t = getCVT(channel_id)
    # 根据类型得到名称
    text = get_nav_text(str(t))
    if request.method == "POST":
        form = CmsShareCouponForm(request.POST)
        if form.data['start_time']:
            form.data['start_time'] = make_timestamp(form.data['start_time'])
        if form.data['end_time']:
            form.data['end_time'] = make_timestamp(form.data['end_time'])
        if form.is_valid():
            share_coupon = form.save()
            CmsViewShareCoupon(channel_id=channel_id, share_coupon=share_coupon).save()
            return HttpResponseRedirect(reverse('share_coupon') + "?t=%d&c=%s&v=%s" % (t, c, v))
    else:
        form = CmsShareCouponForm()
    errors, fields = format_form(form)
    citygroups = get_city_group()
    cities = get_city_list()
    actions = get_actions_select()
    return render_to_response(template_name, {
        "t": t,
        "v": v,
        "c": c,
        "id": id,
        "text": text,
        "channel": channel_id,
        "errors": json.dumps(errors),
        "fields": fields,
        "citygroups": citygroups,
        "cities": cities,
        "product_types": product_types,
        "actions": actions,
    }, context_instance=RequestContext(request))


@login_required
@permission_required(u'%s.%s' % (AuthCodeName.APP_LABEL, AuthCodeName.CONFIG), raise_exception=True)
@add_main_var
def edit(request, template_name):
    id = request.GET.get("id")
    channel_id = request.GET.get('channel')
    c, v, t = getCVT(channel_id)
    # 根据类型得到名称
    text = get_nav_text(str(t))
    coupon = CmsShareCoupon.objects.get(id=id)
    if request.method == "POST":
        form = CmsShareCouponForm(request.POST, instance=coupon)
        if form.data['start_time']:
            form.data['start_time'] = make_timestamp(form.data['start_time'])
        if form.data['end_time']:
            form.data['end_time'] = make_timestamp(form.data['end_time'])
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('share_coupon') + "?t=%d&c=%s&v=%s" % (t, c, v))
    else:
        form = CmsShareCouponForm(instance=coupon)
    errors, fields = format_form(form)
    citygroups = get_city_group()
    cities = get_city_list()
    actions = get_actions_select()
    if 'start_time' in fields.keys() and fields['start_time'] != '""':
        fields['start_time'] = json.dumps(timestamp2str(fields['start_time']))
    if 'end_time' in fields.keys() and fields['end_time'] != '""':
        fields['end_time'] = json.dumps(timestamp2str(fields['end_time']))
    return render_to_response(template_name, {
        "t": t,
        "v": v,
        "c": c,
        "id": id,
        "text": text,
        "channel": channel_id,
        "errors": json.dumps(errors),
        "fields": fields,
        "citygroups": citygroups,
        "cities": cities,
        "product_types": product_types,
        "actions": actions
    }, context_instance=RequestContext(request))


@login_required
@permission_required(u'%s.%s' % (AuthCodeName.APP_LABEL, AuthCodeName.CONFIG), raise_exception=True)
def delelte(request):
    id = request.POST.get('id')
    CmsShareCoupon.objects.get(id=id).delete()
    return HttpResponse(0)
