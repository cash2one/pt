#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'putao'
__mtime__ = '3/28/2016'
"""

# from config.views.config_pub import *
from django.db.models import Q

from common.views import make_timestamp_h, timestamp2str_h, make_timestamp, timestamp2str
from config.views.config_pub import new_associate
from main.models import ViewCmsSecKillView, CmsChannels, getCVT, CmsSecKill
from main.models import CmsActions
from main.models import OpGoodsActivityView
from main.models import CmsSecKillView
from config.forms import CmsSeckilForm
import logging
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required, permission_required
import json
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

from common.const import AuthCodeName, get_nav_text, CONFIG_ITEMS, product_types

from main.views.main_pub import add_main_var, get_city_list, get_city_group, format_form, \
    get_actions_select

log = logging.getLogger('config.app')


@login_required
@add_main_var
def seckills(request, template_name):
    t = request.GET.get("t")
    if not t:
        t = "1"
    v = request.GET.get("v")
    c = request.GET.get("c")
    channel = CmsChannels.objects.get(channel_no=c, app_version__app_version=v, app_version__type_id=t).id
    print("channel_id is:[" + str(channel) + "]")
    return render_to_response(template_name, {
        "text": get_nav_text(t),
        "t": t,
        "v": v,
        "c": c,
        "channel": channel
    }, context_instance=RequestContext(request))


def search(request):
    channel = request.GET.get("channel")
    list = ViewCmsSecKillView.objects.filter(channel_id=channel)
    result_list = []
    if list is not None:
        for item in list:
            res = {}
            res['image_bcg'] = item.image_bcg
            res['title'] = item.title
            res['desc'] = item.desc
            res['price_desc'] = item.price_desc
            res['price_sub_desc'] = item.price_sub_desc
            res['image_mark'] = item.image_mark
            if item.show_start_time and item.show_end_time:
                res['time'] = "展示开始时间：" + str(item.show_start_time) + "<br/>展示结束时间：" + str(item.show_end_time)
            else:
                res['time'] = '未定义'
            res['city'] = item.city
            res['id'] = item.seckill_id
            result_list.append(res)
    return HttpResponse(json.dumps(result_list))


@add_main_var
def new(request, template_name):
    log.error("in SECKILL")
    channel_id = request.GET.get('channel')
    list = ViewCmsSecKillView.objects.filter(channel_id=channel_id)
    c, v, t = getCVT(channel_id)
    log.error(str(c) + ":" + str(v) + ":" + str(t))
    # 根据类型得到名称
    text = get_nav_text(str(t))
    is_ok_time = True
    if request.method == "POST":
        log.error(request.POST)
        form = CmsSeckilForm(request.POST)
        if form.data['show_start_time']:
            form.data['show_start_time'] = timestamp2str_h(make_timestamp(form.data['show_start_time']))
        if form.data['show_end_time']:
            form.data['show_end_time'] = timestamp2str_h(make_timestamp(form.data['show_end_time']))
        log.error(form.data)
        if form.is_valid():
            if check_time(list, 0, make_timestamp_h(form.data['show_start_time']),
                          make_timestamp_h(form.data['show_end_time'])):
                seckill = form.save()
                new_associate(channel_id, seckill.id, CONFIG_ITEMS.SECKILLS, request)
                CmsSecKillView(channel_id=channel_id, seckill_id=seckill.id, status=0).save()
                return HttpResponseRedirect(reverse('seckills') + "?t=%d&c=%s&v=%s" % (t, c, v))
            else:
                is_ok_time = False
    else:
        form = CmsSeckilForm()
    # 准备Action数据
    actionsall = CmsActions.objects.all()
    # 准备秒杀字段
    opGoodsActivitys = OpGoodsActivityView.objects.filter(is_seckill=1)
    map = {}
    if opGoodsActivitys is not None:
        for oga in opGoodsActivitys:
            map[oga.activityId] = oga
    op_goods_list = []
    for k, vl in map.items():
        op_goods_list.append(vl)
    errors, fields = format_form(form)
    if not is_ok_time:
        errors['time'] = '起始时间与结束时间不能与同渠道其他秒杀活动重合'
    citygroups = get_city_group()
    # cities = get_city_list()
    actions = get_actions_select()
    return render_to_response(template_name, {
        "t": t,
        "v": v,
        "c": c,
        "id": id,
        "text": text,
        "channel": channel_id,
        "errors": errors,
        "fields": fields,
        "citygroups": citygroups,
        "op_goods_list": op_goods_list,
        "actions": actions,
        "actionsall": actionsall
    }, context_instance=RequestContext(request))


@login_required
@permission_required(u'%s.%s' % (AuthCodeName.APP_LABEL, AuthCodeName.CONFIG), raise_exception=True)
@add_main_var
def edit(request, template_name):
    id = request.GET.get("id")
    channel_id = request.GET.get('channel')
    c, v, t = getCVT(channel_id)
    list = ViewCmsSecKillView.objects.filter(channel_id=channel_id)
    # 根据类型得到名称
    text = get_nav_text(str(t))
    seckill = CmsSecKill.objects.get(id=id)
    log.error(str(seckill.id) + "----" + seckill.title)
    is_ok_time = True
    if request.method == "POST":
        form = CmsSeckilForm(request.POST, instance=seckill)
        if form.data['show_start_time']:
            form.data['show_start_time'] = timestamp2str_h(make_timestamp(form.data['show_start_time']))
        if form.data['show_end_time']:
            form.data['show_end_time'] = timestamp2str_h(make_timestamp(form.data['show_end_time']))
        if form.is_valid():
            if check_time(list, id, make_timestamp_h(form.data['show_start_time']),
                          make_timestamp_h(form.data['show_end_time'])):
                form.save()
                return HttpResponseRedirect(reverse('seckills') + "?t=%d&c=%s&v=%s" % (t, c, v))
            else:
                is_ok_time = False
    else:
        form = CmsSeckilForm(instance=seckill)
        if form.initial['show_start_time']:
            form.initial['show_start_time'] = str(form.initial['show_start_time'])
        if form.initial['show_end_time']:
            form.initial['show_end_time'] = str(form.initial['show_end_time'])
    log.error(form.initial)
    errors, fields = format_form(form)
    if not is_ok_time:
        errors['time'] = '起始时间与结束时间不能与同渠道其他秒杀活动重合'
    if 'show_start_time' in fields.keys() and fields['show_start_time'] != '""':
        fields['show_start_time'] = json.dumps(
            timestamp2str(make_timestamp_h(str(fields['show_start_time']).replace("\"", ""))))
    if 'show_end_time' in fields.keys() and fields['show_end_time'] != '""':
        fields['show_end_time'] = json.dumps(
            timestamp2str(make_timestamp_h(str(fields['show_end_time']).replace("\"", ""))))
    citygroups = get_city_group()
    cities = get_city_list()
    actions = get_actions_select()
    actionsall = CmsActions.objects.all()
    # 准备秒杀字段
    opGoodsActivitys = OpGoodsActivityView.objects.filter(is_seckill=1)
    op = OpGoodsActivityView.objects.filter(Q(activityId=seckill.activity_id) & Q(is_seckill=1)).first()
    map = {}
    if opGoodsActivitys is not None:
        for oga in opGoodsActivitys:
            map[oga.activityId] = oga
    op_goods_list = []
    for k, vl in map.items():
        op_goods_list.append(vl)
    current_city = seckill.city
    if current_city == '*':
        current_city = '不限(全国)'
    return render_to_response(template_name, {
        "t": t,
        "v": v,
        "c": c,
        "id": id,
        "text": text,
        "channel": channel_id,
        "errors": errors,
        "fields": fields,
        "citygroups": citygroups,
        "cities": cities,
        "product_types": product_types,
        "actions": actions,
        "op_goods_list": op_goods_list,
        "actionsall": actionsall,
        "activity_id": seckill.activity_id,
        "origin_city": op.activityCity,
        "current_city": current_city,
    }, context_instance=RequestContext(request))


def check_time(list, id, start_time, end_time):
    if list is not None:
        for sk in list:
            if not (str(sk.seckill_id) == str(id)):
                if start_time <= make_timestamp_h(
                        str(sk.show_end_time).replace("\"", "")) and start_time >= make_timestamp_h(
                    str(sk.show_start_time).replace("\"", "")):
                    return False
        return True
    else:
        return True


@login_required
@permission_required(u'%s.%s' % (AuthCodeName.APP_LABEL, AuthCodeName.CONFIG), raise_exception=True)
def delelte(request):
    id = request.POST.get('id')
    CmsSecKill.objects.get(id=id).delete()
    list = CmsSecKillView.objects.filter(seckill_id=id)
    if list is not None:
        for l in list:
            l.delete()
    return HttpResponse(0)
