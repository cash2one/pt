#coding: utf-8

"""
    渠道详情
"""


from django.shortcuts import render_to_response
import json
from main.models import TRpDAppuseCombine, TRpDAppuseUsetimes, TRpDAppuseReturnuser
from main_pub import *


def get_one_channel_data(app_key, channel, start_date, end_date):
    """
    获取渠道详情的所有数据，全部应用无法查看渠道详情
    :param app_key: 应用ID
    :param period: 今日、周日、最近7天
    :return:
    """
    #设置一些默认值
    data = []
    objs = TRpDAppuseCombine.objects.filter(
        app_key=app_key,
        app_version=Const.PLUS99,
        channel_no=channel,
        statdate__range=[start_date, end_date])\
        .order_by("-statdate")
    for obj in objs:
        try:
            usetimeobjs = TRpDAppuseUsetimes.objects.filter(
                app_key=app_key,
                app_version=Const.PLUS99,
                channel_no=obj.channel_no,
                statdate=obj.statdate)
            s_usetime_total = get_objp_sum(usetimeobjs, 's_usetime')
            c_usetime_total = get_objp_sum(usetimeobjs, 'c_usetime')
            usetime = Cal.sec2time(s_usetime_total / c_usetime_total)
        except:
            usetime = Const.NONE
        try:
            returnobj = TRpDAppuseReturnuser.objects.get(
                app_key=app_key,
                app_version=Const.PLUS99,
                channel_no=obj.channel_no,
                statdate=obj.statdate,
                predate=1)
            lave = Cal.percent(returnobj.c_usernew_return, returnobj.c_usernew)
        except:
            lave = Const.NONE
        data.append([Cal.int(obj.statdate), Cal.int(obj.c_usernew), Cal.int(obj.c_user),
                     Cal.int(obj.c_useapp), usetime, lave])
    if not data:
        data.append([Const.NONE] * 6)
    return data



@login_required
@permission_required(u'man.%s' % MainConst.USER_ON, raise_exception=True)
@add_common_var
def one_channel(request, template_name):
    app_key = request.GET.get("app")
    if not app_key or app_key == Const.PLUS99:
        return report_render(request,Const.TEMPLATE_PLUS99, {"zh":"渠道详情", "en":"one_channel"})
    channel = request.GET.get("channel")
    start_date = get_datestr(29, "%Y%m%d")
    end_date = get_datestr(0, "%Y%m%d")
    channels, versions = get_channels_versions(app_key)
    data = get_one_channel_data(app_key, channel, start_date, end_date)
    return report_render(request,template_name, {
        "data": data,
        "currentdate": get_datestr(0, "%Y-%m-%d"),
        "channels": channels,
        "cur_chan": channel #传递当前选择的channel
    })


@login_required
@permission_required(u'man.%s' % MainConst.USER_ON, raise_exception=True)
def one_channel_ajax(request):
    start_date = request.POST["start_date"]
    end_date = request.POST["end_date"]
    app_key = request.POST["app"]
    channel = request.POST["channel"]
    result = get_one_channel_data(app_key, channel, start_date, end_date)
    return HttpResponse(json.dumps(result))


@login_required
@permission_required(u'man.%s' % MainConst.USER_ON, raise_exception=True)
def one_channel_csv(request):
    app_key = request.GET.get("app")
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")
    channel = request.GET.get("channel")
    app_name = TSysApp.objects.get(app_key=app_key)
    filename = '渠道详情数据表(%s-%s-%s-%s).csv' % (app_name, str(channel), str(start_date), str(end_date))
    csv_data = [["日期", "新增用户", "活跃用户", '启动次数', '单次使用时长', '次日留存率']]
    csv_data.extend(get_one_channel_data(app_key, channel, start_date, end_date))
    return get_csv_response(filename, csv_data)