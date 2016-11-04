# coding: utf-8

"""
    分类页服务 即客户端导航
"""
from django.db.models import Q

from cms.settings import INSTALL_TYPE
from common.const import CategoryGroupType
# from config.views.config_pub import *
# from main.forms import *
# from config.forms import *
from config.forms import NavicategoriesForm
from main.forms import ServiceForm, CmsGoods, CmsNaviCategory, GoodsForm, NaviCategoryForm
from main.views.interface_category import sync_search
import time
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required, permission_required
import json
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

from common.const import AuthCodeName, get_nav_text, get_2array_value, CmsModule, CheckOpType, CONFIG_ITEMS, \
    CheckStatu
from common.views import get_check_status_str, filter_none, get_relate_channel_list, CheckManager
from config.views.config_pub import CMS_CHECK_ON, CmsCheck, new_associate, get_services, get_goods, exchange_obj
from main.models import CmsChannels, get_valid_time, get_city_str, \
    getCVT, CmsNavicategories, CmsCategoryGroup, CmsNavicatesCategory, CmsNavicatesServices, CmsNavicatesGoods, \
    CmsViewNavi, CmsServices
from main.views.main_pub import add_main_var, get_scenes, get_city_list, get_city_group, format_form, \
    get_actions_select, \
    get_first_categories, get_categories, show_style_list


# 分类页服务列表
@login_required
@add_main_var
def category_pages_services(request, template_name):
    t = request.GET.get("t")
    if not t:
        t = "1"
    v = request.GET.get("v")
    c = request.GET.get("c")
    channel = CmsChannels.objects.get(channel_no=c, app_version__app_version=v, app_version__type_id=t).id
    services = get_services()
    goods = get_goods()
    return render_to_response(template_name, {
        "text": get_nav_text(t),
        "t": t,
        "v": v,
        "c": c,
        "channel": channel,
        "services": services,
        "goods": goods
    }, context_instance=RequestContext(request))


# 获取分类页服务列表数据
@login_required
def search_category_pages_services(request):
    channel = request.GET.get("channel")
    groups = list(CmsNavicategories.objects.filter(cmsviewnavi__channel_id=channel))
    result = []
    try:
        groups.sort(key=lambda o: (CmsCategoryGroup.objects.get(cmsviewgroupcategory__category=o.category).name))
    except:
        pass
    for group in groups:
        # group_scene = get_scene_name(group.scene_id)
        open_type = 2
        try:
            group_name = CmsCategoryGroup.objects.get(cmsviewgroupcategory__category=group.category).name
            if group_name == CategoryGroupType.daojia:
                open_type = 1
            elif group_name == CategoryGroupType.live:
                open_type = 0
        except:
            group_name = ""
        try:
            status_str, status_int = get_check_status_str("CmsNavicategories", group.id)
            item = {"group": [
                # group_scene,
                group_name,
                group.location,
                group.category.name,
                group.name_style,
                group.dot_info,
                open_type,
                status_str,
                status_int,
                group.id
            ], "members": []}
        except:
            continue
        # 分类
        navi_categories = CmsNavicatesCategory.objects.filter(cate=group)
        for navi_category in navi_categories:
            category = navi_category.category
            status_str_cate, status_int_cate = get_check_status_str("CmsNaviCategory", category.id)
            status_str_view, status_int_view = get_check_status_str("CmsNavicatesCategory", navi_category.id)
            item["members"].append([
                category.small_icon_url,
                category.location,
                "分类",
                category.name,
                category.name_style,
                category.desc,
                category.desc_style,
                category.search_keyword,
                category.dot_info,
                category.action_id,
                get_valid_time(category.valid_time),
                get_city_str(category.city),
                status_str_view,
                1,
                "%d/%d" % (status_int_cate, status_int_view),
                category.id
            ])
        # 服务
        navi_services = CmsNavicatesServices.objects.filter(cate=group)
        for navi_service in navi_services:
            try:
                service = navi_service.service
            except:
                continue
            status_str, status_int = get_check_status_str("CmsServices", service.id)
            item["members"].append([
                service.small_icon_url,
                service.location,
                "服务",
                service.name,
                service.name_style,
                service.desc,
                service.desc_style,
                service.search_keyword,
                service.dot_info,
                service.action_id,
                get_valid_time(service.valid_time),
                get_city_str(service.city),
                status_str,
                2,
                "%d/%d" % (status_int, status_int),
                service.id
            ])
        # 商品
        navi_goods = CmsNavicatesGoods.objects.filter(cate=group)
        for navi_good in navi_goods:
            try:
                goods = navi_good.goods
            except:
                continue
            status_str, status_int = get_check_status_str("CmsGoods", goods.id)
            item["members"].append([
                goods.small_icon_url,
                goods.location,
                "商品",
                goods.name,
                goods.name_style,
                goods.desc,
                goods.desc_style,
                goods.search_keyword,
                goods.dot_info,
                goods.action_id,
                get_valid_time(goods.valid_time),
                get_city_str(goods.city),
                status_str,
                3,
                "%d/%d" % (status_int, status_int),
                goods.id
            ])
        item["members"].sort(key=lambda o: (o[2], o[1]))
        result.append(item)
    filter_none(result)
    return HttpResponse(json.dumps(result))


