# -*- coding: utf-8 -*-
# Author:wrd
import json
import time
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import timezone

from common.views import PermissionType, add_common_var
from man.models import AuthUser, AuthUserUserPermissions, ModuleGroup, AuthPermission
from man.views.add_user import AddUserForm
from man.views.man_pub import get_auth_permission, add_man_var
from report.views.report_pub import PtHttpResponse


def get_modules():
    modules = ModuleGroup.objects.all().order_by('id')
    result = []
    for obj in modules:
        result.append([obj.id, obj.name])
    return result


def get_one_module(mid):
    data = {}
    data['data'] = dict(
        id=mid.id,
        name=mid.name,
    )
    data['code'] = '0'
    return data


def get_one_permission(mid):
    data = {}
    data['data'] = dict(
        id=mid.id,
        name=mid.name,
        codename=mid.codename,
        content_type_id=mid.content_type_id,
        module_id=mid.module_id,
    )
    data['code'] = '0'
    return data


def update_module(pk, request):
    data = {}
    try:
        mid = ModuleGroup.objects.filter(id=pk)
        request_data = json.loads(request.body) if request.body else ''
        if request_data:
            name = request_data.get('name', '')
            mid.update(
                name=str(name),
            )
            return {"msg": u"添加成功", "code": 0}
        data = {"msg": u"缺少参数", "code": 1}
    except Exception as err:
        data = {"msg": err.message, "code": 1}

    return data


def delete_module(mid):
    try:
        mid.delete()
    except Exception as err:
        return {'msg': err.message, 'code': '1'}
    return {'msg': 'ok', 'code': '0'}



def delete_permission(mid):
    try:
        mid.delete()
    except Exception as err:
        return {'msg': err.message, 'code': '1'}
    return {'msg': 'ok', 'code': '0'}


@login_required
@staff_member_required
@add_common_var
def modules_group(request, template_name):
    module_select = get_modules()
    modules = get_auth_permission(PermissionType.MODULE)
    return render_to_response(template_name, {
        "module_select": module_select,
        'modules': modules,
    }, context_instance=RequestContext(request))


@login_required
@staff_member_required
@add_common_var
def modules_group_select(request):
    if request.method == 'GET':
        module_select = get_auth_permission(PermissionType.MODULE)
        return PtHttpResponse(module_select)
    elif request.method == 'POST':
        name = request.POST.get('name')
        codename = request.POST.get('codename')
        module_id = request.POST.get('module_id')
        content_type_id = PermissionType.MODULE
        try:
            AuthPermission.objects.create(name=name,codename=codename,module_id=module_id,content_type_id=content_type_id)
        except Exception as err:
            if AuthPermission.objects.filter(codename=codename):
                return PtHttpResponse({'msg': '不能有相同的名称', 'code': '1'})
            return PtHttpResponse({'msg': err.message, 'code': '1'})
        return PtHttpResponse({'msg': 'ok', 'code': '0'})

@login_required
@staff_member_required
@add_common_var
def modules_group_detail(request,pk):
    try:
        mid = AuthPermission.objects.get(id=pk)
    except:
        return PtHttpResponse({'msg': u'没有这个值', 'code': '1'})
    if request.method == 'GET':
        data = get_one_permission(mid)
        return PtHttpResponse(data)
    elif request.method == 'PUT':
        try:
            mid = AuthPermission.objects.filter(id=pk)
            request_data = json.loads(request.body) if request.body else ''
            if request_data:
                codename = request_data.get('codename', '')
                module_id = request_data.get('module_id', '')
                name = request_data.get('name', '')
                mid.update(
                    name=str(name),
                    codename=codename,
                    module_id=module_id
                )
        except Exception as err:
            return PtHttpResponse({'msg': err.message, 'code': '1'})
        return PtHttpResponse({'msg': 'ok', 'code': '0'})
    elif request.method == 'DELETE':
        data = delete_permission(mid)
        return PtHttpResponse(data)


@login_required
@staff_member_required
@add_common_var
def modules_list(request, template_name):
    module_select = get_modules()
    return render_to_response(template_name, {
        "module_select": module_select,
    }, context_instance=RequestContext(request))


@login_required
@staff_member_required
@add_common_var
def modules_edit(request):
    if request.method == 'GET':
        module_select = get_modules()
        return HttpResponse(json.dumps(module_select))
    elif request.method == 'POST':
        m_name = request.POST.get('name')
        try:
            ModuleGroup.objects.create(name=m_name)
        except Exception as err:
            if ModuleGroup.objects.filter(name=m_name):
                return PtHttpResponse({'msg': '不能有相同的名称', 'code': '1'})
            return PtHttpResponse({'msg': err.message, 'code': '1'})
        return PtHttpResponse({'msg': 'ok', 'code': '0'})


@login_required
@staff_member_required
@add_common_var
def modules_detail(request, pk):
    try:
        mid = ModuleGroup.objects.get(id=pk)
    except:
        return PtHttpResponse({'msg': u'没有这个值', 'code': '1'})
    if request.method == 'GET':
        data = get_one_module(mid)
        return PtHttpResponse(data)
    elif request.method == 'PUT':
        data = update_module(pk, request)
        return PtHttpResponse(data)
    elif request.method == 'DELETE':
        data = delete_module(mid)
        return PtHttpResponse(data)
