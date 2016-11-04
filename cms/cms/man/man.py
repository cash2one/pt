# coding: utf-8
"""
    账号管理，不做审核，也就是不移动到正式数据库里
"""
from django.contrib.auth.hashers import make_password
import json
from django.views.decorators.http import require_POST

from common.const import AuthCodeName
# from .main_pub import *
# from main.forms import *
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

from main.forms import AuthUserForm
from .models import AuthUser, AuthPermission, AuthUserUserPermissions, AuthUserGroups, AuthGroup
from main.views.main_pub import add_main_var, format_form


@login_required
@permission_required(u'%s.%s' % (AuthCodeName.APP_LABEL, AuthCodeName.MAN), raise_exception=True)
@add_main_var
def man(request, template_name):
    staffs = AuthUser.objects.filter(is_staff=1).values_list("username", "is_superuser")
    operators = AuthUser.objects.filter(is_staff=0).values_list("username")
    check = AuthPermission.objects.get(codename=AuthCodeName.CHECK).id
    config = AuthPermission.objects.get(codename=AuthCodeName.CONFIG).id
    objs = AuthUser.objects.all()
    user_datas = []
    for obj in objs:
        auth = {}
        try:
            auth["config"] = AuthUserUserPermissions.objects.get(
                user=obj, permission=AuthPermission.objects.get(codename=AuthCodeName.CONFIG)).permission.id
        except:
            pass
        try:
            auth["check"] = AuthUserUserPermissions.objects.get(
                user=obj, permission=AuthPermission.objects.get(codename=AuthCodeName.CHECK)).permission.id
        except:
            pass
        user_datas.append({
            "id": obj.id,
            "username": obj.username,
            "email": obj.email,
            "auth": auth
        })
    return render_to_response(template_name, {
        "staffs": staffs,
        "operators": operators,
        "check": check,
        "config": config,
        "user_datas": json.dumps(user_datas)
    }, context_instance=RequestContext(request))


@login_required
@staff_member_required
def delete_operators(request):
    ids = json.loads(request.POST.get('ids'))
    AuthUser.objects.filter(id__in=ids, is_superuser=0, is_staff=0).delete()
    return HttpResponse(0)


@login_required
@permission_required(u'user.is_superuser', raise_exception=True)
def delete_staffs(request):
    ids = json.loads(request.POST.get('ids'))
    AuthUser.objects.filter(id__in=ids, is_superuser=0, is_staff=1).delete()
    return HttpResponse(0)


@login_required
@permission_required(u'user.is_superuser', raise_exception=True)
@require_POST
def new_staff(request):
    """
    新建 管理员
    url : {% url 'new_staff' %}
    :请求方式：ajax
    :请求参数：permissions权限id列表 对其进行序列化
        username
        password
        email
        is_staff 值为1
    :返回: 成功返回0 错误返回errors
    """
    if request.method == "POST":
        permissions = request.POST.get("permissions")
        permissions = json.loads(permissions)
        data = request.POST.copy()
        password = make_password(data["password"])
        data["password"] = password
        form = AuthUserForm(data)
        if form.is_valid():
            try:
                authuser = form.save()
                AuthUserGroups(user=authuser, group=AuthGroup.objects.get(id=5)).save()
                for permission in permissions:
                    AuthUserUserPermissions(user=authuser, permission=AuthPermission.objects.get(id=permission)).save()
                return HttpResponse(0)
            except Exception as ex:
                return HttpResponse(ex.args[0])
        else:
            errors, fields = format_form(form)
            return HttpResponse(errors)


@login_required
@staff_member_required
@require_POST
def new_operator(request):
    """
    新建 运营人员
    url : {% url 'new_operator' %}
    :请求方式：ajax
    :请求参数：permissions权限id列表 对其进行序列化
        username
        password
        email
        is_staff 值为0
    :返回: 成功返回0 错误返回errors
    """
    if request.method == "POST":
        permissions = json.loads(request.POST.get("permissions"))
        data = request.POST.copy()
        password = make_password(data["password"])
        data["password"] = password
        form = AuthUserForm(data)
        if form.is_valid():
            try:
                authuser = form.save()
                AuthUserGroups(user=authuser, group=AuthGroup.objects.get(id=3)).save()
                for permission in permissions:
                    AuthUserUserPermissions(user=authuser, permission=AuthPermission.objects.get(id=permission)).save()
                return HttpResponse(0)
            except Exception as ex:
                return HttpResponse(ex.args[0])
        else:
            errors, fields = format_form(form)
            return HttpResponse(errors)


@login_required
@permission_required(u'user.is_superuser', raise_exception=True)
@require_POST
def edit_staff(request):
    """
    编辑 管理员
    url : {% url 'edit_staff' %}
    :请求方式：ajax
    :请求参数：
        id 用户表id
        permissions权限id列表 对其进行序列化
        username
        password
        email
        is_staff 值为1
    :返回: 成功返回0 错误返回errors
    """
    if request.method == "POST":
        permissions = json.loads(request.POST.get("permissions"))
        id = request.POST.get("id")
        authuser = AuthUser.objects.get(id=id)
        data = request.POST.copy()

        password = make_password(data["password"])
        if data["password"] and password != authuser.password:
            data["password"] = password
        else:
            data["password"] = authuser.password
        form = AuthUserForm(data, instance=authuser)
        if form.is_valid():
            try:
                form.save()
                AuthUserUserPermissions.objects.filter(user=authuser).delete()
                for permission in permissions:
                    AuthUserUserPermissions(user=authuser, permission=AuthPermission.objects.get(id=permission)).save()
                return HttpResponse(0)
            except Exception as ex:
                return HttpResponse(ex.args[0])
        else:
            errors, fields = format_form(form)
            return HttpResponse(errors)


@login_required
@staff_member_required
@require_POST
def edit_operator(request):
    """
    编辑 运营人员
    url : {% url 'edit_operator' %}
    :请求方式：ajax
    :请求参数：
        id 用户表id
        permissions权限id列表 对其进行序列化
        username
        password
        email
        is_staff 值为0
    :返回: 成功返回0 错误返回errors
    """
    if request.method == "POST":
        permissions = json.loads(request.POST.get("permissions"))
        id = request.POST.get("id")
        authuser = AuthUser.objects.get(id=id)
        data = request.POST.copy()
        password = make_password(data["password"])
        if data["password"] and password != authuser.password:
            data["password"] = password
        else:
            data["password"] = authuser.password
        form = AuthUserForm(data, instance=authuser)
        if form.is_valid():
            try:
                form.save()
                AuthUserUserPermissions.objects.filter(user=authuser).delete()
                for permission in permissions:
                    AuthUserUserPermissions(user=authuser, permission=AuthPermission.objects.get(id=permission)).save()
                return HttpResponse(0)
            except Exception as ex:
                return HttpResponse(ex.args[0])
        else:
            errors, fields = format_form(form)
            return HttpResponse(errors)