# 新增分类页服务组即一级分类
@login_required
@permission_required(u'%s.%s' % (AuthCodeName.APP_LABEL, AuthCodeName.CONFIG), raise_exception=True)
@add_main_var
def new_group(request, template_name):
    """
    新建 分类页服务组
    url :{% url 'category_pages_services_new_group' %}?channel={{ channel }}
    :请求方式: Get
    :请求参数：channel
    :返回数据： scenes 场景列表 categories 一级分类列表
    :例如：scenes 场景列表 和之前一样 streams_type = [[1,"活动"],[2,"服务"],[3,"商品"],[4,"搜索"]]

    :请求方式：Post
    :请求参数：
    """
    channel = request.GET.get("channel")
    c, v, t = getCVT(channel)
    text = get_nav_text(str(t))
    if request.method == "POST":
        form = NavicategoriesForm(request.POST)
        if form.is_valid():
            navicategories = form.save()
            if CMS_CHECK_ON:
                CmsCheck(channel_id=channel,
                         module=CmsModule.CONFIG_PAGE,
                         table_name='CmsNavicategories',
                         data_id=navicategories.id,
                         op_type=CheckOpType.NEW,
                         alter_person=request.user.username,
                         alter_date=time.strftime("%Y-%m-%d %X", time.localtime())).save()
            cmschannel = CmsChannels.objects.get(id=channel)
            oviewnavi = CmsViewNavi(navicat=navicategories, channel=cmschannel, status=0)
            oviewnavi.save()
            if CMS_CHECK_ON:
                CmsCheck(channel_id=channel,
                         module=CmsModule.CONFIG_PAGE,
                         table_name='CmsViewNavi',
                         data_id=oviewnavi.id,
                         op_type=CheckOpType.NEW,
                         is_show=0,
                         alter_person=request.user.username,
                         alter_date=time.strftime("%Y-%m-%d %X", time.localtime())).save()
            new_associate(channel, navicategories.id, CONFIG_ITEMS.CATEGORY_PAGE_SERVICES, request)
            return HttpResponseRedirect(reverse("category_pages_services") + "?t=%s&c=%s&v=%s" % (t, c, v))
    else:
        form = NavicategoriesForm()
    errors, fields = format_form(form)
    # 一级分类
    categories = get_first_categories()
    scenes = get_scenes()
    return render_to_response(template_name, {
        "categories": categories,
        "scenes": scenes,
        "fields": fields,
        "errors": errors,
        "channel": channel,
        "text": text,
        "t": t,
        "c": c,
        "v": v
    }, context_instance=RequestContext(request))


