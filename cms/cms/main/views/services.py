# coding: utf-8

"""
    服务
"""
from audioop import reverse

from cms.settings import CMS_CHECK_ON
from common.const import CmsModule, MainConst
# from .main_pub import *
# from main.forms import *
import time
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
import json
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from common.const import AuthCodeName, CheckStatu, CheckOpType
from common.views import filter_none, get_check_status_str, search_key, get_table_paginator
from main.forms import ServiceForm
from main.models import CmsCheck, CmsServices, get_valid_time, get_city_str
from main.views.main_pub import add_main_var, format_form, get_actions_select, get_scenes, get_city_list, get_city_group


@login_required
@add_main_var
def services(request, template_name):
    return render_to_response(template_name, context_instance=RequestContext(request))


# 搜索服务
@login_required
def search_services(request):
    per_page = request.GET.get("per_page")
    if not per_page:
        per_page = MainConst.PER_PAGE
    cur_page = request.GET.get("cur_page")
    if not cur_page:
        cur_page = 1
    key = request.GET.get("key")
    objs = CmsServices.objects.filter(parent_id=0, type=0).order_by("-id")
    services = []
    for obj in objs:
        status_str, status_int = get_check_status_str("CmsServices", obj.id)
        services.append([
            obj.name,
            obj.small_icon_url,
            obj.icon_url,
            obj.desc,
            obj.memo,
            get_valid_time(obj.valid_time),
            get_city_str(obj.city),
            status_str,
            status_int,
            obj.id
        ])
    result = search_key(services, key, [1, 2, 8, 9])
    result, num_pages = get_table_paginator(result, per_page, cur_page)
    filter_none(result)
    return HttpResponse(json.dumps([list(result), num_pages]))


@login_required
@permission_required(u'%s.%s' % (AuthCodeName.APP_LABEL, AuthCodeName.CONFIG), raise_exception=True)
@add_main_var
def new_service(request, template_name):
    if request.method == "POST":
        form = ServiceForm(request.POST)
        if form.is_valid():
            oService = form.save()
            if CMS_CHECK_ON:
                CmsCheck(module=CmsModule.MAIN_SERVICE,
                         table_name='CmsServices',
                         data_id=oService.id,
                         op_type=CheckOpType.NEW,
                         alter_person=request.user.username,
                         alter_date=time.strftime("%Y-%m-%d %X", time.localtime())).save()
            return HttpResponseRedirect(reverse('services'))
    else:
        form = ServiceForm()
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
        "fields": fields,
        "errors": errors
    }, context_instance=RequestContext(request))


# 编辑服务
@login_required
@permission_required(u'%s.%s' % (AuthCodeName.APP_LABEL, AuthCodeName.CONFIG), raise_exception=True)
@add_main_var
def edit_service(request, template_name):
    id = request.GET.get("id")
    if request.method == "POST":
        services = CmsServices.objects.get(id=id)
        form = ServiceForm(request.POST, instance=services)
        if form.is_valid():
            form.save()
            if CMS_CHECK_ON:
                CmsCheck(module=CmsModule.MAIN_SERVICE,
                         table_name='CmsServices',
                         data_id=id,
                         op_type=CheckOpType.EDIT,
                         alter_person=request.user.username,
                         alter_date=time.strftime("%Y-%m-%d %X", time.localtime())).save()
            return HttpResponseRedirect(reverse('services'))
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
        "errors": errors
    }, context_instance=RequestContext(request))


# 删除服务
@login_required
@permission_required(u'%s.%s' % (AuthCodeName.APP_LABEL, AuthCodeName.CONFIG), raise_exception=True)
def del_service(request):
    id = request.POST.get("id")
    service = CmsServices.objects.get(id=id)
    if CMS_CHECK_ON:
        check = CmsCheck(
            module=CmsModule.MAIN_SERVICE,
            table_name="CmsServices",
            data_id=id,
            op_type=CheckOpType.DELETE,
            status=CheckStatu.WAIT_SUBMIT,
            is_show=1,
            alter_person=request.user.username,
            alter_date=time.strftime("%Y-%m-%d %X", time.localtime()))
        check.save()
    service.delete()
    return HttpResponse(0)
