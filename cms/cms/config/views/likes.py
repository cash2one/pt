# coding: utf-8

"""
    猜你喜欢
"""
# from config.views.config_pub import *
# from config.forms import *
# from main.forms import *
from django.db.models import Q

from cms.settings import INSTALL_TYPE
from config.forms import LikesForm
from main.forms import ServiceForm, CmsGoods, CmsNaviCategory, GoodsForm
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
    getCVT, CmsServices, CmsLikes, get_scene_name, CmsViewLike, CmsLikesGoods, CmsLikesServices
from main.views.main_pub import add_main_var, get_scenes, get_city_list, get_city_group, format_form, \
    get_actions_select, get_categories


@login_required
@add_main_var
def likes(request, template_name):
    t = request.GET.get("t")
    if not t:
        t = "1"
    v = request.GET.get("v")
    c = request.GET.get("c")
    channel = CmsChannels.objects.get(channel_no=c, app_version__app_version=v, app_version__type_id=t).id
    goods = get_goods()
    services = get_services()
    return render_to_response(template_name,{
        "text": get_nav_text(t),
        "t": t,
        "v": v,
        "c": c,
        "channel": channel,
        "goods": goods,
        "services": services
    }, context_instance=RequestContext(request))


@login_required
def search_likes(request):
    channel = request.GET.get("channel")
    groups = CmsLikes.objects.filter(cmsviewlike__channel__id=channel)
    result = []
    for group in groups:
        group_scene = get_scene_name(group.scene_id)
        status_str, status_int = get_check_status_str("CmsLikes", group.id)
        item = {"group": [
            group_scene,
            group.title,
            group.title_style,
            group.desc,
            group.desc_style,
            status_str,
            status_int,
            group.id
        ], "members": []}
        #服务
        services = CmsServices.objects.filter(cmslikesservices__like=group)
        for service in services:
            status_str, status_int = get_check_status_str("CmsServices", service.id)
            item["members"].append([
                service.small_icon_url,
                service.name,
                service.name_style,
                service.desc,
                service.desc_style,
                service.location,
                service.dot_info,
                service.action_id,
                "服务",
                get_valid_time(service.valid_time),
                get_city_str(service.city),
                status_str,
                1,
                status_int,
                service.id
            ])
        #商品
        goods = CmsGoods.objects.filter(cmslikesgoods__like=group)
        for good in goods:
            status_str, status_int = get_check_status_str("CmsGoods", good.id)
            item["members"].append([
                good.small_icon_url,
                good.name,
                good.name_style,
                good.desc,
                good.desc_style,
                good.location,
                good.dot_info,
                good.action_id,
                "商品",
                get_valid_time(good.valid_time),
                get_city_str(good.city),
                status_str,
                0,
                status_int,
                good.id
            ])
        result.append(item)
        item["members"].sort(key=lambda o: (o[8], o[5]))
    filter_none(result)
    return HttpResponse(json.dumps(result))


@login_required
@permission_required(u'%s.%s' % (AuthCodeName.APP_LABEL,AuthCodeName.CONFIG), raise_exception=True)
def exchange_likes(request):
    id1 = request.POST.get("id1")
    type1 = request.POST.get("type1")
    id2 = request.POST.get("id2")
    type2 = request.POST.get("type2")
    channel_id = request.POST.get("channel")

    arr = [["0", CmsGoods], ["1", CmsServices]]
    class1 = get_2array_value(arr, type1)
    class2 = get_2array_value(arr, type2)
    exchange_obj(class1, id1, class2, id2, channel_id, CmsModule.CONFIG_LIKE,request)
    return HttpResponse(0)


