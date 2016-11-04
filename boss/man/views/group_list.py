# coding: utf-8


"""
    分组列表
"""


from django.shortcuts import render_to_response
import json
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import RequestContext
from man_pub import *



@login_required
@staff_member_required
@add_common_var
def group_list(request, template_name):
    return render_to_response(template_name)



@login_required
@staff_member_required
@add_common_var
def redirect_per_list(request, template_name):
    usr = request.user
    if usr is None:
        return render_to_response(template_name)
    u = str(usr.id)
    n = str(usr.username)
    return HttpResponseRedirect('/man/view_user/?u='+u+'&n='+n)


@login_required
@staff_member_required
def group_list_ajax(request):
    result = get_group_list()
    return HttpResponse(json.dumps(result))


class EditGroupForm(GroupForm):
    pass



@login_required
@staff_member_required
@add_common_var
def edit_group(request, template_name):
    group_id = request.GET.get("g")
    group = AuthGroup.objects.get(id=group_id)
    if request.method == 'POST':
        form = EditGroupForm(request.POST)
        if form.is_valid():
            group_name = request.POST.get("group_name", "")
            staff_on = request.POST.get("staff_on", "")
            user_on = request.POST.get("user_on", "")
            modules = request.POST.getlist("module", [])
            apps = request.POST.getlist("app", [])
            zfs = request.POST.getlist("zf", [])
            group.name = group_name
            group.save()
            AuthGroupPermissions.objects.filter(group=group_id).delete()
            if staff_on:
                a = AuthGroupPermissions(group=AuthGroup.objects.get(name=group_name), permission=AuthPermission.objects.get(content_type_id=PermissionType.STAFF_ON))
                a.save()
            if user_on:
                a = AuthGroupPermissions(group=AuthGroup.objects.get(name=group_name), permission=AuthPermission.objects.get(content_type_id=PermissionType.USER_ON))
                a.save()
            for module in modules:
                a = AuthGroupPermissions(group=AuthGroup.objects.get(name=group_name), permission=AuthPermission.objects.get(id=module))
                a.save()
            for app in apps:
                a = AuthGroupPermissions(group=AuthGroup.objects.get(name=group_name), permission=AuthPermission.objects.get(id=app))
                a.save()
            for zf in zfs:
                a = AuthGroupPermissions(group=AuthGroup.objects.get(name=group_name), permission=AuthPermission.objects.get(id=zf))
                a.save()
            return HttpResponseRedirect(reverse("group_list"))
    else:
        form = EditGroupForm()

    modules = get_auth_permission(PermissionType.MODULE)
    apps = get_auth_permission(PermissionType.APP)
    zfs = get_auth_permission(PermissionType.ZF)
    staff_on, user_on, m_select, a_select, z_select = get_group_m_a(group_id)
    return render_to_response(template_name, {
        "staff_on": staff_on,
        "user_on": user_on,
        "modules": modules,
        "apps": apps,
        "zfs": zfs,
        "group_name": group.name,
        "m_select": m_select,
        "a_select": a_select,
        "z_select": z_select,
        "errors": form.errors
    },context_instance=RequestContext(request))


@login_required
@staff_member_required
def del_group(request):
    g = request.POST.get("g", "")
    AuthGroup.objects.get(id=g).delete()
    result = get_group_list()
    return HttpResponse(json.dumps(result))



@login_required
@staff_member_required
@add_common_var
def view_group(request, template_name):
    g = request.GET.get("g", "")
    n = request.GET.get("n", "")
    user_on = "关"
    staff_on = "关"
    modules = []
    apps = []
    if g:
        objs = AuthGroupPermissions.objects.filter(group__id__exact=g)
        for obj in objs:
            if obj.permission.content_type_id == PermissionType.MODULE:
                modules.append(obj.permission.codename)
            elif obj.permission.content_type_id == PermissionType.APP:
                apps.append(obj.permission.codename)
            elif obj.permission.content_type_id == PermissionType.USER_ON:
                user_on = "开"
            elif obj.permission.content_type_id == PermissionType.STAFF_ON:
                staff_on = "开"
    if not modules:
        modules = ["无"]
    if not apps:
        apps = ["无"]
    return render_to_response(template_name, {
        "user_on": user_on,
        "staff_on": staff_on,
        "modules": modules,
        "apps": apps,
        "name": n
    })