# 编辑分类页服务组即一级分类
@login_required
@permission_required(u'%s.%s' % (AuthCodeName.APP_LABEL, AuthCodeName.CONFIG), raise_exception=True)
@add_main_var
def edit_group(request, template_name):
    """
    编辑 分类页服务组
    url :{% url 'category_pages_services_new_group' %}?channel={{ channel }}
    :请求方式: Get
    :请求参数：channel ,id
    :返回数据：scenes 场景列表 categories 一级分类列表
    :例如：scenes 场景列表 和之前一样 streams_type = [[1,"活动"],[2,"服务"],[3,"商品"],[4,"搜索"]]

    :请求方式：Post
    :请求参数：
    """
    id = request.GET.get("id")
    navicategories = CmsNavicategories.objects.get(id=id)
    channel = request.GET.get("channel")
    c, v, t = getCVT(channel)
    text = get_nav_text(str(t))
    if request.method == "POST":
        form = NavicategoriesForm(request.POST, instance=navicategories)
        if form.is_valid():
            form.save()
            if CMS_CHECK_ON:
                CmsCheck(channel_id=channel,
                         module=CmsModule.CONFIG_PAGE,
                         table_name='CmsNavicategories',
                         data_id=id,
                         op_type=CheckOpType.EDIT,
                         alter_person=request.user.username,
                         alter_date=time.strftime("%Y-%m-%d %X", time.localtime())).save()
            return HttpResponseRedirect(reverse("category_pages_services") + "?t=%s&c=%s&v=%s" % (t, c, v))
    else:
        form = NavicategoriesForm(instance=navicategories)
    errors, fields = format_form(form)
    # 一级分类
    categories = get_first_categories()
    scenes = get_scenes()
    return render_to_response(template_name, {
        "categories": categories,
        "scenes": scenes,
        "fields": fields,
        "errors": errors,
        "channel": channel,
        "text": text,
        "t": t,
        "c": c,
        "v": v,
        "id": id
    }, context_instance=RequestContext(request))


# 删除分类页服务组即一级分类
@login_required
@permission_required(u'%s.%s' % (AuthCodeName.APP_LABEL, AuthCodeName.CONFIG), raise_exception=True)
def delete_group(request):
    id = request.POST.get("id")
    channel_id = request.POST.get('channel')
    cmsnavicategoods = CmsNavicatesGoods.objects.filter(cate_id=id)
    for cmsnavicategood in cmsnavicategoods:
        if CMS_CHECK_ON:
            check = CmsCheck(
                channel_id=channel_id,
                module=CmsModule.CONFIG_PAGE,
                table_name="CmsNavicatesGoods",
                data_id=cmsnavicategood.id,
                op_type=CheckOpType.DELETE,
                status=CheckStatu.WAIT_SUBMIT,
                is_show=0,
                alter_person=request.user.username,
                alter_date=time.strftime("%Y-%m-%d %X", time.localtime()))
            check.save()
            check = CmsCheck(
                channel_id=channel_id,
                module=CmsModule.CONFIG_PAGE,
                table_name="CmsGoods",
                data_id=cmsnavicategood.goods.id,
                op_type=CheckOpType.DELETE,
                status=CheckStatu.WAIT_SUBMIT,
                is_show=0,
                alter_person=request.user.username,
                alter_date=time.strftime("%Y-%m-%d %X", time.localtime()))
            check.save()
        cmsnavicategood.goods.delete()
        cmsnavicategood.delete()
    cmsnavicateservices = CmsNavicatesServices.objects.filter(cate_id=id)
    for cmsnavicateservice in cmsnavicateservices:
        if CMS_CHECK_ON:
            check = CmsCheck(
                channel_id=channel_id,
                module=CmsModule.CONFIG_PAGE,
                table_name="CmsNavicatesServices",
                data_id=cmsnavicateservice.id,
                op_type=CheckOpType.DELETE,
                status=CheckStatu.WAIT_SUBMIT,
                is_show=0,
                alter_person=request.user.username,
                alter_date=time.strftime("%Y-%m-%d %X", time.localtime()))
            check.save()
            check = CmsCheck(
                channel_id=channel_id,
                module=CmsModule.CONFIG_PAGE,
                table_name="CmsServices",
                data_id=cmsnavicateservice.service.id,
                op_type=CheckOpType.DELETE,
                status=CheckStatu.WAIT_SUBMIT,
                is_show=0,
                alter_person=request.user.username,
                alter_date=time.strftime("%Y-%m-%d %X", time.localtime()))
            check.save()
        cmsnavicateservice.service.delete()
        cmsnavicateservice.delete()
    cmsnavicatescategorys = CmsNavicatesCategory.objects.filter(cate_id=id)
    for cmsnavicatescategory in cmsnavicatescategorys:
        if CMS_CHECK_ON:
            check = CmsCheck(
                channel_id=channel_id,
                module=CmsModule.CONFIG_PAGE,
                table_name="CmsNavicatesCategory",
                data_id=cmsnavicatescategory.id,
                op_type=CheckOpType.DELETE,
                status=CheckStatu.WAIT_SUBMIT,
                is_show=0,
                alter_person=request.user.username,
                alter_date=time.strftime("%Y-%m-%d %X", time.localtime()))
            check.save()
        cmsnavicatescategory.delete()
    related_channels = get_relate_channel_list(channel_id, CONFIG_ITEMS.CATEGORY_PAGE_SERVICES)
    related_channels.append(channel_id)
    for channel in related_channels:
        views = CmsViewNavi.objects.filter(navicat_id=id, channel_id=channel)
        for view in views:
            if CMS_CHECK_ON:
                check = CmsCheck(
                    channel_id=channel_id,
                    module=CmsModule.CONFIG_PAGE,
                    table_name="CmsViewNavi",
                    data_id=view.id,
                    op_type=CheckOpType.DELETE,
                    status=CheckStatu.WAIT_SUBMIT,
                    is_show=0,
                    alter_person=request.user.username,
                    alter_date=time.strftime("%Y-%m-%d %X", time.localtime()))
                check.save()
            view.delete()
    CmsNavicategories.objects.get(id=id).delete()
    if CMS_CHECK_ON:
        check = CmsCheck(
            channel_id=channel_id,
            module=CmsModule.CONFIG_PAGE,
            table_name="CmsNavicategories",
            data_id=id,
            op_type=CheckOpType.DELETE,
            status=CheckStatu.WAIT_SUBMIT,
            is_show=1,
            alter_person=request.user.username,
            alter_date=time.strftime("%Y-%m-%d %X", time.localtime()))
        check.save()
    return HttpResponse(0)


