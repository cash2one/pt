#coding: utf-8

"""
    使用频率
"""


from django.shortcuts import render_to_response
import json
from main.models import TRpDAppuseUsetimes, TRpWAppuseUsetimes, TRpMAppuseUsetimes
from main_pub import *



def get_used_frequency_d_data(app_key, date, ver, channel):
    """
    获取使用频率-日启动次数分布数据
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
    objs = TRpDAppuseUsetimes.objects.filter(
        app_key=app_key,
        channel_no=channel,
        app_version=ver,
        statdate=date)\
        .order_by('usetimes')
    c_user_total = get_objp_sum(objs, "c_user")
    for obj in objs:
        temp = ""
        usetimes = int(obj.usetimes)
        if usetimes == 1:
            temp = "1"
        elif usetimes == 2:
            temp = "2~3"
        elif usetimes == 3:
            temp = "4~5"
        elif usetimes == 4:
            temp = "6~10"
        elif usetimes == 5:
            temp = "11~20"
        elif usetimes == 6:
            temp = "21~50"
        elif usetimes == 7:
            temp = "51~"
        else:
            temp = "0"
        data.append([temp, Cal.int(obj.c_user),
                     Cal.percent(obj.c_user, c_user_total)])
    if not data:
        data.append([Const.NONE] * 3)
    return data


def get_used_frequency_w_data(app_key, date, ver, channel):
    """
    获取使用频率-周启动次数分布数据
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
    weekobjs = TDimWeek.objects.filter(i_weekend__lt=date).order_by("i_week")
    week = (list(weekobjs))[-1]
    data = []
    objs = TRpWAppuseUsetimes.objects.filter(
        app_key=app_key,
        channel_no=channel,
        app_version=ver,
        statweek=week.i_week)\
        .order_by('usetimes')
    c_user_total = get_objp_sum(objs, "c_user")
    for obj in objs:
        temp = ""
        usetimes = int(obj.usetimes)
        if usetimes == 1:
            temp = "1"
        elif usetimes == 2:
            temp = "2~3"
        elif usetimes == 3:
            temp = "4~5"
        elif usetimes == 4:
            temp = "6~10"
        elif usetimes == 5:
            temp = "11~20"
        elif usetimes == 6:
            temp = "21~50"
        elif usetimes == 7:
            temp = "51~100"
        elif usetimes == 8:
            temp = "101~200"
        elif usetimes == 9:
            temp = "201~"
        else:
            temp = "0"
        data.append([temp, Cal.int(obj.c_user),
                     Cal.percent(obj.c_user, c_user_total)])
    if not data:
        data.append([Const.NONE] * 3)
    return data, week.i_weekstart, week.i_weekend


def get_used_frequency_m_data(app_key, date, ver, channel):
    """
    获取使用频率-月启动次数分布数据
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
    month = date[:6]
    objs = TRpMAppuseUsetimes.objects.filter(
        app_key=app_key,
        channel_no=channel,
        app_version=ver,
        statmonth=month)\
        .order_by('usetimes')
    c_user_total = get_objp_sum(objs, "c_user")
    for obj in objs:
        temp = ""
        usetimes = int(obj.usetimes)
        if usetimes == 1:
            temp = "1~2"
        elif usetimes == 2:
            temp = "3~5"
        elif usetimes == 3:
            temp = "6~9"
        elif usetimes == 4:
            temp = "10~19"
        elif usetimes == 5:
            temp = "20~49"
        elif usetimes == 6:
            temp = "50~99"
        elif usetimes == 7:
            temp = "100~"
        else:
            temp = "0"
        data.append([temp, Cal.int(obj.c_user),
                     Cal.percent(obj.c_user, c_user_total)])
    if not data:
        data.append([Const.NONE] * 3)
    return data



@login_required
@permission_required(u'man.%s' % MainConst.USER_ON, raise_exception=True)
@add_common_var
def used_frequency(request, template_name):
    #使用频率默认都是显示昨天的数据
    app_key = request.GET.get("app")
    date = get_datestr(1, "%Y%m%d")
    ver = request.GET.get("ver")
    channel = request.GET.get("channel")
    channels, versions = get_channels_versions(app_key)
    data1 = get_used_frequency_d_data(app_key, date, ver, channel)
    data2 = get_used_frequency_w_data(app_key, date, ver, channel)
    data3 = get_used_frequency_m_data(app_key, date, ver, channel)
    return report_render(request,template_name, {
        "currentdate": get_datestr(1, "%Y-%m-%d"),
        "data1": json.dumps(data1),
        "data2": json.dumps(data2),
        "data3": json.dumps(data3),
        "versions": versions,
        "channels": channels
    })


@login_required
@permission_required(u'man.%s' % MainConst.USER_ON, raise_exception=True)
def used_frequency_ajax(request):
    date = request.POST["date"]
    app_key = request.POST["app"]
    ver = request.POST["ver"]
    channel = request.POST["channel"]
    result = [
        get_used_frequency_d_data(app_key, date, ver, channel),
        get_used_frequency_w_data(app_key, date, ver, channel),
        get_used_frequency_m_data(app_key, date, ver, channel),
    ]
    return HttpResponse(json.dumps(result))


@login_required
@permission_required(u'man.%s' % MainConst.USER_ON, raise_exception=True)
def used_frequency_d_csv(request):
    app_key = request.GET.get("app")
    date = request.GET.get("date")
    ver = request.GET.get("ver")
    channel = request.GET.get("channel")
    if not app_key:
        app_key = Const.PLUS99
    app_name = TSysApp.objects.get(app_key=app_key)
    filename = '日启动次数分布表(%s-%s).csv' % (app_name, str(date))
    csv_data = [["启动次数", "用户数", "用户数比例"]]
    csv_data.extend(get_used_frequency_d_data(app_key, date, ver, channel))
    return get_csv_response(filename, csv_data)


@login_required
@permission_required(u'man.%s' % MainConst.USER_ON, raise_exception=True)
def used_frequency_w_csv(request):
    app_key = request.GET.get("app")
    date = request.GET.get("date")
    ver = request.GET.get("ver")
    channel = request.GET.get("channel")
    if not app_key:
        app_key = Const.PLUS99
    app_name = TSysApp.objects.get(app_key=app_key)
    data, start, end = get_used_frequency_w_data(app_key, date, ver, channel)
    filename = '周启动次数分布表(%s-%d-%d).csv' % (app_name, start, end)
    csv_data = [["启动次数", "用户数", "用户数比例"]]
    csv_data.extend(data)
    return get_csv_response(filename, csv_data)


@login_required
@permission_required(u'man.%s' % MainConst.USER_ON, raise_exception=True)
def used_frequency_m_csv(request):
    app_key = request.GET.get("app")
    date = request.GET.get("date")
    ver = request.GET.get("ver")
    channel = request.GET.get("channel")
    if not app_key:
        app_key = Const.PLUS99
    app_name = TSysApp.objects.get(app_key=app_key)
    filename = '月启动次数分布表(%s-%s).csv' % (app_name, str(date[:6]))
    csv_data = [["启动次数", "用户数", "用户数比例"]]
    csv_data.extend(get_used_frequency_m_data(app_key, date, ver, channel))
    return get_csv_response(filename, csv_data)