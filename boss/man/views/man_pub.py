# coding: utf-8


from django.contrib.auth.decorators import login_required
import functools
from django.contrib import auth
from django.core.exceptions import PermissionDenied

from man.models import *
from django import forms
from common.views import *

def staff_member_required(view_func):
    """
    Decorator for views that checks that the user is logged in and is a staff
    member, displaying the login page if necessary.
    """
    @functools.wraps(view_func)
    def _checklogin(request, *args, **kwargs):
        if request.user.is_active and request.user.is_staff:
            # The user is valid. Continue to the admin page.
            return view_func(request, *args, **kwargs)

        raise PermissionDenied

    return _checklogin

def add_man_var(f):
    @functools.wraps(f)
    def _(*args, **kwargs):
        result = f(*args, **kwargs)
        vars = {
            "user": auth.get_user(args[0]).username,
            # "lasturl": args[0].path
            "lasturl": args[0].get_full_path(),
        }
        for key in vars:
            result.content = result.content.replace("{_tongji_begin_%s_end_}" % key, vars[key])
        return result
    return _


class GroupForm(forms.Form):
    group_name = forms.CharField(min_length=1, max_length=80)
    modules = forms.CharField(required=False)
    apps = forms.CharField(required=False)


class UserForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(max_length=128)
    modules = forms.CharField(required=False)
    apps = forms.CharField(required=False)


def get_auth_permission(content_type_id):
    """
    获取report应用需要控制的所有权限
    :return:
    """
    objs = AuthPermission.objects.filter(content_type_id=content_type_id).order_by('module_id')
    result = []
    for obj in objs:
        mg= ModuleGroup.objects.filter(id = obj.module_id) if obj.module_id  is not None else ''
        module_name = mg[0].name if  mg else ''
        result.append([obj.id, obj.codename, module_name,obj.module_id,obj.name])
    print("auth permission is ", content_type_id, result)
    return result


def get_group_m_a(group_id):
    staff_on = False
    user_on = False
    m_select = []
    a_select = []
    z_select = []
    if group_id:
        group = AuthGroup.objects.get(id=group_id)
        authpermission = AuthGroupPermissions.objects.filter(group=group)
        for a in authpermission:
            t = a.permission
            if t.content_type_id == PermissionType.MODULE:
                m_select.append(int(t.id))
            elif t.content_type_id == PermissionType.APP:
                a_select.append(int(t.id))
            elif t.content_type_id == PermissionType.ZF:
                z_select.append(int(t.id))
            elif t.content_type_id == PermissionType.USER_ON:
                user_on = True
            elif t.content_type_id == PermissionType.STAFF_ON:
                staff_on = True
    return staff_on, user_on, m_select, a_select, z_select


def get_group_list():
    objs = AuthGroup.objects.all()
    result = []
    for obj in objs:
        result.append([obj.name, obj.id])
    return result


def get_user_m_a(user_id):
    user = AuthUser.objects.get(id=user_id)
    authpermission = AuthUserUserPermissions.objects.filter(user=user)
    user_on = False
    staff_on = user.is_staff
    m_select = []
    a_select = []
    z_select = []
    for a in authpermission:
        t = a.permission
        if t.content_type_id == PermissionType.MODULE:
            m_select.append(int(t.id))
        elif t.content_type_id == PermissionType.APP:
            a_select.append(int(t.id))
        elif t.content_type_id == PermissionType.ZF:
            z_select.append(int(t.id))
        elif t.content_type_id == PermissionType.USER_ON:
            user_on = True
    return staff_on, user_on, m_select, a_select, z_select


def get_user_list():
    objs = AuthUser.objects.all()
    result = []
    for obj in objs:
        try:
            name = AuthUserGroups.objects.get(user=obj).group.name
        except:
            name = ""
        result.append([obj.username, name, obj.id])
    return result


