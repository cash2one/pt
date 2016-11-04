#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = '活动'
__author__ = 'rfd'
__mtime__ = '2015/10/8'
"""
import time
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required, permission_required
import json
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

from common.const import AuthCodeName, get_nav_text, get_2array_value, open_type, CmsModule, CheckOpType, CONFIG_ITEMS, \
    CheckStatu
# from config.views.config_pub import *
# from config.forms import *
from common.views import get_check_status_str, filter_none, make_timestamp, timestamp2str
from config.forms import ActivitiesForm
from config.views.config_pub import exchange_obj, CMS_CHECK_ON, CmsCheck, new_associate
from main.models import CmsChannels, CmsActivities, get_scene_name, get_valid_time, get_city_str, CmsViewActivity, \
    getCVT
from main.views.main_pub import add_main_var, get_scenes, get_city_list, get_city_group, format_form


@login_required
@add_main_var
def activities(request, template_name):
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
def search_activities(request):
    channel_id = request.GET.get('channel')
    objs = CmsActivities.objects.filter(cmsviewactivity__channel_id=channel_id)
    result = []
    for obj in objs:
        status_str, status_int = get_check_status_str("CmsActivities", obj.id)
        result.append([
            get_scene_name(obj.scene_id),
            obj.location,
            obj.url,
            get_2array_value(open_type, obj.open_type),
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
def exchange_activities(request):
    id1 = request.POST.get("id1")
    id2 = request.POST.get("id2")
    channel_id = request.POST.get("channel")
    exchange_obj(CmsActivities, id1, CmsActivities, id2, channel_id, CmsModule.CONFIG_ACTIVITY, request)
    return HttpResponse(0)


@login_required
@permission_required(u'%s.%s' % (AuthCodeName.APP_LABEL, AuthCodeName.CONFIG), raise_exception=True)
@add_main_var
def new_activity(request, template_name):
    """
    配置库 新建活动
    url :{% url 'new_activity' %}?channel={{ channel }}
    :请求方式: Get
    :请求参数：channel
    :返回数据：fields errors scenes 场景列表 open_type(类别) citygroups cities
    :例如：scenes 场景列表 和之前一样

    :请求方式：Post
    :请求参数：
    """
    channel_id = request.GET.get('channel')
    c, v, t = getCVT(channel_id)
    channel = CmsChannels.objects.get(id=channel_id)
    # 根据类型得到名称
    text = get_nav_text(str(t))
    if request.method == 'POST':
        form = ActivitiesForm(request.POST)
        form.data['start'] = make_timestamp(form.data['start'])
        form.data['end'] = make_timestamp(form.data['end'])
        if form.is_valid():
            activity = form.save()
            if CMS_CHECK_ON:
                CmsCheck(channel_id=channel_id,
                         module=CmsModule.CONFIG_ACTIVITY,
                         table_name='CmsActivities',
                         data_id=activity.id,
                         op_type=CheckOpType.NEW,
                         alter_person=request.user.username,
                         alter_date=time.strftime("%Y-%m-%d %X", time.localtime())).save()
            viewactivity = CmsViewActivity(activity=activity, channel=channel)
            viewactivity.save()
            if CMS_CHECK_ON:
                CmsCheck(channel_id=channel_id,
                         module=CmsModule.CONFIG_ACTIVITY,
                         table_name='CmsViewActivity',
                         data_id=viewactivity.id,
                         op_type=CheckOpType.NEW,
                         is_show=0,
                         alter_person=request.user.username,
                         alter_date=time.strftime("%Y-%m-%d %X", time.localtime())).save()
            new_associate(channel_id, activity.id, CONFIG_ITEMS.ACTIVITY, request)
            return HttpResponseRedirect(reverse("activities") + "?t=%d&c=%s&v=%s" % (t, c, v))
    else:
        form = ActivitiesForm()
    scenes = get_scenes()
    cities = get_city_list()
    citygroups = get_city_group()
    errors, fields = format_form(form)
    if 'start' in fields.keys():
        fields['start'] = json.dumps(timestamp2str(fields['start']))
    if 'end' in fields.keys():
        fields['end'] = json.dumps(timestamp2str(fields['end']))
    return render_to_response(template_name, {
        "scenes": scenes,
        "fields": fields,
        "errors": errors,
        "cities": cities,
        "citygroups": citygroups,
        "open_type": open_type,
        "t": t,
        "c": c,
        "v": v,
        "text": text,
        "channel": channel_id
    }, context_instance=RequestContext(request))


@login_required
@permission_required(u'%s.%s' % (AuthCodeName.APP_LABEL, AuthCodeName.CONFIG), raise_exception=True)
@add_main_var
def edit_activity(request, template_name):
    """
    配置库 编辑活动
    url :{% url 'edit_activity' %}?channel={{ channel }}&id={{ id }}
    :请求方式: Get
    :请求参数：channel,id
    :返回数据：fields errors scenes 场景列表 open_type(类别) citygroups cities
    :例如：scenes 场景列表 和之前一样

    :请求方式：Post
    :请求参数：
    """
    channel_id = request.GET.get('channel')
    id = request.GET.get("id")
    activity = CmsActivities.objects.get(id=id)
    c, v, t = getCVT(channel_id)
    # 根据类型得到名称
    text = get_nav_text(str(t))
    if request.method == 'POST':
        form = ActivitiesForm(request.POST, instance=activity)
        form.data['start'] = make_timestamp(form.data['start'])
        form.data['end'] = make_timestamp(form.data['end'])
        if form.is_valid():
            form.save()
            if CMS_CHECK_ON:
                CmsCheck(channel_id=channel_id,
                         module=CmsModule.CONFIG_ACTIVITY,
                         table_name='CmsActivities',
                         data_id=id,
                         op_type=CheckOpType.EDIT,
                         alter_person=request.user.username,
                         alter_date=time.strftime("%Y-%m-%d %X", time.localtime())).save()
            return HttpResponseRedirect(reverse("activities") + "?t=%d&c=%s&v=%s" % (t, c, v))
    else:
        form = ActivitiesForm(instance=activity)
    scenes = get_scenes()
    cities = get_city_list()
    citygroups = get_city_group()
    errors, fields = format_form(form)
    if 'start' in fields.keys():
        fields['start'] = json.dumps(timestamp2str(fields['start']))
    if 'end' in fields.keys():
        fields['end'] = json.dumps(timestamp2str(fields['end']))
    return render_to_response(template_name, {
        "scenes": scenes,
        "fields": fields,
        "errors": errors,
        "cities": cities,
        "citygroups": citygroups,
        "open_type": open_type,
        "t": t,
        "c": c,
        "v": v,
        "text": text,
        "channel": channel_id,
        "id": id
    }, context_instance=RequestContext(request))


@login_required
@permission_required(u'%s.%s' % (AuthCodeName.APP_LABEL, AuthCodeName.CONFIG), raise_exception=True)
def delete_activity(request):
    id = request.POST.get("id")
    channel_id = request.POST.get("channel")
    view_activities = CmsViewActivity.objects.filter(activity_id=id)
    for view_activity in view_activities:
        if CMS_CHECK_ON:
            check = CmsCheck(
                channel_id=channel_id,
                module=CmsModule.CONFIG_ACTIVITY,
                table_name="CmsViewActivity",
                data_id=view_activity.id,
                op_type=CheckOpType.DELETE,
                status=CheckStatu.WAIT_SUBMIT,
                is_show=0,
                alter_person=request.user.username,
                alter_date=time.strftime("%Y-%m-%d %X", time.localtime()))
            check.save()
        view_activity.delete()
    CmsActivities.objects.get(id=id).delete()
    if CMS_CHECK_ON:
        check = CmsCheck(
            channel_id=channel_id,
            module=CmsModule.CONFIG_ACTIVITY,
            table_name="CmsActivities",
            data_id=id,
            op_type=CheckOpType.DELETE,
            status=CheckStatu.WAIT_SUBMIT,
            is_show=1,
            alter_person=request.user.username,
            alter_date=time.strftime("%Y-%m-%d %X", time.localtime()))
        check.save()
    return HttpResponse(0)
