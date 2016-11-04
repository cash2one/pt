#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'putao'
__mtime__ = '1/26/2016'
"""


from report_pub import *
from django.db.models import Sum,Avg

g_data =[]

@login_required
@add_common_var
def exchange_activity(request, template_name):
    app = request.GET.get("app")
    report_check_app(request, app)
    vers = get_app_versions(app)
    channels = get_app_channels(app)
    products = get_order_types()
    today = datetime.datetime.now()
    if not app:
        app = 'PLUS99'
    summary = TongjiRpDTurnoverActivitySummary.objects.filter(app_id=app, activity_id='PLUS99', app_version='PLUS99',
    channel_no='PLUS99', statdate=today.strftime("%Y-%m-%d"))
    if summary:
        summary = summary[0]
    last_summary = TongjiRpDTurnoverActivitySummary.objects.filter(app_id=app, activity_id='PLUS99', app_version='PLUS99',
    channel_no='PLUS99', statdate=get_datestr(1,"%Y-%m-%d"))
    if last_summary:
        last_summary = last_summary[0]
    return report_render(request, template_name, {
        "currentdate": get_datestr(1, "%Y-%m-%d"),
        "vers": vers,
        "channels": channels,
        "products": products,
        "summary": summary,
        "last_summary": last_summary
    })

def exchange_activity_summaries(request):
    ot, app, ver, channel = get_app_ver_channel(request)
    today_summary = []
    last_summary_result = []
    today = datetime.datetime.now()
    summary = TongjiRpDTurnoverActivitySummary.objects.filter(activity_id='PLUS99', app_id=app, app_version=ver,
    channel_no=channel, statdate=today.strftime("%Y-%m-%d"))
    if summary:
        summary = summary[0]
        today_summary.append(str(summary.pv))  #PV
        today_summary.append(str(summary.uv))   #UV
        today_summary.append(str(summary.coupon_get_count))   #活动领券次数
        today_summary.append(str(summary.unique_user_coupon_get_count)) #独立用户领券
        today_summary.append(str(summary.converted_order_count))  #活动转化
        today_summary.append(str(summary.convertion_rate)) #活动转化率

    else:
        today_summary =[0,0,0,0,0,0]
    last_summary = TongjiRpDTurnoverActivitySummary.objects.filter(activity_id='PLUS99', app_id=app, app_version=ver,
    channel_no=channel,statdate=get_datestr(1,"%Y-%m-%d"))
    if last_summary:
        last_summary = last_summary[0]
        last_summary_result.append(str(last_summary.pv))
        last_summary_result.append(str(last_summary.uv))
        last_summary_result.append(str(last_summary.coupon_get_count))
        last_summary_result.append(str(last_summary.unique_user_coupon_get_count))
        last_summary_result.append(str(last_summary.converted_order_count))
    else:
        last_summary_result =[0,0,0,0,0]
    return HttpResponse(json.dumps([today_summary,last_summary_result]))


def get_exchange_activity_line_data(request):
    today = datetime.datetime.now()
    start_date = request.POST["start_date"]
    end_date = request.POST["end_date"]
    ot, app, ver, channel = get_app_ver_channel(request)
    pv = []    #pv
    uv = []    #uv
    coupon_get_count = []  #领券次数
    unique_user_coupon_get_count = []    #独立用户领券
    converted_order_count =[]     #活动转化
    global g_data #返回列表数据
    g_data = []
    x_axis = []
    if not start_date:
        start_date = get_datestr(6,"%Y-%m-%d")
    if not end_date:
        end_date = get_datestr(1,"%Y-%m-%d")
    if start_date and end_date and start_date != end_date:
        summaries = TongjiRpDTurnoverActivitySummary.objects.filter(app_id=app, activity_id='PLUS99', app_version=ver,
        channel_no=channel, statdate__gte=start_date,statdate__lte=end_date)

        table_summaries = TongjiRpDTurnoverActivitySummary.objects.filter(app_id=app, app_version=ver,
        channel_no=channel, statdate__gte=start_date,statdate__lte=end_date).exclude(activity_id='PLUS99') .order_by('-statdate')

        for summary in summaries:
            pv.append(int(summary.pv))
            uv.append(int(summary.uv))
            coupon_get_count.append(int(summary.coupon_get_count))
            unique_user_coupon_get_count.append(int(summary.unique_user_coupon_get_count))
            converted_order_count.append(int(summary.converted_order_count))
            # coupon_use_ratio_result.append(str(summary.coupon_use_ratio*100))
            x_axis.append(summary.statdate.strftime("%Y-%m-%d"))

        for record in table_summaries:
            g_data.append([record.statdate.strftime("%Y-%m-%d"),
                           int(record.activity_id),
                           str(record.activity_name),
                           int(record.pv),
                           int(record.uv),
                           int(record.coupon_get_count),
                           int(record.unique_user_coupon_get_count),
                           int(record.converted_order_count),
                           float(record.convertion_rate)])

    else:
        summaries = TongjiRpDTurnoverActivitySummary.objects.filter(app_id=app, app_version=ver,
        channel_no=channel, statdate=today.strftime("%Y-%m-%d")).exclude(activity_id='PLUS99')
        for summary in summaries:
            pv.append(float(summary.pv))
            uv.append(float(summary.uv))
            coupon_get_count.append(float(summary.coupon_get_count))
            unique_user_coupon_get_count.append(float(summary.unique_user_coupon_get_count))
            converted_order_count.append(float(summary.converted_order_count))
            x_axis.append(summary.statdate.strftime("%Y-%m-%d"))
    result=[]
    result.append({"data":pv,"type":"line","name":"PV"})
    result.append({"data":uv,"type":"line","name":"UV"})
    result.append({"data":coupon_get_count,"type":"line","name":"领券次数"})
    result.append({"data":unique_user_coupon_get_count,"type":"line","name":"独立用户领券"})
    result.append({"data":converted_order_count,"type":"line","name":"活动转化"})
    not_show = ["独立用户领券","活动转化"]
    x_axis = sorted(x_axis)
    return HttpResponse(json.dumps([result, x_axis, not_show, g_data]))



def get_app_ver_channel(request):
    ot = request.POST.get("ot")
    if not ot:
        ot = "PLUS99"
    app = request.POST.get("app")
    report_check_app(request, app)
    if not app:
        app = "PLUS99"
    ver = request.POST.get("ver") #数据有问题
    if not ver:
        ver = "PLUS99"
    channel = request.POST.get("channel")
    if not channel:
        channel = "PLUS99"
    return ot, app, ver, channel


@login_required
# @permission_required(u'man.%s' % ReportConst.ORDER_REPORTS, raise_exception=True)
def exchange_activity_reports_csv(request):
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")
    filename = '%s(%s-%s).csv' % ("活动分析", str(start_date), str(end_date))
    csv_data = [["日期",
                "活动ID",
                "活动名称",
                "PV",
                "UV",
                "领券次数",
                "独立用户领券",
                "活动转化",
                "活动转化率"]]
    csv_data.extend(g_data)
    return get_csv_response(filename, csv_data)