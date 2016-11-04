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

from common.const import AuthCodeName, get_nav_text, CmsModule, CheckOpType, CONFIG_ITEMS, \
    CheckStatu, open_type
from common.views import get_check_status_str, filter_none, make_timestamp, timestamp2str
from config.forms import CmsNativeActivityForm, ActivitiesForm
from config.views.config_pub import CMS_CHECK_ON, CmsCheck, new_associate, exchange_obj
from main.models import CmsChannels, get_valid_time, get_city_str, CmsNativeActivity, get_scene_name, \
    timestamp2str_space, getCVT, CmsViewNativeActivity
from main.views.main_pub import add_main_var, get_scenes, get_city_list, get_city_group, format_form, \
    get_actions_select


@login_required
@add_main_var
def native_activities(request, template_name):
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
    objs = CmsNativeActivity.objects.filter(cmsviewnativeactivity__channel_id=channel_id)
    result = []
    for obj in objs:
        try:
            status_str, status_int = get_check_status_str("CmsNativeActivity", obj.id)
            result.append([
                get_scene_name(obj.scene_id),
                obj.sort,
                obj.title,
                obj.title_color,
                obj.subtitle,
                obj.image_url,
                timestamp2str_space(obj.start_time),
                timestamp2str_space(obj.end_time),
                obj.action_id,
                get_valid_time(obj.valid_time),
                get_city_str(obj.city),
                status_str,
                status_int,
                obj.id])
        except:
            continue
    result.sort(key=lambda o: (o[0], o[1]))
    filter_none(result)
    return HttpResponse(json.dumps(result))


@login_required
@permission_required(u'%s.%s' % (AuthCodeName.APP_LABEL, AuthCodeName.CONFIG), raise_exception=True)
def exchange_activities(request):
    id1 = request.POST.get("id1")
    id2 = request.POST.get("id2")
    channel_id = request.POST.get("channel")
    exchange_obj(CmsNativeActivity, id1, CmsNativeActivity, id2, channel_id, CmsModule.CONFIG_NATIVE_ACTIVITY, request,
                 "sort", "sort")
    return HttpResponse(0)


