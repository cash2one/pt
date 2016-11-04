#coding: utf-8

"""
    事件详情
"""

from django.shortcuts import render_to_response
import json
from main.models import TRpDAppuseEventSum, TRpDAppuseSum, PtTotalEventWeb, TRpDAppuseEventSumParams
from main_pub import *
from django.db.models import Sum

def get_event_detail_data(app_key, event_id, start_date, end_date, ver, channel):
    """
    获取事件的详细数据

    """
    #设置一些默认值
    if not app_key:
        app_key = Const.PLUS99
    if not ver:
        ver = Const.PLUS99
    if not channel:
        channel = Const.PLUS99
    data = []
    objs = TRpDAppuseEventSum.objects.filter(
        app_key=app_key,
        event_id=event_id,
        channel_no=channel,
        app_version=ver,
        statdate__range=[start_date, end_date])\
        .order_by('-statdate')
    for obj in objs:
        try:
            c_useapp = TRpDAppuseSum.objects.get(
                app_key=app_key,
                channel_no=channel,
                app_version=ver,
                statdate=obj.statdate
            ).c_useapp
        except:
            c_useapp = Const.NONE
        data.append([
            Cal.int(obj.statdate),
            Cal.int(obj.c_event),
            Cal.dev(obj.c_event, c_useapp),
            Cal.int(obj.c_user),
            Cal.sec2time(Cal.dev(obj.s_usetime, obj.c_usetime))
        ])
    return data


def get_param_detail_data(app_key, event_id, start_date, end_date, ver, channel):
    """
    获取参数的详细数据

    """
    #设置一些默认值
    if not app_key:
        app_key = Const.PLUS99
    if not ver:
        ver = Const.PLUS99
    if not channel:
        channel = Const.PLUS99

    data = []
    objs = TRpDAppuseEventSumParams.objects.filter(
        app_key=app_key,
        event_id=event_id,
        channel_no=channel,
        app_version=ver,
        statdate__range=[start_date, end_date])\
        .values('param_key', 'param_value')\
        .annotate(c_params_total=Sum('c_params_count'))
    total = get_dictp_sum(objs, "c_params_total")
    for obj in objs:
        data.append([
            obj["param_key"],
            obj["param_value"],
            Cal.int(obj["c_params_total"]),
            Cal.percent(obj["c_params_total"], total)
        ])
    return data



@login_required
@permission_required(u'man.%s' % MainConst.USER_ON, raise_exception=True)
@add_common_var
def event_detail(request, template_name):
    app_key = request.GET.get("app")
    eventid = request.GET.get("eventid")
    start_date = get_datestr(29, "%Y%m%d")
    end_date = get_datestr(0, "%Y%m%d")
    ver = request.GET.get("ver")
    channel = request.GET.get("channel")
    channels, versions = get_channels_versions(app_key)
    data = get_event_detail_data(app_key, eventid, start_date, end_date, ver, channel)
    objs = PtTotalEventWeb.objects.filter(app_key=app_key)
    events = []
    for obj in objs:
        events.append(obj.event_id)
    data2 = get_param_detail_data(app_key, eventid, start_date, end_date, ver, channel)
    return report_render(request,template_name, {
        "currentdate": get_datestr(0, "%Y-%m-%d"),
        "data": json.dumps(data),
        "data2": json.dumps(data2),
        "versions": versions,
        "channels": channels,
        "events": events,
        "eventid": eventid
    })


@login_required
@permission_required(u'man.%s' % MainConst.USER_ON, raise_exception=True)
def event_detail_ajax(request):
    start_date = request.POST["start_date"]
    end_date = request.POST["end_date"]
    app_key = request.POST["app"]
    eventid = request.POST["eventid"]
    ver = request.POST["ver"]
    channel = request.POST["channel"]
    result = [
        get_event_detail_data(app_key, eventid, start_date, end_date, ver, channel),
        get_param_detail_data(app_key, eventid, start_date, end_date, ver, channel)
    ]
    return HttpResponse(json.dumps(result))


@login_required
@permission_required(u'man.%s' % MainConst.USER_ON, raise_exception=True)
def event_detail_csv(request):
    app_key = request.GET.get("app")
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")
    eventid = request.GET.get("eventid")
    ver = request.GET.get("ver")
    channel = request.GET.get("channel")
    if not app_key:
        app_key = Const.PLUS99
    app_name = TSysApp.objects.get(app_key=app_key)
    filename = '事件统计明细(%s-%s-%s-%s).csv' % (app_name, str(eventid), str(start_date), str(end_date))
    csv_data = [["日期", "消息数量", "消息数/启动次数", "独立用户", "消息时长"]]
    csv_data.extend(get_event_detail_data(app_key, eventid, start_date, end_date, ver, channel))
    return get_csv_response(filename, csv_data)


@login_required
@permission_required(u'man.%s' % MainConst.USER_ON, raise_exception=True)
def event_param_csv(request):
    app_key = request.GET.get("app")
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")
    eventid = request.GET.get("eventid")
    ver = request.GET.get("ver")
    channel = request.GET.get("channel")
    if not app_key:
        app_key = Const.PLUS99
    app_name = TSysApp.objects.get(app_key=app_key)
    filename = '事件参数明细(%s-%s-%s-%s).csv' % (app_name, str(eventid), str(start_date), str(end_date))
    csv_data = [["参数key", "参数值", "消息数量", "占比"]]
    csv_data.extend(get_param_detail_data(app_key, eventid, start_date, end_date, ver, channel))
    return get_csv_response(filename, csv_data)