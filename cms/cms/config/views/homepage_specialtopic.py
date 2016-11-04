# coding: utf-8

"""
    首页专题
"""
# from config.views.config_pub import *
# from main.forms import *
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
from common.views import get_check_status_str, filter_none, CheckManager, get_relate_channel_list
from config.views.config_pub import CMS_CHECK_ON, CmsCheck, new_associate, exchange_obj, get_services, get_goods, \
    get_topics
from main.forms import SpecialTopicForm
from main.models import CmsChannels, get_valid_time, get_city_str, \
    getCVT, CmsViewHomepageTopic, get_scene_name, CmsSpecialTopic
from main.views.main_pub import add_main_var, get_city_list, get_city_group, format_form, get_actions_select, get_scenes


# 首页专题列表页
@login_required
@add_main_var
def homepage_specialtopic(request, template_name):
    t = request.GET.get("t")
    if not t:
        t = "1"
    v = request.GET.get("v")
    c = request.GET.get("c")
    channel = CmsChannels.objects.get(channel_no=c, app_version__app_version=v, app_version__type_id=t).id
    topics = get_topics()
    return render_to_response(template_name, {
        "text": get_nav_text(t),
        "t": t,
        "v": v,
        "c": c,
        "channel": channel,
        "topics": topics
    }, context_instance=RequestContext(request))


# 获取首页专题列表数据
@login_required
def search_homepage_specialtopic(request):
    channel_id = request.GET.get('channel')
    objs = CmsViewHomepageTopic.objects.filter(channel_id=channel_id)
    result = []
    for obj in objs:
        topic = obj.topic
        scene_name = get_scene_name(topic.scene_id)
        status_str_topic, status_int_topic = get_check_status_str("CmsSpecialTopic", topic.id)
        status_str_view, status_int_view = get_check_status_str("CmsViewHomepageTopic", obj.id)
        result.append([
            scene_name,
            topic.image_url,
            topic.title,
            topic.title_color,
            topic.subtitle,
            topic.subtitle_color,
            topic.action_id,
            get_valid_time(topic.valid_time),
            get_city_str(topic.city),
            status_str_view,
            "%d/%d" % (status_int_topic, status_int_view),
            topic.id
        ])
    filter_none(result)
    return HttpResponse(json.dumps(result))


# 删除首页专题
@login_required
@permission_required(u'%s.%s' % (AuthCodeName.APP_LABEL, AuthCodeName.CONFIG), raise_exception=True)
def delete_homepage_specialtopic(request):
    id = request.POST.get("id")
    channel_id = request.POST.get("channel")
    relate_channels = get_relate_channel_list(channel_id, CONFIG_ITEMS.HOMEPAGE)
    relate_channels.append(channel_id)
    for c in relate_channels:
        hometopics = CmsViewHomepageTopic.objects.filter(topic=id, channel=c)
        for hometopic in hometopics:
            if CMS_CHECK_ON:
                is_show = 0
                remark = ""
                if int(c) == int(channel_id):
                    is_show = 1
                    remark = "删除标题为%s的首页专题" % CheckManager.wrap_style(hometopic.topic.title)
                check = CmsCheck(
                    channel_id=channel_id,
                    module=CmsModule.CONFIG_HOMEPAGE,
                    table_name="CmsViewHomepageTopic",
                    data_id=hometopic.id,
                    op_type=CheckOpType.DELETE,
                    status=CheckStatu.WAIT_SUBMIT,
                    is_show=is_show,
                    remark=remark,
                    alter_person=request.user.username,
                    alter_date=time.strftime("%Y-%m-%d %X", time.localtime()))
                check.save()
            hometopic.delete()
    return HttpResponse(0)


# 新增首页专题
@login_required
@permission_required(u'%s.%s' % (AuthCodeName.APP_LABEL, AuthCodeName.CONFIG), raise_exception=True)
@add_main_var
def new_homepage_specialtopic(request):
    """
    配置库： 新增首页专题
    :请求方式：ajax Post
    :请求URL：{% url 'new_homepage_specialtopic' %}
    :请求参数：specialtopic_id  channel_id
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
            try:
                specialtopic_id = request.POST.get("specialtopic_id")
                channel_id = request.POST.get("channel_id")
                ospecialtopic = CmsSpecialTopic.objects.get(id=specialtopic_id)
                oCmsViewHomepageTopic = CmsViewHomepageTopic(topic=ospecialtopic,
                                                             channel=CmsChannels.objects.get(id=channel_id))
                oCmsViewHomepageTopic.save()
                if CMS_CHECK_ON:
                    CmsCheck(channel_id=channel_id,
                             module=CmsModule.CONFIG_HOMEPAGE,
                             table_name='CmsViewHomepageTopic',
                             data_id=oCmsViewHomepageTopic.id,
                             op_type=CheckOpType.NEW,
                             remark="增加标题为%s的首页专题" % (CheckManager.wrap_style(ospecialtopic.title),),
                             alter_person=request.user.username,
                             alter_date=time.strftime("%Y-%m-%d %X", time.localtime())).save()
                new_associate(channel_id, specialtopic_id, CONFIG_ITEMS.HOMEPAGE, request)
            except Exception as ex:
                if 'Duplicate entry' in ex.args[0]:
                    return HttpResponse(1)
                return HttpResponse(ex.args[0])
            return HttpResponse(0)


# 编辑首页专题
@login_required
@permission_required(u'%s.%s' % (AuthCodeName.APP_LABEL, AuthCodeName.CONFIG), raise_exception=True)
@add_main_var
def edit_homepage_specialtopic(request, template_name):
    """
     编辑 首页专题
     url:{% url edit_homepage_specialtopic %}?channel={{ channel }}&id={{ id }}
    #插入到专题表 cms_special_topic
    :请求方式:Get
    :请求参数： id , channel：渠道id
    :返回数据： form 表单 citygroups 城市分组 actions：动作列表  cities:所有城市（格式和之前一致）
    :格式：[[id,name],....]

    :请求方式：Post
    :请求参数：cms_special_topic的表字段。
    :
    """
    id = request.GET.get("id")
    channel_id = request.GET.get('channel')
    c, v, t = getCVT(channel_id)
    text = get_nav_text(str(t))
    specialtopic = CmsSpecialTopic.objects.get(id=id)
    if request.method == 'POST':
        form = SpecialTopicForm(request.POST, instance=specialtopic)
        if form.is_valid():
            form.save()
            if CMS_CHECK_ON:
                CmsCheck(channel_id=channel_id,
                         module=CmsModule.CONFIG_HOMEPAGE,
                         table_name='CmsSpecialTopic',
                         data_id=id,
                         op_type=CheckOpType.EDIT,
                         alter_person=request.user.username,
                         alter_date=time.strftime("%Y-%m-%d %X", time.localtime())).save()
            return HttpResponseRedirect(reverse('homepage_specialtopic') + "?t=%d&c=%s&v=%s" % (t, c, v))
    else:
        form = SpecialTopicForm(instance=specialtopic)
    citygroups = get_city_group()
    actions = get_actions_select()
    cities = get_city_list()
    scenes = get_scenes()
    errors, fields = format_form(form)
    return render_to_response(template_name, {
        "fields": fields,
        "errors": errors,
        "citygroups": citygroups,
        "actions": actions,
        "cities": cities,
        "open_type": open_type,
        "scenes": scenes,
        "t": t,
        "c": c,
        "v": v,
        "text": text,
        "channel": channel_id,
        "id": id
    }, context_instance=RequestContext(request))