#新增组
@login_required
@permission_required(u'%s.%s' % (AuthCodeName.APP_LABEL,AuthCodeName.CONFIG), raise_exception=True)
@add_main_var
def new_group(request, template_name):
    """
    猜你喜欢 新建组
    url :{% url 'new_likes_group' %}?channel={{ channel }}
    :请求方式: Get
    :请求参数：channel
    :返回数据：form 表单 scenes 场景列表
    :例如：scenes 场景列表 和之前一样

    :请求方式：Post
    :请求参数：
    """
    channel_id = request.GET.get('channel')
    c,v,t = getCVT(channel_id)
    channel = CmsChannels.objects.get(id=channel_id)
    #根据类型得到名称
    text = get_nav_text(str(t))
    if request.method =='POST':
        form = LikesForm(request.POST)
        if form.is_valid():
            likes = form.save()
            if CMS_CHECK_ON:
                CmsCheck(channel_id=channel_id,
                         module=CmsModule.CONFIG_LIKE,
                         table_name='CmsLikes',
                         data_id=likes.id,
                         op_type=CheckOpType.NEW,
                         alter_person=request.user.username,
                         alter_date=time.strftime("%Y-%m-%d %X",time.localtime())).save()
            oCmsViewLike=CmsViewLike(like=likes,channel=channel,status=0)
            oCmsViewLike.save()
            if CMS_CHECK_ON:
                CmsCheck(channel_id=channel_id,
                         module=CmsModule.CONFIG_LIKE,
                         table_name='CmsViewLike',
                         data_id=oCmsViewLike.id,
                         op_type=CheckOpType.NEW,
                         is_show=0,
                         alter_person=request.user.username,
                         alter_date=time.strftime("%Y-%m-%d %X",time.localtime())).save()
            new_associate(channel_id,likes.id,CONFIG_ITEMS.LIKES,request)
            return HttpResponseRedirect(reverse("likes")+"?t=%d&c=%s&v=%s" % (t,c,v))
    else:
        form = LikesForm()
    scenes = get_scenes()
    errors,fields = format_form(form)
    return render_to_response(template_name,{
        "scenes": scenes,
        "fields": fields,
        "errors":errors,
        "t":t,
        "c":c,
        "v":v,
        "text":text,
        "channel":channel_id
    },context_instance=RequestContext(request))


#编辑组
@login_required
@permission_required(u'%s.%s' % (AuthCodeName.APP_LABEL,AuthCodeName.CONFIG), raise_exception=True)
@add_main_var
def edit_group(request, template_name):
    """
    猜你喜欢 编辑组
    url :{% url 'edit_likes_group' %}?channel={{ channel }}&id={{ id }}
    :请求方式: Get
    :请求参数：channel,id
    :返回数据：form 表单 scenes 场景列表
    :例如：scenes 场景列表 和之前一样

    :请求方式：Post
    :请求参数：
    """
    channel_id = request.GET.get('channel')
    id = request.GET.get("id")
    c,v,t = getCVT(channel_id)
    likes = CmsLikes.objects.get(id=id)
    #根据类型得到名称
    text = get_nav_text(str(t))
    if request.method =='POST':
        form = LikesForm(request.POST,instance=likes)
        if form.is_valid():
            form.save()
            if CMS_CHECK_ON:
                CmsCheck(channel_id=channel_id,
                         module=CmsModule.CONFIG_LIKE,
                         table_name='CmsLikes',
                         data_id=id,
                         op_type=CheckOpType.EDIT,
                         alter_person=request.user.username,
                         alter_date=time.strftime("%Y-%m-%d %X",time.localtime())).save()
            return HttpResponseRedirect(reverse("likes")+"?t=%d&c=%s&v=%s" % (t,c,v))
    else:
        form = LikesForm(instance=likes)
    scenes = get_scenes()
    errors,fields = format_form(form)
    return render_to_response(template_name,{
        "scenes": scenes,
        "fields": fields,
        "errors":errors,
        "t":t,
        "c":c,
        "v":v,
        "text":text,
        "channel":channel_id,
        "id":id
    },context_instance=RequestContext(request))


