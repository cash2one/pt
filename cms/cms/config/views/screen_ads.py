# coding: utf-8


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

from cms.settings import CMS_CHECK_ON
from common.const import AuthCodeName, get_nav_text, CmsModule, CheckOpType, CONFIG_ITEMS, \
    CheckStatu, get_2array_value, screen_ad_times, open_type
from common.views import filter_none, get_check_status_str, make_timestamp, timestamp2str
from config.forms import CmsScreenadsForm, CmsAdbeansForm
from config.views.config_pub import new_associate
from main.models import CmsChannels, CmsScreenads, get_valid_time, get_city_str, getCVT, CmsCheck, CmsViewScreenads
from main.views.main_pub import add_main_var, get_scenes, get_city_list, get_city_group, format_form, get_actions_select


@login_required
@add_main_var
def screen_ads(request, template_name):
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
def search_screen_ads(request):
    channel_id = request.GET.get('channel')
    objs = CmsScreenads.objects.filter(cmsviewscreenads__channel_id=channel_id)
    result = []
    for obj in objs:
        try:
            show_hold = "不限" if obj.show_hold == -1 else str(obj.show_hold) + "秒"
            status_str, status_int = get_check_status_str("CmsScreenads", obj.id)
            result.append([
                obj.name,
                obj.img_url,
                get_2array_value(screen_ad_times, obj.show_times),
                show_hold,
                get_valid_time(obj.valid_time),
                get_city_str(obj.city),
                status_str,
                status_int,
                obj.id
            ])
        except:
            continue
    result.sort(key=lambda o: (o[0]))
    filter_none(result)
    return HttpResponse(json.dumps(result))


@login_required
@permission_required(u'%s.%s' % (AuthCodeName.APP_LABEL, AuthCodeName.CONFIG), raise_exception=True)
@add_main_var
def new_ad(request, template_name):
    """
    新建开屏广告
    #插入到开屏广告表，插入开屏广告和渠道关联表
    url :{% url 'new_screen_ad' %}?channel={{ channel }}
    :请求方式:Get
    :请求参数：channel：渠道id
    :返回数据： form 表单 citygroups 城市分组 actions：动作列表 (services 服务列表 goods 商品列表) open_type:类别 cities:所有城市（格式和之前一致）
               screen_ad_times = [[1, "仅展示一次"], [100, "每次进入展示"]]
    :格式：[[id,name],....]

    :请求方式：Post
    :请求参数：cms_screenads 表各字段
    :
    """
    channel_id = request.GET.get('channel')
    c, v, t = getCVT(channel_id)
    text = get_nav_text(str(t))
    if request.method == 'POST':
        form = CmsScreenadsForm(request.POST)
        form.data['start'] = make_timestamp(form.data['start'])
        form.data['end'] = make_timestamp(form.data['end'])
        if form.is_valid():
            oCmsScreenads = form.save()
            if CMS_CHECK_ON:
                check = CmsCheck(
                    channel_id=channel_id,
                    module=CmsModule.CONFIG_SCREEN_AD,
                    table_name="CmsScreenads",
                    data_id=oCmsScreenads.id,
                    op_type=CheckOpType.NEW,
                    status=CheckStatu.WAIT_SUBMIT,
                    alter_person=request.user.username,
                    alter_date=time.strftime("%Y-%m-%d %X", time.localtime()))
                check.save()
            new_associate(channel_id, oCmsScreenads.id, CONFIG_ITEMS.SCREEN_AD, request)
            oCmsViewScreenads = CmsViewScreenads(screenad=oCmsScreenads, channel=CmsChannels.objects.get(id=channel_id),
                                                 status=0)
            oCmsViewScreenads.save()
            if CMS_CHECK_ON:
                check = CmsCheck(
                    channel_id=channel_id,
                    module=CmsModule.CONFIG_SCREEN_AD,
                    table_name="CmsViewScreenads",
                    data_id=oCmsViewScreenads.id,
                    op_type=CheckOpType.NEW,
                    status=CheckStatu.WAIT_SUBMIT,
                    is_show=0,
                    alter_person=request.user.username,
                    alter_date=time.strftime("%Y-%m-%d %X", time.localtime()))
                check.save()
            return HttpResponseRedirect(reverse('screen_ads') + "?t=%d&c=%s&v=%s" % (t, c, v))

    else:
        form = CmsAdbeansForm()
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
        "screen_ad_times": screen_ad_times,
        "t": t,
        "c": c,
        "v": v,
        "text": text,
        "channel": channel_id
    }, context_instance=RequestContext(request))


