#coding: utf-8

"""
    整体趋势
"""

from django.shortcuts import render_to_response
import json
from main.models import TRpDAppuseCombine
from main_pub import *


def get_all_trend_data(app_key, start_date, end_date):
    """
    获取整体趋势的详细数据
    :param app_key: 应用ID
    :param start_date: 起始日期
    :param end_date: 结束日期
    :return:
    """
    objs = TRpDAppuseCombine.objects.filter(
        app_key=app_key,
        channel_no=Const.PLUS99,
        app_version=Const.PLUS99,
        statdate__range=[start_date, end_date])\
        .order_by('-statdate')\
        .all()
    data = []
    for obj in objs:
        data.append([
            Cal.int(obj.statdate),
            Cal.int(obj.c_usernew),
            Cal.int(obj.c_user),
            Cal.int(obj.c_useapp),
            Cal.int(obj.c_useracc)
        ])
    #如果没有数据，则返回None字符串
    if not data:
        data.append([Const.NONE] * 5)
    return data


@login_required
@add_common_var
def user_index(request, template_name):
    return report_render(request,template_name)



@login_required
@permission_required(u'man.%s' % MainConst.USER_ON, raise_exception=True)
@add_common_var
def all_trend(request, template_name):
    start_date = get_datestr(29, "%Y%m%d")
    end_date = get_datestr(0, "%Y%m%d")
    app_key = request.GET.get("app")
    if not app_key:
        app_key = Const.PLUS99
    #获取整体趋势的应用概要
    try:
        sumobj = TRpDAppuseCombine.objects.get(
            app_key=app_key,
            channel_no=Const.PLUS99,
            app_version=Const.PLUS99,
            statdate=end_date)
        total_users = Cal.int(sumobj.c_useracc)
        active_users_7 = Cal.int(sumobj.c_user_p7)
        active_users_30 = Cal.int(sumobj.c_user_p30)
        Average_hours_7 = Cal.sec2time(sumobj.s_usetime_p7)
    except Exception as e:
        total_users = active_users_7 = active_users_30 = Average_hours_7 = Const.NONE
    #获取整体趋势的详细数据
    data = get_all_trend_data(app_key, start_date, end_date)
    return report_render(request,template_name, {
        "total_users":total_users,
        "active_users_7":active_users_7,
        "active_users_30":active_users_30,
        "Average_hours_7":Average_hours_7,
        "data":data,
        "currentdate": get_datestr(0, "%Y-%m-%d")
    })


@login_required
@permission_required(u'man.%s' % MainConst.USER_ON, raise_exception=True)
def all_trend_ajax(request):
    start_date = request.POST["start_date"]
    end_date = request.POST["end_date"]
    app_key = request.POST["app"]
    if not app_key:
        app_key = Const.PLUS99
    result = get_all_trend_data(app_key, start_date, end_date)
    return HttpResponse(json.dumps(result))


@login_required
@permission_required(u'man.%s' % MainConst.USER_ON, raise_exception=True)
def all_trend_csv(request):
    app_key = request.GET.get("app")
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")
    if not app_key:
        app_key = Const.PLUS99
    app_name = TSysApp.objects.get(app_key=app_key)
    filename = '整体趋势数据表(%s-%s-%s).csv' % (app_name, str(start_date), str(end_date))
    csv_data = [["日期", "新增用户", "活跃用户", "启动次数", "累计用户"]]
    csv_data.extend(get_all_trend_data(app_key, start_date, end_date))
    return get_csv_response(filename, csv_data)