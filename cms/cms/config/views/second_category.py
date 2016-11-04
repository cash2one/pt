# coding: utf-8
# coding: utf-8

"""
    二级分类
"""
# from config.views.config_pub import *
# from config.forms import *
# from main.forms import *
import time

from cms.settings import CMS_CHECK_ON
from common.const import AuthCodeName, get_nav_text, CmsModule, CheckOpType, CONFIG_ITEMS, \
    CheckStatu
from common.views import get_check_status_str, analyze_shop_content, filter_none, CheckManager
from config.forms import CmsCategoryItemForm
from main.forms import CmsCategoryItembeanForm
from main.views.static_data import op_content_edit, op_content_save
from config.views.config_pub import new_associate, get_shops, get_services, exchange_obj
from main.models import CmsChannels, getCVT, CmsCategoryItem, get_scene_name, CmsCategoryItembean, get_valid_time, \
    get_city_str, CmsCheck, CmsViewCategoryitem, CmsCategoryitemItembean
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required, permission_required
import json
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from main.views.main_pub import add_main_var, get_city_list, get_city_group, format_form, get_scenes


# 二级分类列表页
@login_required
@add_main_var
def second_category(request, template_name):
    t = request.GET.get("t")
    if not t:
        t = "1"
    v = request.GET.get("v")
    c = request.GET.get("c")
    channel = CmsChannels.objects.get(channel_no=c, app_version__app_version=v, app_version__type_id=t).id
    shops = get_shops()
    return render_to_response(template_name, {
        "text": get_nav_text(t),
        "t": t,
        "v": v,
        "c": c,
        "channel": channel,
        "shops": shops
    }, context_instance=RequestContext(request))


@login_required
def search_second_category(request):
    channel = request.GET.get("channel")
    categories = CmsCategoryItem.objects.filter(cmsviewcategoryitem__channel_id=channel)
    result = []
    for category in categories:
        scene = get_scene_name(category.scene_id)
        status_str, status_int = get_check_status_str("CmsCategoryItem", category.id)
        item = {"group": [
            scene,
            category.sort,
            category.service.name,
            category.name,
            category.name_color,
            status_str,
            status_int,
            category.id
        ], "members": []}
        members = CmsCategoryItembean.objects.filter(cmscategoryitemitembean__category_item=category)
        for member in members:
            photoUrl, photo_str, search_show, s_key, search_category, home, weibo = analyze_shop_content(member)
            status_str, status_int = get_check_status_str("CmsCategoryItembean", member.id)
            item["members"].append([
                member.item_id,
                photoUrl,
                member.name,
                member.sort,
                photo_str,
                search_show,
                search_category,
                s_key,
                member.search_sort,
                get_valid_time(member.valid_time),
                get_city_str(member.city),
                status_str,
                status_int,
                member.id
            ])
        item["members"].sort(key=lambda o: (o[3]))
        result.append(item)
    filter_none(result)
    result.sort(key=lambda o: (o["group"][0], o["group"][1]))
    return HttpResponse(json.dumps(result))


