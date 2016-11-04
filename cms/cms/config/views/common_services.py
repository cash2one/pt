# coding: utf-8

"""
    常用服务
"""
from django.db.models import Q
from django.views.decorators.http import require_POST

from cms.settings import INSTALL_TYPE
# from config.views.config_pub import *
# from main.forms import *
from main.forms import ServiceForm, GoodsForm, NaviCategoryForm, CmsCategoryGroup
from main.views.interface_category import sync_search
import time
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required, permission_required
import json
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

from common.const import AuthCodeName, get_nav_text, CmsModule, CheckOpType, CONFIG_ITEMS, \
    CheckStatu, CategoryGroupType, CATE_TYPE, get_2array_value
from common.views import get_check_status_str, filter_none, CheckManager, get_relate_channel_list
from config.views.config_pub import CMS_CHECK_ON, CmsCheck, new_associate, exchange_obj, get_services, get_goods
from main.models import CmsChannels, get_valid_time, get_city_str, \
    getCVT, CmsViewService, CmsServices, CmsNaviCategory, CmsGoods, CmsViewGroupCategory
from main.views.main_pub import add_main_var, get_city_list, get_city_group, format_form, get_categories, \
    get_v37_categories, get_actions_select, get_scenes, show_style_list, get_first_categories


@login_required
@add_main_var
def common_services(request, template_name):
    t = request.GET.get("t")
    if not t:
        t = "1"
    v = request.GET.get("v")
    c = request.GET.get("c")
    channel = CmsChannels.objects.get(channel_no=c, app_version__app_version=v, app_version__type_id=t).id
    services = get_services()
    goods = get_goods()
    if v[0].isdigit() and v >= '3.7.0':
        categories = get_v37_categories()
    else:
        categories = get_categories()
    return render_to_response(template_name, {
        "text": get_nav_text(t),
        "t": t,
        "v": v,
        "c": c,
        "channel": channel,
        "services": services,
        "goods": goods,
        "categories": categories,
    }, context_instance=RequestContext(request))


@login_required
def search_common_services(request):
    channel = request.GET.get("channel")
    items = []
    # 添加服务
    view_services = CmsViewService.objects.filter(open_type=0, channel__id=channel)
    for view_service in view_services:
        try:
            status_str, status_int = get_check_status_str("CmsServices", view_service.service_id)
            items.append(["功能服务", "服务", status_str, "%d/%d" % (status_int, status_int),
                          CmsServices.objects.get(id=view_service.service_id)])
        except:
            continue
    # 添加商品
    view_goods = CmsViewService.objects.filter(open_type=1, channel__id=channel)
    for view_good in view_goods:
        try:
            status_str, status_int = get_check_status_str("CmsGoods", view_good.service_id)
            items.append(["功能服务", "商品", status_str, "%d/%d" % (status_int, status_int),
                          CmsGoods.objects.get(id=view_good.service_id)])
        except:
            continue
    # 添加一级分类
    view_first_categories = CmsViewService.objects.filter(open_type=3, channel__id=channel)
    for view_first_category in view_first_categories:
        try:
            status_str_cate, status_int_cate = get_check_status_str("CmsNaviCategory", view_first_category.service_id)
            status_str_view, status_int_view = get_check_status_str("CmsViewService", view_first_category.id)
            items.append(["功能服务", "功能一级分类", status_str_view, "%d/%d" % (status_int_cate, status_int_view),
                          CmsNaviCategory.objects.get(id=view_first_category.service_id)])
        except:
            continue
    # 添加二级分类
    view_second_categories = CmsViewService.objects.filter(open_type=4, channel__id=channel)
    for view_second_category in view_second_categories:
        try:
            status_str_cate, status_int_cate = get_check_status_str("CmsNaviCategory", view_second_category.service_id)
            status_str_view, status_int_view = get_check_status_str("CmsViewService", view_second_category.id)
            items.append(["功能服务", "功能二级分类", status_str_view, "%d/%d" % (status_int_cate, status_int_view),
                          CmsNaviCategory.objects.get(id=view_second_category.service_id)])
        except:
            continue
    # 添加到家服务
    view_second_categories = CmsViewService.objects.filter(open_type=5, channel__id=channel)
    for view_second_category in view_second_categories:
        try:
            status_str_cate, status_int_cate = get_check_status_str("CmsNaviCategory", view_second_category.service_id)
            status_str_view, status_int_view = get_check_status_str("CmsViewService", view_second_category.id)
            items.append(["到家服务", "到家一级分类", status_str_view, "%d/%d" % (status_int_cate, status_int_view),
                          CmsNaviCategory.objects.get(id=view_second_category.service_id)])
        except:
            continue
    # 添加到家服务
    view_second_categories = CmsViewService.objects.filter(open_type=6, channel__id=channel)
    for view_second_category in view_second_categories:
        try:
            status_str_cate, status_int_cate = get_check_status_str("CmsNaviCategory", view_second_category.service_id)
            status_str_view, status_int_view = get_check_status_str("CmsViewService", view_second_category.id)
            items.append(["到家服务", "到家二级分类", status_str_view, "%d/%d" % (status_int_cate, status_int_view),
                          CmsNaviCategory.objects.get(id=view_second_category.service_id)])
        except:
            continue
    result = []
    for group, type, status_str, status_int, item in items:
        # scene_name = get_scene_name(item.scene_id)
        if type == "服务" or type == "商品":
            location = item.location
        else:
            location = item.location2
        temp = [
            # scene_name,
            group,
            location,
            item.icon_url,
            item.name,
            item.dot_info,
            item.action_id,
            get_valid_time(item.valid_time),
            get_city_str(item.city),
            type,
            status_str,
            status_int,
            item.id
        ]
        result.append(temp)
    filter_none(result)
    result.sort(key=lambda o: (o[0], o[1]))
    return HttpResponse(json.dumps(result))


