# coding: utf-8

"""
    日报表
"""
import time

from finance.models import VmPtVipCardFinanceSummary, VmPtVipCardSubOrdersSummary
from finance_pub import *


@login_required
@permission_required(u'man.%s' % FinanceConst.FINANCE_OPERATION_VIP_OPERATION_SUMMARY, raise_exception=True)
@add_common_var
def daily_operate_vip(request, template_name):
    vip_table_columns = get_vip_finance_table_columns()
    vip_card_types = get_vip_card_types()
    return report_render(request, template_name,{
        "currentdate": get_datestr(1, "%Y-%m-%d"),
        "vip_table_columns": vip_table_columns,
        "vip_card_types": vip_card_types,
    })


def vip_card_fianace(start_date, end_date):
    start_date = start_date.replace('-','')
    end_date = end_date.replace('-','')
    try:
        cursor = connections['order'].cursor()
        cursor.execute("call `SP_T_RP_D_VIP_CARD_FINANCE_REPORT`(%s, %s, %s)",[start_date, end_date, 1])
        # cursor.execute("commit")
        vdata = cursor.fetchall()
        return vdata
    except Exception as err:
        pass

def check_order_info(vip_data,vip_card_type):
    if vip_card_type:
        if vip_data[2] != vip_card_type:
            return False
    return True

@login_required
@permission_required(u'man.%s' % FinanceConst.FINANCE_OPERATION_VIP_OPERATION_SUMMARY, raise_exception=True)
def daily_operate_vip_ajax(request):
    per_page = request.POST.get("per_page")
    cur_page = request.POST.get("cur_page")
    start_date = request.POST.get("start_date")
    end_date = request.POST.get("end_date")
    vip_card_type = request.POST.get("vip_card_type")
    end_date_d = datetime.datetime.strptime(end_date, "%Y-%m-%d") + datetime.timedelta(days=1)
    # vip_data = VmPtVipCardFinanceSummary.objects.using('order').filter(c_time__gte=start_date, c_time__lte=end_date_d)
    vip_data = vip_card_fianace(start_date, end_date)
    # if key is not None:
    #     vip_data = vip_data.filter(order_no=key)
    # if vip_mobile_num is not None:
    #     vip_data = vip_data.filter(user_mobile=vip_mobile_num)

    # 获取VIP卡数据
    # vip_data = VmPtVipCardFinanceSummary.objects.using('order')\
    #     .filter(c_time__gte=start_date, c_time__lte=end_date_d,vip_card_type__contains=vip_card_type)

    # 获取订单列表下载信息
    tt_products = []
    for product in vip_data:
        if check_order_info(product,vip_card_type):
            tt_products.append(product)
    global g_data
    g_data = []
    g_data = update_order_info(tt_products, 0, 0)

    # 列表展示信息
    orders, num_pages = pag(tt_products, per_page, cur_page)
    result = update_order_info(orders, int(cur_page), int(per_page))

    # 仅展示被选中的列表信息
    # show_result = show_selected_columns(result, selected_columns)

    return HttpResponse(json.dumps([result, num_pages]))


@login_required
@permission_required(u'man.%s' % FinanceConst.FINANCE_OPERATION_VIP_OPERATION_SUMMARY, raise_exception=True)
def daily_operate_vip_csv(request):
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")
    filename = '%s(%s-%s).csv' % ("VIP卡业务订单详情", str(start_date), str(end_date))
    csv_data = [["用户ID",
                 "VIP卡ID",
                 "VIP卡类型",
                 "本期实收款",
                 "本期额度",
                 "本期消耗",
                 "剩余额度",
                 "本期实付",
                 ]]
    csv_data.extend(g_data)
    return get_csv_response(filename, csv_data)


def update_order_info(orders, cur_page, per_page):
    vip_orders = []
    for obj in orders:
        if obj[2] == u'exchange':
            type = u'次卡'
        elif obj[2] == u'recharege':
            type = u'充值卡'
        else:
            type = u'无此类卡'
        vip_orders.append(
            [
                str(obj[0]),
                str(obj[1]),
                str(type),
                str(obj[3]),
                str(obj[4]),
                str(obj[5]),
                str(obj[6]),
                str(obj[7]),
            ]
        )
    return vip_orders


@login_required
@permission_required(u'man.%s' % FinanceConst.FINANCE_OPERATION_VIP_OPERATION_SUMMARY, raise_exception=True)
@add_common_var
def daily_operate_vip_detail(request, template_name):
    pt_user_id = request.GET.get("pt_user_id")
    vip_card_id = request.GET.get("vip_card_id")
    return report_render(request, template_name,
                         {"currentdate": get_datestr(1, "%Y-%m-%d"), "pt_user_id": pt_user_id,
                          "vip_card_id": vip_card_id})


@login_required
@permission_required(u'man.%s' % FinanceConst.FINANCE_OPERATION_VIP_OPERATION_SUMMARY, raise_exception=True)
def daily_operate_vip_detail_ajax(request):
    per_page = request.POST.get("per_page")
    cur_page = request.POST.get("cur_page")
    pt_user_id = request.POST.get("pt_user_id")
    vip_card_id = request.POST.get("vip_card_id")
    vip_data = VmPtVipCardSubOrdersSummary.objects.using('order').filter(pt_user_id=str(pt_user_id),
                                                                         vip_card_id=str(vip_card_id))
    if not vip_data:
        return HttpResponse('no')
    global v_data
    v_data = []
    v_data = update_order_detail_info(vip_data, 0, 0)

    # 列表展示信息
    orders, num_pages = pag(vip_data, per_page, cur_page)
    result = update_order_detail_info(orders, int(cur_page), int(per_page))

    return HttpResponse(json.dumps([result, num_pages]))


@login_required
@permission_required(u'man.%s' % FinanceConst.FINANCE_OPERATION_VIP_OPERATION_SUMMARY, raise_exception=True)
def daily_operate_vip_detail_csv(request):
    pt_user_id = request.GET.get("pt_user_id")
    vip_card_id = request.GET.get("vip_card_id")
    filename = '%s(%s).csv' % ("VIP卡用户详情", str(pt_user_id))
    csv_data = [["用户ID",
                 "VIP卡ID",
                 "订单号",
                 "服务商",
                 "商品名称",
                 "应付款",
                 "应收款",
                 "实收款",
                 "实退款",
                 "实付款",
                 "优惠券",
                 "批价策略",
                 ]]
    csv_data.extend(v_data)
    return get_csv_response(filename, csv_data)


def update_order_detail_info(orders, cur_page, per_page):
    vip_orders = []
    for obj in orders:
        vip_orders.append(
            [
                str(obj.pt_user_id),
                str(obj.vip_card_id),
                str(obj.order_no),
                str(obj.provider),
                str(obj.name),
                str(obj.cp_sell_price),
                str(obj.pt_sell_price),
                str(obj.pay_price),
                str(obj.refund_price),
                str(obj.pt_should_pay_price),
                str(obj.pt_favo_price),
                str(obj.cp_favo_price),
            ]
        )
    return vip_orders