# 新增二级分类
@login_required
@permission_required(u'%s.%s' % (AuthCodeName.APP_LABEL, AuthCodeName.CONFIG), raise_exception=True)
@add_main_var
def new_second_category(request, template_name):
    """
    新建二级分类
    url :{% url 'sc_new_second_category' %}?channel={{ channel }}
    :请求方式: Get
    :请求参数：channel
    :返回数据：form 表单 scenes 场景列表 services 服务列表
    :例如：scenes 场景列表 和之前一样 streams_type = [[1,"活动"],[2,"服务"],[3,"商品"],[4,"搜索"]]

    :请求方式：Post
    :请求参数：
    """
    channel_id = request.GET.get('channel')
    c, v, t = getCVT(channel_id)
    channel = CmsChannels.objects.get(id=channel_id)
    # 根据类型得到名称
    text = get_nav_text(str(t))
    if request.method == 'POST':
        form = CmsCategoryItemForm(request.POST)
        if form.is_valid():
            category_item = form.save()
            if CMS_CHECK_ON:
                CmsCheck(channel_id=channel_id,
                         module=CmsModule.CONFIG_SECOND_CATEGORY,
                         table_name='CmsCategoryItem',
                         data_id=category_item.id,
                         op_type=CheckOpType.NEW,
                         alter_person=request.user.username,
                         alter_date=time.strftime("%Y-%m-%d %X", time.localtime())).save()
            oCmsViewCategoryitem = CmsViewCategoryitem(category_item=category_item, channel=channel)
            oCmsViewCategoryitem.save()
            if CMS_CHECK_ON:
                CmsCheck(channel_id=channel_id,
                         module=CmsModule.CONFIG_SECOND_CATEGORY,
                         table_name='CmsViewCategoryitem',
                         data_id=oCmsViewCategoryitem.id,
                         op_type=CheckOpType.NEW,
                         is_show=0,
                         alter_person=request.user.username,
                         alter_date=time.strftime("%Y-%m-%d %X", time.localtime())).save()
            new_associate(channel_id, category_item.id, CONFIG_ITEMS.SECOND_CATEGORY, request)
            return HttpResponseRedirect(reverse("second_category") + "?t=%d&c=%s&v=%s" % (t, c, v))
    else:
        form = CmsCategoryItemForm()
    scenes = get_scenes()
    services = get_services()
    errors, fields = format_form(form)
    return render_to_response(template_name, {
        "scenes": scenes,
        "services": services,
        "fields": fields,
        "errors": errors,
        "t": t,
        "c": c,
        "v": v,
        "text": text,
        "channel": channel_id
    }, context_instance=RequestContext(request))


# 编辑二级分类
@login_required
@permission_required(u'%s.%s' % (AuthCodeName.APP_LABEL, AuthCodeName.CONFIG), raise_exception=True)
@add_main_var
def edit_second_category(request, template_name):
    """
    编辑二级分类
    url :{% url 'sc_edit_second_category' %}?channel={{ channel }}&id={{ id }}
    :请求方式: Get
    :请求参数：channel,id
    :返回数据：form 表单 scenes 场景列表 services 服务列表
    :例如：scenes 场景列表 和之前一样 streams_type = [[1,"活动"],[2,"服务"],[3,"商品"],[4,"搜索"]]

    :请求方式：Post
    :请求参数：
    """
    channel_id = request.GET.get('channel')
    id = request.GET.get("id")
    category_item = CmsCategoryItem.objects.get(id=id)
    c, v, t = getCVT(channel_id)
    # 根据类型得到名称
    text = get_nav_text(str(t))
    if request.method == 'POST':
        form = CmsCategoryItemForm(request.POST, instance=category_item)
        if form.is_valid():
            form.save()
            if CMS_CHECK_ON:
                CmsCheck(channel_id=channel_id,
                         module=CmsModule.CONFIG_SECOND_CATEGORY,
                         table_name='CmsCategoryItem',
                         data_id=id,
                         op_type=CheckOpType.EDIT,
                         alter_person=request.user.username,
                         alter_date=time.strftime("%Y-%m-%d %X", time.localtime())).save()
            return HttpResponseRedirect(reverse("second_category") + "?t=%d&c=%s&v=%s" % (t, c, v))
    else:
        form = CmsCategoryItemForm(instance=category_item)
    scenes = get_scenes()
    services = get_services()
    errors, fields = format_form(form)
    return render_to_response(template_name, {
        "scenes": scenes,
        "services": services,
        "fields": fields,
        "errors": errors,
        "t": t,
        "c": c,
        "v": v,
        "text": text,
        "channel": channel_id,
        "id": id
    }, context_instance=RequestContext(request))


