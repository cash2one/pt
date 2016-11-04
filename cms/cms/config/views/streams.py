#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'putao'
__mtime__ = '2015/9/14'
"""
# from config.views.config_pub import *
# from config.forms import *
from django.db.models import Q

from config.forms import StreamcontentForm, CmsAdsForm, StreamcontentbeansForm
from main.forms import GoodsForm
from main.views.interface_category import sync_search
import time

from cms.settings import CMS_CHECK_ON, INSTALL_TYPE
from common.const import AuthCodeName, get_nav_text, CmsModule, CheckOpType, CONFIG_ITEMS, \
    CheckStatu, get_2array_value, streams_type, open_type
from common.views import get_check_status_str, filter_none, CheckManager
from config.views.config_pub import new_associate, exchange_obj, get_goods
from main.models import CmsChannels, getCVT, get_scene_name, get_valid_time, \
    get_city_str, CmsCheck, CmsStreamcontent, CmsGoods, CmsStreamcontentbeans, CmsViewStream, CmsStreamcontentsGoods, \
    CmsStreamcontentsBeans, CmsNaviCategory
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required, permission_required
import json
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from main.views.main_pub import add_main_var, get_city_list, get_city_group, format_form, get_scenes, \
    get_actions_select, \
    get_categories


@login_required
@add_main_var
def streams(request, template_name):
    t = request.GET.get("t")
    if not t:
        t = "1"
    v = request.GET.get("v")
    c = request.GET.get("c")
    channel = CmsChannels.objects.get(channel_no=c, app_version__app_version=v, app_version__type_id=t).id
    goods = get_goods()
    return render_to_response(template_name, {
        "text": get_nav_text(t),
        "t": t,
        "v": v,
        "c": c,
        "channel": channel,
        "goods": goods
    }, context_instance=RequestContext(request))


@login_required
def search_streams(request):
    channel = request.GET.get("channel")
    groups = CmsStreamcontent.objects.filter(cmsviewstream__channel__id=channel)
    result = []
    for group in groups:
        group_scene = get_scene_name(group.scene_id)
        group_type = get_2array_value(streams_type, group.type)
        status_str, status_int = get_check_status_str("CmsStreamcontent", group.id)
        item = {"group": [
            group_scene,
            group.location,
            group_type,
            status_str,
            status_int,
            group.id
        ], "members": []}
        # 商品
        goods = CmsGoods.objects.filter(cmsstreamcontentsgoods__streamcontent=group)
        for g in goods:
            status_str, status_int = get_check_status_str("CmsGoods", g.id)
            item["members"].append([
                g.icon_url,
                g.location,
                g.title,
                g.title_style,
                g.desc,
                g.desc_style,
                g.name,
                g.name_style,
                str(g.fav_price),
                g.fav_price_style,
                g.fav_price_desc,
                g.fav_price_desc_style,
                str(g.price),
                g.sold,
                g.action_id,
                get_valid_time(g.valid_time),
                get_city_str(g.city),
                "商品",
                status_str,
                0,
                status_int,
                g.id
            ])
        # 内容流
        beans = CmsStreamcontentbeans.objects.filter(cmsstreamcontentsbeans__streamcontent=group)
        for b in beans:
            status_str, status_int = get_check_status_str("CmsStreamcontentbeans", b.id)
            item["members"].append([
                b.img_url,
                b.location,
                b.title,
                b.title_style,
                b.descibe,
                b.descibe_style,
                b.name,
                b.name_style,
                str(b.price),
                b.price_style,
                b.price_desc,
                b.price_desc_style,
                str(b.price),
                b.sold,
                b.action_id,
                get_valid_time(b.valid_time),
                get_city_str(b.city),
                "内容流",
                status_str,
                1,
                status_int,
                b.id
            ])
        item["members"].sort(key=lambda o: (o[17], o[1]))
        result.append(item)
    filter_none(result)
    return HttpResponse(json.dumps(result))


@login_required
@permission_required(u'%s.%s' % (AuthCodeName.APP_LABEL, AuthCodeName.CONFIG), raise_exception=True)
@add_main_var
def new_streamsgroup(request, template_name):
    """
    新建 内容流组
    url :{% url 'new_streamsgroup' %}?channel={{ channel }}
    :请求方式: Get
    :请求参数：channel
    :返回数据：form 表单 scenes 场景列表 streams_type:类型
    :例如：scenes 场景列表 和之前一样 streams_type = [[1,"活动"],[2,"服务"],[3,"商品"],[4,"搜索"]]

    :请求方式：Post
    :请求参数：`type` `location`  `scene_id`
    """
    channel_id = request.GET.get('channel')
    c, v, t = getCVT(channel_id)
    channel = CmsChannels.objects.get(id=channel_id)
    # 根据类型得到名称
    text = get_nav_text(str(t))
    if request.method == 'POST':
        form = StreamcontentForm(request.POST)
        if form.is_valid():
            streamcontent = form.save()
            if CMS_CHECK_ON:
                CmsCheck(channel_id=channel_id,
                         module=CmsModule.CONFIG_STREAM,
                         table_name='CmsStreamcontent',
                         data_id=streamcontent.id,
                         op_type=CheckOpType.NEW,
                         alter_person=request.user.username,
                         alter_date=time.strftime("%Y-%m-%d %X", time.localtime())).save()
            oCmsViewStream = CmsViewStream(streamcontent=streamcontent, channel=channel, status=0)
            oCmsViewStream.save()
            if CMS_CHECK_ON:
                CmsCheck(channel_id=channel_id,
                         module=CmsModule.CONFIG_STREAM,
                         table_name='CmsViewStream',
                         data_id=oCmsViewStream.id,
                         op_type=CheckOpType.NEW,
                         is_show=0,
                         alter_person=request.user.username,
                         alter_date=time.strftime("%Y-%m-%d %X", time.localtime())).save()
            new_associate(channel_id, streamcontent.id, CONFIG_ITEMS.STREAMS, request)
            return HttpResponseRedirect(reverse("streams") + "?t=%d&c=%s&v=%s" % (t, c, v))
    else:
        form = CmsAdsForm()
    scenes = get_scenes()
    errors, fields = format_form(form)
    return render_to_response(template_name, {
        "scenes": scenes,
        "streams_type": streams_type,
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
def edit_streamsgroup(request, template_name):
    """
    编辑 内容流组
    url : url :{% url 'new_streamsgroup' %}?channel={{ channel }}&id={{ id }}
    :请求方式:Get
    :请求参数：id
    :返回数据：form 表单 scenes 场景列表 streams_type:类型
    :例如：scenes 场景列表 和之前一样 streams_type = [[1,"活动"],[2,"服务"],[3,"商品"],[4,"搜索"]]

    :请求方式：Post
    :请求参数：`type` `location`  `scene_id`
    """
    id = request.GET.get("id")
    channel_id = request.GET.get('channel')
    c, v, t = getCVT(channel_id)
    # 根据类型得到名称
    streamscontent = CmsStreamcontent.objects.get(id=id)
    text = get_nav_text(str(t))
    if request.method == 'POST':
        form = StreamcontentForm(request.POST, instance=streamscontent)
        if form.is_valid():
            form.save()
            if CMS_CHECK_ON:
                CmsCheck(channel_id=channel_id,
                         module=CmsModule.CONFIG_STREAM,
                         table_name='CmsStreamcontent',
                         data_id=id,
                         op_type=CheckOpType.EDIT,
                         alter_person=request.user.username,
                         alter_date=time.strftime("%Y-%m-%d %X", time.localtime())).save()
            return HttpResponseRedirect(reverse("streams") + "?t=%d&c=%s&v=%s" % (t, c, v))
    else:
        form = CmsAdsForm(instance=streamscontent)
    scenes = get_scenes()
    errors, fields = format_form(form)
    return render_to_response(template_name, {
        "scenes": scenes,
        "streams_type": streams_type,
        "fields": fields,
        "errors": errors,
        "t": t,
        "c": c,
        "v": v,
        "text": text,
        "channel": channel_id,
        "id": id
    }, context_instance=RequestContext(request))


@login_required
@permission_required(u'%s.%s' % (AuthCodeName.APP_LABEL, AuthCodeName.CONFIG), raise_exception=True)
def delete_streamsgroup(request):
    id = request.POST.get("id")
    channel_id = request.POST.get("channel")
    views = CmsViewStream.objects.filter(streamcontent_id=id)
    if CMS_CHECK_ON:
        for view in views:
            check = CmsCheck(
                channel_id=channel_id,
                module=CmsModule.CONFIG_STREAM,
                table_name="CmsViewStream",
                data_id=view.id,
                op_type=CheckOpType.DELETE,
                status=CheckStatu.WAIT_SUBMIT,
                is_show=0,
                alter_person=request.user.username,
                alter_date=time.strftime("%Y-%m-%d %X", time.localtime()))
            check.save()
    views.delete()
    streamcontentgoods = CmsStreamcontentsGoods.objects.filter(streamcontent_id=id)
    for streamcontentgood in streamcontentgoods:
        if CMS_CHECK_ON:
            check = CmsCheck(
                channel_id=channel_id,
                module=CmsModule.CONFIG_STREAM,
                table_name="CmsGoods",
                data_id=streamcontentgood.goods_id,
                op_type=CheckOpType.DELETE,
                status=CheckStatu.WAIT_SUBMIT,
                is_show=0,
                alter_person=request.user.username,
                alter_date=time.strftime("%Y-%m-%d %X", time.localtime()))
            check.save()
            check = CmsCheck(
                channel_id=channel_id,
                module=CmsModule.CONFIG_STREAM,
                table_name="CmsStreamcontentsGoods",
                data_id=streamcontentgood.id,
                op_type=CheckOpType.DELETE,
                status=CheckStatu.WAIT_SUBMIT,
                is_show=0,
                alter_person=request.user.username,
                alter_date=time.strftime("%Y-%m-%d %X", time.localtime()))
            check.save()
        streamcontentgood.goods.delete()
    streamcontentgoods.delete()
    streamcontentsbeans = CmsStreamcontentsBeans.objects.filter(streamcontent_id=id)
    for streamcontentsbean in streamcontentsbeans:
        if CMS_CHECK_ON:
            check = CmsCheck(
                channel_id=channel_id,
                module=CmsModule.CONFIG_STREAM,
                table_name="CmsStreamcontentbeans",
                data_id=streamcontentsbean.bean_id,
                op_type=CheckOpType.DELETE,
                status=CheckStatu.WAIT_SUBMIT,
                is_show=0,
                alter_person=request.user.username,
                alter_date=time.strftime("%Y-%m-%d %X", time.localtime()))
            check.save()
            check = CmsCheck(
                channel_id=channel_id,
                module=CmsModule.CONFIG_STREAM,
                table_name="CmsStreamcontentsBeans",
                data_id=streamcontentsbean.id,
                op_type=CheckOpType.DELETE,
                status=CheckStatu.WAIT_SUBMIT,
                is_show=0,
                alter_person=request.user.username,
                alter_date=time.strftime("%Y-%m-%d %X", time.localtime()))
            check.save()
        streamcontentsbean.bean.delete()
    streamcontentsbeans.delete()
    CmsStreamcontent.objects.get(id=id).delete()
    if CMS_CHECK_ON:
        check = CmsCheck(
            channel_id=channel_id,
            module=CmsModule.CONFIG_STREAM,
            table_name="CmsStreamcontent",
            data_id=id,
            op_type=CheckOpType.DELETE,
            status=CheckStatu.WAIT_SUBMIT,
            is_show=1,
            alter_person=request.user.username,
            alter_date=time.strftime("%Y-%m-%d %X", time.localtime()))
        check.save()
    return HttpResponse(0)


@login_required
@permission_required(u'%s.%s' % (AuthCodeName.APP_LABEL, AuthCodeName.CONFIG), raise_exception=True)
def new_goods(request):
    """
     新建 内容流 商品
    :请求方式：ajax Post
    :请求URL：{% url 'streams_new_goods' %}
    :请求参数：goods_id(商品id) group_id(内容流组id)
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
                goods_id = request.POST.get("goods_id")
                group_id = request.POST.get("group_id")
                channel_id = request.POST.get("channel_id")
                streamcontent = CmsStreamcontent.objects.get(id=group_id)
                goods = CmsGoods.objects.get(id=goods_id)
                goods.parent_id = goods_id
                goods.id = None
                goods.save()
                if CMS_CHECK_ON:
                    CmsCheck(channel_id=channel_id,
                             module=CmsModule.CONFIG_STREAM,
                             table_name='CmsGoods',
                             data_id=goods.id,
                             op_type=CheckOpType.NEW,
                             remark="增加了名称为%s的商品" % (CheckManager.wrap_style(goods.name),),
                             alter_person=request.user.username,
                             alter_date=time.strftime("%Y-%m-%d %X", time.localtime())).save()
                oCmsStreamcontentsGoods = CmsStreamcontentsGoods(streamcontent=streamcontent, goods=goods)
                oCmsStreamcontentsGoods.save()
                if CMS_CHECK_ON:
                    CmsCheck(channel_id=channel_id,
                             module=CmsModule.CONFIG_STREAM,
                             table_name='CmsStreamcontentsGoods',
                             data_id=oCmsStreamcontentsGoods.id,
                             op_type=CheckOpType.NEW,
                             is_show=0,
                             alter_person=request.user.username,
                             alter_date=time.strftime("%Y-%m-%d %X", time.localtime())).save()
            except Exception as ex:
                return HttpResponse(ex.args[0])
            return HttpResponse(0)


