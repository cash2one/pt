# coding: utf-8

"""
    发现页专题
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
    CheckStatu, JPUSH, open_type
from common.views import get_check_status_str, filter_none, CheckManager, get_relate_channel_list
from config.views.config_pub import CMS_CHECK_ON, CmsCheck, new_associate, get_topics, push_foundpage
from main.forms import SpecialTopicForm
from main.models import CmsChannels, get_valid_time, get_city_str, CmsViewFindTopic, CmsSpecialTopic, get_scene_name, \
    getCVT, CmsChannelJpush
from main.views.main_pub import add_main_var, get_city_list, get_city_group, format_form, \
    get_actions_select, get_scenes


# 发现页专题列表页
@login_required
@add_main_var
def foundpage_specialtopic(request, template_name):
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


# 获取发现页专题列表数据
@login_required
def search_foundpage_specialtopic(request):
    channel_id = request.GET.get('channel')
    objs = CmsViewFindTopic.objects.filter(channel_id=channel_id, is_deleted=0)
    result = []
    for obj in objs:
        topic = CmsSpecialTopic.objects.get(id=obj.topic_id)
        if obj.is_deleted == 0:
            scene_name = get_scene_name(topic.scene_id)
            is_top = "是" if obj.is_top else "否"
            status_str_topic, status_int_topic = get_check_status_str("CmsSpecialTopic", topic.id)
            status_str_view, status_int_view = get_check_status_str("CmsViewFindTopic", obj.id)
            result.append([
                scene_name,
                topic.image_url,
                topic.title,
                topic.title_color,
                topic.subtitle,
                topic.subtitle_color,
                topic.action_id,
                is_top,
                obj.mark_info,
                get_valid_time(topic.valid_time),
                get_city_str(topic.city),
                status_str_view,
                "%d/%d" % (status_int_topic, status_int_view),
                topic.id
            ])
    filter_none(result)
    return HttpResponse(json.dumps(result))


# 删除发现页专题
@login_required
@permission_required(u'%s.%s' % (AuthCodeName.APP_LABEL, AuthCodeName.CONFIG), raise_exception=True)
def delete_foundpage_specialtopic(request):
    id = request.POST.get("id")
    channel_id = request.POST.get("channel")
    relate_channels = get_relate_channel_list(channel_id, CONFIG_ITEMS.FOUNDPAGE)
    relate_channels.append(channel_id)
    for c in relate_channels:
        find_topics = CmsViewFindTopic.objects.filter(topic_id=id, channel_id=c, is_deleted=0)
        for find_topic in find_topics:
            find_topic.is_deleted = 1
            # find_topic.update_time = timezone.now()
            find_topic.delete_time = time.timezone.now()
            find_topic.save()
            if CMS_CHECK_ON:
                is_show = 0
                remark = ""
                if int(c) == int(channel_id):
                    is_show = 1
                    remark = "删除标题为%s的发现页专题" % (
                        CheckManager.wrap_style(CmsSpecialTopic.objects.get(id=find_topic.topic_id).title),)
                check = CmsCheck(
                    channel_id=channel_id,
                    module=CmsModule.CONFIG_FOUNDPAGE,
                    table_name="CmsViewFindTopic",
                    data_id=find_topic.id,
                    op_type=CheckOpType.DELETE,
                    status=CheckStatu.WAIT_SUBMIT,
                    is_show=is_show,
                    remark=remark,
                    alter_person=request.user.username,
                    alter_date=time.strftime("%Y-%m-%d %X", time.localtime()))
                check.save()
    return HttpResponse(0)


# 是否置顶
@login_required
@permission_required(u'%s.%s' % (AuthCodeName.APP_LABEL, AuthCodeName.CONFIG), raise_exception=True)
def top_foundpage_specialtopic(request):
    id = request.POST.get("id")
    top = request.POST.get("top")
    channel_id = request.POST.get("channel")
    relate_channels = get_relate_channel_list(channel_id, CONFIG_ITEMS.FOUNDPAGE)
    relate_channels.append(channel_id)
    for c in relate_channels:
        find_topics = CmsViewFindTopic.objects.filter(topic_id=id, channel_id=c, is_deleted=0)
        for find_topic in find_topics:
            find_topic.is_top = top
            find_topic.save()
            if CMS_CHECK_ON:
                check = CmsCheck(
                    channel_id=channel_id,
                    module=CmsModule.CONFIG_FOUNDPAGE,
                    table_name="CmsViewFindTopic",
                    data_id=find_topic.id,
                    op_type=CheckOpType.EDIT,
                    status=CheckStatu.WAIT_SUBMIT,
                    is_show=1,
                    alter_person=request.user.username,
                    alter_date=time.strftime("%Y-%m-%d %X", time.localtime()))
                check.save()
    return HttpResponse(0)


# 设置运营标签
@login_required
@permission_required(u'%s.%s' % (AuthCodeName.APP_LABEL, AuthCodeName.CONFIG), raise_exception=True)
def mark_info_foundpage(request):
    id = request.POST.get("id")
    mark_info = request.POST.get("mark_info")
    channel_id = request.POST.get("channel")
    relate_channels = get_relate_channel_list(channel_id, CONFIG_ITEMS.FOUNDPAGE)
    relate_channels.append(channel_id)
    for c in relate_channels:
        find_topics = CmsViewFindTopic.objects.filter(topic_id=id, channel_id=c, is_deleted=0)
        for find_topic in find_topics:
            find_topic.mark_info = mark_info
            find_topic.save()
            if CMS_CHECK_ON:
                check = CmsCheck(
                    channel_id=channel_id,
                    module=CmsModule.CONFIG_FOUNDPAGE,
                    table_name="CmsViewFindTopic",
                    data_id=find_topic.id,
                    op_type=CheckOpType.EDIT,
                    status=CheckStatu.WAIT_SUBMIT,
                    is_show=1,
                    alter_person=request.user.username,
                    alter_date=time.strftime("%Y-%m-%d %X", time.localtime()))
                check.save()
    return HttpResponse(0)


# 新增发现页专题
@login_required
@permission_required(u'%s.%s' % (AuthCodeName.APP_LABEL, AuthCodeName.CONFIG), raise_exception=True)
@add_main_var
def new_foundpage_specialtopic(request):
    """
    配置库： 新增发现页专题
    :请求方式：ajax Post
    :请求URL：{% url 'new_foundpage_specialtopic' %}
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
                c, v, t = getCVT(channel_id)
                ospecialtopic = CmsSpecialTopic.objects.get(id=specialtopic_id)
                oCmsViewFindTopic = CmsViewFindTopic(channel_id=channel_id, topic_id=specialtopic_id,
                                                     create_time=time.timezone.now(), update_time=time.timezone.now())
                oCmsViewFindTopic.save()
                if CMS_CHECK_ON:
                    CmsCheck(channel_id=channel_id,
                             module=CmsModule.CONFIG_FOUNDPAGE,
                             table_name='CmsViewFindTopic',
                             data_id=oCmsViewFindTopic.id,
                             op_type=CheckOpType.NEW,
                             remark="增加标题为%s的发现页专题" % (CheckManager.wrap_style(ospecialtopic.title),),
                             alter_person=request.user.username,
                             alter_date=time.strftime("%Y-%m-%d %X", time.localtime())).save()
                new_associate(channel_id, specialtopic_id, CONFIG_ITEMS.FOUNDPAGE, request)
                # jpush_foundpage(CmsChannels.objects.get(id=channel_id).channel_no,v,oCmsViewFindTopic.id,ospecialtopic.title,ospecialtopic.city)
                push_foundpage(channel_id, specialtopic_id)
                return HttpResponse(0)
            except Exception as ex:
                if 'Duplicate entry' in ex.args[0]:
                    return HttpResponse(1)
                return HttpResponse(ex.args[0])


