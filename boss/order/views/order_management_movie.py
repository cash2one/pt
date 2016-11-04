# coding: utf-8


from django.shortcuts import render_to_response
from order.models import PtDaojiaOrder,PtDaojiaOrderGuarantee
from order_pub import *
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.hashers import make_password
from django.template import RequestContext
from django.db import connection,transaction
import time


@login_required
@permission_required(u'man.%s' % ReportConst.ORDER_MANAGEMENT_MOVIE, raise_exception=True)
@add_common_var
def order_management_movie(request, template_name):
    movie_table_columns = get_movie_table_columns()

    return report_render(request, template_name,{
        "currentdate": get_datestr(0, "%Y-%m-%d"),
        "movie_table_columns":movie_table_columns,
    })

def get_order_detail(order_no):
    cursor = connections['order'].cursor()
    cursor.execute("CALL `pt_biz_db`.`SP_T_RP_D_ORDER_MANAGEMENT_RECHARGE`(%s, %s, %s);",
                    [order_no])
    objs = cursor.fetchall()
    data = [["订单号","活动类型","活动时间","活动消息","获取url","请求参数","返回消息","创建时间","修改时间"]]
    for obj in objs:
        data.append(
            [
                str(obj[0]),
                str(obj[1]),
                str(obj[2]),
                str(obj[3]),
                str(obj[4]),
                str(obj[5]),
                str(obj[6]),
                str(obj[7]),
                str(obj[8]),
            ]
        )
    if not data:
        data.append([Const.NONE] * 9)
    else:
        data.sort(key=lambda o: o[0], reverse=True)
    return data

def update_order_info(orders,cur_page,per_page):
    recharge_orders = []
    for obj in orders:
        #定义CP名称
        if str(obj[15]) == "2":
            cp_name = "格瓦拉"
        elif str(obj[15]) == "3":
            cp_name = "中影"
        elif str(obj[15]) == "5":
            cp_name = "卖座"
        elif str(obj[15]) == "115":
            cp_name = "微票"
        elif str(obj[15]) == "116":
            cp_name = "抠电影"
        else:
            cp_name = "未知CP"
        #定义支付类型
        if str(obj[22]) == "1":
            payment_type = "支付宝"
        elif str(obj[22]) == "2":
            payment_type = "微信支付"
        elif str(obj[22]) in ["6","7"]:
            payment_type = "金立支付"
        elif str(obj[22]) == "8":
            payment_type = "拉卡拉支付"
        else:
            payment_type = "未知支付"

        recharge_orders.append(
            [
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
                str(obj[11]),
                str(obj[12]),
                str(obj[13]),
                str(obj[14]),
                cp_name,
                str(obj[16]),
                str(obj[17]),
                str(obj[18]),
                str(obj[19]),
                str(obj[20]),
                str(obj[21]),
                payment_type,
                str(obj[23]),
                str(obj[24]),
                str(obj[25]),
                str(obj[26]),
                str(obj[27]),
                str(obj[28]),
            ]
        )
    if not recharge_orders:
        recharge_orders.append([Const.NONE] * 26)
    else:
        recharge_orders.sort(key=lambda o: o[21], reverse=True)
    return recharge_orders

def show_selected_columns(result,selected_columns):
    movie_table_columns = get_movie_table_columns()
    show_columns = []
    show_result = []
    row = []
    for col in selected_columns:
        for d_col in movie_table_columns:
            if col == d_col[1]:
                show_columns.append(d_col[0])
    for obj in result:
        for s_col in show_columns:
            row.append(obj[s_col])
        show_result.append(row)
        row = []
    return show_result

@login_required
@permission_required(u'man.%s' % ReportConst.ORDER_MANAGEMENT_MOVIE, raise_exception=True)
def order_management_movie_ajax(request):
    per_page = request.POST.get("per_page")
    cur_page = request.POST.get("cur_page")
    key = request.POST.get("key")
    if key == u'':
        key = None
    recharge_mobile_num = request.POST.get("search_recharge_mobile")
    if recharge_mobile_num == u'':
        recharge_mobile_num = None
    search_trade_no = request.POST.get("search_trade_no")
    if search_trade_no == u'':
        search_trade_no = None
    account_mobile_num = request.POST.get("search_account_mobile")
    if account_mobile_num == u'':
        account_mobile_num = None
    account_transaction_num = request.POST.get("search_payment_transaction_no")
    if account_transaction_num == u'':
        account_transaction_num = None
    start_date = request.POST.get("start_date")
    end_date = request.POST.get("end_date")
    selected_columns = request.POST.getlist("daojia_table[]")
    end_date_d = datetime.datetime.strptime(end_date, "%Y-%m-%d")+datetime.timedelta(days=1)

    cursor = connections['order'].cursor()
    cursor.execute("CALL `pt_biz_db`.`SP_T_RP_D_ORDER_MANAGEMENT_MOVIE`(%s, %s, %s, %s, %s);",
                    [key,search_trade_no,recharge_mobile_num,account_mobile_num,account_transaction_num])
    orders = cursor.fetchall()

   #获取订单列表下载信息
    global g_data
    g_data = []
    g_data = update_order_info(orders, 0, 0)

   #列表展示信息
    orders, num_pages = pag(orders, per_page, cur_page)
    result = update_order_info(orders, int(cur_page), int(per_page))

    #仅展示被选中的列表信息
    show_result = show_selected_columns(result,selected_columns)

    return HttpResponse(json.dumps([show_result, num_pages]))

@login_required
@permission_required(u'man.%s' % ReportConst.ORDER_MANAGEMENT_MOVIE, raise_exception=True)
def order_management_movie_detail_ajax(request):
    order_no = request.POST["order_no"]
    result = get_order_detail(order_no)
    return HttpResponse(json.dumps(result))

@login_required
@permission_required(u'man.%s' % ReportConst.ORDER_MANAGEMENT_MOVIE, raise_exception=True)
def order_management_movie_csv(request):
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")
    filename = '%s(%s-%s).csv' % ("电影业务订单详情", str(start_date), str(end_date))
    csv_data = [["ID",
                  "葡萄订单号",
                  "CP订单号",
                  "影院名称",
                  "放映时间",
                  "影厅",
                  "座位信息",
                  "取票码",
                  "取票单号",
                  "取票验证吗",
                 "业务类型",
                 "面值",
                 "充值电话",
                 "下单人电话",
                 "商品名称",
                 "CP名称",
                 "数量",
                 "支付价格",
                 "用户唯一标实",
                 "优惠券ID",
                 "优惠券面值",
                 "订单创建时间",
                 "支付类型",
                 "订单状态",
                 "应用渠道",
                 "支付渠道",
                 "应用ID",
                 "应用版本"]]
    csv_data.extend(g_data)
    return get_csv_response(filename, csv_data)