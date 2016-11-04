#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'putao'
__mtime__ = '1/26/2016'
"""


from report_pub import *

g_data =[]

@login_required
@add_common_var
def exchange_order(request, template_name):
    app = request.GET.get("app")
    report_check_app(request, app)
    vers = get_app_versions(app)
    channels = get_app_channels(app)
    products = get_order_types()
    today = datetime.datetime.now()
    if not app:
        app = 'PLUS99'
    summary = TongjiRpDTurnoverBusinessSummary.objects.filter(app_id=app, app_version='PLUS99',
    channel_no='PLUS99', product_type='PLUS99', statdate=today.strftime("%Y-%m-%d"))
    if summary:
        summary = summary[0]
    last_summary = TongjiRpDTurnoverBusinessSummary.objects.filter(app_id=app, app_version='PLUS99',
    channel_no='PLUS99', product_type='PLUS99', statdate=get_datestr(1,"%Y-%m-%d"))
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

def exchange_order_summaries(request):
    ot, app, ver, channel = get_app_ver_channel(request)
    today_summary = []
    last_summary_result = []
    today = datetime.datetime.now()
    summary = TongjiRpDTurnoverBusinessSummary.objects.filter(app_id=app, app_version=ver,
    channel_no=channel,product_type=ot, statdate=today.strftime("%Y-%m-%d"))
    if summary:
        summary = summary[0]
        today_summary.append(str(summary.total_order_count))  #订单总量
        today_summary.append(str(summary.total_order_pay_count))   #支付订单数
        today_summary.append(str(summary.total_order_success_count))   #成功订单数
        today_summary.append(str(summary.total_order_failed_count)) #失败订单数
        today_summary.append(str(summary.total_coupon_count))  #用券订单数
        #today_summary.append(str(summary.total_refund_success_price)) #退款成功订单金额
        #today_summary.append(str(summary.total_coupon_cost))    #用券核销额
    else:
        today_summary =[0,0,0,0,0,0,0]
    last_summary = TongjiRpDTurnoverBusinessSummary.objects.filter(app_id=app, app_version=ver,
    channel_no=channel, product_type=ot, statdate=get_datestr(1,"%Y-%m-%d"))
    if last_summary:
        last_summary = last_summary[0]
        last_summary_result.append(str(last_summary.total_order_count))
        last_summary_result.append(str(last_summary.total_order_pay_count))
        last_summary_result.append(str(last_summary.total_order_success_count))
        last_summary_result.append(str(last_summary.total_order_failed_count))
        last_summary_result.append(str(last_summary.total_coupon_count))
    else:
        last_summary_result =[0,0,0]
    return HttpResponse(json.dumps([today_summary,last_summary_result]))


def get_exchange_order_line_data(request):
    today = datetime.datetime.now()
    start_date = request.POST["start_date"]
    end_date = request.POST["end_date"]
    ot, app, ver, channel = get_app_ver_channel(request)
    total_order_count = []    #订单总量
    total_order_pay_count = []    #交易单数
    total_order_success_count = []  #成功订单数
    total_order_failed_count = []    #失败订单数
    total_order_processing_count =[]     #处理中订单数
    total_refund_processing_count = []   #退款中订单数
    total_refund_success_count =[]   #退款成功订单数
    total_coupon_count =[]   #用券订单数
    global g_data #返回列表数据
    g_data = []
    x_axis = []
    if not start_date:
        start_date = get_datestr(6,"%Y-%m-%d")
    if not end_date:
        end_date = get_datestr(1,"%Y-%m-%d")
    if start_date and end_date and start_date!=end_date:
        summaries = TongjiRpDTurnoverBusinessSummary.objects.filter(app_id=app, app_version=ver,
        channel_no=channel, product_type=ot,statdate__gte=start_date,statdate__lte=end_date)
        for summary in summaries:
            total_order_count.append(int(summary.total_order_count))
            total_order_pay_count.append(int(summary.total_order_pay_count))
            total_order_success_count.append(int(summary.total_order_success_count))
            total_order_failed_count.append(int(summary.total_order_failed_count))
            total_order_processing_count.append(int(summary.total_order_processing_count))
            total_refund_processing_count.append(int(summary.total_refund_processing_count))
            total_refund_success_count.append(int(summary.total_refund_success_count))
            total_coupon_count.append(int(summary.total_coupon_count))
            g_data.append([summary.statdate.strftime("%Y-%m-%d"),
                           int(summary.total_order_count),
                           int(summary.total_order_pay_count),
                           int(summary.total_order_success_count),
                           int(summary.total_order_failed_count),
                           int(summary.total_order_processing_count),
                           int(summary.total_refund_processing_count),
                           int(summary.total_refund_success_count),
                           int(summary.total_coupon_count)])
            # coupon_use_ratio_result.append(str(summary.coupon_use_ratio*100))
            x_axis.append(summary.statdate.strftime("%Y-%m-%d"))

    else:
        summaries = TongjiRpDTurnoverBusinessSummary.objects.filter(app_id=app, app_version=ver,
        channel_no=channel, product_type=ot, statdate=today.strftime("%Y-%m-%d"))
        for summary in summaries:
            total_order_count.append(int(summary.total_order_count))
            total_order_pay_count.append(int(summary.total_order_pay_count))
            total_order_success_count.append(int(summary.total_order_success_count))
            total_order_failed_count.append(int(summary.total_order_failed_count))
            total_order_processing_count.append(int(summary.total_order_processing_count))
            total_refund_processing_count.append(int(summary.total_refund_processing_count))
            total_refund_success_count.append(int(summary.total_refund_success_count))
            total_coupon_count.append(int(summary. total_coupon_count))
            x_axis.append(summary.statdate.strftime("%Y-%m-%d"))
    result=[]
    result.append({"data":total_order_count,"type":"line","name":"订单总量"})
    result.append({"data":total_order_pay_count,"type":"line","name":"交易单数"})
    result.append({"data":total_order_success_count,"type":"line","name":"成功订单数"})
    result.append({"data":total_order_failed_count,"type":"line","name":"失败订单数"})
    result.append({"data":total_order_processing_count,"type":"line","name":"处理中订单数"})
    result.append({"data":total_refund_processing_count,"type":"line","name":"退款中订单数"})
    result.append({"data":total_refund_success_count,"type":"line","name":"退款成功订单数"})
    result.append({"data":total_coupon_count,"type":"line","name":"用券订单数"})
    not_show = ["退款中订单数","退款成功订单数","用券订单数"]
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
def exchange_order_reports_csv(request):
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")
    filename = '%s(%s-%s).csv' % ("交易分析", str(start_date), str(end_date))
    csv_data = [["日期",
                "订单总量",
                "交易单数",
                "成功订单数",
                "失败订单数",
                "处理中订单数",
                "退款中订单数",
                "退款成功订单数",
                "用券订单数"]]
    csv_data.extend(g_data)
    return get_csv_response(filename, csv_data)