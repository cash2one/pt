#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'putao'
__mtime__ = '1/26/2016'
"""
from django.views.decorators.csrf import csrf_exempt

from order.views.order_pub import get_daojia_goods_category
from report.views.exchange_daojia_order_summary import format_douhao
from report_pub import *

g_data = []


@login_required
@add_common_var
def exchange_daojia_order_cash(request, template_name):
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
        # "summary": summary,
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
        if i[0] not in f_dict.keys():
            f_dict[i[0]] = [i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7]]
        else:
            if not isinstance(i[3], float) or not isinstance(i[4], float) or not isinstance(i[5],
                                                                                            float) or not isinstance(
                    i[6], float) or not isinstance(i[7], float):
                continue
            f_dict[i[0]][3] += i[3]
            f_dict[i[0]][4] += i[4]
            f_dict[i[0]][5] += i[5]
            f_dict[i[0]][6] += i[6]
            f_dict[i[0]][7] += i[7]
    return f_dict


def get_exchange_daojia_order_cash_table_data(request):
    start_date = request.POST["start_date"]
    end_date = request.POST["end_date"]
    table_type = request.POST["show_table_type"]
    period_type = request.POST["show_time_table_type"]
    citys_select = request.POST.get("citys_select") if request.POST.get("citys_select") != '0' else None
    ot, app, ver, channel = get_app_ver_channel(request)
    # category_info = get_daojia_goods_category()
    global g_data  # 返回列表数据
    g_data = []
    cat_data = {}
    if table_type == u"1":
        table_num = 2
    else :
        table_num = 3
    cursor = connections['order'].cursor()
    cursor.execute("call `SP_T_RP_D_TURNOVER_DAOJIA_PRODUCT_SUMMARY_CASH`(%s, %s, %s, %s, %s, %s)",
                   [start_date.replace('-', ''), end_date.replace('-', ''), citys_select, channel, period_type, table_num])
    objs = cursor.fetchall()
    week_k = {}
    for obj in objs:
        data = []
        if table_type == u"1":
            data = [
                str(obj[0]),
                format_douhao(str(obj[1])),
                str(obj[2]),
                str(obj[4]),
                str(obj[5]),
                str(obj[6]),
                str(obj[7]),
                str(obj[8]),
                str(obj[9]),
                str(obj[10]),
            ]
            if period_type == 'W':
                week_list = obj[0].split('-')
                if week_list[0] not in week_k.keys():
                    week_k[str(week_list[0])] = [str(obj[0]),
                        float(obj[1]),
                        float(obj[2]),
                        float(obj[4]),
                        float(obj[5]),
                        float(obj[6]),
                        float(obj[7]),
                        float(obj[8]),
                        float(obj[9]),
                        float(obj[10])]
                else:
                    act = week_k[obj[0].split('-')[0]][0].split('-')
                    if float(week_list[1]) > float(act[1]):
                        t_time = obj[0]
                    else:
                        t_time = week_k[obj[0].split('-')[0]][0]
                    data = [
                        t_time,
                        float(obj[1]) + week_k[obj[0].split('-')[0]][1],
                        union_price(float(obj[1]),week_k[obj[0].split('-')[0]][1],float(obj[2]),week_k[obj[0].split('-')[0]][2]),
                        union_price(float(obj[1]),week_k[obj[0].split('-')[0]][1],float(obj[4]),week_k[obj[0].split('-')[0]][3]),
                        union_price(float(obj[1]),week_k[obj[0].split('-')[0]][1],float(obj[5]),week_k[obj[0].split('-')[0]][4]),
                        union_price(float(obj[1]),week_k[obj[0].split('-')[0]][1],float(obj[6]),week_k[obj[0].split('-')[0]][5]),
                        union_price(float(obj[1]),week_k[obj[0].split('-')[0]][1],float(obj[7]),week_k[obj[0].split('-')[0]][6]),
                        union_price(float(obj[1]),week_k[obj[0].split('-')[0]][1],float(obj[8]),week_k[obj[0].split('-')[0]][7]),
                        union_price(float(obj[1]),week_k[obj[0].split('-')[0]][1],float(obj[9]),week_k[obj[0].split('-')[0]][8]),
                        union_price(float(obj[1]),week_k[obj[0].split('-')[0]][1],float(obj[10]),week_k[obj[0].split('-')[0]][9])
                    ]
                    g_data.pop()

        elif table_type == u"5":
            data = [
                str(obj[1]),  #
                format_douhao(str(obj[2])),  #
                format_douhao(str(obj[3])),  #
                format_douhao(str(obj[4])),  #
                format_douhao(str(obj[5])),  #
                format_douhao(str(obj[6])),  #
                str(obj[7]),  #
                format_douhao(str(obj[8])),  #
                str(obj[9]),  #
                format_douhao(str(obj[10])),  #
                format_douhao(str(obj[11])),  #
                format_douhao(str(obj[12])),
                format_douhao(str(obj[13])),
                format_douhao(str(obj[14])),
                format_douhao(str(obj[15])),  #
                format_douhao(str(obj[16])),  #
            ]
        if data:
            g_data.append(
                data
            )
    if not g_data:
        if table_type == u"1":
            g_data.append([Const.NONE] * 10)
        elif table_type == u"5":
            g_data.append([Const.NONE] * 16)
    if table_type == u"5":
        g_data.sort(key=lambda o: float(''.join(o[9].split(','))), reverse=True)
    else:
        pass
        # g_data.sort(key=lambda o: float(o[1]), reverse=True)
    return HttpResponse(json.dumps(g_data))

def union_price(first_total,second_total,first_price,second_price):
    """
    合并多余项当 week时刻
    :param total:
    :param price:
    :return:
    """
    try:
        if float(first_price) == 100:
            price_rate = round(first_total/float(first_total+second_total)*100,2)
        elif float(second_price) == 100:
            price_rate = round(second_total/float(first_total+second_total)*100,2)
        else:
            price_rate = float(first_price)+float(second_price)
        return price_rate
    except:
        price_rate = first_price + second_price
        return price_rate


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
def exchange_daojia_order_cash_reports_csv(request):
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")
    table_type = request.GET.get("show_time_table_type")
    csv_data = []
    if table_type == u"1":
        table_name = '活动成本分析'
    else :
        table_name = 'CP成本分析'
    filename = '%s(%s-%s).csv' % (str(table_name), str(start_date), str(end_date))
    if table_type == u"1":
        csv_data = [["日期",
                     "补贴",
                     "VIP补贴/占比",
                     "秒杀补贴/占比",
                     "邀新有礼补贴/占比",
                     "红包补贴/占比",
                     "新人领券补贴/占比",
                     "评论补贴/占比",
                     "保障补贴/占比",
                     "其他补贴差额/占比"]]
    elif table_type == u"5":
        csv_data = [["服务商名称",
                     "GMV",
                     "成本",
                     "订单补贴",
                     "VIP补贴",
                     "葡萄卡盈利",
                     "补贴率",
                     "毛利",
                     "毛利率",
                     "有效成单数",
                     "有效用户数",
                     "ARPU",
                     "平均每单补贴额",
                     "平均每人补贴额",
                     "平均每单补毛利",
                     "平均每人补毛利",
                     ]]
    csv_data.extend(g_data)
    return get_csv_response(filename, csv_data)





def get_every_order(cur_page=1, limit_page=30, all=False, p_type='D', start_date=None, end_date=None, citys_select=None,
                    channel=None):
    data = {}

    # 获取业务现金情况数据
    cursor = connections['order'].cursor()
    cursor.execute("call `SP_T_RP_D_TURNOVER_DAOJIA_PRODUCT_SUMMARY_CASH`(%s, %s, %s, %s, %s, %s)",
                   [start_date.replace('-', ''), end_date.replace('-', ''), citys_select, channel, p_type, 1])
    evedata = cursor.fetchall()
    if all:
        p_data = evedata
    else:
        p = Paginator(evedata, limit_page)
        num_pags = p.num_pages
        p_data = p.page(cur_page)
        data['page'] = num_pags
        data['code'] = '0'
    every_order = []
    for i in p_data:
        every_order_single = [
            str(i[0]),
            format_douhao(str(i[1])),
            format_douhao(str(i[2])),
            format_douhao(str(i[3])),
            format_douhao(str(i[4])),
            format_douhao(str(i[5])),
            str(i[6]),
            format_douhao(str(i[7])),
            str(i[8]),
            format_douhao(str(i[9])),
            format_douhao(str(i[10])),
            format_douhao(str(i[11])),
            format_douhao(str(i[12])),
            format_douhao(str(i[13])),
            format_douhao(str(i[14])),
            format_douhao(str(i[15])),
        ]
        every_order.append(every_order_single)

    data['data'] = every_order
    data['code'] = '0'
    return data


@login_required
# @csrf_exempt
def exchange_daojia_order_cash_evemonth(request):
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
def exchange_daojia_order_cash_evemonth_csv(request):
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")
    period_type = request.GET.get("show_time_table_type")
    citys_select = request.GET.get("citys_select") if request.GET.get("citys_select") != '0' else None
    channel = request.GET.get("channel") if request.GET.get("channel") != '0' else None
    csv = get_every_order(all=True, p_type=period_type, start_date=start_date, end_date=end_date,
                          citys_select=citys_select, channel=channel)['data']
    name = "到家现金分析".encode('utf-8')
    filename = '%s.csv' % (name)
    csv_data = [["日期",
                 "GMV",
                 "成本",
                 "订单补贴",
                 "VIP补贴",
                 "葡萄卡盈利",
                 "补贴率",
                 "毛利",
                 "毛利率",
                 "有效成单数",
                 "有效用户数",
                 "ARPU",
                 "平均每单补贴额",
                 "平均每人补贴额",
                 "平均每单补毛利",
                 "平均每人补毛利",
                 ]]
    csv_data.extend(csv)
    return get_csv_response(filename, csv_data)
