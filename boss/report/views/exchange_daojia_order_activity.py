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
def exchange_daojia_order_activity(request, template_name):
    app = request.GET.get("app")
    report_check_app(request, app)
    vers = get_app_versions(app)
    channels = get_app_channels(app)
    products = get_order_types()
    today = datetime.datetime.now()
    cursor = connections['report'].cursor()
    cursor.execute("CALL `SP_T_RP_D_EXCHANGE_DAOJIA_ORDER_ACTIVITY`();")
    objs = cursor.fetchall()
    summary = []
    for obj in objs:
        summary.append([
            str(obj[0]),  # activity_id
            str(obj[1]),  # cp_name
            str(obj[2]),  # goods_name
            str(obj[3]),  # begin_date
            str(obj[4]),  # end_date
            str(obj[5]),  # second_kill_price
            str(obj[6]),  # capacity
            str(obj[7]),  # goods_sell_count
            str(obj[8]),  # total_pay_price
            str(obj[9]),  # pt_cost
            str(obj[10]),  # total_pt_cost_price
            str(obj[11]),  # new_user_count
            str(obj[12]),  # new_user_rate
        ])
    return report_render(request, template_name, {
        "currentdate": get_datestr(0, "%Y-%m-%d"),
        "vers": vers,
        "channels": channels,
        "products": products,
        "summary": summary,
    })


def exchange_daojia_order_activity_ajax(request):
    today = datetime.datetime.now()
    start_date = request.POST["start_date"]
    end_date = request.POST["end_date"]
    ot, app, ver, channel = get_app_ver_channel(request)
    global g_data #返回列表数据
    g_data = []
    cursor = connections['report'].cursor()
    cursor.execute("CALL `SP_T_RP_D_EXCHANGE_DAOJIA_ORDER_ACTIVITY`();")
    objs = cursor.fetchall()
    for obj in objs:
        data = [
                obj[0],  # activity_id
            str(obj[1]),  # cp_name
            str(obj[2]),  # goods_name
            str(obj[3]),  # begin_date
            str(obj[4]),  # end_date
            str(obj[5]),  # second_kill_price
            str(obj[6]),  # capacity
            str(obj[7]),  # goods_sell_count
            str(obj[8]),  # total_pay_price
            str(obj[9]),  # pt_cost
            str(obj[10]),  # total_pt_cost_price
            str(obj[11]),  # new_user_count
            str(obj[12]),  # new_user_rate
        ]
        if data:
            g_data.append(
                data
            )
    if not g_data:
        g_data.append([Const.NONE] * 11)
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
def exchange_daojia_order_activity_csv(request):
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")
    filename = '%s(%s-%s).csv' % ("到家交易-秒杀活动分析", str(start_date), str(end_date))
    csv_data = [["活动ID",
                "CP名称",
                "商品名称",
                "秒杀价",
                "活动开始时间",
                "活动结束时间",
                "秒杀数量",
                "销售数量",
                "成交金额",
                "补贴单价",
                "补贴成本",
                "新用户下单",
                "新用户占比"]]
    csv_data.extend(g_data)
    return get_csv_response(filename, csv_data)

