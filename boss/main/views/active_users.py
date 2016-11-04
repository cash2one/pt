#coding: utf-8

"""
    活跃用户
"""

from django.shortcuts import render_to_response
from django.db.models import Sum
import json
from main.models import TRpDAppuseCombine, TRpWAppuseSum, TRpMAppuseSum
from main_pub import *


def get_active_users_data(app_key, start_date, end_date, vers, channels, period):
    """获取活跃用户的详细数据"""
    #设置一些默认值
    if not app_key:
        app_key = Const.PLUS99
    if not vers:
        vers = Const.PLUS99
    if not channels:
        channels = Const.PLUS99
    if not period:
        period = PeriodType.DAY
    vers = vers.split(",")
    channels = channels.split(",")
    data = []
    if period == PeriodType.DAY:
        #按日统计，暂时保留支持多渠道，多版本的选择
        objs = TRpDAppuseCombine.objects.filter(
            app_key=app_key,
            channel_no__in=channels,
            app_version__in=vers,
            statdate__range=[start_date, end_date])\
            .values('statdate')\
            .annotate(c_user_total=Sum('c_user'))\
            .order_by('-statdate')
        c_user_total_all = get_dictp_sum(objs, "c_user_total")
        for obj in objs:
            data.append([Cal.int(obj["statdate"]), Cal.int(obj["c_user_total"]),
                         Cal.percent(obj["c_user_total"], c_user_total_all)])
        if not data:
            data.append([Const.NONE] * 3)
    elif period == PeriodType.WEEK:
        #按周统计，暂时保留支持多渠道，多版本的选择
        i_weeks, week_maps = get_statweeks(start_date, end_date)
        objs = TRpWAppuseSum.objects.filter(
            app_key=app_key,
            channel_no__in=channels,
            app_version__in=vers,
            statweek__in=i_weeks)\
            .order_by("-statweek")\
            .values('statweek')\
            .annotate(c_user_total=Sum('c_user'))
        c_user_total_all = get_dictp_sum(objs, "c_user_total")
        for obj in objs:
            #活跃用户占比
            percentage = Cal.percent(obj["c_user_total"], c_user_total_all)
            #周活跃率，最后一天可能数据库还没存
            try:
                sumobj = TRpDAppuseCombine.objects.get(
                    app_key=app_key,
                    channel_no__in=channels,
                    app_version__in=vers,
                    statdate=week_maps[str(obj["statweek"])][1])
                percentage2 = Cal.percent(obj["c_user_total"], sumobj.c_useracc)
            except:
                percentage2 = Const.NONE
            datestr ="%d - %d" % (week_maps[str(obj["statweek"])][0], week_maps[str(obj["statweek"])][1])
            data.append([datestr, Cal.int(obj["c_user_total"]), percentage, percentage2])
        if not data:
            data.append([Const.NONE] * 4)
    elif period == PeriodType.MONTH:
        #按月统计，暂时保留支持多渠道，多版本的选择
        start_month = start_date[:6]
        end_month = end_date[:6]
        objs = TRpMAppuseSum.objects.filter(
            app_key=app_key,
            channel_no__in=channels,
            app_version__in=vers,
            statmonth__range=[start_month, end_month])\
            .values('statmonth')\
            .annotate(c_user_total=Sum('c_user'))\
            .order_by('-statmonth')
        c_user_total_all = get_dictp_sum(objs, "c_user_total")
        for obj in objs:
            #活跃用户占比
            percentage = Cal.percent(obj["c_user_total"], c_user_total_all)
            #月活跃率
            ed = get_month_last_day(obj["statmonth"])
            try:
                sumobj = TRpDAppuseCombine.objects.get(
                    app_key=app_key,
                    channel_no__in=channels,
                    app_version__in=vers,
                    statdate=ed)
                percentage2 = Cal.percent(obj["c_user_total"], sumobj.c_useracc)
            except:
                percentage2 = Const.NONE
            data.append(["%d01 - %s" % (obj["statmonth"], ed), Cal.int(obj["c_user_total"]), percentage, percentage2])
        if not data:
            data.append([Const.NONE] * 4)
    return data



@login_required
@permission_required(u'man.%s' % MainConst.USER_ON, raise_exception=True)
@add_common_var
def active_users(request, template_name):
    start_date = get_datestr(29, "%Y%m%d")
    yesterday = get_datestr(1, "%Y%m%d")
    end_date = get_datestr(0, "%Y%m%d")
    app_key = request.GET.get("app")
    if not app_key:
        app_key = Const.PLUS99
    #获取活跃用户概况
    try:
        sumobj = TRpDAppuseCombine.objects.get(
            app_key=app_key,
            channel_no=Const.PLUS99,
            app_version=Const.PLUS99,
            statdate=yesterday)
        active_users_1 = sumobj.c_user
    except Exception as e:
        active_users_1 = None
    try:
        sumobj = TRpDAppuseCombine.objects.get(
            app_key=app_key,
            channel_no=Const.PLUS99,
            app_version=Const.PLUS99,
            statdate=end_date)
        active_users_7 = sumobj.c_user_p7
        active_users_7_div = Cal.percent(active_users_1, active_users_7)
        active_users_30 = sumobj.c_user_p30
        active_users_30_div = Cal.percent(active_users_1, active_users_30)
    except Exception as e:
        active_users_7 = active_users_30 = active_users_7_div = active_users_30_div = Const.NONE
    channels, versions = get_channels_versions(app_key)
    #获取活跃用户明细
    data = get_active_users_data(app_key, start_date, end_date, Const.PLUS99, Const.PLUS99, PeriodType.DAY)
    return report_render(request,template_name, {
        "active_users_1": Cal.int(active_users_1),
        "active_users_7": Cal.int(active_users_7),
        "active_users_7_div": active_users_7_div,
        "active_users_30": Cal.int(active_users_30),
        "active_users_30_div": active_users_30_div,
        "currentdate": get_datestr(0, "%Y-%m-%d"),
        "data": data,
        "channels": channels,
        "versions": versions
    })


@login_required
@permission_required(u'man.%s' % MainConst.USER_ON, raise_exception=True)
def active_users_ajax(request):
    start_date = request.POST["start_date"]
    end_date = request.POST["end_date"]
    app_key = request.POST["app"]
    period = int(request.POST["period"])
    vers = request.POST["vers"]
    channels = request.POST["channels"]
    result = get_active_users_data(app_key, start_date, end_date, vers, channels, period)
    return HttpResponse(json.dumps(result))


@login_required
@permission_required(u'man.%s' % MainConst.USER_ON, raise_exception=True)
def active_users_csv(request):
    app_key = request.GET.get("app")
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")
    period = int(request.GET.get("period"))
    vers = request.GET.get("vers")
    channels = request.GET.get("channels")
    if not app_key:
        app_key = Const.PLUS99
    app_name = TSysApp.objects.get(app_key=app_key)
    filename = '活跃用户数据表(%s-%s-%s).csv' % (app_name, str(start_date), str(end_date))
    if period == PeriodType.DAY:
        csv_data = [["日期", "活跃用户", "活跃用户占比"]]
    elif period == PeriodType.WEEK:
        csv_data = [["日期", "活跃用户", "活跃用户占比", "周活跃率"]]
    else:
        csv_data = [["日期", "活跃用户", "活跃用户占比", "月活跃率"]]
    csv_data.extend(get_active_users_data(app_key, start_date, end_date, vers, channels, period))
    return get_csv_response(filename, csv_data)