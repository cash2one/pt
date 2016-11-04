#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'putao'
__mtime__ = '1/8/2016'
"""

# from config.views.config_pub import *
from config.forms import CmsActivityV37Form
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
import json
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

from common.const import get_nav_text
from common.views import filter_none
from config.views.config_pub import get_goods, get_all_coupon_activities, get_all_cps
from main.models import CmsChannels, get_valid_time, get_city_str, \
    getCVT, CmsGoods, CmsActivityGoods, CmsActivityCP, CmsCP, CmsViewActivity37, CmsActivityV37
from main.views.main_pub import add_main_var, get_city_list, get_city_group, format_form, \
    get_actions_select


@login_required
@add_main_var
def coupon_activities(request, template_name):
    t = request.GET.get("t")
    if not t:
        t = "1"
    v = request.GET.get("v")
    c = request.GET.get("c")
    coupon_activities = get_all_coupon_activities()
    channel = CmsChannels.objects.get(channel_no=c, app_version__app_version=v, app_version__type_id=t).id
    return render_to_response(template_name, {
        "text": get_nav_text(t),
        "t": t,
        "v": v,
        "c": c,
        "coupon_activities": coupon_activities,
        "channel": channel
    }, context_instance=RequestContext(request))


@login_required
def search(request):
    channel = request.GET.get("channel")
    activities = CmsActivityV37.objects.filter(cmsviewactivity37__channel__id=channel)
    result = []
    for activity in activities:
        goods = [o.title for o in activity.goods.all()]
        cps = [o.name for o in activity.cp.all()]
        status_str, status_int = "", 1
        item = [
            activity.name,
            activity.img,
            "<br/>".join(cps),
            "<br/>".join(goods),
            get_valid_time(activity.valid_time),
            get_city_str(activity.city),
            status_str,
            status_int,
            activity.id
        ]
        result.append(item)
    filter_none(result)
    return HttpResponse(json.dumps(result))


@login_required
@add_main_var
def new(request, template_name):
    channel_id = request.GET.get('channel')
    c, v, t = getCVT(channel_id)
    # 根据类型得到名称
    text = get_nav_text(str(t))
    if request.method == "POST":
        form = CmsActivityV37Form(request.POST)
        if form.is_valid():
            ins_activityv37 = form.save()
            goods_lst = request.POST.get("goods_lst").split(",")
            if goods_lst == ["*"]:
                goods = CmsGoods.objects.filter(parent_id=-1)
            else:
                goods = CmsGoods.objects.filter(id__in=goods_lst)
            # add by mkh
            CmsActivityGoods.objects.filter(activity=ins_activityv37).delete()
            for good in goods:
                acitvitygoods_ins, status = CmsActivityGoods.objects.get_or_create(activity=ins_activityv37, goods=good)
                acitvitygoods_ins.save()
            cp_lst = request.POST.get("cp_lst").split(",")
            if cp_lst == ['*']:
                cps = CmsCP.objects.all()
            else:
                cps = CmsCP.objects.filter(id__in=cp_lst)
            # add by mkh
            CmsActivityCP.objects.filter(activity=ins_activityv37).delete()
            for cp in cps:
                activitycp_ins, status = CmsActivityCP.objects.get_or_create(activity=ins_activityv37, cp=cp)
                activitycp_ins.save()
            CmsViewActivity37(channel_id=channel_id, activity=ins_activityv37).save()
            return HttpResponseRedirect(reverse('coupon_activities') + "?t=%d&c=%s&v=%s" % (t, c, v))
    else:
        form = CmsActivityV37Form()
    errors, fields = format_form(form)
    cps = get_all_cps()
    goods = get_goods()
    actions = get_actions_select()
    citygroups = get_city_group()
    cities = get_city_list()
    return render_to_response(template_name, {
        "t": t,
        "v": v,
        "c": c,
        "id": id,
        "text": text,
        "channel": channel_id,
        "errors": errors,
        "fields": fields,
        "cps": cps,
        "goods": goods,
        "actions": actions,
        "citygroups": citygroups,
        "cities": cities
    }, context_instance=RequestContext(request))


@login_required
@add_main_var
def edit(request, template_name):
    id = request.GET.get("id")
    channel_id = request.GET.get('channel')
    c, v, t = getCVT(channel_id)
    # 根据类型得到名称
    text = get_nav_text(str(t))
    ins_activityv37 = CmsActivityV37.objects.get(id=id)
    if request.method == "POST":
        form = CmsActivityV37Form(request.POST, instance=ins_activityv37)
        if form.is_valid():
            ins_activityv37 = form.save()
            goods_lst = request.POST.get("goods_lst").split(",")
            if goods_lst == ["*"]:
                goods = CmsGoods.objects.filter(parent_id=-1)
            else:
                goods = CmsGoods.objects.filter(id__in=goods_lst)
            # add by mkh
            CmsActivityGoods.objects.filter(activity=ins_activityv37).delete()
            for good in goods:
                acitvitygoods_ins, status = CmsActivityGoods.objects.get_or_create(activity=ins_activityv37, goods=good)
                acitvitygoods_ins.save()
            cp_lst = request.POST.get("cp_lst").split(",")
            if cp_lst == ['*']:
                cps = CmsCP.objects.all()
            else:
                cps = CmsCP.objects.filter(id__in=cp_lst)
            # add by mkh
            CmsActivityCP.objects.filter(activity=ins_activityv37).delete()
            for cp in cps:
                activitycp_ins, status = CmsActivityCP.objects.get_or_create(activity=ins_activityv37, cp=cp)
                activitycp_ins.save()
            return HttpResponseRedirect(reverse('coupon_activities') + "?t=%d&c=%s&v=%s" % (t, c, v))
    else:
        form = CmsActivityV37Form(instance=ins_activityv37)
    errors, fields = format_form(form)
    goods_lst = []
    lst_good = ins_activityv37.goods.all()
    for good in lst_good:
        goods_lst.append(str(good.id))
    goods_lst = ",".join(goods_lst)
    cp_lst = []
    lst_cp = ins_activityv37.cp.all()
    for cp in lst_cp:
        cp_lst.append(str(cp.id))
    cp_lst = ",".join(cp_lst)
    fields['goods_lst'] = json.dumps(goods_lst)
    fields['cp_lst'] = json.dumps(cp_lst)
    cps = get_all_cps()
    goods = get_goods()
    actions = get_actions_select()
    citygroups = get_city_group()
    cities = get_city_list()
    return render_to_response(template_name, {
        "t": t,
        "v": v,
        "c": c,
        "id": id,
        "text": text,
        "channel": channel_id,
        "errors": errors,
        "fields": fields,
        "cps": cps,
        "goods": goods,
        "actions": actions,
        "citygroups": citygroups,
        "cities": cities
    }, context_instance=RequestContext(request))


@login_required
def delete(request):
    id = request.POST.get('id')
    CmsActivityV37.objects.get(id=id).delete()
    return HttpResponse(0)
