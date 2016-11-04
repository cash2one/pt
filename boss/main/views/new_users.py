#coding: utf-8

"""
    新增用户
"""


from django.shortcuts import render_to_response
from django.db.models import Sum
import json
from main.models import TRpDAppuseCombine, TRpWAppuseSum, TRpMAppuseSum
from main_pub import *


def get_new_users_data(app_key, start_date, end_date, vers, channels, period):
    """
    获取新增用户的所有数据
    :param app_key: 应用ID
    :param start_date: 开始日期
    :param end_date: 结束日期
    :param vers: 版本，以逗号间隔
    :param channels: 渠道，以逗号间隔
    :param period: 按日、周、月统计
    :return:
    """
    #设置一些默认值，渠道和应用都是PLUS99，按日排列
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
        #按日统计, 暂时保留支持多渠道，多版本的选择
        #这里需要按日进行分组叠加
        objs = TRpDAppuseCombine.objects.filter(
            app_key=app_key,
            channel_no__in=channels,
            app_version__in=vers,
            statdate__range=[start_date, end_date])\
            .values('statdate')\
            .annotate(c_usernew_total=Sum('c_usernew'),
                      c_user_total=Sum('c_user'))\
            .order_by('-statdate')
        for obj in objs:
            #非空再进行计算
            data.append([Cal.int(obj["statdate"]), Cal.int(obj["c_usernew_total"]),
                         Cal.percent(obj["c_usernew_total"], obj["c_user_total"])])
    elif period == PeriodType.WEEK:
        #按周统计, 暂时保留支持多渠道，多版本的选择
        #这里需要按周进行分组叠加
        i_weeks, week_maps = get_statweeks(start_date, end_date)
        objs = TRpWAppuseSum.objects.filter(
            app_key=app_key,
            channel_no__in=channels,
            app_version__in=vers,
            statweek__in=i_weeks)\
            .order_by("-statweek")\
            .values('statweek')\
            .annotate(c_usernew_total=Sum('c_usernew'),
                      c_user_total=Sum('c_user'))
        for obj in objs:
            datestr ="%d - %d" % (week_maps[str(obj["statweek"])][0], week_maps[str(obj["statweek"])][1])
            data.append([datestr, Cal.int(obj["c_usernew_total"]),
                         Cal.percent(obj["c_usernew_total"], obj["c_user_total"])])
    elif period == PeriodType.MONTH:
        #按月统计，根据起始日期和结束日期的前六位判断
        #暂时保留支持多渠道，多版本的选择
        start_month = start_date[:6]
        end_month = end_date[:6]
        objs = TRpMAppuseSum.objects.filter(
            app_key=app_key,
            channel_no__in=channels,
            app_version__in=vers,
            statmonth__range=[start_month, end_month])\
            .values('statmonth')\
            .annotate(c_usernew_total=Sum('c_usernew'),
                      c_user_total=Sum('c_user'))\
            .order_by('-statmonth')
        for obj in objs:
            monthstr = "%d01 - %s" % (obj["statmonth"], get_month_last_day(obj["statmonth"]))
            data.append([monthstr, Cal.int(obj["c_usernew_total"]),
                         Cal.percent(obj["c_usernew_total"], obj["c_user_total"])])
    if not data:
        data.append([Const.NONE] * 3)
    return data



@login_required
@permission_required(u'man.%s' % MainConst.USER_ON, raise_exception=True)
@add_common_var
def new_users(request, template_name):
    app_key = request.GET.get("app")
    channels, versions = get_channels_versions(app_key)
    return report_render(request,template_name, {
        "currentdate": get_datestr(0, "%Y-%m-%d"),
        "channels": channels,
        "versions": versions
    })


@login_required
@permission_required(u'man.%s' % MainConst.USER_ON, raise_exception=True)
def new_users_ajax(request):
    start_date = request.POST["start_date"]
    end_date = request.POST["end_date"]
    app_key = request.POST["app"]
    period = int(request.POST["period"])
    vers = request.POST["vers"]
    channels = request.POST["channels"]
    result = get_new_users_data(app_key, start_date, end_date, vers, channels, period)
    return HttpResponse(json.dumps(result))


@login_required
@permission_required(u'man.%s' % MainConst.USER_ON, raise_exception=True)
def new_users_csv(request):
    app_key = request.GET.get("app")
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")
    period = int(request.GET.get("period"))
    vers = request.GET.get("vers")
    channels = request.GET.get("channels")
    if not app_key:
        app_key = Const.PLUS99
    app_name = TSysApp.objects.get(app_key=app_key)
    filename = '新增用户数据表(%s-%s-%s).csv' % (app_name, str(start_date), str(end_date))
    csv_data = [["日期", "新增用户", "新增用户占比"]]
    csv_data.extend(get_new_users_data(app_key, start_date, end_date, vers, channels, period))
    return get_csv_response(filename, csv_data)
