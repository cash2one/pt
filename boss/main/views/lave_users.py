#coding: utf-8

"""
    留存用户
"""


from django.shortcuts import render_to_response
import json
from main.models import TRpWAppuseReturnuser, TRpDAppuseReturnuser, TRpMAppuseReturnuser
from main_pub import *


def get_lave_users_data(app_key, start_date, end_date, ver, channel, period):
    """
    获取留存用户的所有数据
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
    temp = {}
    if period == PeriodType.DAY:
        #按日统计
        objs = TRpDAppuseReturnuser.objects.filter(
            app_key=app_key,
            channel_no=channel,
            app_version=ver,
            statdate__range=[start_date, end_date])
        for obj in objs:
            if not temp.get(str(obj.statdate)):
                temp[str(obj.statdate)] = {}
            temp[str(obj.statdate)]["c_usernew"] = Cal.int(obj.c_usernew)
            temp[str(obj.statdate)][str(obj.predate)] = Cal.percent(obj.c_usernew_return, obj.c_usernew)
        #把temp转为数组
        for item in temp:
            data.append([
                item,
                temp[item].get("c_usernew", Const.NONE),
                temp[item].get("1", Const.NONE),
                temp[item].get("2", Const.NONE),
                temp[item].get("3", Const.NONE),
                temp[item].get("4", Const.NONE),
                temp[item].get("5", Const.NONE),
                temp[item].get("6", Const.NONE),
                temp[item].get("7", Const.NONE),
                temp[item].get("14", Const.NONE),
                temp[item].get("30", Const.NONE),
            ])
        data.sort()#reverse=True
    elif period == PeriodType.WEEK:
        #按周统计
        i_weeks, week_maps = get_statweeks(start_date, end_date)
        objs = TRpWAppuseReturnuser.objects.filter(
            app_key=app_key,
            channel_no=channel,
            app_version=ver,
            statweek__in=i_weeks)
        for obj in objs:
            if not temp.get(str(obj.statweek)):
                temp[str(obj.statweek)] = {}
            temp[str(obj.statweek)]["c_usernew"] = Cal.int(obj.c_usernew)
            temp[str(obj.statweek)][str(obj.preweek)] = Cal.percent(obj.c_usernew_return, obj.c_usernew)
        #把temp转为数组
        for item in temp:
            data.append([
                "%d - %d" % (week_maps[item][0], week_maps[item][1]),
                temp[item].get("c_usernew", Const.NONE),
                temp[item].get("1", Const.NONE),
                temp[item].get("2", Const.NONE),
                temp[item].get("3", Const.NONE),
                temp[item].get("4", Const.NONE),
                temp[item].get("5", Const.NONE),
                temp[item].get("6", Const.NONE),
                temp[item].get("7", Const.NONE),
                temp[item].get("8", Const.NONE),
                temp[item].get("9", Const.NONE),
            ])
        data.sort()#reverse=True
    elif period == PeriodType.MONTH:
        #按月统计
        start_month = start_date[:6]
        end_month = end_date[:6]
        objs = TRpMAppuseReturnuser.objects.filter(
            app_key=app_key,
            channel_no=channel,
            app_version=ver,
            statmonth__range=[start_month, end_month])
        for obj in objs:
            if not temp.get(str(obj.statmonth)):
                temp[str(obj.statmonth)] = {}
            temp[str(obj.statmonth)]["c_usernew"] = Cal.int(obj.c_usernew)
            temp[str(obj.statmonth)][str(obj.premonth)] = Cal.percent(obj.c_usernew_return, obj.c_usernew)
        #把temp转为数组
        for item in temp:
            data.append([
                "%s01 - %s" % (item, get_month_last_day(int(item))),
                temp[item].get("c_usernew", Const.NONE),
                temp[item].get("1", Const.NONE),
                temp[item].get("2", Const.NONE),
                temp[item].get("3", Const.NONE),
                temp[item].get("4", Const.NONE),
                temp[item].get("5", Const.NONE),
                temp[item].get("6", Const.NONE),
                temp[item].get("7", Const.NONE),
                temp[item].get("8", Const.NONE),
                temp[item].get("9", Const.NONE),
            ])
        data.sort()#reverse=True
    if not data:
        data.append([Const.NONE] * 11)
    return data



@login_required
@permission_required(u'man.%s' % MainConst.USER_ON, raise_exception=True)
@add_common_var
def lave_users(request, template_name):
    start_date = get_datestr(29, "%Y%m%d")
    end_date = get_datestr(0, "%Y%m%d")
    app_key = request.GET.get("app")
    channels, versions = get_channels_versions(app_key)
    #默认渠道和应用都是PLUS99，按日排列
    data = get_lave_users_data(app_key, start_date, end_date, Const.PLUS99, Const.PLUS99, PeriodType.DAY)
    return report_render(request,template_name, {
        "currentdate": get_datestr(0, "%Y-%m-%d"),
        "data": data,
        "channels": channels,
        "versions": versions
    })


@login_required
@permission_required(u'man.%s' % MainConst.USER_ON, raise_exception=True)
def lave_users_ajax(request):
    start_date = request.POST["start_date"]
    end_date = request.POST["end_date"]
    app_key = request.POST["app"]
    period = int(request.POST["period"])
    vers = request.POST["vers"]
    channels = request.POST["channels"]
    result = get_lave_users_data(app_key, start_date, end_date, vers, channels, period)
    return HttpResponse(json.dumps(result))


@login_required
@permission_required(u'man.%s' % MainConst.USER_ON, raise_exception=True)
def lave_users_csv(request):
    app_key = request.GET.get("app")
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")
    period = int(request.GET.get("period"))
    vers = request.GET.get("vers")
    channels = request.GET.get("channels")
    if not app_key:
        app_key = Const.PLUS99
    app_name = TSysApp.objects.get(app_key=app_key)
    filename = '留存用户数据表(%s-%s-%s).csv' % (app_name, str(start_date), str(end_date))
    csv_data = [["首次使用时间", "新增用户", "留存率"]]
    if period == PeriodType.DAY:
        csv_data.append(["", "", "1天后", "2天后", "3天后", "4天后", "5天后", "6天后", "7天后", "14天后", "30天后"])
    elif period == PeriodType.WEEK:
        csv_data.append(["", "", "1周后", "2周后", "3周后", "4周后", "5周后", "6周后", "7周后", "8周后", "9周后"])
    else:
        csv_data.append(["", "", "1月后", "2月后", "3月后", "4月后", "5月后", "6月后", "7月后", "8月后", "9月后"])
    csv_data.extend(get_lave_users_data(app_key, start_date, end_date, vers, channels, period))
    return get_csv_response(filename, csv_data)
