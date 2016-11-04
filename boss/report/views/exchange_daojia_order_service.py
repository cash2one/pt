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
def exchange_daojia_order_service(request, template_name):
    app = request.GET.get("app")
    report_check_app(request, app)
    vers = get_app_versions(app)
    channels = get_app_channels(app)
    products = get_order_types()
    today = datetime.datetime.now()
    cursor = connections['report'].cursor()
    cursor.execute("call `SP_T_RP_D_EXCHANGE_DAOJIA_ORDER_SERVICE`(%s, %s, %s)",
                    [get_datestr(1, "%Y-%m-%d"),today.strftime("%Y-%m-%d"), 1])
    objs = cursor.fetchall()
    summary = []
    for obj in objs:
        summary.append([
            str(obj[0]),#statdate
            str(obj[1]),#new_order_count
            str(obj[2]),#real_order_count
            str(obj[3]),#order_pay_price
            str(obj[4]),#total_user_count
            str(obj[5]),#total_complain_count
            str(obj[6]),#total_order_count
        ])
    return report_render(request, template_name, {
        "currentdate": get_datestr(0, "%Y-%m-%d"),
        "vers": vers,
        "channels": channels,
        "products": products,
        "summary": summary,
    })


def exchange_daojia_order_service_ajax(request):
    today = datetime.datetime.now()
    start_date = request.POST["start_date"]
    end_date = request.POST["end_date"]
    table_type = request.POST["show_table_type"]
    ot, app, ver, channel = get_app_ver_channel(request)
    global g_data #返回列表数据
    g_data = []
    cursor = connections['report'].cursor()
    cursor.execute("call `SP_T_RP_D_EXCHANGE_DAOJIA_ORDER_SERVICE`(%s, %s, %s)",
                    [start_date, end_date, table_type])
    objs = cursor.fetchall()
    for obj in objs:
        data = []
        if table_type == u"1":
            data = [
                str(obj[0]),  # statdate
                str(obj[1]),  # channel_no
                str(obj[2]),  # umeng_active_user
                str(obj[3]),  # umeng_new_user
                str(obj[4]),  # total_order_user_count
                str(obj[5]),  # new_order_user_count
                str(obj[6]),  # overall_conversion_ratio
            ]
        if table_type == u"2":
            data = [
                str(obj[0]),  # statdate
                str(obj[1]),  # channel_no
                str(obj[2]),  # jiazheng_order_count
                str(obj[3]),  # vip_order_count
                str(obj[4]),  # vip_order_pay_price
                str(obj[5]),  # vip_order_bonus
                str(obj[6]),  # five_times_card_order_count
                str(obj[7]),  # ten_times_card_order_count
                str(obj[8]),  # twenty_times_card_order_count
                str(obj[9]),  # daojia_order_count
                str(obj[10]),  # cancel_order_count
                str(obj[11]),  # avg_orders
                str(obj[12]),  # avg_pay
                str(obj[13]),  # total_sell_price
                str(obj[14]),  # total_favo_price
            ]
        if table_type == u"3":
            data = [
                str(obj[0]),  # statdate
                str(obj[1]),  # channel_no
                str(obj[2]),  # service_order_count
                str(obj[3]),  # appeal_order_count
                str(obj[4]),  # bad_comment_order_count
                str(obj[5]),  # appeal_rate
            ]
        if data:
            g_data.append(
                data
            )
    if not g_data:
        if table_type == u"1":
            g_data.append([Const.NONE] * 7)
        if table_type == u"2":
            g_data.append([Const.NONE] * 15)
        if table_type == u"3":
            g_data.append([Const.NONE] * 6)
    else:
        g_data.sort(key=lambda o: o[0], reverse=True)
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
def exchange_daojia_order_service_csv(request):
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")
    table_type = request.GET.get("table_type")
    csv_data = []
    filename = '%s(%s-%s).csv' % ("交易分析", str(start_date), str(end_date))
    if table_type == u"1":
        csv_data = [["日期",
                    "客户端",
                    "日活",
                    "新增用户",
                    "总成单用户",
                    "新下单用户",
                    "总转化率"]]
    elif table_type == u"2":
        csv_data = [["日期",
                    "客户端",
                    "家政订单数",
                    "VIP订单数",
                    "VIP总充值额",
                    "VIP充送总额",
                    "5次卡订单数",
                    "10次卡订单数",
                    "20次卡订单数",
                    "总成单",
                    "取消订单",
                    "人均订单",
                    "客单价",
                    "销售额",
                    "营销成本"]]
    elif table_type == u"3":
        csv_data = [["日期",
                    "客户端",
                    "服务订单数",
                    "申诉订单数",
                    "差评订单数",
                    "投诉率"]]
    csv_data.extend(g_data)
    return get_csv_response(filename, csv_data)
