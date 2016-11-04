#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = '精品分类'
__author__ = 'rfd'
__mtime__ = '2015/10/8'
"""
from common.const import AuthCodeName, open_type
# from config.views.config_pub import *
# from config.forms import *
from config.forms import ChoicenessCategoryForm
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
from common.views import get_check_status_str, filter_none
from config.views.config_pub import CMS_CHECK_ON, CmsCheck, new_associate, exchange_obj
from main.models import CmsChannels, get_valid_time, get_city_str, \
    getCVT, CmsChoicenessCategory, CmsViewChoicenessCategory
from main.views.main_pub import add_main_var, get_city_list, get_city_group, format_form, get_categories


@login_required
@add_main_var
def choiceness_categories(request, template_name):
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
def search_choiceness_categories(request):
    channel_id = request.GET.get('channel')
    objs = CmsChoicenessCategory.objects.filter(cmsviewchoicenesscategory__channel_id=channel_id)
    result = []
    for obj in objs:
        try:
            status_str, status_int = get_check_status_str("CmsChoicenessCategory", obj.id)
            result.append([
                obj.location,
                obj.category.name,
                obj.img_url,
                obj.img_url_d,
                obj.background_color,
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
def exchange_choiceness_categories(request):
    id1 = request.POST.get("id1")
    id2 = request.POST.get("id2")
    channel_id = request.POST.get("channel")
    exchange_obj(CmsChoicenessCategory, id1, CmsChoicenessCategory, id2, channel_id, CmsModule.CONFIG_CHOICENESS,
                 request)
    return HttpResponse(0)


@login_required
@permission_required(u'%s.%s' % (AuthCodeName.APP_LABEL, AuthCodeName.CONFIG), raise_exception=True)
@add_main_var
def new_choiceness_category(request, template_name):
    """
    配置库 新建精品分类
    url :{% url 'new_choiceness_category' %}?channel={{ channel }}
    :请求方式: Get
    :请求参数：channel
    :返回数据：fields errors   分类列表 categories 城市分组citygroups cities
    :例如： 和之前一样

    :请求方式：Post
    :请求参数：注意 channel_id变成channel category_id变为category
    """
    channel_id = request.GET.get('channel')
    c, v, t = getCVT(channel_id)
    # 根据类型得到名称
    text = get_nav_text(str(t))
    if request.method == 'POST':
        form = ChoicenessCategoryForm(request.POST)
        if form.is_valid():
            choiceness_category = form.save()
            if CMS_CHECK_ON:
                CmsCheck(channel_id=channel_id,
                         module=CmsModule.CONFIG_CHOICENESS,
                         table_name='CmsChoicenessCategory',
                         data_id=choiceness_category.id,
                         op_type=CheckOpType.NEW,
                         alter_person=request.user.username,
                         alter_date=time.strftime("%Y-%m-%d %X", time.localtime())).save()
            oCmsViewChoicenessCategory = CmsViewChoicenessCategory(choiceness_category=choiceness_category,
                                                                   channel=CmsChannels.objects.get(id=channel_id))
            oCmsViewChoicenessCategory.save()
            if CMS_CHECK_ON:
                CmsCheck(channel_id=channel_id,
                         module=CmsModule.CONFIG_CHOICENESS,
                         table_name='CmsViewChoicenessCategory',
                         data_id=oCmsViewChoicenessCategory.id,
                         op_type=CheckOpType.NEW,
                         is_show=0,
                         alter_person=request.user.username,
                         alter_date=time.strftime("%Y-%m-%d %X", time.localtime())).save()
            new_associate(channel_id, choiceness_category.id, CONFIG_ITEMS.CHOICENESS_CATEGORY, request)
            return HttpResponseRedirect(reverse("choiceness_categories") + "?t=%d&c=%s&v=%s" % (t, c, v))
    else:
        form = ChoicenessCategoryForm()
    categories = get_categories()
    cities = get_city_list()
    citygroups = get_city_group()
    errors, fields = format_form(form)
    return render_to_response(template_name, {
        "categories": categories,
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
def edit_choiceness_category(request, template_name):
    """
    配置库 编辑精品分类
    url :{% url 'edit_choiceness_category' %}?channel={{ channel }}&id={{ id }}
    :请求方式: Get
    :请求参数：channel,id
    :返回数据：fields errors   分类列表 categories 城市分组citygroups cities
    :例如： 和之前一样

    :请求方式：Post
    :请求参数：注意 channel_id变成channel category_id变为category
    """
    channel_id = request.GET.get('channel')
    id = request.GET.get("id")
    choicenesscategory = CmsChoicenessCategory.objects.get(id=id)
    c, v, t = getCVT(channel_id)
    # 根据类型得到名称
    text = get_nav_text(str(t))
    if request.method == 'POST':
        form = ChoicenessCategoryForm(request.POST, instance=choicenesscategory)
        if form.is_valid():
            form.save()
            if CMS_CHECK_ON:
                CmsCheck(channel_id=channel_id,
                         module=CmsModule.CONFIG_CHOICENESS,
                         table_name='CmsChoicenessCategory',
                         data_id=id,
                         op_type=CheckOpType.EDIT,
                         alter_person=request.user.username,
                         alter_date=time.strftime("%Y-%m-%d %X", time.localtime())).save()
            return HttpResponseRedirect(reverse("choiceness_categories") + "?t=%d&c=%s&v=%s" % (t, c, v))
    else:
        form = ChoicenessCategoryForm(instance=choicenesscategory)
    categories = get_categories()
    cities = get_city_list()
    citygroups = get_city_group()
    errors, fields = format_form(form)
    return render_to_response(template_name, {
        "categories": categories,
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
def delete_choiceness_category(request):
    id = request.POST.get("id")
    channel_id = request.POST.get("channel")
    views = CmsViewChoicenessCategory.objects.filter(choiceness_category_id=id)
    for view in views:
        if CMS_CHECK_ON:
            check = CmsCheck(
                channel_id=channel_id,
                module=CmsModule.CONFIG_CHOICENESS,
                table_name="CmsViewChoicenessCategory",
                data_id=view.id,
                op_type=CheckOpType.DELETE,
                status=CheckStatu.WAIT_SUBMIT,
                is_show=0,
                alter_person=request.user.username,
                alter_date=time.strftime("%Y-%m-%d %X", time.localtime()))
            check.save()
        view.delete()
    CmsChoicenessCategory.objects.get(id=id).delete()
    if CMS_CHECK_ON:
        check = CmsCheck(
            channel_id=channel_id,
            module=CmsModule.CONFIG_CHOICENESS,
            table_name="CmsChoicenessCategory",
            data_id=id,
            op_type=CheckOpType.DELETE,
            status=CheckStatu.WAIT_SUBMIT,
            is_show=1,
            alter_person=request.user.username,
            alter_date=time.strftime("%Y-%m-%d %X", time.localtime()))
        check.save()
    return HttpResponse(0)
