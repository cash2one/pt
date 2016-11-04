# coding: utf-8

"""
    动作
"""
import time
from django.contrib.auth.decorators import login_required, permission_required
import json
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

from cms.settings import CMS_CHECK_ON
from common.const import AuthCodeName, CmsModule, MainConst, CheckOpType, CheckStatu
# from .main_pub import *
# from main.forms import *
from common.views import get_check_status_str, search_key, get_table_paginator, filter_none, get_url_arg
from main.forms import ActionForm
from main.models import CmsCheck, CmsActions
from main.views.main_pub import add_main_var, format_form, slice_actions_select
from .main_pub import get_actions_select

@login_required
@add_main_var
def actions(request, template_name):
    return render_to_response(template_name, context_instance=RequestContext(request))


# 新增动作
@login_required
@permission_required(u'%s.%s' % (AuthCodeName.APP_LABEL, AuthCodeName.CONFIG), raise_exception=True)
@add_main_var
def new_action(request, template_name):
    if request.method == "POST":
        form = ActionForm(request.POST)
        if form.is_valid():
            actions = form.save()
            if CMS_CHECK_ON:
                CmsCheck(module=CmsModule.MAIN_ACTION,
                         table_name='CmsActions',
                         data_id=actions.id,
                         op_type=CheckOpType.NEW,
                         alter_person=request.user.username,
                         alter_date=time.strftime("%Y-%m-%d %X", time.localtime())).save()
            return HttpResponseRedirect(reverse('actions'))
    else:
        form = ActionForm()
    errors, fields = format_form(form)
    return render_to_response(template_name, {
        "errors": errors,
        "fields": fields
    }, context_instance=RequestContext(request))


# 编辑动作
@login_required
@permission_required(u'%s.%s' % (AuthCodeName.APP_LABEL, AuthCodeName.CONFIG), raise_exception=True)
@add_main_var
def edit_action(request, template_name):
    id = request.GET.get("id")
    if request.method == 'POST':
        actions = CmsActions.objects.get(id=id)
        form = ActionForm(request.POST, instance=actions)
        if form.is_valid():
            form.save()
            if CMS_CHECK_ON:
                CmsCheck(module=CmsModule.MAIN_ACTION,
                         table_name='CmsActions',
                         data_id=id,
                         op_type=CheckOpType.EDIT,
                         alter_person=request.user.username,
                         alter_date=time.strftime("%Y-%m-%d %X", time.localtime())).save()
            return HttpResponseRedirect(reverse('actions'))
    else:
        actions = CmsActions.objects.get(id=id)
        form = ActionForm(instance=actions)
    errors, fields = format_form(form)
    return render_to_response(template_name, {
        "id": id,
        "errors": errors,
        "fields": fields
    }, context_instance=RequestContext(request))


@login_required
def search_actions(request):
    per_page = request.GET.get("per_page")
    if not per_page:
        per_page = MainConst.PER_PAGE
    cur_page = request.GET.get("cur_page")
    if not cur_page:
        cur_page = 1
    key = request.GET.get("key")
    objs = CmsActions.objects.all()
    actions = []
    for obj in objs:
        if obj.type == 1:
            type = "打开特定服务页面"
        elif obj.type == 2:
            type = "打开特定链接H5页面"
        else:
            type = ""
        status_str, status_int = get_check_status_str("CmsActions", obj.id)
        actions.append([
            obj.id,
            obj.dest_title,
            type,
            obj.dest_activity,
            obj.dest_url,
            obj.cp_info,
            status_str,
            status_int,
            obj.id
        ])
    result = search_key(actions, key, [7, 8])
    result, num_pages = get_table_paginator(result, per_page, cur_page)
    filter_none(result)
    return HttpResponse(json.dumps([
        list(result), num_pages
    ]))


# 删除动作
@login_required
@permission_required(u'%s.%s' % (AuthCodeName.APP_LABEL, AuthCodeName.CONFIG), raise_exception=True)
def del_action(request):
    id = request.POST.get("id")
    action = CmsActions.objects.get(id=id)
    if CMS_CHECK_ON:
        check = CmsCheck(
            module=CmsModule.MAIN_ACTION,
            table_name="CmsActions",
            data_id=id,
            op_type=CheckOpType.DELETE,
            status=CheckStatu.WAIT_SUBMIT,
            is_show=1,
            alter_person=request.user.username,
            alter_date=time.strftime("%Y-%m-%d %X", time.localtime()))
        check.save()
    action.delete()
    return HttpResponse(0)


# ajax获取动作
def ajax_actions(request):
    page = get_url_arg(request, 'page', int, 1)
    per_page = get_url_arg(request, 'per_page', int, 15)
    search_key = get_url_arg(request, 'search_key', str, None)
    total_page, actions = slice_actions_select(search_key, page=page, per_page=per_page)
    result = {'total_page': total_page, 'cur_page': page, "actions": actions}
    return HttpResponse(json.dumps(result))