@login_required
@permission_required(u'%s.%s' % (AuthCodeName.APP_LABEL, AuthCodeName.CONFIG), raise_exception=True)
def exchange_common_service(request):
    id1 = request.POST.get("id1")
    type1 = request.POST.get("type1")
    id2 = request.POST.get("id2")
    type2 = request.POST.get("type2")
    channel_id = request.POST.get("channel")

    arr = [
        ["服务", [CmsServices, "location"]],
        ["商品", [CmsGoods, "location"]],
        ["功能一级分类", [CmsNaviCategory, "location2"]],
        ["功能二级分类", [CmsNaviCategory, "location2"]],
        ["到家一级分类", [CmsNaviCategory, "location2"]],
        ["到家二级分类", [CmsNaviCategory, "location2"]]
    ]
    class1, word1 = get_2array_value(arr, type1)
    class2, word2 = get_2array_value(arr, type2)
    exchange_obj(class1, id1, class2, id2, channel_id, CmsModule.CONFIG_COMMON_SERVICES, request, word1=word1,
                 word2=word2)
    return HttpResponse(0)


@login_required
@permission_required(u'%s.%s' % (AuthCodeName.APP_LABEL, AuthCodeName.CONFIG), raise_exception=True)
def delete_common_service(request):
    id = request.POST.get("id")
    channel = request.POST.get("channel")
    views = CmsViewService.objects.filter(service_id=id, open_type=0)
    for view in views:
        if CMS_CHECK_ON:
            check = CmsCheck(
                channel_id=channel,
                module=CmsModule.CONFIG_COMMON_SERVICES,
                table_name="CmsViewService",
                data_id=view.id,
                op_type=CheckOpType.DELETE,
                status=CheckStatu.WAIT_SUBMIT,
                is_show=0,
                alter_person=request.user.username,
                alter_date=time.strftime("%Y-%m-%d %X", time.localtime()))
            check.save()
        view.delete()
    CmsServices.objects.get(id=id).delete()
    if CMS_CHECK_ON:
        check = CmsCheck(
            channel_id=channel,
            module=CmsModule.CONFIG_COMMON_SERVICES,
            table_name="CmsServices",
            data_id=id,
            op_type=CheckOpType.DELETE,
            status=CheckStatu.WAIT_SUBMIT,
            is_show=1,
            alter_person=request.user.username,
            alter_date=time.strftime("%Y-%m-%d %X", time.localtime()))
        check.save()
    return HttpResponse(0)


