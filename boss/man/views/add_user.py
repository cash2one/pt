# coding: utf-8

"""
    添加用户
"""

from django.contrib.auth.decorators import permission_required
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
import json, datetime, time
from man_pub import *
from man.models import AuthUser
from django.utils import timezone


class AddUserForm(UserForm):
    pass


@login_required
@staff_member_required
@add_common_var
def add_user(request, template_name):
    if request.method == 'POST':
        print("request.method")
        form = AddUserForm(request.POST)
        if form.is_valid():
            username = request.POST.get("username", "")
            password = request.POST.get("password", "")
            group = request.POST.get("group", "")
            staff_on = request.POST.get("staff_on", "")
            user = AuthUser(username=username, password=make_password(password))
            if staff_on:
                user.is_staff = 1
            else:
                user.is_staff = 0
            user.is_active = 1
            user.is_superuser = 0
            user.last_login = timezone.now()
            user.date_joined = timezone.now()
            user.save()
            time.sleep(1)
            user_on = request.POST.get("user_on", "")
            modules = request.POST.getlist("module", [])
            apps = request.POST.getlist("app", [])
            zfs = request.POST.getlist("zf", [])
            if user_on:
                a = AuthUserUserPermissions(user=AuthUser.objects.get(username=username),
                                            permission=AuthPermission.objects.get(
                                                content_type_id=PermissionType.USER_ON))
                a.save()
            for module in modules:
                a = AuthUserUserPermissions(user=AuthUser.objects.get(username=username),
                                            permission=AuthPermission.objects.get(id=module))
                a.save()
            for app in apps:
                a = AuthUserUserPermissions(user=AuthUser.objects.get(username=username),
                                            permission=AuthPermission.objects.get(id=app))
                a.save()
            for zf in zfs:
                a = AuthUserUserPermissions(user=AuthUser.objects.get(username=username),
                                            permission=AuthPermission.objects.get(id=zf))
                a.save()
            if group:
                usergroup = AuthUserGroups(user=AuthUser.objects.get(username=username),
                                           group=AuthGroup.objects.get(id=group))
                usergroup.save()
            return HttpResponseRedirect(reverse("user_list"))
    else:
        form = AddUserForm()
    modules = get_auth_permission(PermissionType.MODULE)
    apps = get_auth_permission(PermissionType.APP)
    zfs = get_auth_permission(PermissionType.ZF)
    print("zfs is ", zfs)
    groups = get_group_list()
    return render_to_response(template_name, {
        "modules": modules,
        "apps": apps,
        "zfs": zfs,
        "groups": groups,
        "errors": form.errors,
    }, context_instance=RequestContext(request))


@login_required
@staff_member_required
def change_group(request):
    """
    根据对应的group，更新对应的模块和应用
    :param request:
    :return:
    """
    group_id = request.POST.get("group")
    staff_on, user_on, modules, apps, zfs = get_group_m_a(group_id)
    return HttpResponse(json.dumps([staff_on, user_on, modules, apps, zfs]))
