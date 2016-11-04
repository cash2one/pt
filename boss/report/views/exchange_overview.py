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
def exchange_overview(request, template_name):

    app = request.GET.get("app")
    report_check_app(request, app)
    vers = get_app_versions(app)
    channels = get_app_channels(app)
    products = get_order_types()
    today = datetime.datetime.now()
    # if not app:
    #     app = 'PLUS99'
    # summary = TongjiRpDTurnoverBusinessSummary.objects.filter(app_id=app, app_version='PLUS99',
    # channel_no='PLUS99', product_type='PLUS99', statdate=today.strftime("%Y-%m-%d"))
    # if summary:
    #     summary = summary[0]
    # last_summary = TongjiRpDTurnoverBusinessSummary.objects.filter(app_id=app, app_version='PLUS99',
    # channel_no='PLUS99', product_type='PLUS99', statdate=get_datestr(1,"%Y-%m-%d"))
    # if last_summary:
    #     last_summary = last_summary[0]
    cursor = connections['report'].cursor()
    cursor.execute("call `SP_T_RP_D_TURNOVER_SUMMARY`(%s, %s, %s, %s, %s, %s, %s)",
                    [get_datestr(1, "%Y-%m-%d"),today.strftime("%Y-%m-%d"), None, None, None, None, 4])
    objs = cursor.fetchall()
    summary = []
    for obj in objs:
        summary.append([
            str(obj[0]),#statdate
            str(obj[1]),#total_price
            str(obj[2]),#total_order_count
            str(obj[3]),#total_order_pay_count
            str(obj[4]),#total_pay_price
            str(obj[5]),#total_user_count
            str(obj[6]),#first_user_count
            str(obj[7]),#avg_user_order_count
            str(obj[8]),#avg_order_pay
            str(obj[9]),#arpu
            str(obj[10]),#total_coupon_count
            str(obj[11]),#total_coupon_cost
            str(obj[12]),#total_coupon_bring_order
        ])
    return report_render(request, template_name, {
        "currentdate": get_datestr(0, "%Y-%m-%d"),
        "vers": vers,
        "channels": channels,
        "products": products,
        "summary": summary,
    })

def exchange_overview_summaries(request):
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


def get_exchange_overview_table_data(request):
    today = datetime.datetime.now()
    start_date = request.POST["start_date"]
    end_date = request.POST["end_date"]
    table_type = request.POST["show_table_type"]
    ot, app, ver, channel = get_app_ver_channel(request)
    global g_data #返回列表数据
    g_data = []
    cursor = connections['report'].cursor()
    cursor.execute("call `SP_T_RP_D_TURNOVER_SUMMARY`(%s, %s, %s, %s, %s, %s, %s)",
                    [start_date, end_date, ot, channel, ver, app, table_type])
    objs = cursor.fetchall()
    for obj in objs:
        data = [
            str(obj[0]),
            str(obj[1]),
            str(obj[2]),
            str(obj[3]),
            str(obj[4]),
            str(obj[5]),
            str(obj[6]),
            str(obj[7]),
            str(obj[8]),
            str(obj[9]),
            str(obj[10]),
            str(obj[11])
        ]
        if table_type == u"2":
            data.append(str(obj[12]));
        data.append("详情")
        g_data.append(
            data
        )
    if not g_data:
        g_data.append([Const.NONE] * 13)
    return HttpResponse(json.dumps(g_data))



def get_app_ver_channel(request):
    ot = request.POST.get("ot")
    if not ot:
        ot = None
    app = request.POST.get("app")
    report_check_app(request, app)
    if not app:
        app = None
    ver = request.POST.get("ver") #数据有问题
    if not ver:
        ver = None
    channel = request.POST.get("channel")
    if not channel:
        channel = None
    return ot, app, ver, channel


@login_required
# @permission_required(u'man.%s' % ReportConst.ORDER_REPORTS, raise_exception=True)
def exchange_overview_reports_csv(request):
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