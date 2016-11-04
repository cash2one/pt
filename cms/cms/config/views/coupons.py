#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = '配置库优惠券'
__author__ = 'rongfudi'
__mtime__ = '2015/10/8'
"""
from common.const import AuthCodeName
# from config.views.config_pub import *
# from config.forms import *
from main.forms import CouponsForm, CmsCoupon
import time
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required, permission_required
import json
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

from common.const import AuthCodeName, get_nav_text, CmsModule, CheckOpType, CONFIG_ITEMS, \
    CheckStatu
from common.views import get_check_status_str, filter_none, CheckManager, make_timestamp, timestamp2str
from config.views.config_pub import CMS_CHECK_ON, CmsCheck, new_associate, exchange_obj, get_coupons
from main.models import CmsChannels, get_valid_time, get_city_str, \
    getCVT, get_scene_name, CmsViewCoupon
from main.views.main_pub import add_main_var, get_city_list, get_city_group, format_form, \
    get_scenes


@login_required
@add_main_var
def coupons(request, template_name):
    t = request.GET.get("t")
    if not t:
        t = "1"
    v = request.GET.get("v")
    c = request.GET.get("c")
    channel = CmsChannels.objects.get(channel_no=c, app_version__app_version=v, app_version__type_id=t).id
    coupons = get_coupons()
    return render_to_response(template_name, {
        "text": get_nav_text(t),
        "t": t,
        "v": v,
        "c": c,
        "channel": channel,
        "coupons": coupons
    }, context_instance=RequestContext(request))


@login_required
def search_coupons(request):
    channel_id = request.GET.get('channel')
    objs = CmsCoupon.objects.filter(cmsviewcoupon__channel_id=channel_id)
    result = []
    for obj in objs:
        scene_name = get_scene_name(obj.scene_id)
        status_str, status_int = get_check_status_str("CmsCoupon", obj.id)
        result.append([
            scene_name,
            obj.location,
            obj.name,
            obj.url,
            get_valid_time(obj.valid_time),
            get_city_str(obj.city),
            status_str,
            status_int,
            obj.id
        ])
    result.sort(key=lambda o: (o[0], o[1]))
    filter_none(result)
    return HttpResponse(json.dumps(result))


@login_required
@permission_required(u'%s.%s' % (AuthCodeName.APP_LABEL, AuthCodeName.CONFIG), raise_exception=True)
def exchange_coupons(request):
    id1 = request.POST.get("id1")
    id2 = request.POST.get("id2")
    channel_id = request.POST.get("channel")
    exchange_obj(CmsCoupon, id1, CmsCoupon, id2, channel_id, CmsModule.CONFIG_COUPON, request)
    return HttpResponse(0)


@login_required
@permission_required(u'%s.%s' % (AuthCodeName.APP_LABEL, AuthCodeName.CONFIG), raise_exception=True)
@add_main_var
def new_coupons(request):
    """
    配置库：新建优惠券
    :请求方式：ajax Post
    :请求URL：{% url 'new_config_coupons' %}
    :请求参数：coupons_id  channel_id
    :类型 :传数字
    返回： 成功：0 错误：错误信息
    """

    if request.method == 'POST':
        data = request.POST.copy()
        error = ""
        for key in data:
            if data[key] == "":
                error += key + " is null \n"
        if error:
            return HttpResponse(error)
        else:
            coupons_id = request.POST.get("coupons_id")
            channel_id = request.POST.get("channel_id")
            try:
                coupons = CmsCoupon.objects.get(id=coupons_id)
                coupons.parent_id = coupons_id
                coupons.id = None
                coupons.save()
                if CMS_CHECK_ON:
                    CmsCheck(channel_id=channel_id,
                             module=CmsModule.CONFIG_COUPON,
                             table_name='CmsCoupon',
                             data_id=coupons.id,
                             op_type=CheckOpType.NEW,
                             remark="增加名称为%s的优惠券" % (CheckManager.wrap_style(coupons.name),),
                             alter_person=request.user.username,
                             alter_date=time.strftime("%Y-%m-%d %X", time.localtime())).save()
                oCmsViewCoupon = CmsViewCoupon(coupon=coupons, channel=CmsChannels.objects.get(id=channel_id))
                oCmsViewCoupon.save()
                if CMS_CHECK_ON:
                    CmsCheck(channel_id=channel_id,
                             module=CmsModule.CONFIG_COUPON,
                             table_name='CmsViewCoupon',
                             data_id=oCmsViewCoupon.id,
                             op_type=CheckOpType.NEW,
                             is_show=0,
                             alter_person=request.user.username,
                             alter_date=time.strftime("%Y-%m-%d %X", time.localtime())).save()
                new_associate(channel_id, coupons.id, CONFIG_ITEMS.COUPONS, request)
            except Exception as ex:
                return HttpResponse(ex.args[0])
            return HttpResponse(0)


@login_required
@permission_required(u'%s.%s' % (AuthCodeName.APP_LABEL, AuthCodeName.CONFIG), raise_exception=True)
@add_main_var
def edit_coupons(request, template_name):
    """
    配置库：编辑优惠券
    url :{% url 'edit_config_coupons' %}？id={{ id }}&channel={{ channel }}
    :请求方式: Get
    :请求参数：id(优惠券id) channel渠道id
    :返回数据：scenes 场景列表 citygroups 城市分组列表，cities 所有城市(列表)
    :[[id,name],[id,name],....]

    :请求方式：Post
    :请求参数：数据库字段(input name)
    """
    id = request.GET.get("id")
    channel_id = request.GET.get('channel')
    c, v, t = getCVT(channel_id)
    # 根据类型得到名称
    text = get_nav_text(str(t))
    oCmsCoupon = CmsCoupon.objects.get(id=id)
    if request.method == "POST":
        form = CouponsForm(request.POST, instance=oCmsCoupon)
        form.data['start'] = make_timestamp(form.data['start'])
        form.data['end'] = make_timestamp(form.data['end'])
        if form.is_valid():
            form.save()
            if CMS_CHECK_ON:
                CmsCheck(channel_id=channel_id,
                         module=CmsModule.CONFIG_COUPON,
                         table_name='CmsCoupon',
                         data_id=id,
                         op_type=CheckOpType.EDIT,
                         alter_person=request.user.username,
                         alter_date=time.strftime("%Y-%m-%d %X", time.localtime())).save()
            return HttpResponseRedirect(reverse("config_coupons") + "?t=%d&c=%s&v=%s" % (t, c, v))
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
        "t": t,
        "c": c,
        "v": v,
        "text": text,
        "channel": channel_id,
        "id": id
    }, context_instance=RequestContext(request))


@login_required
@permission_required(u'%s.%s' % (AuthCodeName.APP_LABEL, AuthCodeName.CONFIG), raise_exception=True)
def delete_coupons(request):
    id = request.POST.get("id")
    channel_id = request.POST.get('channel')
    views = CmsViewCoupon.objects.filter(coupon_id=id)
    for view in views:
        if CMS_CHECK_ON:
            check = CmsCheck(
                channel_id=channel_id,
                module=CmsModule.CONFIG_COUPON,
                table_name="CmsViewCoupon",
                data_id=view.id,
                op_type=CheckOpType.DELETE,
                status=CheckStatu.WAIT_SUBMIT,
                is_show=0,
                alter_person=request.user.username,
                alter_date=time.strftime("%Y-%m-%d %X", time.localtime()))
            check.save()
        view.delete()
    CmsCoupon.objects.get(id=id).delete()
    if CMS_CHECK_ON:
        check = CmsCheck(
            channel_id=channel_id,
            module=CmsModule.CONFIG_COUPON,
            table_name="CmsCoupon",
            data_id=id,
            op_type=CheckOpType.DELETE,
            status=CheckStatu.WAIT_SUBMIT,
            is_show=1,
            alter_person=request.user.username,
            alter_date=time.strftime("%Y-%m-%d %X", time.localtime()))
        check.save()
    return HttpResponse(0)