def jpush_foundpage(channel_no, version, id, title, city):
    if JPUSH.SWITCH and channel_no == JPUSH.DEFAULT_CHANNELNO and version >= JPUSH.DEFAULT_VERSION:
        import jpush
        oCmsChannelJpush = CmsChannelJpush.objects.get(channel_no=channel_no)
        cities = city.split(",")
        new_cities = []
        for city in cities:
            if len(city) > 2 and city[-1] in ["市", "县"]:
                city = city[:-1]
            new_cities.append(city)
        cities = new_cities
        version = "Putao_" + version.replace(".", "_")
        app_key = oCmsChannelJpush.app_key
        master_secret = oCmsChannelJpush.master_secret
        _jpush = jpush.JPush(app_key, master_secret)
        push = _jpush.create_push()
        push.platform = jpush.all_
        for i in range(0, len(cities), 20):
            city = cities[i:i + 20]
            msg_time = int(time.time())
            city_list = []
            # push.audience = jpush.all_
            if "*" in city:
                push.audience = jpush.audience(
                    jpush.tag(channel_no, version)
                )
            else:
                push.audience = jpush.audience(
                    jpush.tag(*city),
                    jpush.tag_and(channel_no, version)
                )
                city_list = city
            # push.notification = jpush.notification(alert="new found page")

            messages = {
                "version": 1,
                "data": [
                    {
                        "msg_digest": title,
                        "msg_type": 10,
                        "msg_subject": title,
                        "msg_id": id,
                        "is_notify": 0,
                        "msg_expand_param": {
                            "tab_index": 1,
                            "city_list": city_list
                        },
                        "msg_time": msg_time,
                        "msg_product_type": "0"
                    }
                ]
            }
            push.message = {
                "msg_content": json.dumps(messages)
            }
            push.send()


# 编辑发现页专题
@login_required
@permission_required(u'%s.%s' % (AuthCodeName.APP_LABEL, AuthCodeName.CONFIG), raise_exception=True)
@add_main_var
def edit_foundpage_specialtopic(request, template_name):
    """
     编辑 发现页专题
    :请求方式:Get
    :请求参数：id, channel：渠道id
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
                         module=CmsModule.CONFIG_FOUNDPAGE,
                         table_name='CmsSpecialTopic',
                         data_id=id,
                         op_type=CheckOpType.EDIT,
                         alter_person=request.user.username,
                         alter_date=time.strftime("%Y-%m-%d %X", time.localtime())).save()
            find_page_views = CmsViewFindTopic.objects.filter(topic_id=id, is_deleted=0)
            for find_page_view in find_page_views:
                find_page_view.update_time = specialtopic.update_time
                find_page_view.save()
                if CMS_CHECK_ON:
                    CmsCheck(channel_id=channel_id,
                             module=CmsModule.CONFIG_FOUNDPAGE,
                             table_name='CmsViewFindTopic',
                             data_id=find_page_view.id,
                             op_type=CheckOpType.EDIT,
                             is_show=0,
                             alter_person=request.user.username,
                             alter_date=time.strftime("%Y-%m-%d %X", time.localtime())).save()
            return HttpResponseRedirect(reverse("foundpage_specialtopic") + "?t=%d&c=%s&v=%s" % (t, c, v))
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
        "scenes": scenes,
        "open_type": open_type,
        "t": t,
        "c": c,
        "v": v,
        "text": text,
        "channel": channel_id,
        "id": id
    }, context_instance=RequestContext(request))
