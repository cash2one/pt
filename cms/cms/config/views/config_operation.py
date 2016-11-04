# coding: utf-8

"""
    运营配置
"""
from common.const import AuthCodeName, OP_CONFIG
# from config.views.config_pub import *
# from main.forms import *
# from config.forms import *
import time
from django.contrib.auth.decorators import login_required, permission_required
import json
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

from common.const import AuthCodeName, get_nav_text, CmsModule, CheckOpType, CONFIG_ITEMS, \
    CheckStatu
from common.views import get_check_status_str
from config.forms import OpconfigForm
from config.views.config_pub import CMS_CHECK_ON, CmsCheck, new_associate
from main.models import CmsChannels, CmsOpconfig, CmsViewOpconfig
from main.views.main_pub import add_main_var


# 运营配置列表页
@login_required
@add_main_var
def config_operation(request, template_name):
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
        "channel": channel,
        "OP_CONFIG": OP_CONFIG
    }, context_instance=RequestContext(request))


# 获取运营列表数据
@login_required
def search_config_operation(request):
    channel_id = request.GET.get('channel')
    objs = CmsOpconfig.objects.filter(cmsviewopconfig__channel_id=channel_id)
    result = []
    for i, obj in enumerate(objs):
        try:
            key = OP_CONFIG.get_key_text(obj.key)
            value = OP_CONFIG.get_value_text(obj.key, obj.value)
            status_str, status_int = get_check_status_str("CmsOpconfig", obj.id)
            result.append([
                i + 1,
                key,
                value,
                status_str,
                status_int,
                obj.id
            ])
        except:
            continue
    return HttpResponse(json.dumps(result))


# 新增运营配置
@login_required
@permission_required(u'%s.%s' % (AuthCodeName.APP_LABEL, AuthCodeName.CONFIG), raise_exception=True)
@add_main_var
def new_config_operation(request):
    """
    新建 运营配置
    url : {% url 'new_config_operation' %}
    :请求方式：ajax
    :请求参数：channel_id key value
    :返回: 成功返回0 错误返回errors
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
            channel_id = request.POST.get("channel_id")
            channel = CmsChannels.objects.get(id=channel_id)
            key = request.POST.get("key")
            try:
                if CmsOpconfig.objects.filter(cmsviewopconfig__channel=channel, key=key):
                    return HttpResponse(-1)
                form = OpconfigForm(request.POST)
                if form.is_valid():
                    opconfig = form.save()
                    if CMS_CHECK_ON:
                        CmsCheck(channel_id=channel_id,
                                 module=CmsModule.CONFIG_OPERATION,
                                 table_name='CmsOpconfig',
                                 data_id=opconfig.id,
                                 op_type=CheckOpType.NEW,
                                 alter_person=request.user.username,
                                 alter_date=time.strftime("%Y-%m-%d %X", time.localtime())).save()
                    oCmsViewOpconfig = CmsViewOpconfig(opconfig=opconfig, channel=channel)
                    oCmsViewOpconfig.save()
                    if CMS_CHECK_ON:
                        CmsCheck(channel_id=channel_id,
                                 module=CmsModule.CONFIG_OPERATION,
                                 table_name='CmsViewOpconfig',
                                 data_id=oCmsViewOpconfig.id,
                                 op_type=CheckOpType.NEW,
                                 is_show=0,
                                 alter_person=request.user.username,
                                 alter_date=time.strftime("%Y-%m-%d %X", time.localtime())).save()
                    new_associate(channel_id, opconfig.id, CONFIG_ITEMS.CONFIG_OPERATION, request)
                    return HttpResponse(0)
            except Exception as ex:
                return HttpResponse(ex.args[0])


# 编辑运营配置
@login_required
@permission_required(u'%s.%s' % (AuthCodeName.APP_LABEL, AuthCodeName.CONFIG), raise_exception=True)
@add_main_var
def edit_config_operation(request):
    """
    编辑 运营配置
    url : {% url 'edit_config_operation' %}
    :请求方式：ajax
    :请求参数：
         id
         key
         value
    :返回: 成功返回0 错误返回errors
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
                id = request.POST.get("id")
                channel_id = request.POST.get("channel_id")
                opconfig = CmsOpconfig.objects.get(id=id)
                form = OpconfigForm(request.POST, instance=opconfig)
                if form.is_valid():
                    form.save()
                    if CMS_CHECK_ON:
                        CmsCheck(channel_id=channel_id,
                                 module=CmsModule.CONFIG_OPERATION,
                                 table_name='CmsOpconfig',
                                 data_id=id,
                                 op_type=CheckOpType.EDIT,
                                 alter_person=request.user.username,
                                 alter_date=time.strftime("%Y-%m-%d %X", time.localtime())).save()
                    return HttpResponse(0)
            except Exception as ex:
                return HttpResponse(ex.args[0])


# 运营配置
@login_required
@permission_required(u'%s.%s' % (AuthCodeName.APP_LABEL, AuthCodeName.CONFIG), raise_exception=True)
def delete_config_operation(request):
    id = request.POST.get("id")
    channel_id = request.POST.get('channel')
    views = CmsViewOpconfig.objects.filter(opconfig_id=id)
    for view in views:
        if CMS_CHECK_ON:
            check = CmsCheck(
                channel_id=channel_id,
                module=CmsModule.CONFIG_OPERATION,
                table_name="CmsViewOpconfig",
                data_id=view.id,
                op_type=CheckOpType.DELETE,
                status=CheckStatu.WAIT_SUBMIT,
                is_show=0,
                alter_person=request.user.username,
                alter_date=time.strftime("%Y-%m-%d %X", time.localtime()))
            check.save()
        view.delete()
    CmsOpconfig.objects.filter(id=id).delete()
    if CMS_CHECK_ON:
        check = CmsCheck(
            channel_id=channel_id,
            module=CmsModule.CONFIG_OPERATION,
            table_name="CmsOpconfig",
            data_id=id,
            op_type=CheckOpType.DELETE,
            status=CheckStatu.WAIT_SUBMIT,
            is_show=1,
            alter_person=request.user.username,
            alter_date=time.strftime("%Y-%m-%d %X", time.localtime()))
        check.save()
    return HttpResponse(0)