@login_required
@permission_required(u'%s.%s' % (AuthCodeName.APP_LABEL, AuthCodeName.CONFIG), raise_exception=True)
@add_main_var
def edit_ad(request, template_name):
    """
    编辑开屏广告
    url :{% url 'edit_screen_ad' %}?channel={{ channel }}&id={{ id }}
    #更新开屏广告表
    :请求方式:Get
    :请求参数：id   channel：渠道id
    :返回数据： form 表单 citygroups 城市分组 actions：动作列表 (services 服务列表 goods 商品列表) open_type:类别 cities:所有城市（格式和之前一致）
                screen_ad_times = [[1, "仅展示一次"], [100, "每次进入展示"]]
    :格式：[[id,name],....]

    :请求方式：Post
    :请求参数：cms_screenads 表各字段
    :
    """
    channel_id = request.GET.get('channel')
    id = request.GET.get("id")
    c, v, t = getCVT(channel_id)
    text = get_nav_text(str(t))
    oCmsScreenads = CmsScreenads.objects.get(id=id)
    if request.method == 'POST':
        form = CmsScreenadsForm(request.POST, instance=oCmsScreenads)
        form.data['start'] = make_timestamp(form.data['start'])
        form.data['end'] = make_timestamp(form.data['end'])
        if form.is_valid():
            form.save()
            if CMS_CHECK_ON:
                check = CmsCheck(
                    channel_id=channel_id,
                    module=CmsModule.CONFIG_SCREEN_AD,
                    table_name="CmsScreenads",
                    data_id=oCmsScreenads.id,
                    op_type=CheckOpType.EDIT,
                    status=CheckStatu.WAIT_SUBMIT,
                    alter_person=request.user.username,
                    alter_date=time.strftime("%Y-%m-%d %X", time.localtime()))
                check.save()
            return HttpResponseRedirect(reverse('screen_ads') + "?t=%d&c=%s&v=%s" % (t, c, v))

    else:
        form = CmsAdbeansForm(instance=oCmsScreenads)
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
        "screen_ad_times": screen_ad_times,
        "t": t,
        "c": c,
        "v": v,
        "text": text,
        "channel": channel_id,
        "id": id
    }, context_instance=RequestContext(request))


@login_required
@permission_required(u'%s.%s' % (AuthCodeName.APP_LABEL, AuthCodeName.CONFIG), raise_exception=True)
def delete_ad(request):
    id = request.POST.get("id")
    channel_id = request.POST.get('channel')
    views = CmsViewScreenads.objects.filter(screenad_id=id)
    if CMS_CHECK_ON:
        for view in views:
            check = CmsCheck(
                channel_id=channel_id,
                module=CmsModule.CONFIG_SCREEN_AD,
                table_name="CmsViewScreenads",
                data_id=view.id,
                op_type=CheckOpType.DELETE,
                status=CheckStatu.WAIT_SUBMIT,
                is_show=0,
                alter_person=request.user.username,
                alter_date=time.strftime("%Y-%m-%d %X", time.localtime()))
            check.save()
    views.delete()
    CmsScreenads.objects.filter(id=id).delete()
    if CMS_CHECK_ON:
        check = CmsCheck(
            channel_id=channel_id,
            module=CmsModule.CONFIG_SCREEN_AD,
            table_name="CmsScreenads",
            data_id=id,
            op_type=CheckOpType.DELETE,
            status=CheckStatu.WAIT_SUBMIT,
            is_show=1,
            alter_person=request.user.username,
            alter_date=time.strftime("%Y-%m-%d %X", time.localtime()))
        check.save()
    return HttpResponse(0)
