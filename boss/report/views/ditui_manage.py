# -*- coding: utf-8 -*-
# Author:wrd
import datetime
import json
from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator
from django.db import connections, transaction
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods

from common.views import add_common_var
from report.models import DiTuiInfo
from report.views.report_pub import add_report_var, ReportConst, report_render, get_datestr, PtHttpResponse


def get_ditui_list(request):
    data = {}
    try:
        per_page = int(request.GET.get("per_page"))
        cur_page = int(request.GET.get("cur_page"))
        start_date = request.GET.get("start_date")
        end_date = request.GET.get("end_date")
        end_date_d = datetime.datetime.strptime(end_date, "%Y-%m-%d") + datetime.timedelta(days=1)
        dituiobj = DiTuiInfo.objects.filter(action_time__gte=start_date, action_time__lte=end_date_d).order_by('-id')
        p = Paginator(dituiobj, per_page)
        num_pags = p.num_pages
        if cur_page > num_pags:
            return data
        dituidata = p.page(cur_page)
        data['data'] = [dict(
            id=obj.id,
            area=obj.area,
            community=obj.community,
            responser=obj.responser,
            action_time=obj.action_time.strftime(
                "%Y-%m-%d %H:%M") if obj.action_time else '',
        ) for obj in dituidata]
        data['page'] = num_pags
        data['code'] = '0'
        return data
    except Exception as err:
        data['msg'] = err.message
        data['code'] = '1'
        return data


def create_ditui(request):
    data = {}
    try:
        request_data = request.POST
        if request_data:
            area = request_data.get('area', '')
            community = request_data.get('community', '')
            responser = request_data.get('responser', '')
            action_time = request_data.get('action_time', '')
            DiTuiInfo.objects.create(
                area=str(area),
                community=str(community),
                responser=str(responser),
                action_time=action_time.replace('T',' ') if action_time else '',
            )
            return {"msg": u"添加成功", "code": 0}
        data = {"msg": u"缺少参数", "code": 1}
    except Exception as err:
        data = {"msg": err.message, "code": 1}

    return data


def get_one_ditui(did):
    data = {}
    data['data'] = dict(
        id=did.id,
        area=did.area,
        community=did.community,
        responser=did.responser,
        action_time=did.action_time.strftime(
            "%Y-%m-%d %H:%M") if did.action_time else '',
    )
    data['code'] = '0'
    return data


def update_ditui(pk, request):
    data = {}
    try:
        did = DiTuiInfo.objects.filter(id=pk)
        request_data = json.loads(request.body) if request.body else ''
        if request_data:
            area = request_data.get('area', '')
            community = request_data.get('community', '')
            responser = request_data.get('responser', '')
            action_time = request_data.get('action_time', '')
            did.update(
                area=str(area),
                community=str(community),
                responser=str(responser),
                action_time=action_time.replace('T', ' ') if action_time else '',
            )
            return {"msg": u"添加成功", "code": 0}
        data = {"msg": u"缺少参数", "code": 1}
    except Exception as err:
        data = {"msg": err.message, "code": 1}

    return data


def delete_ditui(did):
    try:
        did.delete()
    except Exception as err:
        return {'msg': err.message, 'code': '1'}
    return {'msg': 'ok', 'code': '0'}


def formate_data(data):
    f_data = data.replace("\t", "")
    f_data = f_data.replace('"', "")
    f_data = f_data.replace("'", "")
    f_data = f_data.strip()
    return f_data


def filter_cp_data(data):
    f_data = data.replace("\r", "")
    fl_data = f_data.replace("﻿", "")
    ff_data = fl_data.replace("'", "")
    a = ff_data.split('\n')
    com_data = []
    for single_data in a:
        single_list = single_data.split(',')
        single_list = map(formate_data, single_list)
        if len(single_list) != 1:
            com_data.append(single_list)

    return com_data


def filter_csv(csv_data):
    try:
        # a = dir(csv_data[0])
        csv_data = csv_data[0].read().decode('gbk').encode('utf-8')
    except:
        csv_data = csv_data[0].read().encode('utf-8')
    filter_data = filter_cp_data(csv_data)
    return filter_data


def dump_cp_data(data):
    try:
        sid = transaction.savepoint()
        for i in data[1:]:
            DiTuiInfo.objects.create(area=str(i[0]),community=str(i[1]),responser=str(i[2]),action_time=str(i[3]).replace('/','-'))
        transaction.savepoint_commit(sid)
    except Exception as err:
        transaction.savepoint_rollback(sid)
        return {'msg': err.args[1], 'code': '1'}
    else:
        return {'msg': 'ok', 'code': '0'}


@login_required
@permission_required(u'man.%s' % ReportConst.REPORT_DITUI_MANAGE, raise_exception=True)
@add_common_var
def ditui_info(request, template_name):
    """
    显示首页
    :param request:
    :param template_name:
    :return:
    """
    return report_render(request, template_name,
                         {"currentdate": get_datestr(1, "%Y-%m-%d")})


@require_http_methods(['GET', 'POST'])
@login_required
@permission_required(u'man.%s' % ReportConst.REPORT_DITUI_MANAGE, raise_exception=True)
def ditui_list(request):
    """
    获取地推数据显示,和增加人员
    :param request:
    :return:
    """
    if request.method == 'GET':
        data = get_ditui_list(request)
        return PtHttpResponse(data)
    elif request.method == 'POST':
        data = create_ditui(request)
        return PtHttpResponse(data)


@require_http_methods(['GET', 'PUT', 'DELETE'])
@login_required
@permission_required(u'man.%s' % ReportConst.REPORT_DITUI_MANAGE, raise_exception=True)
def ditui_detail(request, pk):
    """
    get 单个信息
    put update信息
    delete 删除信息
    :param request:
    :param pk: 键值
    :return:
    """
    try:
        did = DiTuiInfo.objects.get(id=pk)
    except:
        return PtHttpResponse({'msg': u'没有这个值', 'code': '1'})
    if request.method == 'GET':
        data = get_one_ditui(did)
        return PtHttpResponse(data)
    elif request.method == 'PUT':
        data = update_ditui(pk, request)
        return PtHttpResponse(data)
    elif request.method == 'DELETE':
        data = delete_ditui(did)
        return PtHttpResponse(data)


@require_http_methods(['DELETE'])
@login_required
@permission_required(u'man.%s' % ReportConst.REPORT_DITUI_MANAGE, raise_exception=True)
def ditui_deletelist(request):
    res = {}
    id_list = json.loads(request.body).get('id') if request.body else []
    did = DiTuiInfo.objects.filter(id__in=id_list)
    for i in did:
        res = delete_ditui(i)
    return res


@login_required
@permission_required(u'man.%s' % ReportConst.REPORT_DITUI_MANAGE, raise_exception=True)
def ditui_up_csv(request):
    csv_data = request.FILES.getlist("file_data")
    try:
        filter_data = filter_csv(csv_data)
        result = dump_cp_data(filter_data)
        return PtHttpResponse(result)
    except Exception as e:
        return PtHttpResponse({'msg': e.message, 'code': '1'})
