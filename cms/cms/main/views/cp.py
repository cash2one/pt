#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'putao'
__mtime__ = '1/8/2016'
"""
import json
from django.core.urlresolvers import reverse
from common.const import MainConst
# from .main_pub import *
# from main.forms import *
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from common.views import get_table_paginator, search_key, setCpAction
from main.forms import CmsCPForm, CmsCPCategoryForm
from main.forms import CmsCpdisplayForm
from main.models import CmsCP, CmsViewCP, CmsCpdisplay, CmsCPCategory
from main.views.main_pub import add_main_var, format_form, get_actions_select

import logging

log = logging.getLogger('config.app')


@login_required
@add_main_var
def cp_list(request, template_name):
    return render_to_response(template_name, context_instance=RequestContext(request))


@login_required
def search_cps(request):
    """CP数据"""
    per_page = request.GET.get("per_page")
    if not per_page:
        per_page = MainConst.PER_PAGE
    cur_page = request.GET.get("cur_page")
    if not cur_page:
        cur_page = 1
    objs = CmsCP.objects.all().order_by("-sort")
    cps = []
    for obj in objs:
        try:
            category = CmsViewCP.objects.get(cp=obj).cp_category.name
        except:
            category = ""
        status_str, status_int = "", 1
        cps.append([
            obj.id,
            obj.name,
            obj.desc,
            obj.icon,
            category,
            # obj.location1,
            obj.location2,
            status_str,
            obj.tag_in_list,
            obj.sort,
            status_int,
            obj.id
        ])
    key = request.GET.get("key")
    cps = search_key(cps, key, [2, 7, 8])
    result, num_pages = get_table_paginator(cps, per_page, cur_page)
    return HttpResponse(json.dumps([list(result), num_pages]))


@login_required
def exchange_sort(request):
    cp_id = request.POST.get('cp_id')
    sort = request.POST.get('sort')
    data = {}
    data['sort'] = sort
    CmsCP.objects.filter(id=cp_id).update(**data)
    return HttpResponse(0)


@login_required
@add_main_var
def edit_cp(request, template_name):
    id = request.GET.get("id")
    ins_cp = CmsCP.objects.get(id=id)
    try:
        cpdis_ins = CmsCpdisplay.objects.get(meta_id=id, parent_id=0)
    except Exception as ex:
        cpdis_ins = None
    if request.method == "POST":
        form = CmsCPForm(request.POST, instance=ins_cp)
        cpdis_form = CmsCpdisplayForm(request.POST, instance=cpdis_ins)
        log.error(cpdis_form.data)
        log.error("form_is_valid:" + str(form.is_valid()))
        log.error("cpdis_form_is_valid:" + str(cpdis_form.is_valid()))
        if form.is_valid() and cpdis_form.is_valid():
            form.save()
            cpdis_form.save()
            cp_category = request.POST.get("cp_category")
            if CmsViewCP.objects.filter(cp_id=id):
                ins_viewcp = CmsViewCP.objects.get(cp_id=id)
                ins_viewcp.cp_category_id = cp_category
                ins_viewcp.save()
            else:
                CmsViewCP(cp_id=id, cp_category_id=cp_category).save()
            setCpAction(id, request.POST.get('action_id'))
            return HttpResponseRedirect(reverse('cp_list'))
    else:
        form = CmsCPForm(instance=ins_cp)
        cpdis_form = CmsCpdisplayForm(instance=cpdis_ins)
    errors, fields = format_form(form)
    cpdiserrors, cpdisfields = format_form(cpdis_form)
    if CmsViewCP.objects.filter(cp_id=id):
        fields['cp_category'] = json.dumps(CmsViewCP.objects.get(cp_id=id).cp_category_id)
    actions = get_actions_select()
    cp_cates = CmsCPCategory.objects.all()
    return render_to_response(template_name, {
        "id": id,
        "errors": errors,
        "fields": fields,
        "cp_cates": cp_cates,
        "actions": actions,
        "cpdiserrors": cpdiserrors,
        "cpdisfields": cpdisfields
    }, context_instance=RequestContext(request))


@login_required
def del_cp(request):
    id = request.POST.get('id')
    CmsCP.objects.get(id=id).delete()
    return HttpResponse(0)


@login_required
@add_main_var
def cp_category_list(request, template_name):
    return render_to_response(template_name, context_instance=RequestContext(request))


@login_required
def search_cp_category(request):
    """CP分类数据"""
    per_page = request.GET.get("per_page")
    if not per_page:
        per_page = MainConst.PER_PAGE
    cur_page = request.GET.get("cur_page")
    if not cur_page:
        cur_page = 1
    objs = CmsCPCategory.objects.all()
    categories = []
    for obj in objs:
        status_str, status_int = "", 1
        categories.append([
            obj.name,
            obj.location,
            status_str,
            status_int,
            obj.id
        ])
    key = request.GET.get("key")
    categories = search_key(categories, key, [3, 4])
    result, num_pages = get_table_paginator(categories, per_page, cur_page)
    return HttpResponse(json.dumps([list(result), num_pages]))


@login_required
@add_main_var
def new_cp_category(request, template_name):
    if request.method == "POST":
        form = CmsCPCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('cp_category_list'))
    else:
        form = CmsCPCategoryForm()
    errors, fields = format_form(form)
    return render_to_response(template_name, {
        "errors": errors,
        "fields": fields
    }, context_instance=RequestContext(request))


@login_required
@add_main_var
def edit_cp_category(request, template_name):
    id = request.GET.get("id")
    ins_cp_category = CmsCPCategory.objects.get(id=id)
    if request.method == "POST":
        form = CmsCPCategoryForm(request.POST, instance=ins_cp_category)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('cp_category_list'))
    else:
        form = CmsCPCategoryForm(instance=ins_cp_category)
    errors, fields = format_form(form)
    return render_to_response(template_name, {
        "id": id,
        "errors": errors,
        "fields": fields
    }, context_instance=RequestContext(request))


@login_required
def del_cp_category(request):
    id = request.POST.get('id')
    CmsCPCategory.objects.get(id=id).delete()
    return HttpResponse(0)
