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
def exchange_daojia(request, template_name):
    app = request.GET.get("app")
    report_check_app(request, app)
    vers = get_app_versions(app)
    channels = get_app_channels(app)
    products = get_order_types()
    today = datetime.datetime.now()
    if not app:
        app = 'PLUS99'
    summary = TongjiRpDTurnoverDaojiaServiceQuality.objects.filter(app_id=app, cp_name='PLUS99', app_version='PLUS99',
    channel_no='PLUS99', statdate=today.strftime("%Y-%m-%d"))
    if summary:
        summary = summary[0]
    last_summary = TongjiRpDTurnoverDaojiaServiceQuality.objects.filter(app_id=app, cp_name='PLUS99', app_version='PLUS99',
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


def exchange_daojia_summaries(request):
    ot, app, ver, channel = get_app_ver_channel(request)
    today_summary = []
    last_summary_result = []
    today = datetime.datetime.now()
    summary = TongjiRpDTurnoverDaojiaServiceQuality.objects.filter(app_id=app, app_version=ver,
    channel_no=channel, statdate=today.strftime("%Y-%m-%d"))
    if summary:
        summary = summary[0]
        today_summary.append(str(summary.self_order_count))  #到家订单总量
        today_summary.append(str(summary.open_order_count))   #成本笔数
        today_summary.append(str(summary.cancel_order_count))   #取消笔数
        today_summary.append(str(summary.cp_cancel_order_count)) #商家取消笔数
        today_summary.append(str(summary.error_order_count))  #接口报警次数
        today_summary.append(str(summary.total_refund_success_price)) #退款成功订单金额
        today_summary.append(str(summary.open_order_rate)) #成单转化率
        today_summary.append(str(summary.cancel_order_rate)) #订单取消占比
        today_summary.append(str(summary.cp_cancel_order_rate)) #服务方取消占比

    else:
        today_summary =[0,0,0,0,0,0,0,]
    last_summary = TongjiRpDTurnoverDaojiaServiceQuality.objects.filter(app_id=app, app_version=ver,
    channel_no=channel,statdate=get_datestr(1,"%Y-%m-%d"))
    if last_summary:
        last_summary = last_summary[0]
        last_summary_result.append(str(last_summary.self_order_count))
        last_summary_result.append(str(last_summary.open_order_count))
        last_summary_result.append(str(last_summary.cancel_order_count))
        last_summary_result.append(str(last_summary.cp_cancel_order_count))
        last_summary_result.append(str(last_summary.error_order_count))
    else:
        last_summary_result =[0,0,0]
    return HttpResponse(json.dumps([today_summary,last_summary_result]))


def get_exchange_daojia_line_data(request):
    today = datetime.datetime.now()
    start_date = request.POST["start_date"]
    end_date = request.POST["end_date"]
    ot, app, ver, channel = get_app_ver_channel(request)
    self_order_count = []    #订单总量
    open_order_count = []    #成单转化
    cancel_order_count = []  #订单取消笔数
    cp_cancel_order_count = []    #商家取消笔数
    error_order_count =[]     #接口报警次数
    service_time_incorrect_count = []   #状态更新不及时次数
    global g_data #返回列表数据
    g_data = []
    x_axis = []
    if not start_date:
        start_date = get_datestr(6,"%Y-%m-%d")
    if not end_date:
        end_date = get_datestr(1,"%Y-%m-%d")
    if start_date and end_date and start_date != end_date:
        summaries = TongjiRpDTurnoverDaojiaServiceQuality.objects.filter(app_id=app, cp_name='PLUS99', app_version=ver,
        channel_no=channel, statdate__gte=start_date,statdate__lte=end_date)

        for summary in summaries:
            self_order_count.append(int(summary.self_order_count))
            open_order_count.append(int(summary.open_order_count))
            cancel_order_count.append(int(summary.cancel_order_count))
            cp_cancel_order_count.append(int(summary.cp_cancel_order_count))
            error_order_count.append(int(summary.error_order_count))
            service_time_incorrect_count.append(int(summary.service_time_incorrect_count))
            # coupon_use_ratio_result.append(str(summary.coupon_use_ratio*100))
            x_axis.append(summary.statdate.strftime("%Y-%m-%d"))

        table_summaries = TongjiRpDTurnoverDaojiaServiceQuality.objects.filter(
            app_id=app,
            app_version=ver,
            channel_no=channel,
            statdate__gte=start_date,
            statdate__lte=end_date)\
            .exclude(cp_name='PLUS99')\
            .exclude(avg_appointment_process_time='N/A')\
            .values('cp_name')\
            .annotate(self_order_count=Sum('self_order_count'),
                      open_order_count=Sum('open_order_count'),
                      cancel_order_count=Sum('cancel_order_count'),
                      cp_cancel_order_count=Sum('cp_cancel_order_count'),
                      avg_appointment_process_time=Avg('avg_appointment_process_time'),
                      service_time_incorrect_count=Sum('service_time_incorrect_count'),
                      error_order_count=Sum('error_order_count'))

        for record in table_summaries:
            g_data.append([record["cp_name"],
                           record["self_order_count"],
                           record["open_order_count"],
                           record["cancel_order_count"],
                           record["cp_cancel_order_count"],
                           round(record["avg_appointment_process_time"], 2),
                           record["error_order_count"],
                           record["service_time_incorrect_count"],
                           '趋势'])

    else:
        summaries = TongjiRpDTurnoverDaojiaServiceQuality.objects.filter(app_id=app, cp_name='PLUS99', app_version=ver,
        channel_no=channel, statdate=today.strftime("%Y-%m-%d"))
        for summary in summaries:
            self_order_count.append(float(summary.self_order_count))
            open_order_count.append(float(summary.open_order_count))
            cancel_order_count.append(float(summary.cancel_order_count))
            cp_cancel_order_count.append(float(summary.cp_cancel_order_count))
            error_order_count.append(float(summary.error_order_count))
            service_time_incorrect_count.append(float(summary.service_time_incorrect_count))
            x_axis.append(summary.statdate.strftime("%Y-%m-%d"))
    result=[]
    result.append({"data":self_order_count,"type":"line","name":"订单总量"})
    result.append({"data":open_order_count,"type":"line","name":"成单笔数"})
    result.append({"data":cancel_order_count,"type":"line","name":"订单取消笔数"})
    result.append({"data":cp_cancel_order_count,"type":"line","name":"商家取消笔数"})
    result.append({"data":error_order_count,"type":"line","name":"状态更新不及时次数"})
    result.append({"data":service_time_incorrect_count,"type":"line","name":"接口报警次数"})
    not_show = ["状态更新不及时次数","接口报警次数"]
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


def get_get_app_ver_channel(request):
    ot = request.GET.get("ot")
    if not ot:
        ot = "PLUS99"
    app = request.GET.get("app")
    report_check_app(request, app)
    if not app:
        app = "PLUS99"
    ver = request.GET.get("ver") #数据有问题
    if not ver:
        ver = "PLUS99"
    channel = request.GET.get("channel")
    if not channel:
        channel = "PLUS99"
    return ot, app, ver, channel


@login_required
# @permission_required(u'man.%s' % ReportConst.ORDER_REPORTS, raise_exception=True)
def exchange_daojia_reports_csv(request):
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")
    filename = '%s(%s-%s).csv' % ("交易分析", str(start_date), str(end_date))
    csv_data = [["商家名",
                "订单总量",
                "成单转化",
                "订单取消笔数",
                "商家取消笔数",
                "接单时长（秒）",
                "状态更新不及时次数",
                "接口报警次数"]]
    csv_data.extend(g_data)
    return get_csv_response(filename, csv_data)


result = []
@login_required
@add_common_var
def exchange_daojia_cp(request, template_name):
    global result
    result = []
    ot, app, ver, channel = get_get_app_ver_channel(request)
    summaries = TongjiRpDTurnoverDaojiaServiceQuality.objects.filter(app_id=app,
    cp_name=request.GET.get("cp_name"), app_version=ver,
    channel_no=channel, statdate__gte=request.GET.get("start_date"),
    statdate__lte=request.GET.get("end_date"),)
    for summary in summaries:
        result.append([
            summary.statdate.strftime("%Y-%m-%d"),
            int(summary.self_order_count),
            int(summary.open_order_count),
            int(summary.cancel_order_count),
            int(summary.cp_cancel_order_count),
            str(summary.avg_appointment_process_time),
            int(summary.error_order_count),
            int(summary.service_time_incorrect_count)
        ])
    return report_render(request, template_name, {
            "result": result,
            "start_date": request.GET.get("start_date"),
            "end_date": request.GET.get("end_date"),
            "cp_name":request.GET.get("cp_name"),
        })




def exchange_daojia_cp_reports_csv(request):
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")
    cp_name = request.GET.get("cp_name")
    filename = '%s(%s-%s)CP报表.csv' % (str(cp_name), str(start_date), str(end_date))
    csv_data = [["日期",
                "订单总量",
                "成单转化",
                "订单取消笔数",
                "商家取消笔数",
                "接单时长（秒）",
                "状态更新不及时次数",
                "接口报警次数"]]
    csv_data.extend(result)
    return get_csv_response(filename, csv_data)