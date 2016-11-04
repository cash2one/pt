# coding: utf-8

"""
    添加分组
"""

from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from man_pub import *


class AddGroupForm(GroupForm):
    def clean_group_name(self):
        group_name = self.cleaned_data['group_name']
        if AuthGroup.objects.filter(name=group_name):
            raise forms.ValidationError("分组名称%s重复" % group_name)
        return group_name



@login_required
@staff_member_required
@add_common_var
def add_group(request, template_name):
    if request.method == 'POST':
        form = AddGroupForm(request.POST)
        if form.is_valid():
            group_name = request.POST.get("group_name", "")
            user_on = request.POST.get("user_on", "")
            staff_on = request.POST.get("staff_on", "")
            modules = request.POST.getlist("module", [])
            apps = request.POST.getlist("app", [])
            zfs = request.POST.getlist("zf", [])
            group = AuthGroup(name=group_name)
            group.save()
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
        form = AddGroupForm()
    modules = get_auth_permission(PermissionType.MODULE)
    apps = get_auth_permission(PermissionType.APP)
    zfs = get_auth_permission(PermissionType.ZF)
    return render_to_response(template_name, {
        "modules": modules,
        "apps": apps,
        "zfs":zfs,
        "errors": form.errors,
    },context_instance=RequestContext(request))