# 在分类页服务下新增服务
@login_required
@permission_required(u'%s.%s' % (AuthCodeName.APP_LABEL, AuthCodeName.CONFIG), raise_exception=True)
@add_main_var
def new_service(request):
    """
     分类导航 新建服务
     :请求URL：{% url 'category_pages_services_new_service' %}
    :请求方式：ajax Post
    :请求参数：service_id  navicategories_id channel_id
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
            # 服务ID
            service_id = request.POST.get("service_id")
            # 导航表ID
            navicategories_id = request.POST.get("navicategories_id")
            channel_id = request.POST.get("channel_id")
            navicategories = CmsNavicategories.objects.get(id=navicategories_id)
            services = CmsServices.objects.get(id=service_id)
            services.type = 1
            services.parent_id = service_id
            services.id = None
            services.save()
            if CMS_CHECK_ON:
                CmsCheck(channel_id=channel_id,
                         module=CmsModule.CONFIG_PAGE,
                         table_name='CmsServices',
                         data_id=services.id,
                         op_type=CheckOpType.NEW,
                         remark="在id为%s的分类组里面增加了名称为%s的服务" % (
                             CheckManager.wrap_style(navicategories_id), CheckManager.wrap_style(services.name)),
                         alter_person=request.user.username,
                         alter_date=time.strftime("%Y-%m-%d %X", time.localtime())).save()
            try:
                ocmsnaviservices = CmsNavicatesServices(cate=navicategories, service=services)
                ocmsnaviservices.save()
                if CMS_CHECK_ON:
                    CmsCheck(channel_id=channel_id,
                             module=CmsModule.CONFIG_PAGE,
                             table_name='CmsNavicatesServices',
                             data_id=ocmsnaviservices.id,
                             op_type=CheckOpType.NEW,
                             is_show=0,
                             alter_person=request.user.username,
                             alter_date=time.strftime("%Y-%m-%d %X", time.localtime())).save()
            except Exception as ex:
                if 'Duplicate entry' in ex.args[0]:
                    return HttpResponse(1)
                return HttpResponse(ex.args[0])
            return HttpResponse(0)


# 在分类页服务下编辑服务
@login_required
@permission_required(u'%s.%s' % (AuthCodeName.APP_LABEL, AuthCodeName.CONFIG), raise_exception=True)
@add_main_var
def edit_service(request, template_name):
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
                         module=CmsModule.CONFIG_PAGE,
                         table_name='CmsServices',
                         data_id=id,
                         op_type=CheckOpType.EDIT,
                         alter_person=request.user.username,
                         alter_date=time.strftime("%Y-%m-%d %X", time.localtime())).save()
            return HttpResponseRedirect(reverse("category_pages_services") + "?t=%d&c=%s&v=%s" % (t, c, v))
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


# 在分类页服务下删除服务
@login_required
@permission_required(u'%s.%s' % (AuthCodeName.APP_LABEL, AuthCodeName.CONFIG), raise_exception=True)
def delete_service(request):
    id = request.POST.get("id")
    channel_id = request.POST.get('channel')
    cmsnavicatesservice = CmsNavicatesServices.objects.get(service_id=id)
    if CMS_CHECK_ON:
        check = CmsCheck(
            channel_id=channel_id,
            module=CmsModule.CONFIG_PAGE,
            table_name="CmsNavicatesServices",
            data_id=cmsnavicatesservice.id,
            op_type=CheckOpType.DELETE,
            status=CheckStatu.WAIT_SUBMIT,
            is_show=0,
            alter_person=request.user.username,
            alter_date=time.strftime("%Y-%m-%d %X", time.localtime()))
        check.save()
    cmsnavicatesservice.delete()
    CmsServices.objects.get(id=id).delete()
    if CMS_CHECK_ON:
        check = CmsCheck(
            channel_id=channel_id,
            module=CmsModule.CONFIG_PAGE,
            table_name="CmsServices",
            data_id=id,
            op_type=CheckOpType.DELETE,
            status=CheckStatu.WAIT_SUBMIT,
            is_show=1,
            alter_person=request.user.username,
            alter_date=time.strftime("%Y-%m-%d %X", time.localtime()))
        check.save()
    return HttpResponse(0)


# 在分类页服务下新建商品
@login_required
@permission_required(u'%s.%s' % (AuthCodeName.APP_LABEL, AuthCodeName.CONFIG), raise_exception=True)
@add_main_var
def new_goods(request):
    """
     分类导航 新建商品
    :请求方式：ajax Post
    :请求URL：{% url 'category_pages_services_new_goods' %}
    :请求参数：goods_id  navicategories_id
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
            # 导航表ID
            navicategories_id = request.POST.get("navicategories_id")
            navicategories = CmsNavicategories.objects.get(id=navicategories_id)
            channel_id = request.POST.get("channel_id")
            try:
                goods = CmsGoods.objects.get(id=goods_id)
                goods.parent_id = goods_id
                goods.id = None
                goods.save()
                if CMS_CHECK_ON:
                    CmsCheck(channel_id=channel_id,
                             module=CmsModule.CONFIG_PAGE,
                             table_name='CmsGoods',
                             data_id=goods.id,
                             op_type=CheckOpType.NEW,
                             remark="在id为%s的分类组里面增加了名称为%s的商品" % (
                                 CheckManager.wrap_style(navicategories_id), CheckManager.wrap_style(goods.name)),
                             alter_person=request.user.username,
                             alter_date=time.strftime("%Y-%m-%d %X", time.localtime())).save()
                ocmsnavicatesgoods = CmsNavicatesGoods(cate=navicategories, goods=goods)
                ocmsnavicatesgoods.save()
                if CMS_CHECK_ON:
                    CmsCheck(channel_id=channel_id,
                             module=CmsModule.CONFIG_PAGE,
                             table_name='CmsNavicatesGoods',
                             data_id=ocmsnavicatesgoods.id,
                             op_type=CheckOpType.NEW,
                             is_show=0,
                             alter_person=request.user.username,
                             alter_date=time.strftime("%Y-%m-%d %X", time.localtime())).save()
            except Exception as ex:
                if 'Duplicate entry' in ex.args[0]:
                    return HttpResponse(1)
                return HttpResponse(ex.args[0])
            return HttpResponse(0)