#删除组
@login_required
@permission_required(u'%s.%s' % (AuthCodeName.APP_LABEL,AuthCodeName.CONFIG), raise_exception=True)
def delete_group(request):
    id = request.POST.get("id")
    channel_id = request.POST.get('channel')
    views = CmsViewLike.objects.filter(like_id=id)
    for view in views:
        if CMS_CHECK_ON:
            check = CmsCheck(
                channel_id=channel_id,
                module=CmsModule.CONFIG_LIKE,
                table_name="CmsViewLike",
                data_id=view.id,
                op_type=CheckOpType.DELETE,
                status=CheckStatu.WAIT_SUBMIT,
                is_show=0,
                alter_person=request.user.username,
                alter_date=time.strftime("%Y-%m-%d %X",time.localtime()))
            check.save()
    views.delete()
    cmslikesgoods = CmsLikesGoods.objects.filter(like_id=id)
    for cmslikesgood in cmslikesgoods:
        if CMS_CHECK_ON:
            check = CmsCheck(
                channel_id=channel_id,
                module=CmsModule.CONFIG_LIKE,
                table_name="CmsGoods",
                data_id=cmslikesgood.goods.id,
                op_type=CheckOpType.DELETE,
                status=CheckStatu.WAIT_SUBMIT,
                is_show=0,
                alter_person=request.user.username,
                alter_date=time.strftime("%Y-%m-%d %X",time.localtime()))
            check.save()
            check = CmsCheck(
                channel_id=channel_id,
                module=CmsModule.CONFIG_LIKE,
                table_name="CmsLikesGoods",
                data_id=cmslikesgood.id,
                op_type=CheckOpType.DELETE,
                status=CheckStatu.WAIT_SUBMIT,
                is_show=0,
                alter_person=request.user.username,
                alter_date=time.strftime("%Y-%m-%d %X",time.localtime()))
            check.save()
        cmslikesgood.goods.delete()
    cmslikesgoods.delete()
    cmslikesservices = CmsLikesServices.objects.filter(like_id=id)
    for cmslikesservice in cmslikesservices:
        if CMS_CHECK_ON:
            check = CmsCheck(
                channel_id=channel_id,
                module=CmsModule.CONFIG_LIKE,
                table_name="CmsServices",
                data_id=cmslikesservice.service.id,
                op_type=CheckOpType.DELETE,
                status=CheckStatu.WAIT_SUBMIT,
                is_show=0,
                alter_person=request.user.username,
                alter_date=time.strftime("%Y-%m-%d %X",time.localtime()))
            check.save()
            check = CmsCheck(
                channel_id=channel_id,
                module=CmsModule.CONFIG_LIKE,
                table_name="CmsLikesServices",
                data_id=cmslikesservice.id,
                op_type=CheckOpType.DELETE,
                status=CheckStatu.WAIT_SUBMIT,
                is_show=0,
                alter_person=request.user.username,
                alter_date=time.strftime("%Y-%m-%d %X",time.localtime()))
            check.save()
        cmslikesservice.service.delete()
    cmslikesservices.delete()
    CmsLikes.objects.get(id=id).delete()
    if CMS_CHECK_ON:
        check = CmsCheck(
            channel_id=channel_id,
            module=CmsModule.CONFIG_LIKE,
            table_name="CmsLikes",
            data_id=id,
            op_type=CheckOpType.DELETE,
            status=CheckStatu.WAIT_SUBMIT,
            is_show=1,
            alter_person=request.user.username,
            alter_date=time.strftime("%Y-%m-%d %X",time.localtime()))
        check.save()
    return HttpResponse(0)


#新增商品
@login_required
@permission_required(u'%s.%s' % (AuthCodeName.APP_LABEL,AuthCodeName.CONFIG), raise_exception=True)
@add_main_var
def new_goods(request):
    """
    猜你喜欢 添加商品
    :请求方式：ajax Post
    :请求URL：{% url 'likes_new_goods' %}
    :请求参数：goods_id  like_id
    :类型 :传数字
    返回： 成功：0 错误：错误信息
    """

    if request.method =='POST':
        data = request.POST.copy()
        error=""
        for key in data:
            if data[key]=="":
                error+=key+" is null \n"
        if error:
            return HttpResponse(error)
        else:
            goods_id = request.POST.get("goods_id")
            like_id = request.POST.get("like_id")
            channel_id = request.POST.get("channel_id")
            try:
                goods = CmsGoods.objects.get(id=goods_id)
                goods.parent_id = goods_id
                goods.id = None
                goods.save()
                if CMS_CHECK_ON:
                    CmsCheck(channel_id=channel_id,
                             module=CmsModule.CONFIG_LIKE,
                             table_name='CmsGoods',
                             data_id=goods.id,
                             op_type=CheckOpType.NEW,
                             remark="增加了名称为%s的商品" % (CheckManager.wrap_style(goods.name),),
                             alter_person=request.user.username,
                             alter_date=time.strftime("%Y-%m-%d %X",time.localtime())).save()
                oCmsLikesGoods=CmsLikesGoods(goods=goods,like=CmsLikes.objects.get(id=like_id))
                oCmsLikesGoods.save()
                if CMS_CHECK_ON:
                    CmsCheck(channel_id=channel_id,
                             module=CmsModule.CONFIG_LIKE,
                             table_name='CmsLikesGoods',
                             data_id=oCmsLikesGoods.id,
                             op_type=CheckOpType.NEW,
                             is_show=0,
                             alter_person=request.user.username,
                             alter_date=time.strftime("%Y-%m-%d %X",time.localtime())).save()
            except Exception as ex:
                return HttpResponse(ex.args[0])
            return HttpResponse(0)


