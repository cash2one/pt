#coding: utf-8

"""
    页面访问路径
"""

from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from main_pub import *




@login_required
@permission_required(u'man.%s' % MainConst.USER_ON, raise_exception=True)
@add_common_var
def page_access_path(request, template_name):
    return report_render(request,template_name)