# 在分类页服务下编辑商品
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
                         module=CmsModule.CONFIG_PAGE,
                         table_name='CmsGoods',
                         data_id=id,
                         op_type=CheckOpType.EDIT,
                         alter_person=request.user.username,
                         alter_date=time.strftime("%Y-%m-%d %X", time.localtime())).save()
            return HttpResponseRedirect(reverse("category_pages_services") + "?t=%d&c=%s&v=%s" % (t, c, v))
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


# 在分类页服务下删除商品
@login_required
@permission_required(u'%s.%s' % (AuthCodeName.APP_LABEL, AuthCodeName.CONFIG), raise_exception=True)
def delete_goods(request):
    id = request.POST.get("id")
    channel_id = request.POST.get('channel')
    cmsnavicatesgoods = CmsNavicatesGoods.objects.get(goods_id=id)
    if CMS_CHECK_ON:
        check = CmsCheck(
            channel_id=channel_id,
            module=CmsModule.CONFIG_PAGE,
            table_name="CmsNavicatesGoods",
            data_id=cmsnavicatesgoods.id,
            op_type=CheckOpType.DELETE,
            status=CheckStatu.WAIT_SUBMIT,
            is_show=0,
            alter_person=request.user.username,
            alter_date=time.strftime("%Y-%m-%d %X", time.localtime()))
        check.save()
    cmsnavicatesgoods.delete()
    CmsGoods.objects.get(id=id).delete()
    if CMS_CHECK_ON:
        check = CmsCheck(
            channel_id=channel_id,
            module=CmsModule.CONFIG_PAGE,
            table_name="CmsGoods",
            data_id=id,
            op_type=CheckOpType.DELETE,
            status=CheckStatu.WAIT_SUBMIT,
            is_show=1,
            alter_person=request.user.username,
            alter_date=time.strftime("%Y-%m-%d %X", time.localtime()))
        check.save()
    return HttpResponse(0)


