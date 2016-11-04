#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'putao'
__mtime__ = '1/11/2016'
"""

# from config.views.config_pub import *
from common.const import get_nav_text
from common.views import filter_none, setCpAction
from config.views.config_pub import get_all_cps
from main.forms import CmsCpdisplayForm, CmsCPForm
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
import json
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

from main.models import CmsChannels, CmsCpdisplay, CmsHomeCP, getCVT, CmsCP, CmsViewCP, CmsCPCategory
from main.views.main_pub import add_main_var, format_form, \
    get_actions_select


# 要支持按照城市筛选
@login_required
@add_main_var
def cps(request, template_name):
    t = request.GET.get("t")
    if not t:
        t = "1"
    v = request.GET.get("v")
    c = request.GET.get("c")
    channel = CmsChannels.objects.get(channel_no=c, app_version__app_version=v, app_version__type_id=t).id
    cps = get_all_cps()
    return render_to_response(template_name, {
        "text": get_nav_text(t),
        "t": t,
        "v": v,
        "c": c,
        "channel": channel,
        "cps": cps
    }, context_instance=RequestContext(request))


def search(request):
    channel = request.GET.get("channel")
    cps = CmsCpdisplay.objects.filter(cmshomecp__channel__id=channel)
    result = []
    for cp in cps:
        status_str, status_int = "", 1
        item = [
            cp.location1,
            cp.meta.location2,
            cp.meta.icon,
            cp.meta.name,
            cp.text,
            cp.mark,
            cp.op_desc,
            cp.meta.action_id,
            status_str,
            status_int,
            cp.id
        ]
        result.append(item)
    filter_none(result)
    return HttpResponse(json.dumps(result))


@login_required
def new(request):
    if request.method == 'POST':
        data = request.POST.copy()
        error = ""
        for key in data:
            if data[key] == "":
                error += key + " is null \n"
        if error:
            return HttpResponse(error)
        else:
            cp_id = request.POST.get("cp_id")
            channel_id = request.POST.get("channel_id")
            try:
                if CmsCpdisplay.objects.filter(meta_id=cp_id, parent_id=0):
                    ins_cpdis = CmsCpdisplay.objects.get(meta_id=cp_id, parent_id=0)
                    ins_cpdis.id = None
                    ins_cpdis.parent_id = 1
                    ins_cpdis.save()
                else:
                    ins_cpdis = CmsCpdisplay(meta_id=cp_id, parent_id=1, location1=1)
                    ins_cpdis.save()
                CmsHomeCP(channel_id=channel_id, cp=ins_cpdis).save()
            except Exception as ex:
                return HttpResponse(ex.args[0])
            return HttpResponse(0)


@login_required
@add_main_var
def edit(request, template_name):
    id = request.GET.get("id")
    channel_id = request.GET.get('channel')
    c, v, t = getCVT(channel_id)
    text = get_nav_text(str(t))
    cpdis_ins = CmsCpdisplay.objects.get(id=id)
    cp_id = cpdis_ins.meta_id
    ins_cp = CmsCP.objects.get(id=cpdis_ins.meta_id)
    if request.method == "POST":
        form = CmsCPForm(request.POST, instance=ins_cp)
        cpdis_form = CmsCpdisplayForm(request.POST, instance=cpdis_ins)
        if form.is_valid() and cpdis_form.is_valid():
            form.save()
            cpdis_form.save()
            cp_category = request.POST.get("cp_category")
            if CmsViewCP.objects.filter(cp_id=cp_id):
                ins_viewcp = CmsViewCP.objects.get(cp_id=cp_id)
                ins_viewcp.cp_category_id = cp_category
                ins_viewcp.save()
            else:
                CmsViewCP(cp_id=cp_id, cp_category_id=cp_category).save()
            setCpAction(cp_id, request.POST.get('action_id'))
            return HttpResponseRedirect(reverse('config_cp_list') + "?t=%d&c=%s&v=%s" % (t, c, v))
    else:
        form = CmsCPForm(instance=ins_cp)
        cpdis_form = CmsCpdisplayForm(instance=cpdis_ins)
    errors, fields = format_form(form)
    cpdiserrors, cpdisfields = format_form(cpdis_form)
    if CmsViewCP.objects.filter(cp_id=cp_id):
        fields['cp_category'] = json.dumps(CmsViewCP.objects.get(cp_id=cp_id).cp_category_id)
    actions = get_actions_select()
    cp_cates = CmsCPCategory.objects.all()
    return render_to_response(template_name, {
        "t": t,
        "v": v,
        "c": c,
        "text": text,
        "id": id,
        "cp_id": cp_id,
        "channel": channel_id,
        "errors": errors,
        "fields": fields,
        "cp_cates": cp_cates,
        "actions": actions,
        "cpdiserrors": cpdiserrors,
        "cpdisfields": cpdisfields
    }, context_instance=RequestContext(request))


@login_required
def delelte(request):
    id = request.POST.get('id')
    CmsCpdisplay.objects.get(id=id).delete()
    return HttpResponse(0)
