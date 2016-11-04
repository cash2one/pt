#coding: utf-8

"""
    启动次数
"""


from django.shortcuts import render_to_response
import json
from main.models import TRpDAppuseCombine, TRpWAppuseSum, TRpMAppuseSum
from main_pub import *


def get_start_times_data(app_key, start_date, end_date, ver, channel, period):
    """
    获取新增用户的所有数据
    :param app_key: 应用ID
    :param start_date: 开始日期
    :param end_date: 结束日期
    :param ver: 版本，单选
    :param channel: 渠道，单选
    :param period: 按日、周、月统计
    :return:
    """
    #设置一些默认值
    if not app_key:
        app_key = Const.PLUS99
    if not ver:
        ver = Const.PLUS99
    if not channel:
        channel = Const.PLUS99
    if not period:
        period = PeriodType.DAY
    data = []
    if period == PeriodType.DAY:
        #按日统计
        objs = TRpDAppuseCombine.objects.filter(
            app_key=app_key,
            channel_no=channel,
            app_version=ver,
            statdate__range=[start_date, end_date])\
            .order_by('-statdate')
        c_useapp_total = get_objp_sum(objs, "c_useapp")
        for obj in objs:
            data.append([Cal.int(obj.statdate), Cal.int(obj.c_useapp),
                         Cal.percent(obj.c_useapp, c_useapp_total)])
    elif period == PeriodType.WEEK:
        #按周统计
        i_weeks, week_maps = get_statweeks(start_date, end_date)
        objs = TRpWAppuseSum.objects.filter(
            app_key=app_key,
            channel_no=channel,
            app_version=ver,
            statweek__in=i_weeks)\
            .order_by("-statweek")
        c_useapp_total = get_objp_sum(objs, "c_useapp")
        for obj in objs:
            #活跃用户占比
            datestr ="%d - %d" % (week_maps[str(obj.statweek)][0], week_maps[str(obj.statweek)][1])
            data.append([datestr, Cal.int(obj.c_useapp), Cal.percent(obj.c_useapp, c_useapp_total)])
    elif period == PeriodType.MONTH:
        #按月统计
        start_month = start_date[:6]
        end_month = end_date[:6]
        objs = TRpMAppuseSum.objects.filter(
            app_key=app_key,
            channel_no=channel,
            app_version=ver,
            statmonth__range=[start_month, end_month])\
            .order_by('-statmonth')
        c_useapp_total = get_objp_sum(objs, "c_useapp")
        for obj in objs:
            #活跃用户占比
            monthstr = "%d01 - %s" % (obj.statmonth, get_month_last_day(obj.statmonth))
            data.append([monthstr, Cal.int(obj.c_useapp), Cal.percent(obj.c_useapp, c_useapp_total)])
    if not data:
        data.append([Const.NONE] * 3)
    return data



@login_required
@permission_required(u'man.%s' % MainConst.USER_ON, raise_exception=True)
@add_common_var
def start_times(request, template_name):
    start_date = get_datestr(29, "%Y%m%d")
    end_date = get_datestr(0, "%Y%m%d")
    app_key = request.GET.get("app")
    channels, versions = get_channels_versions(app_key)
    data = get_start_times_data(app_key, start_date, end_date, 'PLUS99', 'PLUS99', PeriodType.DAY)
    return report_render(request,template_name, {
        "currentdate": get_datestr(0, "%Y-%m-%d"),
        "data": data,
        "channels": channels,
        "versions": versions
    })


@login_required
@permission_required(u'man.%s' % MainConst.USER_ON, raise_exception=True)
def start_times_ajax(request):
    start_date = request.POST["start_date"]
    end_date = request.POST["end_date"]
    app_key = request.POST["app"]
    period = int(request.POST["period"])
    vers = request.POST["vers"]
    channels = request.POST["channels"]
    result = get_start_times_data(app_key, start_date, end_date, vers, channels, period)
    return HttpResponse(json.dumps(result))


@login_required
@permission_required(u'man.%s' % MainConst.USER_ON, raise_exception=True)
def start_times_csv(request):
    app_key = request.GET.get("app")
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")
    period = int(request.GET.get("period"))
    vers = request.GET.get("vers")
    channels = request.GET.get("channels")
    if not app_key:
        app_key = Const.PLUS99
    app_name = TSysApp.objects.get(app_key=app_key)
    filename = '启动次数数据表(%s-%s-%s).csv' % (app_name, str(start_date), str(end_date))
    csv_data = [["日期", "启动次数", "启动次数占比"]]
    csv_data.extend(get_start_times_data(app_key, start_date, end_date, vers, channels, period))
    return get_csv_response(filename, csv_data)