# 在分类页服务下新增分类（二级分类）
@login_required
@permission_required(u'%s.%s' % (AuthCodeName.APP_LABEL, AuthCodeName.CONFIG), raise_exception=True)
@add_main_var
def new_category(request):
    """
    分类页服务  新建分类（二级分类）
    :请求方式：ajax Post
    :请求URL：{% url 'category_pages_services_new_category' %}
    :请求参数：navicategories_id(分类组表id)  category_id(分类表id)
    :直接插入关系表 导航与分类关系表 cms_navicates_category
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
                category_id = request.POST.get("category_id")
                # 分类组ID
                navicategories_id = request.POST.get("navicategories_id")
                channel_id = request.POST.get("channel_id")
                c, v, t = getCVT(channel_id)
                navicategories = CmsNavicategories.objects.get(id=navicategories_id)
                category = CmsNaviCategory.objects.get(id=category_id)
                oCmsNavicatesCategory = CmsNavicatesCategory(cate=navicategories, category=category)
                oCmsNavicatesCategory.save()
                if CMS_CHECK_ON:
                    CmsCheck(channel_id=channel_id,
                             module=CmsModule.CONFIG_PAGE,
                             table_name='CmsNavicatesCategory',
                             data_id=oCmsNavicatesCategory.id,
                             op_type=CheckOpType.NEW,
                             remark="在id为%s的分类组里面增加了名称为%s的分类" % (
                                 CheckManager.wrap_style(navicategories_id), CheckManager.wrap_style(category.name)),
                             alter_person=request.user.username,
                             alter_date=time.strftime("%Y-%m-%d %X", time.localtime())).save()
            except Exception as ex:
                if 'Duplicate entry' in ex.args[0]:
                    return HttpResponse(1)
                return HttpResponse(ex.args[0])
            return HttpResponse(0)


# 在分类页服务下新增分类（二级分类）
@login_required
@permission_required(u'%s.%s' % (AuthCodeName.APP_LABEL, AuthCodeName.CONFIG), raise_exception=True)
@add_main_var
def edit_category(request, template_name):
    """
    分类页服务  编辑分类
    :请求方式：Get
    :请求URL：{% url 'category_pages_services_edit_category' %}
    :请求参数：channel（渠道号），id (CmsNaviCategory分类表id)
    :类型 :传数字
    返回： 成功：0 错误：错误信息
    """
    channel_id = request.GET.get('channel')
    c, v, t = getCVT(channel_id)
    text = get_nav_text(str(t))
    id = request.GET.get("id")
    if request.method == "POST":
        navicategory = CmsNaviCategory.objects.get(id=id)
        form = NaviCategoryForm(request.POST, instance=navicategory)
        if form.is_valid():
            form.save()
            if CMS_CHECK_ON:
                CmsCheck(module=CmsModule.MAIN_CATEGORY,
                         table_name='CmsNaviCategory',
                         data_id=id,
                         op_type=CheckOpType.EDIT,
                         alter_person=request.user.username,
                         alter_date=time.strftime("%Y-%m-%d %X", time.localtime())).save()
            return HttpResponseRedirect(reverse("category_pages_services") + "?t=%d&c=%s&v=%s" % (t, c, v))
    else:
        navicategory = CmsNaviCategory.objects.get(id=id)
        form = NaviCategoryForm(instance=navicategory)
    errors, fields = format_form(form)
    scenes = get_scenes()
    actions = get_actions_select()
    citygroups = get_city_group()
    cities = get_city_list()
    cate2s = get_first_categories()
    return render_to_response(template_name, {
        "scenes": scenes,
        "actions": actions,
        "citygroups": citygroups,
        "show_style_list": show_style_list,
        "cities": cities,
        "cate2s": cate2s,
        "fields": fields,
        "errors": errors,
        "t": t,
        "c": c,
        "v": v,
        "text": text,
        "channel": channel_id,
        "id": id
    }, context_instance=RequestContext(request))


# 在分类页服务下删除分类（二级分类）
@login_required
@permission_required(u'%s.%s' % (AuthCodeName.APP_LABEL, AuthCodeName.CONFIG), raise_exception=True)
def delete_category(request):
    id = request.POST.get("id")
    channel_id = request.POST.get('channel')
    groups = CmsNavicatesCategory.objects.filter(category_id=id, cate__cmsviewnavi__channel_id=channel_id)
    for group in groups:
        if CMS_CHECK_ON:
            check = CmsCheck(
                channel_id=channel_id,
                module=CmsModule.CONFIG_PAGE,
                table_name="CmsNavicatesCategory",
                data_id=group.id,
                op_type=CheckOpType.DELETE,
                status=CheckStatu.WAIT_SUBMIT,
                is_show=1,
                remark="在id为%s的分类组删除了名称为%s的分类" % (
                    CheckManager.wrap_style(group.cate.id), CheckManager.wrap_style(group.category.name)),
                alter_person=request.user.username,
                alter_date=time.strftime("%Y-%m-%d %X", time.localtime()))
            check.save()
        group.delete()
    return HttpResponse(0)


@login_required
@permission_required(u'%s.%s' % (AuthCodeName.APP_LABEL, AuthCodeName.CONFIG), raise_exception=True)
def exchange_category(request):
    id1 = request.POST.get("id1")
    id2 = request.POST.get("id2")
    channel_id = request.POST.get("channel")
    type1 = request.POST.get("type1")
    type2 = request.POST.get("type2")

    arr = [["1", CmsNaviCategory], ["2", CmsServices], ["3", CmsGoods]]
    class1 = get_2array_value(arr, type1)
    class2 = get_2array_value(arr, type2)
    exchange_obj(class1, id1, class2, id2, channel_id, CmsModule.CONFIG_PAGE, request)
    return HttpResponse(0)


@login_required
def get_second_category(request):
    id = request.GET.get("id")
    category = CmsNavicategories.objects.get(id=id).category
    categories = CmsNaviCategory.objects.filter(fatherid=category.id, parent_id=0).order_by("name").values_list('id',
                                                                                                                'name',
                                                                                                                'memo')
    result = list(categories)
    filter_none(result)
    return HttpResponse(json.dumps(result))


# 新建到家类别
@login_required
def new_home_cate(request):
    return HttpResponse(0)


@login_required
@add_main_var
def edit_home_cate(request, template_name):
    return render_to_response(template_name, context_instance=RequestContext(request))


def del_home_cate(request):
    return HttpResponse(0)
