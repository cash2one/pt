# coding: utf-8


from django.shortcuts import render_to_response
from order.models import PtDaojiaOrder, PtDaojiaOrderGuarantee, PtVoucherResource, VmPtVipOrder
from order_pub import *
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.hashers import make_password
from django.template import RequestContext
from django.db import connection, transaction
import time


@login_required
@permission_required(u'man.%s' % ReportConst.ORDER_MANAGEMENT_VIP, raise_exception=True)
@add_common_var
def order_management_vip(request, template_name):
    vip_table_columns = get_vip_table_columns()
    order_status = get_normal_order_status()

    return report_render(request, template_name, {
        "currentdate": get_datestr(0, "%Y-%m-%d"),
        "vip_table_columns": vip_table_columns,
        "order_status": order_status,
    })


def update_order_info(orders, cur_page, per_page):
    vip_orders = []
    for obj in orders:
        get_app_name(obj.app_id)
        # 定义app名称
        if obj.order_status == 0:
            status = "订单取消"
        elif obj.order_status == 1:
            status = "订单待支付"
        elif obj.order_status == 3:
            status = "订单处理中"
        elif obj.order_status == 4:
            status = "交易成功"
        elif obj.order_status == 5:
            status = "退款中"
        elif obj.order_status == 6:
            status = "退款成功"
        elif obj.order_status == 7:
            status = "订单关闭"

        vip_orders.append(
            [
                str(obj.id),
                str(obj.order_no),
                str(obj.goods_name),
                str(obj.user_mobile),
                str(obj.cost_price),
                str(obj.pay_price),
                status,
                str(get_app_name(obj.app_id)),
                str(obj.app_version),
                str(obj.channel_no),
                str(obj.pt_u_id),
                str(obj.c_time),
                str(obj.favo_price),
            ]
        )
    if not vip_orders:
        vip_orders.append([Const.NONE] * 13)
    else:
        vip_orders.sort(key=lambda o: o[11], reverse=True)
    return vip_orders


def check_order_info(order, order_status):
    if order_status:
        if str(order.order_status) not in order_status:
            return False

    return True


def show_selected_columns(result, selected_columns):
    vip_table_columns = get_vip_table_columns()
    show_columns = []
    show_result = []
    row = []
    for col in selected_columns:
        for d_col in vip_table_columns:
            if col == d_col[1]:
                show_columns.append(d_col[0])
    for obj in result:
        for s_col in show_columns:
            row.append(obj[s_col])
        show_result.append(row)
        row = []
    return show_result


@login_required
@permission_required(u'man.%s' % ReportConst.ORDER_MANAGEMENT_VIP, raise_exception=True)
def order_management_vip_ajax(request):
    per_page = request.POST.get("per_page")
    cur_page = request.POST.get("cur_page")
    key = request.POST.get("key")
    if key == u'':
        key = None
    vip_mobile_num = request.POST.get("search_vip_mobile")
    if vip_mobile_num == u'':
        vip_mobile_num = None
    order_status = request.POST.getlist("order_status[]")
    start_date = request.POST.get("start_date")
    end_date = request.POST.get("end_date")
    selected_columns = request.POST.getlist("daojia_table[]")
    end_date_d = datetime.datetime.strptime(end_date, "%Y-%m-%d") + datetime.timedelta(days=1)
    vip_data = VmPtVipOrder.objects.using('order').order_by('id').filter(c_time__gte=start_date, c_time__lte=end_date_d)

    if key is not None:
        vip_data = vip_data.filter(order_no=key)
    if vip_mobile_num is not None:
        vip_data = vip_data.filter(user_mobile=vip_mobile_num)

    # 有效订单校验
    tt_orders = []
    for order in vip_data:
        if check_order_info(order, order_status):
            tt_orders.append(order)

    # 获取订单列表下载信息
    global g_data
    g_data = []
    g_data = update_order_info(tt_orders, 0, 0)

    # 列表展示信息
    orders, num_pages = pag(tt_orders, per_page, cur_page)
    result = update_order_info(orders, int(cur_page), int(per_page))

    # 仅展示被选中的列表信息
    show_result = show_selected_columns(result, selected_columns)

    return HttpResponse(json.dumps([show_result, num_pages]))


@login_required
@permission_required(u'man.%s' % ReportConst.ORDER_MANAGEMENT_VIP, raise_exception=True)
def order_management_vip_csv(request):
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")
    filename = '%s(%s-%s).csv' % ("VIP卡业务订单详情", str(start_date), str(end_date))
    csv_data = [["ID",
                 "订单号",
                 "商品名称",
                 "用户手机号",
                 "订单金额",
                 "实付金额",
                 "订单状态",
                 "应用ID",
                 "版本号",
                 "渠道号",
                 "用户ID",
                 "创建时间",
                 "促销活动信息",
                 ]]
    csv_data.extend(g_data)
    return get_csv_response(filename, csv_data)
