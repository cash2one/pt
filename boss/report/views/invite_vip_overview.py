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
def invite_vip_overview(request, template_name):

    app = request.GET.get("app")
    report_check_app(request, app)
    vers = get_app_versions(app)
    channels = get_app_channels(app)
    products = get_order_types()
    today = datetime.datetime.now()
    cursor = connections['order'].cursor()
    cursor.execute("call `SP_T_RP_D_INVITE_AND_REWARD_SUMMARY_VIP`(%s, %s, %s)",
                    [get_datestr(1, "%Y-%m-%d"),today.strftime("%Y-%m-%d"), 1])
    objs = cursor.fetchall()
    summary = []
    for obj in objs:
        summary.append([
            str(obj[0]),  # old_user_count
            str(obj[1]),  # new_user_count
            str(obj[2]),  # new_user_order_count
            str(obj[3]),  # new_user_order_finish_count
            str(obj[4]),  # old_user_get_money
            str(obj[5]),  # new_user_get_money
        ])
    return report_render(request, template_name, {
        "currentdate": get_datestr(0, "%Y-%m-%d"),
        "vers": vers,
        "channels": channels,
        "products": products,
        "summary": summary,
    })

def get_invite_vip_overview_table_data(request):
    today = datetime.datetime.now()
    start_date = request.POST["start_date"]
    end_date = request.POST["end_date"]
    table_type = request.POST["show_table_type"]
    ot, app, ver, channel = get_app_ver_channel(request)
    global g_data #返回列表数据
    g_data = []
    cursor = connections['order'].cursor()
    cursor.execute("call `SP_T_RP_D_INVITE_AND_REWARD_SUMMARY_VIP`(%s, %s, %s)",
                    [start_date, end_date, table_type])
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
        ]
        g_data.append(
            data
        )
    if not g_data:
        g_data.append([Const.NONE] * 7)
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
def invite_vip_overview_reports_csv(request):
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")
    filename = '%s(%s-%s).csv' % ("邀新有礼VIP汇总分析", str(start_date), str(end_date))
    csv_data = [["日期",
                "邀请人总数",
                "被邀请人总数",
                "被邀请人-首单下单成功总数",
                "被邀请人-首单服务完成总数",
                "邀请人获VIP额度总值",
                "被邀请人获VIP额度总值"]]
    csv_data.extend(g_data)
    return get_csv_response(filename, csv_data)