@login_required
@permission_required(u'%s.%s' % (AuthCodeName.APP_LABEL, AuthCodeName.CONFIG), raise_exception=True)
@add_main_var
def new_activity(request, template_name):
    """
    配置库 本地活动
    url :{% url 'new_native_activity' %}?channel={{ channel }}
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
    times = ['start_time', 'end_time', 'open_time', 'close_time']
    if request.method == 'POST':
        form = CmsNativeActivityForm(request.POST)
        for time1 in times:
            if form.data[time1]:
                form.data[time1] = make_timestamp(form.data[time1])
        if form.is_valid():
            activity = form.save()
            import time
            if CMS_CHECK_ON:
                check = CmsCheck(
                    channel_id=channel_id,
                    module=CmsModule.CONFIG_NATIVE_ACTIVITY,
                    table_name="CmsNativeActivity",
                    data_id=activity.id,
                    op_type=CheckOpType.NEW,
                    status=CheckStatu.WAIT_SUBMIT,
                    is_show=1,
                    alter_person=request.user.username,
                    alter_date=time.strftime("%Y-%m-%d %X", time.localtime()))
                check.save()
            new_associate(channel_id, activity.id, CONFIG_ITEMS.NATIVE_ACTIVITY, request)
            oCmsViewNativeActivity = CmsViewNativeActivity(nactivity=activity, channel=channel)
            oCmsViewNativeActivity.save()
            if CMS_CHECK_ON:
                check = CmsCheck(
                    channel_id=channel_id,
                    module=CmsModule.CONFIG_NATIVE_ACTIVITY,
                    table_name="CmsViewNativeActivity",
                    data_id=oCmsViewNativeActivity.id,
                    op_type=CheckOpType.NEW,
                    status=CheckStatu.WAIT_SUBMIT,
                    is_show=0,
                    alter_person=request.user.username,
                    alter_date=time.strftime("%Y-%m-%d %X", time.localtime()))
                check.save()
            return HttpResponseRedirect(reverse("native_activities") + "?t=%d&c=%s&v=%s" % (t, c, v))
    else:
        form = ActivitiesForm()
    actions = get_actions_select()
    scenes = get_scenes()
    cities = get_city_list()
    citygroups = get_city_group()
    errors, fields = format_form(form)
    for time in times:
        if time in fields.keys() and json.loads(fields[time]):
            fields[time] = json.dumps(timestamp2str(fields[time]))
    return render_to_response(template_name, {
        "scenes": scenes,
        "actions": actions,
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
    配置库 编辑本地活动
    url :{% url 'edit_native_activity' %}?channel={{ channel }}&id={{ id }}
    :请求方式: Get
    :请求参数：channel
    :返回数据：fields errors scenes 场景列表 open_type(类别) citygroups cities actions
    :例如：scenes 场景列表 和之前一样

    :请求方式：Post
    :请求参数：
    """
    channel_id = request.GET.get('channel')
    c, v, t = getCVT(channel_id)
    id = request.GET.get("id")
    oCmsNativeActivity = CmsNativeActivity.objects.get(id=id)
    # 根据类型得到名称
    text = get_nav_text(str(t))
    times = ['start_time', 'end_time', 'open_time', 'close_time']
    if request.method == 'POST':
        form = CmsNativeActivityForm(request.POST, instance=oCmsNativeActivity)
        for time in times:
            if form.data[time]:
                form.data[time] = make_timestamp(form.data[time])
        if form.is_valid():
            activity = form.save()
            import time
            if CMS_CHECK_ON:
                check = CmsCheck(
                    channel_id=channel_id,
                    module=CmsModule.CONFIG_NATIVE_ACTIVITY,
                    table_name="CmsNativeActivity",
                    data_id=activity.id,
                    op_type=CheckOpType.EDIT,
                    status=CheckStatu.WAIT_SUBMIT,
                    is_show=1,
                    alter_person=request.user.username,
                    alter_date=time.strftime("%Y-%m-%d %X", time.localtime()))
                check.save()
            return HttpResponseRedirect(reverse("native_activities") + "?t=%d&c=%s&v=%s" % (t, c, v))
    else:
        form = ActivitiesForm(instance=oCmsNativeActivity)
    scenes = get_scenes()
    cities = get_city_list()
    citygroups = get_city_group()
    actions = get_actions_select()
    errors, fields = format_form(form)
    for time in times:
        if time in fields.keys() and json.loads(fields[time]):
            fields[time] = json.dumps(timestamp2str(fields[time]))
    return render_to_response(template_name, {
        "scenes": scenes,
        "fields": fields,
        "errors": errors,
        "cities": cities,
        "actions": actions,
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
    channel_id = request.POST.get('channel')
    views = CmsViewNativeActivity.objects.filter(nactivity_id=id)
    if CMS_CHECK_ON:
        for view in views:
            check = CmsCheck(
                channel_id=channel_id,
                module=CmsModule.CONFIG_NATIVE_ACTIVITY,
                table_name="CmsViewNativeActivity",
                data_id=view.id,
                op_type=CheckOpType.DELETE,
                status=CheckStatu.WAIT_SUBMIT,
                is_show=0,
                alter_person=request.user.username,
                alter_date=time.strftime("%Y-%m-%d %X", time.localtime()))
            check.save()
    views.delete()
    CmsNativeActivity.objects.filter(id=id).delete()
    if CMS_CHECK_ON:
        check = CmsCheck(
            channel_id=channel_id,
            module=CmsModule.CONFIG_NATIVE_ACTIVITY,
            table_name="CmsNativeActivity",
            data_id=id,
            op_type=CheckOpType.DELETE,
            status=CheckStatu.WAIT_SUBMIT,
            is_show=1,
            alter_person=request.user.username,
            alter_date=time.strftime("%Y-%m-%d %X", time.localtime()))
        check.save()
    return HttpResponse(0)
