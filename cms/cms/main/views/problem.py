#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'haole'
__mtime__ = '2016/4/18'
"""
from audioop import reverse

from django.contrib.auth.decorators import login_required, permission_required
import json
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from common.const import AuthCodeName, MainConst
# from .main_pub import *
# from main.forms import *
from common.views import get_check_status_str, search_key, get_table_paginator, filter_none
from main.forms import CmsProblemForm
from main.models import CmsProblem
import logging

from main.views.main_pub import add_main_var, format_form

log = logging.getLogger('config.app')


@login_required
@add_main_var
def problem(request, template_name):
    return render_to_response(template_name, context_instance=RequestContext(request))


@login_required
def search_problem(request):
    per_page = request.GET.get("per_page")
    if not per_page:
        per_page = MainConst.PER_PAGE
    cur_page = request.GET.get("cur_page")
    if not cur_page:
        cur_page = 1
    key = request.GET.get("key")
    objs = CmsProblem.objects.all().order_by('-sort')
    problems = []
    for obj in objs:
        status_str, status_int = get_check_status_str("CmsProblem", obj.id)
        problems.append([
            obj.problem,
            obj.answer,
            obj.sort,
            obj.id
        ])
    result = search_key(problems, key, [2, 3])
    result, num_pages = get_table_paginator(result, per_page, cur_page)
    filter_none(result)
    return HttpResponse(json.dumps([list(result), num_pages]))


@add_main_var
def new(request, template_name):
    log.error("in problem")
    if request.method == "POST":
        log.error(request.POST)
        form = CmsProblemForm(request.POST)
        log.error(form.data)
        if form.is_valid():
            problem = form.save()
            return HttpResponseRedirect(reverse('problems'))
    else:
        form = CmsProblemForm()
    errors, fields = format_form(form)
    return render_to_response(template_name, {
        "errors": errors,
        "fields": fields,
    }, context_instance=RequestContext(request))


@add_main_var
def edit(request, template_name):
    id = request.GET.get("id")
    problem = CmsProblem.objects.get(id=id)

    if request.method == "POST":
        form = CmsProblemForm(request.POST, instance=problem)
        if form.is_valid():
            problem = form.save()
            return HttpResponseRedirect(reverse('problems'))
    else:
        form = CmsProblemForm(instance=problem)
    log.error(form.initial)
    errors, fields = format_form(form)
    return render_to_response(template_name, {
        "id": id,
        "errors": errors,
        "fields": fields,
    }, context_instance=RequestContext(request))


@login_required
@permission_required(u'%s.%s' % (AuthCodeName.APP_LABEL, AuthCodeName.CONFIG), raise_exception=True)
def delelte(request):
    id = request.POST.get('id')
    CmsProblem.objects.get(id=id).delete()
    return HttpResponse(0)
