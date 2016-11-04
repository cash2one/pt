# coding：utf-8
import json

from django.shortcuts import render, render_to_response
from django.template import RequestContext


# 获取提交过来的数据返回给app选择页面
def up_shelves_app(request, template_name):
    # up_data=request.POST.copy()
    up_data = [u'64', u'GY']
    return render_to_response(template_name, {"up_data": up_data}, context_instance=RequestContext(request))


def up_shelves(request, template_name):
    up_data = [u'64', u'GY']
    return render_to_response(template_name, {"up_data": up_data}, context_instance=RequestContext(request))


def down_shelves():
    pass
