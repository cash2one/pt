#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'putao'
__mtime__ = '2015/9/14'
"""
from common.const import AuthCodeName, ad_size, ad_type
# from config.views.config_pub import *
# from config.forms import *
import time
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required, permission_required
import json
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

from common.const import AuthCodeName, get_nav_text, get_2array_value, open_type, CmsModule, CheckOpType, CONFIG_ITEMS, \
    CheckStatu
from common.views import get_check_status_str, filter_none, make_timestamp, timestamp2str
from config.forms import CmsAdsForm, CmsAdbeansForm
from config.views.config_pub import CMS_CHECK_ON, CmsCheck, new_associate
from main.models import CmsChannels, get_scene_name, get_valid_time, get_city_str, \
    getCVT, CmsAds, CmsAdbeans, CmsViewAd, CmsAdsBeans
from main.views.main_pub import add_main_var, get_scenes, get_city_list, get_city_group, format_form, get_actions_select


@login_required
@add_main_var
def ads(request, template_name):
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


@login_required
def search_ads(request):
    channel = request.GET.get("channel")
    ads = CmsAds.objects.filter(cmsviewad__channel__id=channel)
    result = []
    for ad in ads:
        status_str, status_int = get_check_status_str("CmsAds", ad.id)
        item = {"ad": [
            get_scene_name(ad.scene_id),
            ad.location,
            get_2array_value(ad_size, ad.size),
            get_2array_value(ad_type, ad.type),
            status_str,
            status_int,
            ad.id
        ], "beans": []}
        beans = CmsAdbeans.objects.filter(cmsadsbeans__ad=ad)
        for bean in beans:
            status_str, status_int = get_check_status_str("CmsAdbeans", bean.id)
            item["beans"].append([
                bean.img_url,
                bean.name,
                bean.location,
                bean.action_id,
                get_valid_time(bean.valid_time),
                get_city_str(bean.city),
                bean.phone_type,
                status_str,
                status_int,
                bean.id
            ])
        result.append(item)
    filter_none(result)
    return HttpResponse(json.dumps(result))


# 删除广告要删除四张表
@login_required
@permission_required(u'%s.%s' % (AuthCodeName.APP_LABEL, AuthCodeName.CONFIG), raise_exception=True)
def delete_ad(request):
    channel_id = request.POST.get("channel")
    ad = request.POST.get("ad")
    views = CmsViewAd.objects.filter(ad_id=ad)
    if CMS_CHECK_ON:
        for view in views:
            check = CmsCheck(
                channel_id=channel_id,
                module=CmsModule.CONFIG_AD,
                table_name="CmsViewAd",
                data_id=view.id,
                op_type=CheckOpType.DELETE,
                status=CheckStatu.WAIT_SUBMIT,
                is_show=0,
                alter_person=request.user.username,
                alter_date=time.strftime("%Y-%m-%d %X", time.localtime()))
            check.save()
    views.delete()
    adsbeans = CmsAdsBeans.objects.filter(ad_id=ad)
    for adsbean in adsbeans:
        if CMS_CHECK_ON:
            check = CmsCheck(
                channel_id=channel_id,
                module=CmsModule.CONFIG_AD,
                table_name="CmsAdsBeans",
                data_id=adsbean.id,
                op_type=CheckOpType.DELETE,
                status=CheckStatu.WAIT_SUBMIT,
                is_show=0,
                alter_person=request.user.username,
                alter_date=time.strftime("%Y-%m-%d %X", time.localtime()))
            check.save()
            check = CmsCheck(
                channel_id=channel_id,
                module=CmsModule.CONFIG_AD,
                table_name="CmsAdbeans",
                data_id=adsbean.bean_id,
                op_type=CheckOpType.DELETE,
                status=CheckStatu.WAIT_SUBMIT,
                is_show=0,
                alter_person=request.user.username,
                alter_date=time.strftime("%Y-%m-%d %X", time.localtime()))
            check.save()
        adsbean.bean.delete()
    adsbeans.delete()
    if CMS_CHECK_ON:
        check = CmsCheck(
            channel_id=channel_id,
            module=CmsModule.CONFIG_AD,
            table_name="CmsAds",
            data_id=ad,
            op_type=CheckOpType.DELETE,
            status=CheckStatu.WAIT_SUBMIT,
            is_show=1,
            alter_person=request.user.username,
            alter_date=time.strftime("%Y-%m-%d %X", time.localtime()))
        check.save()
    CmsAds.objects.get(id=ad).delete()
    return HttpResponse(0)


@login_required
@permission_required(u'%s.%s' % (AuthCodeName.APP_LABEL, AuthCodeName.CONFIG), raise_exception=True)
def delete_bean(request):
    bean = request.POST.get("bean")
    channel_id = request.POST.get("channel")
    oCmsAdsBeans = CmsAdsBeans.objects.get(bean_id=bean)
    if CMS_CHECK_ON:
        check = CmsCheck(
            channel_id=channel_id,
            module=CmsModule.CONFIG_AD,
            table_name="CmsAdsBeans",
            data_id=oCmsAdsBeans.id,
            op_type=CheckOpType.DELETE,
            status=CheckStatu.WAIT_SUBMIT,
            is_show=0,
            alter_person=request.user.username,
            alter_date=time.strftime("%Y-%m-%d %X", time.localtime()))
        check.save()
    oCmsAdsBeans.delete()
    CmsAdbeans.objects.get(id=bean).delete()
    if CMS_CHECK_ON:
        check = CmsCheck(
            channel_id=channel_id,
            module=CmsModule.CONFIG_AD,
            table_name="CmsAdbeans",
            data_id=bean,
            op_type=CheckOpType.DELETE,
            status=CheckStatu.WAIT_SUBMIT,
            is_show=1,
            alter_person=request.user.username,
            alter_date=time.strftime("%Y-%m-%d %X", time.localtime()))
        check.save()
    return HttpResponse(0)


@login_required
@permission_required(u'%s.%s' % (AuthCodeName.APP_LABEL, AuthCodeName.CONFIG), raise_exception=True)
@add_main_var
def new_adgroup(request, template_name):
    """
    新建 广告分组
    插入广告组表和广告组和渠道关联表
    :请求方式:Get
    :请求参数：无
    :返回数据：form 表单 scenes 场景列表 ad_size：篇幅列表 ad_type: 类型 (list)
    :例如：scenes 场景列表 和之前一样， ad_size = [[2,"半栏"],[1,"通栏"]] ad_type = [[2,"单播"],[1,"轮播"]]

    :请求方式：Post
    :请求参数：排序：location 篇幅  size 类型：type 场景：scene_id
    :备注 :传数字
    """
    channel_id = request.GET.get('channel')
    c, v, t = getCVT(channel_id)
    # 根据类型得到名称
    text = get_nav_text(str(t))
    if request.method == 'POST':
        form = CmsAdsForm(request.POST)
        if form.is_valid():
            oCmsAds = form.save()
            if CMS_CHECK_ON:
                CmsCheck(channel_id=channel_id,
                         module=CmsModule.CONFIG_AD,
                         table_name='CmsAds',
                         data_id=oCmsAds.id,
                         op_type=CheckOpType.NEW,
                         alter_person=request.user.username,
                         alter_date=time.strftime("%Y-%m-%d %X", time.localtime())).save()
            oViewAd = CmsViewAd(ad=oCmsAds, channel=CmsChannels.objects.get(id=channel_id))
            oViewAd.save()
            if CMS_CHECK_ON:
                CmsCheck(channel_id=channel_id,
                         module=CmsModule.CONFIG_AD,
                         table_name='CmsViewAd',
                         data_id=oViewAd.id,
                         op_type=CheckOpType.NEW,
                         is_show=0,
                         alter_person=request.user.username,
                         alter_date=time.strftime("%Y-%m-%d %X", time.localtime())).save()
            new_associate(channel_id, oCmsAds.id, CONFIG_ITEMS.AD, request)
            return HttpResponseRedirect(reverse('ads') + "?t=%d&c=%s&v=%s" % (t, c, v))
    else:
        form = CmsAdsForm()
    scenes = get_scenes()
    errors, fields = format_form(form)
    return render_to_response(template_name, {
        "scenes": scenes,
        "ad_size": ad_size,
        "ad_type": ad_type,
        "fields": fields,
        "errors": errors,
        "t": t,
        "c": c,
        "v": v,
        "text": text,
        "channel": channel_id
    }, context_instance=RequestContext(request))


@login_required
@permission_required(u'%s.%s' % (AuthCodeName.APP_LABEL, AuthCodeName.CONFIG), raise_exception=True)
@add_main_var
def edit_adgroup(request, template_name):
    """
     编辑 广告分组
    :请求方式:Get
    :请求参数：id 广告组表id号 channel：渠道id
    :返回数据：form 表单 scenes 场景列表 ad_size：篇幅列表 ad_type: 类型 (list)
    :例如：scenes 场景列表 和之前一样， ad_size = [[2,"半栏"],[1,"通栏"]] ad_type = [[2,"单播"],[1,"轮播"]]

    :请求方式：Post
    :请求参数：排序：location 篇幅  size 类型：type 场景：scene_id
    :备注 :传数字
    """
    id = request.GET.get("id")
    channel_id = request.GET.get('channel')
    c, v, t = getCVT(channel_id)
    text = get_nav_text(str(t))
    if request.method == "POST":
        ads = CmsAds.objects.get(id=id)
        form = CmsAdsForm(request.POST, instance=ads)
        if form.is_valid():
            form.save()
            if CMS_CHECK_ON:
                CmsCheck(channel_id=channel_id,
                         module=CmsModule.CONFIG_AD,
                         table_name='CmsAds',
                         data_id=id,
                         op_type=CheckOpType.EDIT,
                         alter_person=request.user.username,
                         alter_date=time.strftime("%Y-%m-%d %X", time.localtime())).save()
            return HttpResponseRedirect(reverse('ads') + "?t=%d&c=%s&v=%s" % (t, c, v))
    else:
        ads = CmsAds.objects.get(id=id)
        form = CmsAdsForm(instance=ads)
    scenes = get_scenes()
    errors, fields = format_form(form)
    return render_to_response(template_name, {
        "id": id,
        "scenes": scenes,
        "ad_size": ad_size,
        "ad_type": ad_type,
        "fields": fields,
        "errors": errors,
        "t": t,
        "c": c,
        "v": v,
        "text": text,
        "channel": channel_id
    }, context_instance=RequestContext(request))


@login_required
@permission_required(u'%s.%s' % (AuthCodeName.APP_LABEL, AuthCodeName.CONFIG), raise_exception=True)
@add_main_var
def new_ads(request, template_name):
    """
    新建 广告
    #插入到广告表，插入广告和广告组关联表
    :请求方式:Get
    :请求参数：id:广告组id,channel：渠道id
    :返回数据：ad_id:广告组id form 表单 citygroups 城市分组 actions：动作列表 (services 服务列表 goods 商品列表) open_type:类别 cities:所有城市（格式和之前一致）
    :格式：[[id,name],....]

    :请求方式：Post
    :请求参数：ad_id,img_url,start,end,location,action_id,strategy(删除了)
    valid_time,city,open_cp_id,open_service_id,open_goods_id,open_type,action_json
    :
    """
    channel_id = request.GET.get('channel')
    c, v, t = getCVT(channel_id)
    text = get_nav_text(str(t))
    location_flag = True
    if request.method == 'POST':
        form = CmsAdbeansForm(request.POST)
        form.data['start'] = make_timestamp(form.data['start'])
        form.data['end'] = make_timestamp(form.data['end'])
        ad_id = request.POST.get('ad_id')

        if form.is_valid():
            if not CmsAdbeans.objects.filter(cmsadsbeans__ad_id=ad_id, location=request.POST.get('location')):
                oCmsAdbeans = form.save()
                if CMS_CHECK_ON:
                    CmsCheck(channel_id=channel_id,
                             module=CmsModule.CONFIG_AD,
                             table_name='CmsAdbeans',
                             data_id=oCmsAdbeans.id,
                             op_type=CheckOpType.NEW,
                             alter_person=request.user.username,
                             alter_date=time.strftime("%Y-%m-%d %X", time.localtime())).save()
                oCmsAdsBeans = CmsAdsBeans(ad=CmsAds.objects.get(id=ad_id), bean=oCmsAdbeans)
                oCmsAdsBeans.save()
                if CMS_CHECK_ON:
                    CmsCheck(channel_id=channel_id,
                             module=CmsModule.CONFIG_AD,
                             table_name='CmsAdsBeans',
                             data_id=oCmsAdsBeans.id,
                             op_type=CheckOpType.NEW,
                             is_show=0,
                             alter_person=request.user.username,
                             alter_date=time.strftime("%Y-%m-%d %X", time.localtime())).save()
                return HttpResponseRedirect(reverse('ads') + "?t=%d&c=%s&v=%s" % (t, c, v))
            else:
                location_flag = False

    else:
        form = CmsAdbeansForm()
    ad_id = request.GET.get('id')
    citygroups = get_city_group()
    actions = get_actions_select()
    cities = get_city_list()
    errors, fields = format_form(form)
    if not location_flag:
        errors['location'] = '广告排序:%s 已存在请填入其他的值' % request.POST.get('location')
    if 'start' in fields.keys():
        fields['start'] = json.dumps(timestamp2str(fields['start']))
    if 'end' in fields.keys():
        fields['end'] = json.dumps(timestamp2str(fields['end']))
    return render_to_response(template_name, {
        "fields": fields,
        "errors": errors,
        "citygroups": citygroups,
        "actions": actions,
        "cities": cities,
        "open_type": open_type,
        "ad_id": ad_id,
        "t": t,
        "c": c,
        "v": v,
        "text": text,
        "channel": channel_id
    }, context_instance=RequestContext(request))


@login_required
@permission_required(u'%s.%s' % (AuthCodeName.APP_LABEL, AuthCodeName.CONFIG), raise_exception=True)
@add_main_var
def edit_ads(request, template_name):
    """
    编辑 广告
    #
    :请求方式:Get
    :请求参数：id 广告id
    :返回数据：form 表单 citygroups 城市分组 actions：动作列表 (services 服务列表 goods 商品列表) open_type:类别 cities:所有城市（格式和之前一致）
    :格式：[[id,name],....]
    :备注：scenes 场景列表 和之前一样，ad_size = [["半栏",2],["通栏",1]]  ad_type = [["轮播",1],["单播",2]]

    :请求方式：Post
    :请求参数：id,img_url,start,end,location,action_id,strategy(删除了)
    valid_time,city,open_cp_id,open_service_id,open_goods_id,open_type,action_json
    :
    """
    id = request.GET.get("id")
    channel_id = request.GET.get('channel')
    c, v, t = getCVT(channel_id)
    text = get_nav_text(str(t))
    if request.method == 'POST':
        cmsadbeans = CmsAdbeans.objects.get(id=id)
        form = CmsAdbeansForm(request.POST, instance=cmsadbeans)
        form.data['start'] = make_timestamp(form.data['start'])
        form.data['end'] = make_timestamp(form.data['end'])
        if form.is_valid():
            form.save()
            if CMS_CHECK_ON:
                CmsCheck(channel_id=channel_id,
                         module=CmsModule.CONFIG_AD,
                         table_name='CmsAdbeans',
                         data_id=id,
                         op_type=CheckOpType.EDIT,
                         alter_person=request.user.username,
                         alter_date=time.strftime("%Y-%m-%d %X", time.localtime())).save()
            return HttpResponseRedirect(reverse('ads') + "?t=%d&c=%s&v=%s" % (t, c, v))
    else:
        cmsadbeans = CmsAdbeans.objects.get(id=id)
        form = CmsAdbeansForm(instance=cmsadbeans)
    citygroups = get_city_group()
    actions = get_actions_select()
    cities = get_city_list()
    errors, fields = format_form(form)
    if 'start' in fields.keys():
        fields['start'] = json.dumps(timestamp2str(fields['start']))
    if 'end' in fields.keys():
        fields['end'] = json.dumps(timestamp2str(fields['end']))
    return render_to_response(template_name, {
        "fields": fields,
        "errors": errors,
        "citygroups": citygroups,
        "actions": actions,
        "cities": cities,
        "open_type": open_type,
        "id": id,
        "t": t,
        "c": c,
        "v": v,
        "text": text,
        "channel": channel_id
    }, context_instance=RequestContext(request))
