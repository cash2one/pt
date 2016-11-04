#coding: utf-8

"""
    使用时长
"""


from django.shortcuts import render_to_response
import json
from main.models import TRpDAppuseTimeregion, TRpDAppuseTimeregionOnce
from main_pub import *


def sort_timeregion(o):
    v = int(o.timeregion)
    if v == 99:
        return -1
    else:
        return v


def get_used_time_once_data(app_key, date, ver, channel):
    """
    获取单次使用时长的所有数据
    :param app_key: 应用ID
    :param date: 查询日期
    :param ver: 版本，单选
    :param channel: 渠道，单选
    :return:
    """
    #设置一些默认值
    if not app_key:
        app_key = Const.PLUS99
    if not ver:
        ver = Const.PLUS99
    if not channel:
        channel = Const.PLUS99
    data = []
    objs = TRpDAppuseTimeregionOnce.objects.filter(
        app_key=app_key,
        channel_no=channel,
        app_version=ver,
        statdate=date)#99要区别对待，不能简单按timeregion排序
    c_useapp_total = get_objp_sum(objs, "c_useapp")
    objs = list(objs)
    objs.sort(key=sort_timeregion)
    for obj in objs:
        time = ""
        timeregion = int(obj.timeregion)
        if timeregion == 1:
            time = "1-3 秒"
        elif timeregion == 2:
            time = "4-10 秒"
        elif timeregion == 3:
            time = "11-30 秒"
        elif timeregion == 4:
            time = "31-60 秒"
        elif timeregion == 5:
            time = "1-3 分"
        elif timeregion == 6:
            time = "3-10 分"
        elif timeregion == 7:
            time = "10-30 分"
        elif timeregion == 8:
            time = "30-60 分"
        elif timeregion == 9:
            time = "60 分~"
        else:
            time = "0-1 秒"
        data.append([time, Cal.int(obj.c_useapp),
                     Cal.percent(obj.c_useapp, c_useapp_total)])
    if not data:
        data.append([Const.NONE] * 3)
    return data


def get_used_time_day_data(app_key, date, ver, channel):
    """
    获取日使用时长的所有数据
    :param app_key: 应用ID
    :param date: 查询日期
    :param ver: 版本，单选
    :param channel: 渠道，单选
    :return:
    """
    #设置一些默认值
    if not app_key:
        app_key = Const.PLUS99
    if not ver:
        ver = Const.PLUS99
    if not channel:
        channel = Const.PLUS99
    data = []
    objs = TRpDAppuseTimeregion.objects.filter(
        app_key=app_key,
        channel_no=channel,
        app_version=ver,
        statdate=date)\
        .order_by('timeregion')
    c_user_total = get_objp_sum(objs, "c_user")
    for obj in objs:
        time = ""
        timeregion = int(obj.timeregion)
        if timeregion == 1:
            time = "1-60 秒"
        elif timeregion == 2:
            time = "1-3 分"
        elif timeregion == 3:
            time = "3-10 分"
        elif timeregion == 4:
            time = "10-30 分"
        elif timeregion == 5:
            time = "30-60 分"
        elif timeregion == 6:
            time = "1-2 小时"
        elif timeregion == 7:
            time = "2-4 小时"
        elif timeregion == 8:
            time = "4小时~"
        else:
            time = "0-1 秒"
        data.append([time, Cal.int(obj.c_user),
                     Cal.percent(obj.c_user, c_user_total)])
    if not data:
        data.append([Const.NONE] * 3)
    return data



@login_required
@permission_required(u'man.%s' % MainConst.USER_ON, raise_exception=True)
@add_common_var
def used_time(request, template_name):
    app_key = request.GET.get("app")
    date = get_datestr(1, "%Y%m%d")
    ver = request.GET.get("ver")
    channel = request.GET.get("channel")
    channels, versions = get_channels_versions(app_key)
    data1 = get_used_time_once_data(app_key, date, ver, channel)
    data2 = get_used_time_day_data(app_key, date, ver, channel)
    return report_render(request,template_name, {
        "currentdate": get_datestr(1, "%Y-%m-%d"),
        "data1": json.dumps(data1),
        "data2": json.dumps(data2),
        "versions": versions,
        "channels": channels,
    })


@login_required
@permission_required(u'man.%s' % MainConst.USER_ON, raise_exception=True)
def used_time_ajax(request):
    date = request.POST["date"]
    app_key = request.POST["app"]
    ver = request.POST["ver"]
    channel = request.POST["channel"]
    result = [
        get_used_time_once_data(app_key, date, ver, channel),
        get_used_time_day_data(app_key, date, ver, channel),
    ]
    return HttpResponse(json.dumps(result))


@login_required
@permission_required(u'man.%s' % MainConst.USER_ON, raise_exception=True)
def used_time_once_csv(request):
    app_key = request.GET.get("app")
    date = request.GET.get("date")
    ver = request.GET.get("ver")
    channel = request.GET.get("channel")
    if not app_key:
        app_key = Const.PLUS99
    app_name = TSysApp.objects.get(app_key=app_key)
    filename = '单次使用时长分布表(%s-%s).csv' % (app_name, str(date))
    csv_data = [["时长", "启动次数", "启动次数占比"]]
    csv_data.extend(get_used_time_once_data(app_key, date, ver, channel))
    return get_csv_response(filename, csv_data)


@login_required
@permission_required(u'man.%s' % MainConst.USER_ON, raise_exception=True)
def used_time_day_csv(request):
    app_key = request.GET.get("app")
    date = request.GET.get("date")
    ver = request.GET.get("ver")
    channel = request.GET.get("channel")
    if not app_key:
        app_key = Const.PLUS99
    app_name = TSysApp.objects.get(app_key=app_key)
    filename = '日使用时长分布表(%s-%s).csv' % (app_name, str(date))
    csv_data = [["时长", "用户数", "用户数比例"]]
    csv_data.extend(get_used_time_day_data(app_key, date, ver, channel))
    return get_csv_response(filename, csv_data)