# 新增常用服务
@login_required
@permission_required(u'%s.%s' % (AuthCodeName.APP_LABEL, AuthCodeName.CONFIG), raise_exception=True)
@require_POST
def new_common_service(request):
    """
     新建服务导航 服务
    :请求方式：ajax Post
    :请求参数：service_id  channel_id
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
            service_id = request.POST.get("service_id")
            channel_id = request.POST.get("channel_id")
            services = CmsServices.objects.get(id=service_id)
            services.type = 1
            services.parent_id = service_id
            services.id = None
            services.save()
            try:
                if CMS_CHECK_ON:
                    CmsCheck(channel_id=channel_id,
                             module=CmsModule.CONFIG_COMMON_SERVICES,
                             table_name='CmsServices',
                             data_id=services.id,
                             op_type=CheckOpType.NEW,
                             remark="增加了名称为%s的服务" % (CheckManager.wrap_style(services.name),),
                             alter_person=request.user.username,
                             alter_date=time.strftime("%Y-%m-%d %X", time.localtime())).save()
                oCmsViewService = CmsViewService(service_id=services.id, channel=CmsChannels.objects.get(id=channel_id),
                                                 open_type=0)
                oCmsViewService.save()
                if CMS_CHECK_ON:
                    CmsCheck(channel_id=channel_id,
                             module=CmsModule.CONFIG_COMMON_SERVICES,
                             table_name='CmsViewService',
                             data_id=oCmsViewService.id,
                             op_type=CheckOpType.NEW,
                             is_show=0,
                             alter_person=request.user.username,
                             alter_date=time.strftime("%Y-%m-%d %X", time.localtime())).save()
                new_associate(channel_id, services.id, CONFIG_ITEMS.COMMON_SERVICES, request)
            except Exception as ex:
                if 'Duplicate entry' in ex.args[0]:
                    return HttpResponse(1)
                return HttpResponse(ex.args[0])
            return HttpResponse(0)


# 编辑常用服务
@login_required
@permission_required(u'%s.%s' % (AuthCodeName.APP_LABEL, AuthCodeName.CONFIG), raise_exception=True)
@add_main_var
def edit_common_service(request, template_name):
    channel_id = request.GET.get('channel')
    c, v, t = getCVT(channel_id)
    text = get_nav_text(str(t))
    id = request.GET.get("id")
    if request.method == "POST":
        services = CmsServices.objects.get(id=id)
        form = ServiceForm(request.POST, instance=services)
        if form.is_valid():
            form.save()
            if CMS_CHECK_ON:
                CmsCheck(channel_id=channel_id,
                         module=CmsModule.CONFIG_COMMON_SERVICES,
                         table_name='CmsServices',
                         data_id=id,
                         op_type=CheckOpType.EDIT,
                         alter_person=request.user.username,
                         alter_date=time.strftime("%Y-%m-%d %X", time.localtime())).save()
            return HttpResponseRedirect(reverse("common_services") + "?t=%d&c=%s&v=%s" % (t, c, v))
    else:
        services = CmsServices.objects.get(id=id)
        form = ServiceForm(instance=services)
    errors, fields = format_form(form)
    scenes = get_scenes()
    actions = get_actions_select()
    citygroups = get_city_group()
    cities = get_city_list()
    return render_to_response(template_name, {
        "scenes": scenes,
        "actions": actions,
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


# 新增常用商品
@login_required
@permission_required(u'%s.%s' % (AuthCodeName.APP_LABEL, AuthCodeName.CONFIG), raise_exception=True)
@require_POST
def new_common_goods(request):
    """
     新建 服务导航 常用商品
    :请求方式：ajax Post
    :请求URL：{% url 'new_common_goods' %}
    :请求参数：goods_id  channel_id
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
            goods_id = request.POST.get("goods_id")
            channel_id = request.POST.get("channel_id")
            try:
                goods = CmsGoods.objects.get(id=goods_id)
                goods.parent_id = goods_id
                goods.id = None
                goods.save()
                if CMS_CHECK_ON:
                    CmsCheck(channel_id=channel_id,
                             module=CmsModule.CONFIG_COMMON_SERVICES,
                             table_name='CmsGoods',
                             data_id=goods.id,
                             op_type=CheckOpType.NEW,
                             remark="增加了名称为%s的商品" % (CheckManager.wrap_style(goods.name),),
                             alter_person=request.user.username,
                             alter_date=time.strftime("%Y-%m-%d %X", time.localtime())).save()
                oCmsViewService = CmsViewService(service_id=goods.id, channel=CmsChannels.objects.get(id=channel_id),
                                                 open_type=1)
                oCmsViewService.save()
                if CMS_CHECK_ON:
                    CmsCheck(channel_id=channel_id,
                             module=CmsModule.CONFIG_COMMON_SERVICES,
                             table_name='CmsViewService',
                             data_id=oCmsViewService.id,
                             op_type=CheckOpType.NEW,
                             is_show=0,
                             alter_person=request.user.username,
                             alter_date=time.strftime("%Y-%m-%d %X", time.localtime())).save()
                new_associate(channel_id, goods.id, CONFIG_ITEMS.COMMON_SERVICES, request, open=1)
            except Exception as ex:
                if 'Duplicate entry' in ex.args[0]:
                    return HttpResponse(1)
                return HttpResponse(ex.args[0])
            return HttpResponse(0)