@login_required
@permission_required(u'%s.%s' % (AuthCodeName.APP_LABEL, AuthCodeName.CONFIG), raise_exception=True)
@add_main_var
def edit_goods(request, template_name):
    channel_id = request.GET.get('channel')
    c, v, t = getCVT(channel_id)
    text = get_nav_text(str(t))
    id = request.GET.get("id")
    if request.method == "POST":
        second_category = request.POST.get("second_category")
        if second_category:
            second_category = CmsNaviCategory.objects.get(id=second_category)
            if second_category.fatherid == 0:
                request.POST["category"] = request.POST["second_category"]
                request.POST['second_category'] = None
            else:
                request.POST["category"] = second_category.fatherid
        new_second_category = request.POST.get("new_second_category")
        if new_second_category:
            new_second_category = CmsNaviCategory.objects.get(id=new_second_category)
            if new_second_category.fatherid == 0:
                request.POST["new_category"] = request.POST["new_second_category"]
                request.POST['new_second_category'] = None
            else:
                request.POST["new_category"] = new_second_category.fatherid
        goods = CmsGoods.objects.get(id=id)
        request.POST['sort'] = goods.sort
        request.POST['is_support_cart'] = goods.is_support_cart
        request.POST['recommend_goodsId'] = goods.recommend_goodsId
        form = GoodsForm(request.POST, instance=goods)
        if form.is_valid():
            form.save()
            data = {}
            cate_fields = ['category', 'second_category', 'new_second_category', 'new_category', 'valid_time']
            for field in cate_fields:
                if request.POST.get(field):
                    data[field] = request.POST.get(field)
            # 更新同一goods_id的商品
            if data:
                CmsGoods.objects.filter(~Q(id=id), goods_id=goods.goods_id).update(**data)
                if INSTALL_TYPE == 2 or INSTALL_TYPE == 3:
                    sync_search(goods.goods_id, data)
            if CMS_CHECK_ON:
                CmsCheck(channel_id=channel_id,
                         module=CmsModule.CONFIG_STREAM,
                         table_name='CmsGoods',
                         data_id=id,
                         op_type=CheckOpType.EDIT,
                         alter_person=request.user.username,
                         alter_date=time.strftime("%Y-%m-%d %X", time.localtime())).save()
            return HttpResponseRedirect(reverse("streams") + "?t=%d&c=%s&v=%s" % (t, c, v))
    else:
        goods = CmsGoods.objects.get(id=id)
        form = GoodsForm(instance=goods)
    errors, fields = format_form(form)
    if 'second_category' in fields.keys() and fields['second_category'] == '""':
        fields['second_category'] = fields['category']
    if 'new_second_category' in fields.keys() and fields['new_second_category'] == '""':
        fields['new_second_category'] = fields['new_category']
    scenes = get_scenes()
    actions = get_actions_select()
    citygroups = get_city_group()
    cities = get_city_list()
    categories = get_categories()
    return render_to_response(template_name, {
        "scenes": scenes,
        "actions": actions,
        "categories": categories,
        "citygroups": citygroups,
        "cities": cities,
        "id": id,
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
def delete_goods(request):
    id = request.POST.get("id")
    channel_id = request.POST.get("channel")
    streamcontentsgood = CmsStreamcontentsGoods.objects.get(goods_id=id)
    if CMS_CHECK_ON:
        check = CmsCheck(
            channel_id=channel_id,
            module=CmsModule.CONFIG_STREAM,
            table_name="CmsStreamcontentsGoods",
            data_id=streamcontentsgood.id,
            op_type=CheckOpType.DELETE,
            status=CheckStatu.WAIT_SUBMIT,
            is_show=0,
            alter_person=request.user.username,
            alter_date=time.strftime("%Y-%m-%d %X", time.localtime()))
        check.save()
    streamcontentsgood.delete()
    CmsGoods.objects.get(id=id).delete()
    if CMS_CHECK_ON:
        check = CmsCheck(
            channel_id=channel_id,
            module=CmsModule.CONFIG_STREAM,
            table_name="CmsGoods",
            data_id=id,
            op_type=CheckOpType.DELETE,
            status=CheckStatu.WAIT_SUBMIT,
            is_show=1,
            alter_person=request.user.username,
            alter_date=time.strftime("%Y-%m-%d %X", time.localtime()))
        check.save()
    return HttpResponse(0)


@login_required
@permission_required(u'%s.%s' % (AuthCodeName.APP_LABEL, AuthCodeName.CONFIG), raise_exception=True)
def streams_exchange(request):
    id1 = request.POST.get("id1")
    type1 = request.POST.get("type1")
    id2 = request.POST.get("id2")
    type2 = request.POST.get("type2")
    channel_id = request.POST.get("channel")

    arr = [["0", CmsGoods], ["1", CmsStreamcontentbeans]]
    class1 = get_2array_value(arr, type1)
    class2 = get_2array_value(arr, type2)
    exchange_obj(class1, id1, class2, id2, channel_id, CmsModule.CONFIG_STREAM, request)
    return HttpResponse(0)


@login_required
@permission_required(u'%s.%s' % (AuthCodeName.APP_LABEL, AuthCodeName.CONFIG), raise_exception=True)
@add_main_var
def new_content_stream(request, template_name):
    """
    新建 内容流
    url :{% url 'new_content_stream' %}?channel={{ channel }}&id={{ id }}
    :请求方式:Get
    :请求参数：channel,id(内容流组id)
    :返回数据：form 表单 open_type 类别（actions 动作 cities 城市列表 citygroups 城市分组）（和之前一致）
    :例如：open_type [[0,"服务"],[1,"商品"]]

    :请求方式：Post
    :请求参数:input name 和数据库表cms_streamcontentbeans字段名称一致(除了id)
    :注意: 其他没有在input展示的要搞个input-hidden value = 0
    """
    channel_id = request.GET.get('channel')
    streamcontent_id = request.GET.get("group_id")
    c, v, t = getCVT(channel_id)
    # 根据类型得到名称
    text = get_nav_text(str(t))
    if request.method == 'POST':
        form = StreamcontentbeansForm(request.POST)
        if form.is_valid():
            streamcontentbeans = form.save()
            if CMS_CHECK_ON:
                CmsCheck(channel_id=channel_id,
                         module=CmsModule.CONFIG_STREAM,
                         table_name='CmsStreamcontentbeans',
                         data_id=streamcontentbeans.id,
                         op_type=CheckOpType.NEW,
                         alter_person=request.user.username,
                         alter_date=time.strftime("%Y-%m-%d %X", time.localtime())).save()
            oCmsStreamcontentsBeans = CmsStreamcontentsBeans(
                streamcontent=CmsStreamcontent.objects.get(id=streamcontent_id), bean=streamcontentbeans)
            oCmsStreamcontentsBeans.save()
            if CMS_CHECK_ON:
                CmsCheck(channel_id=channel_id,
                         module=CmsModule.CONFIG_STREAM,
                         table_name='CmsStreamcontentsBeans',
                         data_id=oCmsStreamcontentsBeans.id,
                         op_type=CheckOpType.NEW,
                         is_show=0,
                         alter_person=request.user.username,
                         alter_date=time.strftime("%Y-%m-%d %X", time.localtime())).save()
            return HttpResponseRedirect(reverse("streams") + "?t=%d&c=%s&v=%s" % (t, c, v))
    else:
        form = CmsAdsForm()
    actions = get_actions_select()
    cities = get_city_list()
    citygroups = get_city_group()
    errors, fields = format_form(form)
    return render_to_response(template_name, {
        "open_type": open_type,
        "actions": actions,
        "cities": cities,
        "citygroups": citygroups,
        "fields": fields,
        "errors": errors,
        "t": t,
        "c": c,
        "v": v,
        "text": text,
        "channel": channel_id,
        "group_id": streamcontent_id
    }, context_instance=RequestContext(request))


@login_required
@permission_required(u'%s.%s' % (AuthCodeName.APP_LABEL, AuthCodeName.CONFIG), raise_exception=True)
@add_main_var
def edit_content_stream(request, template_name):
    """
    编辑 内容流
    url :{% url 'new_content_stream' %}?channel={{ channel }}&id={{ id }}
    :请求方式:Get
    :请求参数：channel,id（内容流id）
    :返回数据：form 表单 open_type 类别（actions 动作 cities 城市列表 citygroups 城市分组）（和之前一致）
    :例如：open_type [[0,"服务"],[1,"商品"]]

    :请求方式：Post
    :请求参数:input name 和数据库表cms_streamcontentbeans字段名称一致(除了id)
    :注意: 其他没有在input展示的要搞个input-hidden value = 0
    """
    channel_id = request.GET.get('channel')
    id = request.GET.get("id")
    c, v, t = getCVT(channel_id)
    # 根据类型得到名称
    text = get_nav_text(str(t))
    if request.method == 'POST':
        beans = CmsStreamcontentbeans.objects.get(id=id)
        form = StreamcontentbeansForm(request.POST, instance=beans)
        if form.is_valid():
            form.save()
            if CMS_CHECK_ON:
                CmsCheck(channel_id=channel_id,
                         module=CmsModule.CONFIG_STREAM,
                         table_name='CmsStreamcontentbeans',
                         data_id=id,
                         op_type=CheckOpType.EDIT,
                         alter_person=request.user.username,
                         alter_date=time.strftime("%Y-%m-%d %X", time.localtime())).save()
            return HttpResponseRedirect(reverse("streams") + "?t=%d&c=%s&v=%s" % (t, c, v))
    else:
        beans = CmsStreamcontentbeans.objects.get(id=id)
        form = CmsAdsForm(instance=beans)
    actions = get_actions_select()
    cities = get_city_list()
    citygroups = get_city_group()
    errors, fields = format_form(form)
    return render_to_response(template_name, {
        "form": form,
        "open_type": open_type,
        "actions": actions,
        "cities": cities,
        "citygroups": citygroups,
        "fields": fields,
        "errors": errors,
        "t": t,
        "c": c,
        "v": v,
        "text": text,
        "channel": channel_id,
        "id": id
    }, context_instance=RequestContext(request))


@login_required
@permission_required(u'%s.%s' % (AuthCodeName.APP_LABEL, AuthCodeName.CONFIG), raise_exception=True)
def delete_content_stream(request):
    id = request.POST.get("id")
    channel_id = request.POST.get("channel")
    streamcontentsbeans = CmsStreamcontentsBeans.objects.get(bean_id=id)
    if CMS_CHECK_ON:
        check = CmsCheck(
            channel_id=channel_id,
            module=CmsModule.CONFIG_STREAM,
            table_name="CmsStreamcontentsBeans",
            data_id=streamcontentsbeans.id,
            op_type=CheckOpType.DELETE,
            status=CheckStatu.WAIT_SUBMIT,
            is_show=0,
            alter_person=request.user.username,
            alter_date=time.strftime("%Y-%m-%d %X", time.localtime()))
        check.save()
    streamcontentsbeans.delete()
    CmsStreamcontentbeans.objects.get(id=id).delete()
    if CMS_CHECK_ON:
        check = CmsCheck(
            channel_id=channel_id,
            module=CmsModule.CONFIG_STREAM,
            table_name="CmsStreamcontentbeans",
            data_id=id,
            op_type=CheckOpType.DELETE,
            status=CheckStatu.WAIT_SUBMIT,
            is_show=1,
            alter_person=request.user.username,
            alter_date=time.strftime("%Y-%m-%d %X", time.localtime()))
        check.save()
    return HttpResponse(0)


@login_required
def new_cp(request):
    return HttpResponse(0)


@login_required
@add_main_var
def edit_cp(request, template_name):
    return render_to_response(template_name, context_instance=RequestContext(request))


@login_required
@add_main_var
def del_cp(request):
    return HttpResponse(0)
