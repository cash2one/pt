# coding: utf-8

# from .main_pub import *
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext

from main.models import CmsChannelChannel
from main.views.main_pub import add_main_var


@login_required
@add_main_var
def show_relate(request, template_name):
    objs = CmsChannelChannel.objects.filter(op_type=0).order_by("-id")
    return render_to_response(template_name, {
        "objs": objs,
    },context_instance=RequestContext(request))