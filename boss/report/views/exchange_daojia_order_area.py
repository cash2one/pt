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
def exchange_daojia_order_area(request, template_name):
    app = request.GET.get("app")
    report_check_app(request, app)
    vers = get_app_versions(app)
    channels = get_app_channels(app)
    products = get_order_types()
    today = datetime.datetime.now()
    cursor = connections['report'].cursor()
    cursor.execute("call `SP_T_RP_D_EXCHANGE_DAOJIA_ORDER_AREA`(%s, %s)",
                    [get_datestr(0, "%Y-%m-%d"),today.strftime("%Y-%m-%d")])
    objs = cursor.fetchall()
    summary = []
    for obj in objs:
        summary.append([
            str(obj[0]),  # area
            str(obj[1]),  # total_order_count
            str(obj[2]),  # cancel_order_count
        ])
    return report_render(request, template_name, {
        "currentdate": get_datestr(0, "%Y-%m-%d"),
        "vers": vers,
        "channels": channels,
        "products": products,
        "summary": summary,
    })


def exchange_daojia_order_area_ajax(request):
    today = datetime.datetime.now()
    start_date = request.POST["start_date"]
    end_date = request.POST["end_date"]
    ot, app, ver, channel = get_app_ver_channel(request)
    global g_data #返回列表数据
    g_data = []
    cursor = connections['report'].cursor()
    cursor.execute("call `SP_T_RP_D_EXCHANGE_DAOJIA_ORDER_AREA`(%s, %s)",
                    [start_date, end_date])
    objs = cursor.fetchall()
    for obj in objs:
        data = [
            str(obj[0]),  # area
            obj[1],  # total_order_count
            str(obj[2]),  # cancel_order_count
        ]
        if data:
            g_data.append(
                data
            )
    area_list = {}
    for i in g_data:
        area = i[0].split('-')
        if area[0] not in area_list.keys():
            area_list[area[0]] = [i[1],int(i[2])]
        else:
            area_list[area[0]][0] += i[1]
            area_list[area[0]][1] += int(i[2])
    if not g_data:
        g_data.append([Const.NONE] * 3)
    else:
        g_data.sort(key=lambda o: o[0], reverse=True)
    total = [0,0]
    for j,y in area_list.items():
        total[0] += y[0]
        total[1] += y[1]
        if str(j) == '外市':
            g_data.insert(0,[str(j)+'-汇总(除北上深)',y[0],y[1]])
        else:
            g_data.insert(0, [str(j) + '-汇总', y[0], y[1]])
    g_data.insert(0, ['总汇', total[0], total[1]])
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
def exchange_daojia_order_area_csv(request):
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")
    filename = '%s(%s-%s).csv' % ("到家交易区域分析", str(start_date), str(end_date))
    csv_data = [["区域",
                "下单",
                "取消订单"]]
    csv_data.extend(g_data)
    return get_csv_response(filename, csv_data)

