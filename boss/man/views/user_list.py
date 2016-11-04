# coding: utf-8


"""
    用户列表
"""


from django.contrib.auth.decorators import permission_required
from django.shortcuts import render_to_response
import json
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.hashers import make_password
from django.template import RequestContext
from man_pub import *




@login_required
@staff_member_required
@add_common_var
def user_list(request, template_name):
    groups = get_group_list()
    return render_to_response(template_name, {
        "groups": groups
    })


@login_required
@staff_member_required
def user_list_ajax(request):
    result = get_user_list()
    return HttpResponse(json.dumps(result))


class EditUserForm(UserForm):
    password = forms.CharField(max_length=128, required=False)

@login_required
@staff_member_required
@add_common_var
def redirect_edit_user(request,template_name):
    usr = request.user
    if usr is None:
        return render_to_response(template_name)
    u = str(usr.id)
    return HttpResponseRedirect('/man/edit_user/?u=' + u)

@login_required
@staff_member_required
@add_common_var
def edit_user(request, template_name):
    user_id = request.GET.get("u")
    user = AuthUser.objects.get(id=user_id)
    if request.method == 'POST':
        form = EditUserForm(request.POST)
        if form.is_valid():
            username = request.POST.get("username", "")
            password = request.POST.get("password", "")
            group = request.POST.get("group", "")
            staff_on = request.POST.get("staff_on", "")
            user_on = request.POST.get("user_on", "")
            modules = request.POST.getlist("module", [])
            apps = request.POST.getlist("app", [])
            zfs = request.POST.getlist("zf", [])
            user.name = username
            if password:
                user.password = make_password(password)
            if staff_on:
                user.is_staff = 1
            else:
                user.is_staff = 0
            user.save()
            AuthUserUserPermissions.objects.filter(user=user).delete()
            if user_on:
                a = AuthUserUserPermissions(user=AuthUser.objects.get(username=username), permission=AuthPermission.objects.get(content_type_id=PermissionType.USER_ON))
                a.save()
            for module in modules:
                a = AuthUserUserPermissions(user=AuthUser.objects.get(username=username), permission=AuthPermission.objects.get(id=module))
                a.save()
            for app in apps:
                a = AuthUserUserPermissions(user=AuthUser.objects.get(username=username), permission=AuthPermission.objects.get(id=app))
                a.save()
            for zf in zfs:
                a = AuthUserUserPermissions(user=AuthUser.objects.get(username=username), permission=AuthPermission.objects.get(id=zf))
                a.save()
            try:
                AuthUserGroups.objects.get(user=user).delete()
            except:
                pass
            if group:
                usergroup = AuthUserGroups(user=user, group=AuthGroup.objects.get(id=group))
                usergroup.save()
            return HttpResponseRedirect(reverse("user_list"))
    else:
        form = EditUserForm()
    modules = get_auth_permission(PermissionType.MODULE)
    apps = get_auth_permission(PermissionType.APP)
    zfs = get_auth_permission(PermissionType.ZF)
    staff_on, user_on, m_select, a_select, z_select = get_user_m_a(user_id)
    try:
        group = AuthUserGroups.objects.get(user=user_id).group.id
    except:
        group = ""
    groups = get_group_list()
    return render_to_response(template_name, {
        "modules": modules,
        "apps": apps,
        "zfs": zfs,
        "username": user.username,
        "groups": groups,
        "group": group,
        "staff_on": staff_on,
        "user_on": user_on,
        "m_select": m_select,
        "a_select": a_select,
        "z_select":z_select,
        "errors": form.errors,
    },context_instance=RequestContext(request))


@login_required
@staff_member_required
def del_user(request):
    u = request.POST.get("u", "")
    AuthUser.objects.get(id=u).delete()
    result = get_user_list()
    return HttpResponse(json.dumps(result))



@login_required
@staff_member_required
@add_common_var
def view_user(request, template_name):
    u = request.GET.get("u", "")
    n = request.GET.get("n", "")
    user_on = "关"
    staff_on = "关"
    modules = []
    apps = []
    zfs = []
    if u:
        objs = AuthUserUserPermissions.objects.filter(user__id__exact=u)
        for obj in objs:
            if obj.permission.content_type_id == PermissionType.MODULE:
                modules.append(obj.permission.codename)
            elif obj.permission.content_type_id == PermissionType.APP:
                apps.append(obj.permission.codename)
            elif obj.permission.content_type_id == PermissionType.USER_ON:
                user_on = "开"
            elif obj.permission.content_type_id == PermissionType.ZF:
                zfs.append(obj.permission.codename)
        if AuthUser.objects.get(id=u).is_staff:
            staff_on = "开"

    if not modules:
        modules = ["无"]
    if not apps:
        apps = ["无"]
    if not zfs:
        zfs = ["无"]
    return render_to_response(template_name, {
        "staff_on": staff_on,
        "user_on": user_on,
        "modules": modules,
        "apps": apps,
        "name": n,
        "zfs": zfs,
    })