# 编辑常用商品
@login_required
@permission_required(u'%s.%s' % (AuthCodeName.APP_LABEL, AuthCodeName.CONFIG), raise_exception=True)
@add_main_var
def edit_common_goods(request, template_name):
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
                         module=CmsModule.CONFIG_COMMON_SERVICES,
                         table_name='CmsGoods',
                         data_id=id,
                         op_type=CheckOpType.EDIT,
                         alter_person=request.user.username,
                         alter_date=time.strftime("%Y-%m-%d %X", time.localtime())).save()
            return HttpResponseRedirect(reverse("common_services") + "?t=%d&c=%s&v=%s" % (t, c, v))
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


# 删除常用商品
@login_required
@permission_required(u'%s.%s' % (AuthCodeName.APP_LABEL, AuthCodeName.CONFIG), raise_exception=True)
def delete_common_goods(request):
    id = request.POST.get("id")
    channel = request.POST.get("channel")
    views = CmsViewService.objects.filter(service_id=id, open_type=1)
    for view in views:
        if CMS_CHECK_ON:
            check = CmsCheck(
                channel_id=channel,
                module=CmsModule.CONFIG_COMMON_SERVICES,
                table_name="CmsViewService",
                data_id=view.id,
                op_type=CheckOpType.DELETE,
                status=CheckStatu.WAIT_SUBMIT,
                is_show=0,
                alter_person=request.user.username,
                alter_date=time.strftime("%Y-%m-%d %X", time.localtime()))
            check.save()
        view.delete()
    CmsGoods.objects.get(id=id).delete()
    if CMS_CHECK_ON:
        check = CmsCheck(
            channel_id=channel,
            module=CmsModule.CONFIG_COMMON_SERVICES,
            table_name="CmsGoods",
            data_id=id,
            op_type=CheckOpType.DELETE,
            status=CheckStatu.WAIT_SUBMIT,
            is_show=1,
            alter_person=request.user.username,
            alter_date=time.strftime("%Y-%m-%d %X", time.localtime()))
        check.save()
    return HttpResponse(0)