# 新增二级分类
@login_required
@permission_required(u'%s.%s' % (AuthCodeName.APP_LABEL, AuthCodeName.CONFIG), raise_exception=True)
@add_main_var
def new_shop(request):
    """
     新建二级分类 商户
    :请求方式：ajax Post
    :请求URL：{% url 'sc_new_shop' %}
    :请求参数：shop_id 商户id category_item_id 二级分类id
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
                shop_id = request.POST.get("shop_id")
                category_item_id = request.POST.get("category_item_id")
                channel_id = request.POST.get("channel_id")
                category_itembean = CmsCategoryItembean.objects.get(id=shop_id)
                category_itembean.parent_id = shop_id
                category_itembean.id = None
                category_itembean.save()
                if CMS_CHECK_ON:
                    CmsCheck(channel_id=channel_id,
                             module=CmsModule.CONFIG_SECOND_CATEGORY,
                             table_name='CmsCategoryItembean',
                             data_id=category_itembean.id,
                             op_type=CheckOpType.NEW,
                             remark="添加商户名为%s的商户" % CheckManager.wrap_style(category_itembean.name),
                             alter_person=request.user.username,
                             alter_date=time.strftime("%Y-%m-%d %X", time.localtime())).save()
                oCmsCategoryitemItembean = CmsCategoryitemItembean(
                    category_item=CmsCategoryItem.objects.get(id=category_item_id), item_bean=category_itembean)
                oCmsCategoryitemItembean.save()
                if CMS_CHECK_ON:
                    CmsCheck(channel_id=channel_id,
                             module=CmsModule.CONFIG_SECOND_CATEGORY,
                             table_name='CmsCategoryitemItembean',
                             data_id=oCmsCategoryitemItembean.id,
                             op_type=CheckOpType.NEW,
                             is_show=0,
                             alter_person=request.user.username,
                             alter_date=time.strftime("%Y-%m-%d %X", time.localtime())).save()
            except Exception as ex:
                return HttpResponse(ex.args[0])
            return HttpResponse(0)


# 编辑二级分类
@login_required
@permission_required(u'%s.%s' % (AuthCodeName.APP_LABEL, AuthCodeName.CONFIG), raise_exception=True)
@add_main_var
def edit_shop(request, template_name):
    """
    编辑二级 商户
    url :{% url 'sc_edit_shop' %}?channel={{ channel }}&id={{ id }}
    :请求方式: Get
    :请求参数：无
    :返回数据： citygroups 城市分组列表，cities 所有城市(列表)
    :[[id,name],[id,name],....]

    :请求方式：Post
    :请求参数：cms_category_itembean字段(input name)
    """
    channel_id = request.GET.get('channel')
    id = request.GET.get("id")
    c, v, t = getCVT(channel_id)
    # 根据类型得到名称
    text = get_nav_text(str(t))
    categoryitembean = CmsCategoryItembean.objects.get(id=id)
    if request.method == "POST":
        postcopys = request.POST.copy()
        content = op_content_save(postcopys)
        postcopys["content"] = json.dumps(content, ensure_ascii=False)
        form = CmsCategoryItembeanForm(postcopys, instance=categoryitembean)
        if form.is_valid():
            form.save()
            if CMS_CHECK_ON:
                CmsCheck(channel_id=channel_id,
                         module=CmsModule.CONFIG_SECOND_CATEGORY,
                         table_name='CmsCategoryItembean',
                         data_id=id,
                         op_type=CheckOpType.EDIT,
                         alter_person=request.user.username,
                         alter_date=time.strftime("%Y-%m-%d %X", time.localtime())).save()
            return HttpResponseRedirect(reverse("second_category") + "?t=%d&c=%s&v=%s" % (t, c, v))
    else:
        form = CmsCategoryItembeanForm(instance=categoryitembean)
    errors, fields = format_form(form)
    fields = op_content_edit(fields)
    citygroups = get_city_group()
    cities = get_city_list()
    return render_to_response(template_name, {
        "fields": fields,
        "errors": errors,
        "citygroups": citygroups,
        "cities": cities,
        "t": t,
        "c": c,
        "v": v,
        "text": text,
        "channel": channel_id,
        "id": id,
    }, context_instance=RequestContext(request))


# 删除二级分类
@login_required
@permission_required(u'%s.%s' % (AuthCodeName.APP_LABEL, AuthCodeName.CONFIG), raise_exception=True)
def delete_second_category(request):
    id = request.POST.get("id")
    channel_id = request.POST.get("channel")
    views = CmsViewCategoryitem.objects.filter(category_item_id=id)
    if CMS_CHECK_ON:
        for view in views:
            check = CmsCheck(
                channel_id=channel_id,
                module=CmsModule.CONFIG_SECOND_CATEGORY,
                table_name="CmsViewCategoryitem",
                data_id=view.id,
                op_type=CheckOpType.DELETE,
                status=CheckStatu.WAIT_SUBMIT,
                is_show=0,
                alter_person=request.user.username,
                alter_date=time.strftime("%Y-%m-%d %X", time.localtime()))
            check.save()
    views.delete()
    categoryitembeans = CmsCategoryitemItembean.objects.filter(category_item_id=id)
    for categoryitembean in categoryitembeans:
        if CMS_CHECK_ON:
            check = CmsCheck(
                channel_id=channel_id,
                module=CmsModule.CONFIG_SECOND_CATEGORY,
                table_name="CmsCategoryItembean",
                data_id=categoryitembean.item_bean_id,
                op_type=CheckOpType.DELETE,
                status=CheckStatu.WAIT_SUBMIT,
                is_show=0,
                alter_person=request.user.username,
                alter_date=time.strftime("%Y-%m-%d %X", time.localtime()))
            check.save()
            check = CmsCheck(
                channel_id=channel_id,
                module=CmsModule.CONFIG_SECOND_CATEGORY,
                table_name="CmsCategoryitemItembean",
                data_id=categoryitembean.id,
                op_type=CheckOpType.DELETE,
                status=CheckStatu.WAIT_SUBMIT,
                is_show=0,
                alter_person=request.user.username,
                alter_date=time.strftime("%Y-%m-%d %X", time.localtime()))
            check.save()
        categoryitembean.item_bean.delete()
    categoryitembeans.delete()
    CmsCategoryItem.objects.get(id=id).delete()
    if CMS_CHECK_ON:
        check = CmsCheck(
            channel_id=channel_id,
            module=CmsModule.CONFIG_SECOND_CATEGORY,
            table_name="CmsCategoryItem",
            data_id=id,
            op_type=CheckOpType.DELETE,
            status=CheckStatu.WAIT_SUBMIT,
            is_show=1,
            alter_person=request.user.username,
            alter_date=time.strftime("%Y-%m-%d %X", time.localtime()))
        check.save()
    return HttpResponse(0)


# 删除商家
@login_required
@permission_required(u'%s.%s' % (AuthCodeName.APP_LABEL, AuthCodeName.CONFIG), raise_exception=True)
def delete_shop(request):
    id = request.POST.get("id")
    channel_id = request.POST.get("channel")
    oCmsCategoryitemItembean = CmsCategoryitemItembean.objects.get(item_bean_id=id)
    if CMS_CHECK_ON:
        check = CmsCheck(
            channel_id=channel_id,
            module=CmsModule.CONFIG_SECOND_CATEGORY,
            table_name="CmsCategoryitemItembean",
            data_id=oCmsCategoryitemItembean.id,
            op_type=CheckOpType.DELETE,
            status=CheckStatu.WAIT_SUBMIT,
            is_show=0,
            alter_person=request.user.username,
            alter_date=time.strftime("%Y-%m-%d %X", time.localtime()))
        check.save()
    oCmsCategoryitemItembean.delete()
    CmsCategoryItembean.objects.get(id=id).delete()
    if CMS_CHECK_ON:
        check = CmsCheck(
            channel_id=channel_id,
            module=CmsModule.CONFIG_SECOND_CATEGORY,
            table_name="CmsCategoryItembean",
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
def exchange(request):
    id1 = request.POST.get("id1")
    id2 = request.POST.get("id2")
    channel_id = request.POST.get("channel")
    exchange_obj(CmsCategoryItembean, id1, CmsCategoryItembean, id2, channel_id, CmsModule.CONFIG_SECOND_CATEGORY,
                 request, "sort", "sort")
    return HttpResponse(0)
