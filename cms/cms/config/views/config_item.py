# coding: utf-8
"""
    配置项
"""
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from common.const import get_nav_text
# from config.views.config_pub import *
from main.models import CmsChannels
from main.views.main_pub import add_main_var


@login_required
@add_main_var
def config_item(request, template_name):
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
        "channel": channel
    },context_instance=RequestContext(request))