# 新增常用分类
@login_required
@permission_required(u'%s.%s' % (AuthCodeName.APP_LABEL, AuthCodeName.CONFIG), raise_exception=True)
@require_POST
def new_common_category(request):
    """
    常用服务  新建常用分类
    :请求方式：ajax Post
    :请求URL：{% url 'new_common_category' %}
    :请求参数：category_id  channel_id
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
            # navicategory.parent_id = category_id
            # navicategory.id = None
            # navicategory.save()
            try:
                category_id = request.POST.get("category_id")
                channel_id = request.POST.get("channel_id")
                navicategory = CmsNaviCategory.objects.get(id=category_id)
                if navicategory.fatherid != 0:
                    group_name = CmsViewGroupCategory.objects.get(category_id=navicategory.fatherid).group.name
                else:
                    group_name = CmsViewGroupCategory.objects.get(category=navicategory).group.name
                if group_name == CategoryGroupType.daojia:
                    open_type = 6
                    if navicategory.fatherid == 0:
                        open_type = 5
                else:
                    open_type = 4
                    if navicategory.fatherid == 0:
                        open_type = 3
                oCmsViewService = CmsViewService(service_id=category_id, channel=CmsChannels.objects.get(id=channel_id),
                                                 open_type=open_type)
                oCmsViewService.save()
                if CMS_CHECK_ON:
                    CmsCheck(channel_id=channel_id,
                             module=CmsModule.CONFIG_COMMON_SERVICES,
                             table_name='CmsViewService',
                             data_id=oCmsViewService.id,
                             op_type=CheckOpType.NEW,
                             remark="增加了名称为%s的%d级分类" % (CheckManager.wrap_style(navicategory.name), open_type - 2),
                             alter_person=request.user.username,
                             alter_date=time.strftime("%Y-%m-%d %X", time.localtime())).save()
                new_associate(channel_id, navicategory.id, CONFIG_ITEMS.COMMON_SERVICES, request, open=open_type)
            except Exception as ex:
                if 'Duplicate entry' in ex.args[0]:
                    return HttpResponse(1)
                return HttpResponse(ex.args[0])
            return HttpResponse(0)


@login_required
@permission_required(u'%s.%s' % (AuthCodeName.APP_LABEL, AuthCodeName.CONFIG), raise_exception=True)
@add_main_var
def edit_common_category_first(request, template_name):
    """
    配置库 编辑一级分类
    url :{% url 'edit_common_category_first' %}?channel={{ channel }}&id={{ id }}
    :请求方式: Get
    :请求参数：channel,id
    :返回数据：和之前一样
    :例如：

    :请求方式：Post
    :请求参数：
    """
    channel_id = request.GET.get('channel')
    c, v, t = getCVT(channel_id)
    text = get_nav_text(str(t))
    id = request.GET.get("id")
    category = CmsNaviCategory.objects.get(id=id)
    if request.method == "POST":
        form = NaviCategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            cate_group_id = request.POST.get("cate_group_id")
            if CmsViewGroupCategory.objects.filter(category=category):
                ins_viewgroupcate = CmsViewGroupCategory.objects.get(category=category)
                ins_viewgroupcate.group_id = cate_group_id
                ins_viewgroupcate.save()
            else:
                CmsViewGroupCategory(category=category, group_id=cate_group_id).save()
            if CMS_CHECK_ON:
                CmsCheck(module=CmsModule.MAIN_CATEGORY,
                         table_name='CmsNaviCategory',
                         data_id=id,
                         op_type=CheckOpType.EDIT,
                         alter_person=request.user.username,
                         alter_date=time.strftime("%Y-%m-%d %X", time.localtime())).save()
            return HttpResponseRedirect(reverse("common_services") + "?t=%d&c=%s&v=%s" % (t, c, v))
    else:
        form = NaviCategoryForm(instance=category)
    errors, fields = format_form(form)
    if CmsViewGroupCategory.objects.filter(category=category):
        ins_viewgroupcate = CmsViewGroupCategory.objects.get(category=category)
        fields["cate_group_id"] = json.dumps(ins_viewgroupcate.group_id)
    scenes = get_scenes()
    actions = get_actions_select()
    citygroups = get_city_group()
    cities = get_city_list()
    cate_groups = CmsCategoryGroup.objects.all()
    return render_to_response(template_name, {
        "scenes": scenes,
        "actions": actions,
        "citygroups": citygroups,
        "cities": cities,
        "show_style_list": show_style_list,
        "id": id,
        "fields": fields,
        "errors": errors,
        "t": t,
        "c": c,
        "v": v,
        "text": text,
        "channel": channel_id,
        "cate_groups": cate_groups,
        "CATE_TYPE": CATE_TYPE
    }, context_instance=RequestContext(request))


@login_required
@permission_required(u'%s.%s' % (AuthCodeName.APP_LABEL, AuthCodeName.CONFIG), raise_exception=True)
@add_main_var
def edit_common_category_second(request, template_name):
    """
    配置库 编辑二级分类
    url :{% url 'edit_common_category_second' %}?channel={{ channel }}&id={{ id }}
    :请求方式: Get
    :请求参数：channel,id
    :返回数据：和之前一样
    :例如：

    :请求方式：Post
    :请求参数：
    """
    channel_id = request.GET.get('channel')
    c, v, t = getCVT(channel_id)
    text = get_nav_text(str(t))
    id = request.GET.get("id")
    if request.method == "POST":
        oNaviCategory = CmsNaviCategory.objects.get(id=id)
        form = NaviCategoryForm(request.POST, instance=oNaviCategory)
        if form.is_valid():
            form.save()
            if CMS_CHECK_ON:
                CmsCheck(module=CmsModule.MAIN_CATEGORY,
                         table_name='CmsNaviCategory',
                         data_id=id,
                         op_type=CheckOpType.EDIT,
                         alter_person=request.user.username,
                         alter_date=time.strftime("%Y-%m-%d %X", time.localtime())).save()
            return HttpResponseRedirect(reverse("common_services") + "?t=%d&c=%s&v=%s" % (t, c, v))
    else:
        navicategory = CmsNaviCategory.objects.get(id=id)
        form = NaviCategoryForm(instance=navicategory)
    cate2s = get_first_categories()
    errors, fields = format_form(form)
    scenes = get_scenes()
    actions = get_actions_select()
    citygroups = get_city_group()
    cities = get_city_list()
    return render_to_response(template_name, {
        "scenes": scenes,
        "actions": actions,
        "citygroups": citygroups,
        "cities": cities,
        "show_style_list": show_style_list,
        "cate2s": cate2s,
        "id": id,
        "fields": fields,
        "errors": errors,
        "t": t,
        "c": c,
        "v": v,
        "text": text,
        "channel": channel_id
    }, context_instance=RequestContext(request))


# 删除一级分类
@login_required
@permission_required(u'%s.%s' % (AuthCodeName.APP_LABEL, AuthCodeName.CONFIG), raise_exception=True)
def delete_common_category(request):
    id = request.POST.get("id")
    channel = request.POST.get("channel")
    related_channels = get_relate_channel_list(channel, CONFIG_ITEMS.COMMON_SERVICES)
    related_channels.append(channel)
    for channel_id in related_channels:
        views = CmsViewService.objects.filter(service_id=id, channel_id=channel_id, open_type__in=[3, 4, 5, 6])
        for view in views:
            if CMS_CHECK_ON:
                is_show = 0
                if int(view.channel_id) == int(channel):
                    is_show = 1
                check = CmsCheck(
                    channel_id=channel,
                    module=CmsModule.CONFIG_COMMON_SERVICES,
                    table_name="CmsViewService",
                    data_id=view.id,
                    op_type=CheckOpType.DELETE,
                    status=CheckStatu.WAIT_SUBMIT,
                    is_show=is_show,
                    alter_person=request.user.username,
                    alter_date=time.strftime("%Y-%m-%d %X", time.localtime()))
                check.save()
            view.delete()
    return HttpResponse(0)


# #删除二级分类
# @login_required
# @permission_required(u'%s.%s' % (AuthCodeName.APP_LABEL,AuthCodeName.CONFIG), raise_exception=True)
# def delete_common_category_second(request):
#     id = request.POST.get("id")
#     channel = request.POST.get("channel")
#     related_channels = get_relate_channel_list(channel,CONFIG_ITEMS.COMMON_SERVICES)
#     related_channels.append(channel)
#     for channel_id in related_channels:
#         views = CmsViewService.objects.filter(service_id=id,channel_id=channel_id,open_type=4)
#         for view in views:
#             is_show=0
#             if int(view.channel_id)==int(channel):
#                 is_show=1
#             if CMS_CHECK_ON:
#                 check = CmsCheck(
#                     channel_id=channel,
#                     module=CmsModule.CONFIG_COMMON_SERVICES,
#                     table_name="CmsViewService",
#                     data_id=view.id,
#                     op_type=CheckOpType.DELETE,
#                     status=CheckStatu.WAIT_SUBMIT,
#                     is_show=is_show,
#                     alter_person=request.user.username,
#                     alter_date=time.strftime("%Y-%m-%d %X",time.localtime()))
#                 check.save()
#             view.delete()
#     return HttpResponse(0)


# @login_required
# @permission_required(u'%s.%s' % (AuthCodeName.APP_LABEL,AuthCodeName.CONFIG), raise_exception=True)
# def delete_daojia_first(request):
#     id = request.POST.get("id")
#     channel = request.POST.get("channel")
#     related_channels = get_relate_channel_list(channel,CONFIG_ITEMS.COMMON_SERVICES)
#     related_channels.append(channel)
#     for channel_id in related_channels:
#         CmsViewService.objects.filter(service_id=id,channel_id=channel_id,open_type=5).delete()
#     return HttpResponse(0)
#
#
# @login_required
# @permission_required(u'%s.%s' % (AuthCodeName.APP_LABEL,AuthCodeName.CONFIG), raise_exception=True)
# def delete_daojia_second(request):
#     id = request.POST.get("id")
#     channel = request.POST.get("channel")
#     related_channels = get_relate_channel_list(channel,CONFIG_ITEMS.COMMON_SERVICES)
#     related_channels.append(channel)
#     for channel_id in related_channels:
#         CmsViewService.objects.filter(service_id=id,channel_id=channel_id,open_type=6).delete()
#     return HttpResponse(0)



# 新建到家类别
@login_required
def new_home_cate(request):
    return HttpResponse(0)


@login_required
@add_main_var
def edit_home_cate(request, template_name):
    return render_to_response(template_name, context_instance=RequestContext(request))
