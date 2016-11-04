#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'putao'
__mtime__ = '1/26/2016'
"""
from django.views.decorators.csrf import csrf_exempt

from order.views.order_pub import get_daojia_goods_category
from report_pub import *

g_data = []


@login_required
@add_common_var
def exchange_daojia_order_summary(request, template_name):
    app = request.GET.get("app")
    report_check_app(request, app)
    vers = get_app_versions(app)
    channels = get_app_channels(app)
    products = get_order_types()
    citys = get_citys
    today = datetime.datetime.now()

    return report_render(request, template_name, {
        "currentdate": get_datestr(0, "%Y-%m-%d"),
        "vers": vers,
        "channels": channels,
        "products": products,
        "citys": citys,
    })


def fetchall_to_dict(fetall):
    """
    把fetchall的数据变为字典
    :param fetall:
    :return:
    """
    f_dict = {}
    for i in fetall:
        if str(i[0]) not in f_dict.keys():
            f_dict[str(i[0])] = [i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9]]
        else:
            if not isinstance(i[3], float) or not isinstance(i[4], float) or not isinstance(i[5],
                                                                                            float) or not isinstance(
                    i[6], float) or not isinstance(i[7], float) or not isinstance(i[8], float) or not isinstance(i[9], float):
                continue
            f_dict[i[0]][3] += i[3]
            f_dict[i[0]][4] += i[4]
            f_dict[i[0]][5] += i[5]
            f_dict[i[0]][6] += i[6]
            f_dict[i[0]][7] += i[7]
            f_dict[i[0]][8] += i[8]
            f_dict[i[0]][9] += i[9]
    return f_dict


def get_exchange_daojia_order_summary_table_data(request):
    start_date = request.POST["start_date"]
    end_date = request.POST["end_date"]
    table_type = request.POST["show_table_type"]
    period_type = request.POST["show_time_table_type"]
    citys_select = request.POST.get("citys_select") if request.POST.get("citys_select") != '0' else None
    ot, app, ver, channel = get_app_ver_channel(request)
    category_info = get_daojia_goods_category()
    global g_data  # 返回列表数据
    g_data = []
    cat_data = {}
    cursor = connections['order'].cursor()
    cursor.execute("call `SP_T_RP_D_TURNOVER_DAOJIA_PRODUCT_SUMMARY_NEW`(%s, %s, %s, %s, %s, %s)",
                   [start_date.replace('-', ''), end_date.replace('-', ''), citys_select, channel, period_type, 2])
    objs = cursor.fetchall()

    cur = connections['report'].cursor()
    if table_type == u"5":
        rp_type = 3
    else:
        rp_type = 2
    cur.execute("call `SP_T_RP_D_TURNOVER_DAOJIA_PRODUCT_SUMMARY_USER`(%s, %s, %s, %s, %s, %s)",
                [start_date.replace('-', ''), end_date.replace('-', ''), citys_select, channel, period_type, rp_type])
    orders = cur.fetchall()
    orders_dict = fetchall_to_dict(orders)
    for obj in objs:
        data = []
        cg_name = "未获取分类信息"
        if str(obj[0]) in category_info.keys():
            cg_name = category_info[str(obj[0])]
        if table_type == u"1":
            data = [
                cg_name,  # app_id
                str(obj[1]),  # cp_name
                format_douhao(str(obj[2])),  # valid_daojia_order_count
                format_douhao(str(obj[3])),  # valid_daojia_user_count
                format_douhao(str(obj[4])),  # gmv
                format_douhao(str(obj[5])),  # user_pay_price
                format_douhao(str(obj[6])),  # total_cost
                format_douhao(str(obj[7])),  # operation_cost
                format_douhao(str(obj[8])),  # vip_operation_cost
                format_douhao(str(obj[9])),  # pt_card_operation_cost 葡萄卡补贴
                format_douhao(str(obj[10])),  # gross_profit
                format_douhao(str(obj[11])),  # avg_pay_per_order
                str(round(float(orders_dict[str(obj[0])][3])*100,2)) + '%' if str(obj[0]) in orders_dict.keys() and orders_dict[str(obj[0])][3] != 'N/A' else "0.00%",  # new_order_rate
                str(round(float(orders_dict[str(obj[0])][8]) * 100, 2)) + '%' if str(obj[0]) in orders_dict.keys() and orders_dict[str(obj[0])][8] != 'N/A' else "0.00%",  # old_order_rate
                str(round(float(orders_dict[str(obj[0])][9]) * 100, 2)) + '%' if str(obj[0]) in orders_dict.keys() and orders_dict[str(obj[0])][9] != 'N/A' else "0.00%",  # over_category_rebuy_rate
                str(obj[12]) + ' / ' + str(obj[13]),  # wait_confirm_order_count / wait_pay_order_count
                str(obj[14]) + ' / ' + str(obj[15]) + ' / ' + str(obj[16]),  # cancel_order_count / refund_order_count
                str(obj[17]) + ' / ' + str(obj[18]),  # processing_order_count
            ]
        elif table_type == u"5":
            if not cat_data.has_key(cg_name):
                data = [
                    cg_name,
                    obj[2] if obj[2] != 'N/A' else 0,  # valid_daojia_order_count
                    obj[3] if obj[3] != 'N/A' else 0,  # valid_daojia_user_count
                    obj[4] if obj[4] != 'N/A' else 0,  # gmv
                    obj[5] if obj[5] != 'N/A' else 0,  # user_pay_price
                    obj[6] if obj[6] != 'N/A' else 0,  # total_cost
                    obj[7] if obj[7] != 'N/A' else 0,  # operation_cost
                    obj[8] if obj[8] != 'N/A' else 0,  # vip_operation_cost
                    obj[9] if obj[9] != 'N/A' else 0,  # pt_card_operation_cost 葡萄卡补贴
                    obj[10] if obj[10] != 'N/A' else 0,  # gross_profit
                    float(obj[11]) if obj[11] != 'N/A' else 0,  # avg_pay_per_order
                    float(orders_dict[cg_name][3]) if cg_name in orders_dict.keys() and orders_dict[cg_name][
                                                                                          3] != 'N/A' else 0,
                    # new_order_rate
                    float(orders_dict[cg_name][8]) if cg_name in orders_dict.keys() and orders_dict[cg_name][
                                                                                          8] != 'N/A' else 0,
                    # old_order_rate
                    float(orders_dict[cg_name][9]) if cg_name in orders_dict.keys() and orders_dict[cg_name][
                                                                                          9] != 'N/A' else 0,
                    # over_category_rebuy_rate
                ]
                cat_data[cg_name] = data
            else:
                cat_data[cg_name][1] += obj[2] if obj[2] != 'N/A' else 0
                cat_data[cg_name][2] += obj[3] if obj[3] != 'N/A' else 0
                cat_data[cg_name][3] += obj[4] if obj[4] != 'N/A' else 0
                cat_data[cg_name][4] += obj[5] if obj[5] != 'N/A' else 0
                cat_data[cg_name][5] += obj[6] if obj[6] != 'N/A' else 0
                cat_data[cg_name][6] += obj[7] if obj[7] != 'N/A' else 0
                cat_data[cg_name][7] += obj[8] if obj[8] != 'N/A' else 0
                cat_data[cg_name][8] += obj[9] if obj[9] != 'N/A' else 0
                cat_data[cg_name][9] += obj[10] if obj[10] != 'N/A' else 0
                cat_data[cg_name][10] += float(obj[11]) if obj[11] != 'N/A' else 0
                new_rate = orders_dict[cg_name][3] if cg_name in orders_dict.keys() and orders_dict[cg_name][
                                                                                          3] != 'N/A' else 0
                old_rate = orders_dict[cg_name][8] if cg_name in orders_dict.keys() and orders_dict[cg_name][
                                                                                          8] != 'N/A' else 0
                over_rate = orders_dict[cg_name][9] if cg_name in orders_dict.keys() and orders_dict[cg_name][
                                                                                           9] != 'N/A' else 0
                cat_data[cg_name][11] = float(new_rate)
                cat_data[cg_name][12] = float(old_rate)
                cat_data[cg_name][13] = float(over_rate)
        if data:
            g_data.append(
                data
            )
    if not g_data:
        if table_type == u"1":
            g_data.append([Const.NONE] * 18)
        elif table_type == u"5":
            g_data.append([Const.NONE] * 14)
    if table_type == u"5":
        g_data = []
        for key, value in cat_data.iteritems():
            g_data.append([
                value[0],
                format_douhao(str(value[1])),
                format_douhao(str(value[2])),
                format_douhao(str(value[3])),
                format_douhao(str(value[4])),
                format_douhao(str(value[5])),
                format_douhao(str(value[6])),
                format_douhao(str(value[7])),
                format_douhao(str(value[8])),
                format_douhao(str(value[9])),
                format_douhao(str(value[10])),
                str(round(float(value[11]) * 100, 2)) + '%',
                str(round(float(value[12]) * 100, 2)) + '%',
                str(round(float(value[13]) * 100, 2)) + '%',
            ])
        g_data.sort(key=lambda o: int(''.join(o[1].split(','))), reverse=True)
    else:
        g_data.sort(key=lambda o: int(''.join(o[2].split(','))), reverse=True)
    return HttpResponse(json.dumps(g_data))


def get_app_ver_channel(request):
    ot = request.POST.get("ot")
    if not ot:
        ot = None
    app = request.POST.get("app")
    report_check_app(request, app)
    if not app:
        app = None
    ver = request.POST.get("ver")  # 数据有问题
    if not ver:
        ver = None
    channel = request.POST.get("channel")
    if not channel or channel == '0':
        channel = None
    return ot, app, ver, channel


@login_required
# @permission_required(u'man.%s' % ReportConst.ORDER_REPORTS, raise_exception=True)
def exchange_daojia_order_summary_reports_csv(request):
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")
    table_type = request.GET.get("show_time_table_type")
    csv_data = []
    if table_type == u"1":
        table_name = '服务成交分析'
    else :
        table_name = '分类成交分析'
    filename = '%s(%s-%s).csv' % (str(table_name), str(start_date), str(end_date))
    if table_type == u"1":
        csv_data = [["分类",
                     "服务商名称",
                     "有效订单数",
                     "有效用户数",
                     "GMV",
                     "用户实付金额",
                     "成本",
                     "订单补贴",
                     "VIP补贴",
                     "葡萄卡补贴",
                     "毛利",
                     "商品平均单价",
                     "新客首单比例",
                     "该CP复购率",
                     "推首单后跨品类复购率",
                     "进行中/完成",
                     "待支付/取消/退款",
                     "超时接单/超时完成"]]
    elif table_type == u"5":
        csv_data = [["分类",
                     "有效订单数",
                     "有效用户数",
                     "GMV",
                     "用户实付金额",
                     "成本",
                     "订单补贴",
                     "葡萄卡补贴",
                     "VIP补贴",
                     "毛利",
                     "商品平均单价",
                     "新客首单比例",
                     "该CP复购率",
                     "推首单后跨品类复购率"]]
    csv_data.extend(g_data)
    return get_csv_response(filename, csv_data)


def get_evedata(start_date,end_date,citys_select,channel,p_type):
    # 获取业务现金情况数据
    cursor = connections['order'].cursor()
    cursor.execute("call `SP_T_RP_D_TURNOVER_DAOJIA_PRODUCT_SUMMARY_NEW`(%s, %s, %s, %s, %s, %s)",
                   [start_date.replace('-', ''), end_date.replace('-', ''), citys_select, channel, p_type, 1])
    evedata = cursor.fetchall()
    return evedata

def get_healthdata(start_date,end_date,citys_select,channel,p_type):
    # 获取健康度数据
    cursor = connections['report'].cursor()
    cursor.execute("call `SP_T_RP_D_TURNOVER_DAOJIA_PRODUCT_SUMMARY_USER`(%s, %s, %s, %s, %s, %s)",
                   [start_date.replace('-', ''), end_date.replace('-', ''), citys_select, channel, p_type, 1])
    healthdata = cursor.fetchall()
    return healthdata

def get_hour_data(start_date,end_date,citys_select,channel):
    # 获取每小时订单数和有效订单数
    cursor = connections['order'].cursor()
    cursor.execute("call `SP_T_RP_D_TURNOVER_DAOJIA_PRODUCT_SUMMARY_NEW_HOUR`(%s, %s, %s, %s)",
                   [start_date.replace('-', ''), end_date.replace('-', ''), citys_select, channel])
    healthdata = cursor.fetchall()
    hour_list = []
    hour_data = []
    for i in healthdata:
        hour_data.append([i[0],i[1],i[2],i[3]])
        hour_list.append(i[3])
    if len(hour_list) != 24:
        for i in range(24):
            if i not in hour_list:
                hour_data.append([str(i)+':00:00-'+str(i)+':59:59',0,0,i])
    hour_data.sort(key=lambda o: int(o[3]), reverse=False)
    return hour_data

def get_every_order(cur_page=1, limit_page=30, all=False, p_type='D', start_date=None, end_date=None, citys_select=None,
                    channel=None):
    data = {}

    evedata = get_evedata(start_date,end_date,citys_select,channel,p_type)

    healthdata = get_healthdata(start_date,end_date,citys_select,channel,p_type)

    if all:
        p_data = evedata
        h_data = healthdata
    else:
        p = Paginator(evedata, limit_page)
        h = Paginator(healthdata, limit_page)
        num_pags = p.num_pages
        p_data = p.page(cur_page)
        if cur_page <= h.num_pages:
            h_data = h.page(cur_page)
        else:
            h_data = []
        data['page'] = num_pags
        data['code'] = '0'
    every_order = []
    for i in p_data:
        every_order_single = []
        for h in h_data:
            if i[0] == h[0]:
                if p_type in  ['W','M'] :
                    k_fugou = round(get_k_fugou(start_date,end_date,p_type,h[0],citys_select,channel)/h[7]*100,2)
                else:
                    k_fugou = h[6]
                every_order_single = [
                    str(i[0]),
                    str(i[1]),
                    str(i[2]),
                    str(i[3]),
                    str(i[4]),
                    format_douhao(float(i[5])),
                    format_douhao(float(i[6])),
                    format_douhao(float(i[7])),
                    format_douhao(float(i[8])),
                    # float(i[9]),
                    format_douhao(float(i[10])),
                    format_douhao(float(i[11])),
                    format_douhao(float(i[12])),
                    format_douhao(float(i[13])),
                    format_douhao(float(i[14])),
                    str(h[1]) + '%',
                    str(h[2]) + '%',
                    str(k_fugou) + '%',
                    str(h[4]) + '%',
                    format_douhao(float(i[15])),
                ]
                break
        if len(every_order_single) == 0:
            every_order_single = [
                str(i[0]),
                str(i[1]),
                str(i[2]),
                str(i[3]),
                str(i[4]),
                format_douhao(float(i[5])),
                format_douhao(float(i[6])),
                format_douhao(float(i[7])),
                format_douhao(float(i[8])),
                # float(i[9]),
                format_douhao(float(i[10])),
                format_douhao(float(i[11])),
                format_douhao(float(i[12])),
                format_douhao(float(i[13])),
                format_douhao(float(i[14])),
                "N/A",
                "N/A",
                "N/A",
                "N/A",
                format_douhao(float(i[15])),
            ]
        every_order.append(every_order_single)

    data['data'] = every_order
    data['code'] = '0'
    print "finish!!!!!!"
    return data


@login_required
# @csrf_exempt
def exchange_daojia_order_summary_evemonth(request):
    try:
        cur_page = int(request.POST.get('cur_page', 1))
        limit_page = int(request.POST.get('limit_page', 30))
        start_date = request.POST["start_date"]
        end_date = request.POST["end_date"]
        period_type = request.POST["show_time_table_type"]
        citys_select = request.POST["citys_select"] if request.POST.get("citys_select") != '0' else None
        channel = request.POST["channel"] if request.POST.get("channel") != '0' else None
        print citys_select, channel
        data = get_every_order(cur_page, limit_page, p_type=period_type, start_date=start_date, end_date=end_date,
                               citys_select=citys_select, channel=channel)
    except Exception as e:
        data = {'code': '-1', 'msg': e.message}
    return HttpResponse(json.dumps(data))


@login_required
# @csrf_exempt
def exchange_daojia_order_summary_evemonth_csv(request):
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")
    period_type = request.GET.get("show_time_table_type")
    citys_select = request.GET.get("citys_select") if request.GET.get("citys_select") != '0' else None
    channel = request.GET.get("channel") if request.GET.get("channel") != '0' else None
    csv = get_every_order(all=True, p_type=period_type, start_date=start_date, end_date=end_date,
                          citys_select=citys_select, channel=channel)['data']
    name = "到家订单分析".encode('utf-8')
    filename = '%s.csv' % (name)
    csv_data = [["日期",
                 "订单数",
                 "有效订单数",
                 "下单用户数",
                 "有效用户数",
                 "葡萄卡销售金额",
                 "VIP储值充入金额",
                 "VIP储值送出金额",
                 "GMV",
                 "成本",
                 "订单补贴",
                 "VIP补贴",
                 "葡萄卡盈利",
                 "毛利",
                 "日活到成单率",
                 "新单比例",
                 "跨品类复购率",
                 "低价单率",
                 "平均每单补贴",
                 ]]
    csv_data.extend(csv)
    return get_csv_response(filename, csv_data)

def exchange_daojia_order_summary_linedata(request):
    try:
        data = get_summary_linedata(request)
    except Exception as e:
        data = {'code': '-1', 'msg': e.message}
    return HttpResponse(json.dumps(data))

def get_summary_linedata(request):
    """
    获取线形图数据
    :param tab_type:
    :return:
    """
    tab_type = request.POST["tab_type"]
    start_date = request.POST["start_date"]
    end_date = request.POST["end_date"]
    period_type = request.POST["show_time_table_type"]
    citys_select = request.POST["citys_select"] if request.POST.get("citys_select") != '0' else None
    channel = request.POST["channel"] if request.POST.get("channel") != '0' else None

    result = []
    x_axis = []
    r_data = []
    not_show = []
    if tab_type == 'two':
        evedata = get_evedata(start_date,end_date,citys_select,channel,period_type)
        daojia_order_count = []
        valid_daojia_order_count = []
        for i in evedata:
            daojia_order_count.append(float(i[1] if i[1] != 'N/A' else 0))
            valid_daojia_order_count.append(float(i[2] if i[2] != 'N/A' else 0))
            x_axis.append(i[0])
        daojia_order_count = list(reversed(daojia_order_count))
        valid_daojia_order_count = list(reversed(valid_daojia_order_count))
        result.append({"data": daojia_order_count, "type": "line", "name": "订单数"})
        result.append({"data": valid_daojia_order_count, "type": "line", "name": "有效成单数"})
    elif tab_type == 'three':
        evedata = get_evedata(start_date, end_date, citys_select, channel, period_type)
        daojia_user_count = []
        valid_daojia_user_count = []
        for i in evedata:
            daojia_user_count.append(float(i[3] if i[3] != 'N/A' else 0))
            valid_daojia_user_count.append(float(i[4] if i[4] != 'N/A' else 0))
            x_axis.append(i[0])
        daojia_user_count = list(reversed(daojia_user_count))
        valid_daojia_user_count = list(reversed(valid_daojia_user_count))
        result.append({"data": daojia_user_count, "type": "line", "name": "下单用户数"})
        result.append({"data": valid_daojia_user_count, "type": "line", "name": "有效用户数"})
    elif tab_type == 'four':
        healthdata = get_healthdata(start_date, end_date, citys_select, channel, period_type)
        active_user_order_rate = []
        for i in healthdata:
            active_user_order_rate.append(float(i[1] if i[1] != 'N/A' else 0))
            x_axis.append(i[0])
        active_user_order_rate = list(reversed(active_user_order_rate))
        result.append({"data": active_user_order_rate, "type": "line", "name": "日活到成单率"})
    elif tab_type == 'five':
        healthdata = get_healthdata(start_date, end_date, citys_select, channel, period_type)
        new_order_rate = []
        for i in healthdata:
            new_order_rate.append(float(i[2] if i[2] != 'N/A' else 0))
            x_axis.append(i[0])
        new_order_rate = list(reversed(new_order_rate))
        result.append({"data": new_order_rate, "type": "line", "name": "新单率"})
    elif tab_type == 'six':
        healthdata = get_healthdata(start_date, end_date, citys_select, channel, period_type)
        over_category_rebuy_rate = []
        for i in healthdata:
            if period_type in ['W', 'M']:
                k_fugou = round(get_k_fugou(start_date, end_date, period_type, i[0]) / i[7] * 100, 2)
            else:
                k_fugou = i[6]
            over_category_rebuy_rate.append(float(k_fugou if k_fugou != 'N/A' else 0))
            x_axis.append(i[0])
        over_category_rebuy_rate = list(reversed(over_category_rebuy_rate))
        result.append({"data": over_category_rebuy_rate, "type": "line", "name": "跨品类复购率"})
    elif tab_type == 'seven':
        healthdata = get_healthdata(start_date, end_date, citys_select, channel, period_type)
        low_paid_order_rate = []
        for i in healthdata:
            low_paid_order_rate.append(float(i[4] if i[4] != 'N/A' else 0))
            x_axis.append(i[0])
        low_paid_order_rate = list(reversed(low_paid_order_rate))
        result.append({"data": low_paid_order_rate, "type": "line", "name": "低价单率"})
    elif tab_type == 'eight':
        evedata = get_evedata(start_date, end_date, citys_select, channel, period_type)
        avg_cost_per_order = []
        for i in evedata:
            avg_cost_per_order.append(float(i[15] if i[15] != 'N/A' else 0))
            x_axis.append(i[0])
        avg_cost_per_order = list(reversed(avg_cost_per_order))
        result.append({"data": avg_cost_per_order, "type": "line", "name": "平均每单补贴"})
    elif tab_type == 'nine':
        evedatas = get_hour_data(start_date,end_date,citys_select,channel)
        daojia_order_count = []
        valid_daojia_order_count = []
        for i in evedatas:
            daojia_order_count.append(float(i[1] if i[1] != 'N/A' else 0))
            valid_daojia_order_count.append(float(i[2] if i[2] != 'N/A' else 0))
            x_axis.append(i[3])
        daojia_order_count = daojia_order_count
        valid_daojia_order_count = valid_daojia_order_count
        result.append({"data": daojia_order_count, "type": "line", "name": "订单数"})
        result.append({"data": valid_daojia_order_count, "type": "line", "name": "有效成单数"})
    else:  # 'one'
        evedata = get_evedata(start_date, end_date, citys_select, channel, period_type)
        gmv = []
        user_pay_price = []
        total_cost = []
        operation_cost = []
        vip_operation_cost = []
        gross_profit = []
        for i in evedata:
            gmv.append(float(i[8] if i[8] != 'N/A' else 0))
            user_pay_price.append(float(i[10] if i[10] != 'N/A' else 0))
            total_cost.append(float(i[11] if i[11] != 'N/A' else 0))
            operation_cost.append(float(i[12] if i[12] != 'N/A' else 0))
            vip_operation_cost.append(float(i[13] if i[13] != 'N/A' else 0))
            gross_profit.append(float(i[14] if i[14] != 'N/A' else 0))
            x_axis.append(i[0])
        gmv = list(reversed(gmv))
        user_pay_price = list(reversed(user_pay_price))
        total_cost = list(reversed(total_cost))
        operation_cost = list(reversed(operation_cost))
        vip_operation_cost = list(reversed(vip_operation_cost))
        gross_profit = list(reversed(gross_profit))
        result.append({"data": gmv, "type": "line", "name": "GMV"})
        result.append({"data": user_pay_price, "type": "line", "name": "成本"})
        result.append({"data": total_cost, "type": "line", "name": "订单补贴"})
        result.append({"data": operation_cost, "type": "line", "name": "VIP补贴"})
        result.append({"data": vip_operation_cost, "type": "line", "name": "葡萄卡盈利"})
        result.append({"data": gross_profit, "type": "line", "name": "毛利"})
        not_show = ["订单补贴", "VIP补贴", "葡萄卡盈利"]
    x_axis = sorted(x_axis) if tab_type != 'nine' else x_axis
    return [result, x_axis, not_show, r_data]


def format_douhao(n):
    """
    格式千分位
    :param n:
    :return:
    """
    try:
        nu = str(n).split('.')
        nu1 = "{:,}".format(int(nu[0]))
        if len(nu) == 1:
            nums = nu1
        else:
            nums = nu1 + '.' + nu[1]
        return nums
    except Exception as e :
        return n


def get_k_fugou(start_date,end_date,type,data_str,citys_select,channel):
    """
    获取跨平类复购数据
    :param type:
    :param data_str:
    :return:
    """
    cursor = connections['report'].cursor()
    sql = "SELECT COUNT(*) FROM (" \
            "SELECT d.`pt_u_id`,COUNT(DISTINCT cg.`new_category`) AS new_category " \
          "FROM pt_biz_report.`tongji_daojia_order_detail` d " \
          "LEFT JOIN pt_cms_db.`view_cms_goods_formal` cg ON cg.`goods_id`  = d.`goodsId` " \
          "LEFT JOIN pt_biz_report.tongji_pay_order o " \
          "ON (CONVERT( d.order_no USING UTF8) = o.ORDER_NO) " \
          "WHERE d.`pt_u_id` IN ( " \
          "SELECT DISTINCT d.`pt_u_id` FROM " \
          "pt_biz_report.`tongji_daojia_order_detail` d " \
          "WHERE DATE(d.create_time) >= %s " \
          " AND DATE(d.create_time) <= %s " \
          "AND d.status NOT IN (5,6,9,10,16,18,19,20,22,0)" \
          ") AND DATE(d.`create_time`) >= %s AND  DATE(d.`create_time`) <= %s %s %s " \
          "AND d.status NOT IN (5,6,9,10,16,18,19,20,22,0) GROUP BY d.`pt_u_id` )C " \
          "WHERE C.new_category > 1; "

    if type == 'W':
        date_t = data_str.split('-')
        if str(channel) == 'ios':
            channel_no =" AND o.channel_no ='app_store'"
        elif str(channel) == 'android':
            channel_no = " AND o.channel_no !='app_store'"
        else:
            channel_no = ""
        if citys_select :
            citys_select = ' AND d.city like "%%'+ str(citys_select)+'%%"'
        else:
            citys_select = ""
        sqls =  sql %(start_date.replace('-', ''), end_date.replace('-', ''), date_t[0],date_t[1],citys_select,channel_no)
        cursor.execute(str(sqls))
    else:
        date_t = data_str.split('-')
        if str(channel) == 'ios':
            channel_no = " AND o.channel_no ='app_store'"
        elif str(channel) == 'android':
            channel_no = " AND o.channel_no !='app_store'"
        else:
            channel_no = ""
        if citys_select:
            citys_select = ' AND d.city like %' + citys_select + '%'
        else:
            citys_select = ''
        import calendar
        date_t = start_date.split('-')
        date_td = end_date.split('-')
        if int(date_t[1]) == int(data_str[-2:]):
            cursor.execute(sql, [start_date.replace('-', ''), end_date.replace('-', ''), start_date.replace('-', ''),
                                 data_str+ str(calendar.monthrange(int(data_str[4:6]),int(data_str[-2:]))[1]),citys_select,channel_no])
        elif int(date_t[1]) < int(data_str[-2:]) and int(date_td[1]) > int(data_str[-2:]):
            cursor.execute(sql, [start_date.replace('-', ''), end_date.replace('-', ''), data_str+'01',
                                 data_str + str(calendar.monthrange(int(data_str[4:6]), int(data_str[-2:]))[1]),citys_select,channel_no])
        else:
            cursor.execute(sql, [start_date.replace('-', ''), end_date.replace('-', ''), data_str+'01',
                                 end_date.replace('-', ''),citys_select,channel_no])
    evedata = cursor.fetchone()
    r_data = evedata[0] if evedata is not None else 0
    return r_data