# -*- coding: utf-8 -*-
# Author:songroger
# Jul.26.2016
from main.views.main_pub import add_main_var
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
import requests
from main.models import CmsChannels
from main.views.main_pub import get_city_list
type_text = {"1": u"葡萄生活Android版", "2": u"生活黄页",
             "4": u"葡萄生活H5版", "5": u"葡萄生活iOS版"}


@login_required
@add_main_var
def url_test(request, template_name):
    return render_to_response(template_name,
                              context_instance=RequestContext(request))


@login_required
@add_main_var
def render_page(request, template_name, uptoken=False, channel=False, city=False):
    data = {}
    if uptoken:
        r = requests.get("http://cms.putao.so/uptoken/")
        up_token = r.json().get("token", None)
        data.update({"token": up_token})
    if channel:
        t = request.GET.get("t", "1")
        v = request.GET.get("v")
        c = request.GET.get("c")
        ch = CmsChannels.objects.get(
            channel_no=c, app_version__app_version=v, app_version__type_id=t)
        data.update({"channel": ch.id, "t": t, "v": v,
                     "c": c, "text": type_text.get(t)})
    if city:
        data.update({"cities": get_city_list()})
    context_instance = RequestContext(request, data)
    return render_to_response(template_name, context_instance=context_instance)