#编辑商品
@login_required
@permission_required(u'%s.%s' % (AuthCodeName.APP_LABEL,AuthCodeName.CONFIG), raise_exception=True)
@add_main_var
def edit_goods(request, template_name):
    channel_id = request.GET.get('channel')
    c,v,t = getCVT(channel_id)
    text = get_nav_text(str(t))
    id= request.GET.get("id")
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
        form = GoodsForm(request.POST,instance=goods)
        if form.is_valid():
            form.save()
            data={}
            cate_fields = ['category', 'second_category', 'new_second_category', 'new_category', 'valid_time']
            for field in cate_fields:
                if request.POST.get(field):
                    data[field] = request.POST.get(field)
            #更新同一goods_id的商品
            if data:
                CmsGoods.objects.filter(~Q(id=id), goods_id=goods.goods_id).update(**data)
                if INSTALL_TYPE == 2 or INSTALL_TYPE == 3:
                    sync_search(goods.goods_id, data)
            if CMS_CHECK_ON:
                CmsCheck(channel_id=channel_id,
                         module=CmsModule.CONFIG_LIKE,
                         table_name='CmsGoods',
                         data_id=id,
                         op_type=CheckOpType.EDIT,
                         alter_person=request.user.username,
                         alter_date=time.strftime("%Y-%m-%d %X",time.localtime())).save()
            return HttpResponseRedirect(reverse("likes")+"?t=%d&c=%s&v=%s" % (t,c,v))
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
    return render_to_response(template_name,{
        "scenes":scenes,
        "actions":actions,
        "categories":categories,
        "citygroups":citygroups,
        "cities": cities,
        "id":id,
        "fields": fields,
        "errors":errors,
        "t":t,
        "c":c,
        "v":v,
        "text":text,
        "channel":channel_id
    }, context_instance=RequestContext(request))


#删除商品
@login_required
@permission_required(u'%s.%s' % (AuthCodeName.APP_LABEL,AuthCodeName.CONFIG), raise_exception=True)
def delete_goods(request):
    id = request.POST.get("id")
    channel_id = request.POST.get('channel')
    cmslikesgoods = CmsLikesGoods.objects.get(goods_id=id)
    if CMS_CHECK_ON:
        check = CmsCheck(
            channel_id=channel_id,
            module=CmsModule.CONFIG_LIKE,
            table_name="CmsLikesGoods",
            data_id=cmslikesgoods.id,
            op_type=CheckOpType.DELETE,
            status=CheckStatu.WAIT_SUBMIT,
            is_show=0,
            alter_person=request.user.username,
            alter_date=time.strftime("%Y-%m-%d %X",time.localtime()))
        check.save()
    CmsGoods.objects.get(id=id).delete()
    if CMS_CHECK_ON:
        check = CmsCheck(
            channel_id=channel_id,
            module=CmsModule.CONFIG_LIKE,
            table_name="CmsGoods",
            data_id=id,
            op_type=CheckOpType.DELETE,
            status=CheckStatu.WAIT_SUBMIT,
            is_show=1,
            alter_person=request.user.username,
            alter_date=time.strftime("%Y-%m-%d %X",time.localtime()))
        check.save()
    return HttpResponse(0)


