#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = '专题'
__author__ = 'rfd'
__mtime__ = '2015/8/28'
"""
# from .main_pub import *
# from main.forms import *
import time
from audioop import reverse

from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
import json
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from cms.settings import CMS_CHECK_ON
from common.const import AuthCodeName, CheckStatu, CheckOpType, MainConst, CmsModule, open_type
from common.views import get_check_status_str, search_key, get_table_paginator
from main.forms import SpecialTopicForm
from main.models import CmsCheck, CmsSpecialTopic, get_valid_time, get_city_str, CmsViewFindTopic
from main.views.main_pub import add_main_var, get_city_group, format_form, get_actions_select, get_city_list, get_scenes


# 专题列表
@login_required
@add_main_var
def specialtopics(request, template_name):
    return render_to_response(template_name, context_instance=RequestContext(request))


# 列表（搜索，分页查看），返回总页码和对象列表
@login_required
def search_specialtopic(request):
    per_page = request.GET.get("per_page")
    if not per_page:
        per_page = MainConst.PER_PAGE
    cur_page = request.GET.get("cur_page")
    if not cur_page:
        cur_page = 1
    objs = CmsSpecialTopic.objects.filter()
    topics = []
    for obj in objs:
        status_str, status_int = get_check_status_str("CmsSpecialTopic", obj.id)
        topics.append([
            obj.image_url,
            obj.title,
            obj.title_color,
            obj.subtitle,
            obj.subtitle_color,
            obj.action_id,
            get_valid_time(obj.valid_time),
            get_city_str(obj.city),
            status_str,
            status_int,
            obj.id
        ])
    key = request.GET.get("key")
    topics = search_key(topics, key, [0, 2, 4, 9, 10])
    result, num_pages = get_table_paginator(topics, per_page, cur_page)
    return HttpResponse(json.dumps([list(result), num_pages]))


# 新增专题
@login_required
@permission_required(u'%s.%s' % (AuthCodeName.APP_LABEL, AuthCodeName.CONFIG), raise_exception=True)
@add_main_var
def new_specialtopic(request, template_name):
    """
    新建专题
    url :{% url 'new_specialtopic' %}
    :请求方式: Get
    :请求参数：无
    :返回数据：scenes 场景列表 citygroups 城市分组列表，cities 所有城市(列表) actions 动作列表 open_type 类型
    :[[id,name],[id,name],....]

    :请求方式：Post
    :请求参数：数据库字段(input name)
    """
    if request.method == "POST":
        form = SpecialTopicForm(request.POST)
        if form.is_valid():
            ospecialtopic = form.save()
            if CMS_CHECK_ON:
                CmsCheck(module=CmsModule.MAIN_TOPIC,
                         table_name='CmsSpecialTopic',
                         data_id=ospecialtopic.id,
                         op_type=CheckOpType.NEW,
                         alter_person=request.user.username,
                         alter_date=time.strftime("%Y-%m-%d %X", time.localtime())).save()
            return HttpResponseRedirect(reverse("specialtopics"))
    else:
        form = SpecialTopicForm()
    errors, fields = format_form(form)
    citygroups = get_city_group()
    actions = get_actions_select()
    cities = get_city_list()
    scenes = get_scenes()
    return render_to_response(template_name, {
        "fields": fields,
        "errors": errors,
        "citygroups": citygroups,
        "actions": actions,
        "cities": cities,
        "scenes": scenes,
        "open_type": open_type,
    }, context_instance=RequestContext(request))


# 编辑专题
@login_required
@permission_required(u'%s.%s' % (AuthCodeName.APP_LABEL, AuthCodeName.CONFIG), raise_exception=True)
@add_main_var
def edit_specialtopic(request, template_name):
    """
    编辑专题
    url :{% url 'edit_specialtopic' %}?id={{ id }}
    :请求方式: Get
    :请求参数：id
    :返回数据：scenes 场景列表 citygroups 城市分组列表，cities 所有城市(列表) actions 动作列表 open_type 类型
    :[[id,name],[id,name],....]

    :请求方式：Post
    :请求参数：数据库字段(input name)
    """
    id = request.GET.get("id")
    specialtopic = CmsSpecialTopic.objects.get(id=id)
    if request.method == "POST":
        form = SpecialTopicForm(request.POST, instance=specialtopic)
        if form.is_valid():
            form.save()
            if CMS_CHECK_ON:
                CmsCheck(module=CmsModule.MAIN_TOPIC, table_name='CmsSpecialTopic', data_id=id,
                         op_type=CheckOpType.EDIT).save()
            find_page_views = CmsViewFindTopic.objects.filter(topic_id=id)
            # 更新时间同步
            for find_page_view in find_page_views:
                find_page_view.update_time = specialtopic.update_time
                find_page_view.save()
                if CMS_CHECK_ON:
                    CmsCheck(module=CmsModule.MAIN_TOPIC,
                             table_name='CmsViewFindTopic',
                             data_id=find_page_view.id,
                             op_type=CheckOpType.EDIT,
                             is_show=0,
                             alter_person=request.user.username,
                             alter_date=time.strftime("%Y-%m-%d %X", time.localtime())).save()
            return HttpResponseRedirect(reverse("specialtopics"))
    else:
        form = SpecialTopicForm(instance=specialtopic)
    errors, fields = format_form(form)
    citygroups = get_city_group()
    actions = get_actions_select()
    cities = get_city_list()
    scenes = get_scenes()
    return render_to_response(template_name, {
        "fields": fields,
        "errors": errors,
        "citygroups": citygroups,
        "actions": actions,
        "cities": cities,
        "scenes": scenes,
        "open_type": open_type,
        "id": id
    }, context_instance=RequestContext(request))


# 删除专题
@login_required
@permission_required(u'%s.%s' % (AuthCodeName.APP_LABEL, AuthCodeName.CONFIG), raise_exception=True)
def delete_specialtopic(request):
    """
    删除内容库的专题，内容库的专题会删除掉，首页专题会删掉，发现页专题is_deleted=1
    :param request:
    :return:
    """
    id = request.POST.get('id')
    topic = CmsSpecialTopic.objects.get(id=id)
    objs = CmsViewFindTopic.objects.filter(topic_id=id)
    for obj in objs:
        obj.is_deleted = 1
        obj.delete_time = time.timezone.now()
        obj.save()
        if CMS_CHECK_ON:
            check = CmsCheck(
                module=CmsModule.MAIN_TOPIC,
                table_name="CmsViewFindTopic",
                data_id=id,
                op_type=CheckOpType.EDIT,
                status=CheckStatu.WAIT_SUBMIT,
                is_show=0,
                alter_person=request.user.username,
                alter_date=time.strftime("%Y-%m-%d %X", time.localtime()))
            check.save()
    if CMS_CHECK_ON:
        check = CmsCheck(
            module=CmsModule.MAIN_TOPIC,
            table_name="CmsSpecialTopic",
            data_id=id,
            op_type=CheckOpType.DELETE,
            status=CheckStatu.WAIT_SUBMIT,
            is_show=1,
            alter_person=request.user.username,
            alter_date=time.strftime("%Y-%m-%d %X", time.localtime()))
        check.save()
    topic.delete()
    return HttpResponse(0)
