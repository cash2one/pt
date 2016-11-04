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
def exchange_user(request, template_name):
    app = request.GET.get("app")
    report_check_app(request, app)
    vers = get_app_versions(app)
    channels = get_app_channels(app)
    products = get_order_types()
    today = datetime.datetime.now()
    if not app:
        app = 'PLUS99'
    summary = TongjiRpDTurnoverUserSummary.objects.filter(app_id=app, app_version='PLUS99',
    channel_no='PLUS99', product_type='PLUS99', statdate=today.strftime("%Y-%m-%d"))
    if summary:
        summary = summary[0]
    last_summary = TongjiRpDTurnoverUserSummary.objects.filter(app_id=app, app_version='PLUS99',
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

def exchange_user_summaries(request):
    ot, app, ver, channel = get_app_ver_channel(request)
    today_summary = []
    last_summary_result = []
    today = datetime.datetime.now()
    summary = TongjiRpDTurnoverUserSummary.objects.filter(app_id=app, app_version=ver,
    channel_no=channel,product_type=ot, statdate=today.strftime("%Y-%m-%d"))
    if summary:
        summary = summary[0]
        today_summary.append(str(summary.total_user_count))  #下单用户
        today_summary.append(str(summary.total_pay_user_count))   #交易用户数
        today_summary.append(str(summary.first_order_user_count))   #平台首购用户
        today_summary.append(str(summary.reorder_user_count)) #平台复购用户
        today_summary.append(str(summary.first_product_order_user_count))  #业务首购用户
        today_summary.append(str(summary.product_reorder_user_count)) #业务复购用户
    else:
        today_summary =[0,0,0,0,0,0,0]
    last_summary = TongjiRpDTurnoverUserSummary.objects.filter(app_id=app, app_version=ver,
    channel_no=channel, product_type=ot, statdate=get_datestr(1,"%Y-%m-%d"))
    if last_summary:
        last_summary = last_summary[0]
        last_summary_result.append(str(last_summary.total_user_count))
        last_summary_result.append(str(last_summary.total_pay_user_count))
        last_summary_result.append(str(last_summary.first_order_user_count))
        last_summary_result.append(str(last_summary.reorder_user_count))
        last_summary_result.append(str(last_summary.first_product_order_user_count))
        last_summary_result.append(str(last_summary.product_reorder_user_count))
    else:
        last_summary_result =[0,0,0]
    return HttpResponse(json.dumps([today_summary,last_summary_result]))


def get_exchange_user_line_data(request):
    today = datetime.datetime.now()
    start_date = request.POST["start_date"]
    end_date = request.POST["end_date"]
    ot, app, ver, channel = get_app_ver_channel(request)
    total_user_count = []    #下单用户
    total_pay_user_count = []    #交易用户数
    first_order_user_count = []  #平台首购用户
    reorder_user_count = []    #平台复购用户
    first_product_order_user_count =[]     #业务首购用户
    product_reorder_user_count = []   #业务复购用户
    global g_data #返回列表数据
    g_data = []
    x_axis = []
    if not start_date:
        start_date = get_datestr(6,"%Y-%m-%d")
    if not end_date:
        end_date = get_datestr(1,"%Y-%m-%d")
    if start_date and end_date and start_date!=end_date:
        summaries = TongjiRpDTurnoverUserSummary.objects.filter(app_id=app, app_version=ver,
        channel_no=channel, product_type=ot,statdate__gte=start_date,statdate__lte=end_date)
        for summary in summaries:
            total_user_count.append(int(summary.total_user_count))
            total_pay_user_count.append(int(summary.total_pay_user_count))
            first_order_user_count.append(int(summary.first_order_user_count))
            reorder_user_count.append(int(summary.reorder_user_count))
            first_product_order_user_count.append(int(summary.first_product_order_user_count))
            product_reorder_user_count.append(int(summary.product_reorder_user_count))
            g_data.append([summary.statdate.strftime("%Y-%m-%d"), int(summary.total_user_count),
                           int(summary.total_pay_user_count), int(summary.first_order_user_count),
                           int(summary.reorder_user_count), int(summary.first_product_order_user_count),
                           int(summary.product_reorder_user_count)])
            # coupon_use_ratio_result.append(str(summary.coupon_use_ratio*100))
            x_axis.append(summary.statdate.strftime("%Y-%m-%d"))

    else:
        summaries = TongjiRpDTurnoverUserSummary.objects.filter(app_id=app, app_version=ver,
        channel_no=channel, product_type=ot, statdate=today.strftime("%Y-%m-%d"))
        for summary in summaries:
            total_user_count.append(int(summary.total_user_count))
            total_pay_user_count.append(int(summary.total_pay_user_count))
            first_order_user_count.append(int(summary.first_order_user_count))
            reorder_user_count.append(int(summary.reorder_user_count))
            first_product_order_user_count.append(int(summary.first_product_order_user_count))
            product_reorder_user_count.append(int(summary.product_reorder_user_count))
            x_axis.append(summary.statdate.strftime("%Y-%m-%d"))
    result=[]
    result.append({"data":total_user_count,"type":"line","name":"下单用户"})
    result.append({"data":total_pay_user_count,"type":"line","name":"交易用户数"})
    result.append({"data":first_order_user_count,"type":"line","name":"平台首购用户"})
    result.append({"data":reorder_user_count,"type":"line","name":"平台复购用户"})
    result.append({"data":first_product_order_user_count,"type":"line","name":"业务首购用户"})
    result.append({"data":product_reorder_user_count,"type":"line","name":"业务复购用户"})
    not_show = ["业务首购用户","业务复购用户"]
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
def exchange_user_reports_csv(request):
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")
    filename = '%s(%s-%s).csv' % ("交易分析", str(start_date), str(end_date))
    csv_data = [["日期",
                "下单用户",
                "交易用户",
                "平台首购用户",
                "平台复购用户",
                "业务首购用户",
                "业务复购用户"]]
    csv_data.extend(g_data)
    return get_csv_response(filename, csv_data)