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
def exchange(request, template_name):
    app = request.GET.get("app")
    report_check_app(request, app)
    vers = get_app_versions(app)
    channels = get_app_channels(app)
    products = get_order_types()
    today = datetime.datetime.now()
    if not app:
        app = 'PLUS99'
    summary = TongjiRpDTurnoverSummary.objects.filter(app_id=app, app_version='PLUS99',
    channel_no='PLUS99', product_type='PLUS99', stathour='PLUS99', statdate=today.strftime("%Y-%m-%d"))
    if summary:
        summary = summary[0]
    last_summary = TongjiRpDTurnoverSummary.objects.filter(app_id=app, app_version='PLUS99',
    channel_no='PLUS99', product_type='PLUS99', stathour='PLUS99', statdate=get_datestr(1,"%Y-%m-%d"))
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

def exchange_summaries(request):
    ot, app, ver, channel = get_app_ver_channel(request)
    today_summary = []
    last_summary_result = []
    today = datetime.datetime.now()
    summary = TongjiRpDTurnoverSummary.objects.filter(app_id=app, app_version=ver,
    channel_no=channel,product_type=ot, stathour='PLUS99', statdate=today.strftime("%Y-%m-%d"))
    if summary:
        summary = summary[0]
        today_summary.append(str(summary.total_order_count))  #交易数
        today_summary.append(str(summary.total_prod_price))   #交易额
        today_summary.append(str(summary.total_user_count))   #用户数
        today_summary.append(str(summary.total_coupon_count)) #用券数
        today_summary.append(str(summary.total_coupon_cost))  #用券额
        today_summary.append(str(summary.total_coupon_bring_order)) #券带动消费金额
        today_summary.append(str(summary.coupon_use_ratio))    #交易占比
    else:
        today_summary =[0,0,0,0,0,0,0]
    last_summary = TongjiRpDTurnoverSummary.objects.filter(app_id=app, app_version=ver,
    channel_no=channel, product_type=ot, stathour='PLUS99', statdate=get_datestr(1,"%Y-%m-%d"))
    if last_summary:
        last_summary = last_summary[0]
        last_summary_result.append(str(last_summary.total_order_count))
        last_summary_result.append(str(last_summary.total_prod_price))
        last_summary_result.append(str(last_summary.total_user_count))
    else:
        last_summary_result =[0,0,0]
    return HttpResponse(json.dumps([today_summary,last_summary_result]))


def get_summary_line_data(request):
    today = datetime.datetime.now()
    start_date = request.POST["start_date"]
    end_date = request.POST["end_date"]
    ot, app, ver, channel = get_app_ver_channel(request)
    total_order_count_result = []    #交易数
    total_prod_price_result = []    #交易额
    total_coupon_count_result = []  #用券数
    total_user_count_result = []    #交易用户数
    total_coupon_cost_result=[]     #用券核销额
    total_coupon_bring_order = []   #券带动消费金额
    # coupon_use_ratio_result =[]   #用券交易占比
    global g_data #返回列表数据
    g_data = []
    x_axis = []
    if start_date and end_date and start_date!=end_date:
        summaries = TongjiRpDTurnoverSummary.objects.filter(app_id=app, app_version=ver,
        channel_no=channel, product_type=ot,stathour='PLUS99',statdate__gte=start_date,statdate__lte=end_date)
        for summary in summaries:
            total_order_count_result.append(int(summary.total_order_count))
            total_prod_price_result.append(float(summary.total_prod_price))
            total_coupon_count_result.append(int(summary.total_coupon_count))
            total_user_count_result.append(int(summary.total_user_count))
            total_coupon_cost_result.append(float(summary.total_coupon_cost))
            total_coupon_bring_order.append(float(summary.total_coupon_bring_order))
            g_data.append([summary.statdate.strftime("%Y-%m-%d"), int(summary.total_order_count),
                           float(summary.total_prod_price), int(summary.total_user_count),
                           int(summary.total_coupon_count), str(summary.coupon_use_ratio*100),
                           float(summary.total_coupon_cost), float(summary.total_coupon_bring_order)])
            # coupon_use_ratio_result.append(str(summary.coupon_use_ratio*100))
            x_axis.append(summary.statdate.strftime("%Y-%m-%d"))

    else:
        summaries = TongjiRpDTurnoverSummary.objects.filter(app_id=app, app_version=ver,
        channel_no=channel, product_type=ot, statdate=today.strftime("%Y-%m-%d"))\
        .exclude(stathour='PLUS99')
        summaries = summaries.extra(select ={'stathour_i':"CAST(stathour AS UNSIGNED)"})
        summaries = summaries.order_by('stathour_i')
        for summary in summaries:
            total_order_count_result.append(int(summary.total_order_count))
            total_prod_price_result.append(float(summary.total_prod_price))
            total_coupon_count_result.append(int(summary.total_coupon_count))
            total_user_count_result.append(int(summary.total_user_count))
            total_coupon_cost_result.append(float(summary.total_coupon_cost))
            total_coupon_bring_order.append(float(summary.total_coupon_bring_order))
            x_axis.append(int(summary.stathour))
            print(summary.stathour)
    result=[]
    result.append({"data":total_order_count_result,"type":"line","name":"交易单数"})
    result.append({"data":total_prod_price_result,"type":"line","name":"交易总额"})
    result.append({"data":total_coupon_count_result,"type":"line","name":"用券订单数"})
    result.append({"data":total_user_count_result,"type":"line","name":"交易用户数"})
    result.append({"data":total_coupon_cost_result,"type":"line","name":"用券核销额"})
    result.append({"data":total_coupon_bring_order,"type":"line","name":"券带动消费金额"})
    not_show = ["交易用户数","用券核销额","券带动消费金额"]
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
def exchange_reports_csv(request):
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")
    filename = '%s(%s-%s).csv' % ("交易分析", str(start_date), str(end_date))
    csv_data = [["日期",
                "交易单数",
                "交易总额",
                "交易用户数",
                "用券订单数",
                "交易用券占比",
                "用券核销额",
                "券带动消费金额"]]
    csv_data.extend(g_data)
    return get_csv_response(filename, csv_data)