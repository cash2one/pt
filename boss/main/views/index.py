#coding: utf-8

"""
    首页
"""

from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from man.models import AuthUserUserPermissions
from main_pub import *




@login_required
@add_common_var
def index(request, template_name):
    user = auth.get_user(request)
    #判断该用户是否有用户模块
    has_user = False
    objs = AuthUserUserPermissions.objects.filter(user__id__exact=user.id)
    for obj in objs:
        if obj.permission.content_type_id == PermissionType.USER_ON:
            has_user = True
            break
    #判断该用户是否有业务模块
    has_report = False
    for obj in objs:
        if obj.permission.content_type_id == PermissionType.MODULE:
            has_report = True
            break
    #往下传递第一个应用
    apps = []
    for obj in objs:
        if obj.permission.content_type_id == PermissionType.APP :
            apps.append(obj.permission.name)
    if not apps:
        first_app = "none"
    elif "" in apps:
        first_app = ""
    else:
        first_app = apps[0]
    return report_render(request,template_name, {
        "is_staff": user.is_staff,
        "has_user": has_user,
        "has_report": has_report,
        "first_app": first_app
    })
