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
def exchange_volume(request, template_name):
    app = request.GET.get("app")
    report_check_app(request, app)
    vers = get_app_versions(app)
    channels = get_app_channels(app)
    products = get_order_types()
    today = datetime.datetime.now()
    if not app:
        app = 'PLUS99'
    summary = TongjiRpDTurnoverTradeVolumeSummary.objects.filter(app_id=app, app_version='PLUS99',
    channel_no='PLUS99', product_type='PLUS99', statdate=today.strftime("%Y-%m-%d"))
    if summary:
        summary = summary[0]
    last_summary = TongjiRpDTurnoverTradeVolumeSummary.objects.filter(app_id=app, app_version='PLUS99',
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

def exchange_volume_summaries(request):
    ot, app, ver, channel = get_app_ver_channel(request)
    today_summary = []
    last_summary_result = []
    today = datetime.datetime.now()
    summary = TongjiRpDTurnoverTradeVolumeSummary.objects.filter(app_id=app, app_version=ver,
    channel_no=channel,product_type=ot, statdate=today.strftime("%Y-%m-%d"))
    if summary:
        summary = summary[0]
        today_summary.append(str(summary.total_pay_price))  #交易金额
        today_summary.append(str(summary.total_order_success_price))   #成功订单金额
        today_summary.append(str(summary.total_order_failed_price))   #失败订单金额
        today_summary.append(str(summary.total_order_processing_price)) #处理中订单金额
        today_summary.append(str(summary.total_refund_processing_price))  #退款中订单金额
        today_summary.append(str(summary.total_refund_success_price)) #退款成功订单金额
        today_summary.append(str(summary.total_coupon_cost))    #用券核销额
    else:
        today_summary =[0,0,0,0,0,0,0]
    last_summary = TongjiRpDTurnoverTradeVolumeSummary.objects.filter(app_id=app, app_version=ver,
    channel_no=channel, product_type=ot, statdate=get_datestr(1,"%Y-%m-%d"))
    if last_summary:
        last_summary = last_summary[0]
        last_summary_result.append(str(last_summary.total_pay_price))
        last_summary_result.append(str(last_summary.total_order_success_price))
        last_summary_result.append(str(last_summary.total_order_failed_price))
        last_summary_result.append(str(last_summary.total_coupon_cost))
        last_summary_result.append(str(last_summary.total_refund_success_price))
    else:
        last_summary_result =[0,0,0]
    return HttpResponse(json.dumps([today_summary,last_summary_result]))


def get_exchange_volume_line_data(request):
    today = datetime.datetime.now()
    start_date = request.POST["start_date"]
    end_date = request.POST["end_date"]
    ot, app, ver, channel = get_app_ver_channel(request)
    total_pay_price = []    #交易金额
    total_order_success_price = []    #成功订单金额
    total_order_failed_price = []  #失败订单金额
    total_order_processing_price = []    #处理中订单金额
    total_refund_processing_price =[]     #退款中订单金额
    total_refund_success_price = []   #退款成功订单金额
    total_coupon_cost =[]   #用券核销额
    global g_data #返回列表数据
    g_data = []
    x_axis = []
    if not start_date:
        start_date = get_datestr(6,"%Y-%m-%d")
    if not end_date:
        end_date = get_datestr(1,"%Y-%m-%d")
    print(start_date,end_date)
    if start_date and end_date and start_date!=end_date:
        summaries = TongjiRpDTurnoverTradeVolumeSummary.objects.filter(app_id=app, app_version=ver,
        channel_no=channel, product_type=ot,statdate__gte=start_date,statdate__lte=end_date)
        for summary in summaries:
            total_pay_price.append(float(summary.total_pay_price))
            total_order_success_price.append(float(summary.total_order_success_price))
            total_order_failed_price.append(float(summary.total_order_failed_price))
            total_order_processing_price.append(float(summary.total_order_processing_price))
            total_refund_processing_price.append(float(summary.total_refund_processing_price))
            total_refund_success_price.append(float(summary.total_refund_success_price))
            total_coupon_cost.append(float(summary.total_coupon_cost))
            g_data.append([summary.statdate.strftime("%Y-%m-%d"), float(summary.total_pay_price),
                           float(summary.total_order_success_price), float(summary.total_order_failed_price),
                           float(summary.total_order_processing_price), float(summary.total_refund_processing_price),
                           float(summary.total_refund_success_price), float(summary.total_coupon_cost)])
            # coupon_use_ratio_result.append(str(summary.coupon_use_ratio*100))
            x_axis.append(summary.statdate.strftime("%Y-%m-%d"))

    else:
        summaries = TongjiRpDTurnoverTradeVolumeSummary.objects.filter(app_id=app, app_version=ver,
        channel_no=channel, product_type=ot, statdate=today.strftime("%Y-%m-%d"))
        for summary in summaries:
            total_pay_price.append(float(summary.total_pay_price))
            total_order_success_price.append(float(summary.total_order_success_price))
            total_order_failed_price.append(float(summary.total_order_failed_price))
            total_order_processing_price.append(float(summary.total_order_processing_price))
            total_refund_processing_price.append(float(summary.total_refund_processing_price))
            total_refund_success_price.append(float(summary.total_refund_success_price))
            total_coupon_cost.append(float(summary.total_coupon_cost))
            x_axis.append(summary.statdate.strftime("%Y-%m-%d"))
    result=[]
    result.append({"data":total_pay_price,"type":"line","name":"交易金额"})
    result.append({"data":total_order_success_price,"type":"line","name":"成功订单金额"})
    result.append({"data":total_order_failed_price,"type":"line","name":"失败订单金额"})
    result.append({"data":total_order_processing_price,"type":"line","name":"处理中订单金额"})
    result.append({"data":total_refund_processing_price,"type":"line","name":"退款中订单金额"})
    result.append({"data":total_refund_success_price,"type":"line","name":"退款成功订单金额"})
    not_show = ["处理中订单金额","退款中订单金额","退款成功订单金额"]
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
def exchange_volume_reports_csv(request):
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")
    filename = '%s(%s-%s).csv' % ("交易分析", str(start_date), str(end_date))
    csv_data = [["日期",
                "交易金额",
                "成功订单金额",
                "失败订单金额",
                "处理中订单金额",
                "退款中订单金额",
                "退款成功订单金额",
                "用券核销额"]]
    csv_data.extend(g_data)
    return get_csv_response(filename, csv_data)