#新增服务
@login_required
@permission_required(u'%s.%s' % (AuthCodeName.APP_LABEL,AuthCodeName.CONFIG), raise_exception=True)
@add_main_var
def new_service(request):
    """
    猜你喜欢 添加服务
    :请求方式：ajax Post
    :请求URL：{% url 'likes_new_service' %}
    :请求参数：service_id  like_id
    :类型 :传数字
    返回： 成功：0 错误：错误信息
    """

    if request.method =='POST':
        data = request.POST.copy()
        error=""
        for key in data:
            if data[key]=="":
                error+=key+" is null \n"
        if error:
            return HttpResponse(error)
        else:
            service_id = request.POST.get("service_id")
            like_id = request.POST.get("like_id")
            channel_id = request.POST.get("channel_id")
            try:
                service = CmsServices.objects.get(id=service_id)
                service.parent_id = service_id
                service.id = None
                service.save()
                if CMS_CHECK_ON:
                    CmsCheck(channel_id=channel_id,
                             module=CmsModule.CONFIG_LIKE,
                             table_name='CmsServices',
                             data_id=service.id,
                             op_type=CheckOpType.NEW,
                             remark="增加了名称为%s的服务" % (CheckManager.wrap_style(service.name),),
                             alter_person=request.user.username,
                             alter_date=time.strftime("%Y-%m-%d %X",time.localtime())).save()
                oCmsLikesServices=CmsLikesServices(service=service,like=CmsLikes.objects.get(id=like_id))
                oCmsLikesServices.save()
                if CMS_CHECK_ON:
                    CmsCheck(channel_id=channel_id,
                             module=CmsModule.CONFIG_LIKE,
                             table_name='CmsLikesServices',
                             data_id=oCmsLikesServices.id,
                             op_type=CheckOpType.NEW,
                             is_show=0,
                             alter_person=request.user.username,
                             alter_date=time.strftime("%Y-%m-%d %X",time.localtime())).save()
            except Exception as ex:
                return HttpResponse(ex.args[0])
            return HttpResponse(0)


#编辑服务
@login_required
@permission_required(u'%s.%s' % (AuthCodeName.APP_LABEL,AuthCodeName.CONFIG), raise_exception=True)
@add_main_var
def edit_service(request, template_name):
    """
     猜你喜欢 编辑服务
    :请求方式：Get
    :请求URL：{% url 'likes_edit_service' %}?channel={{ channel }}&id={{ id }}
    :请求参数：id(服务表id),channel(渠道号)
    :类型 :传数字
    """
    channel_id = request.GET.get('channel')
    c,v,t = getCVT(channel_id)
    text = get_nav_text(str(t))
    id = request.GET.get("id")
    if request.method == "POST":
        services = CmsServices.objects.get(id=id)
        form = ServiceForm(request.POST,instance=services)
        if form.is_valid():
            form.save()
            if CMS_CHECK_ON:
                CmsCheck(channel_id=channel_id,
                         module=CmsModule.CONFIG_LIKE,
                         table_name='CmsServices',
                         data_id=id,
                         op_type=CheckOpType.EDIT,
                         alter_person=request.user.username,
                         alter_date=time.strftime("%Y-%m-%d %X",time.localtime())).save()
            return HttpResponseRedirect(reverse("likes")+"?t=%d&c=%s&v=%s" % (t,c,v))
    else:
        services = CmsServices.objects.get(id=id)
        form = ServiceForm(instance=services)
    errors,fields = format_form(form)
    scenes = get_scenes()
    actions = get_actions_select()
    citygroups = get_city_group()
    cities = get_city_list()
    return render_to_response(template_name,{
        "scenes": scenes,
        "actions": actions,
        "citygroups":citygroups,
        "cities": cities,
        "id":id,
        "fields":fields,
        "errors":errors,
        "t":t,
        "c":c,
        "v":v,
        "text":text,
        "channel":channel_id
    },context_instance=RequestContext(request))


#删除服务
@login_required
@permission_required(u'%s.%s' % (AuthCodeName.APP_LABEL,AuthCodeName.CONFIG), raise_exception=True)
def delete_service(request):
    id = request.POST.get("id")
    channel_id = request.POST.get('channel')
    cmslikesservice = CmsLikesServices.objects.get(service_id=id)
    if CMS_CHECK_ON:
        check = CmsCheck(
            channel_id=channel_id,
            module=CmsModule.CONFIG_LIKE,
            table_name="CmsLikesServices",
            data_id=cmslikesservice.id,
            op_type=CheckOpType.DELETE,
            status=CheckStatu.WAIT_SUBMIT,
            is_show=0,
            alter_person=request.user.username,
            alter_date=time.strftime("%Y-%m-%d %X",time.localtime()))
        check.save()
    cmslikesservice.delete()
    CmsServices.objects.get(id=id).delete()
    if CMS_CHECK_ON:
        check = CmsCheck(
            channel_id=channel_id,
            module=CmsModule.CONFIG_LIKE,
            table_name="CmsServices",
            data_id=id,
            op_type=CheckOpType.DELETE,
            status=CheckStatu.WAIT_SUBMIT,
            is_show=1,
            alter_person=request.user.username,
            alter_date=time.strftime("%Y-%m-%d %X",time.localtime()))
        check.save()
    return HttpResponse(0)

