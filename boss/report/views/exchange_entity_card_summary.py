# coding: utf-8

"""
    日报表
"""
import time

from finance.models import VmPtVipCardFinanceSummary, VmPtVipCardSubOrdersSummary
from report_pub import *


@login_required
@add_common_var
def exchange_entity_card_summary(request, template_name):
    entity_card_columns = get_entity_card_columns()
    vip_card_types = get_vip_card_types()
    return report_render(request, template_name,{
        "currentdate": get_datestr(0, "%Y-%m-%d"),
        "entity_card_columns": entity_card_columns,
    })


def vip_card_fianace(start_date, end_date):
    start_date = start_date.replace('-','')
    end_date = end_date.replace('-','')
    try:
        cursor = connections['order'].cursor()
        cursor.execute("call `SP_T_RP_D_ENTITY_CARD_REPORT`(%s, %s)",[start_date, end_date])
        # cursor.execute("commit")
        vdata = cursor.fetchall()
        return vdata
    except Exception as err:
        pass

@login_required
def exchange_entity_card_summary_ajax(request):
    per_page = request.POST.get("per_page")
    cur_page = request.POST.get("cur_page")
    start_date = request.POST.get("start_date")
    end_date = request.POST.get("end_date")
    vip_data = vip_card_fianace(start_date, end_date)
    # 获取订单列表下载信息
    tt_products = []
    for product in vip_data:
        print product
        tt_products.append(product)
    global g_data
    g_data = []
    g_data = update_order_info(tt_products, 0, 0)

    # 列表展示信息
    orders, num_pages = pag(tt_products, per_page, cur_page)
    result = update_order_info(orders, int(cur_page), int(per_page))

    return HttpResponse(json.dumps([result, num_pages]))


@login_required
def exchange_entity_card_summary_csv(request):
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")
    filename = '%s(%s-%s).csv' % ("葡萄实体卡统计", str(start_date), str(end_date))
    csv_data = [["实体卡批次",
                 "卡片名称",
                 "卡片备注",
                 "卡片次数",
                 "卡片售价",
                 "有效期",
                 "生成时间",
                 "生成数量",
                 "激活数量",
                 "订单创建次数",
                 "服务完成次数",
                 "操作",
                 ]]
    csv_data.extend(g_data)
    return get_csv_response(filename, csv_data)


def update_order_info(orders, cur_page, per_page):
    vip_orders = []
    for obj in orders:
        vip_orders.append(
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
            ]
        )
    return vip_orders


@login_required
@add_common_var
def exchange_entity_card_summary_detail(request, template_name):
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")
    card_id = request.GET.get("card_id")
    return report_render(request, template_name,
                         {"currentdate": get_datestr(1, "%Y-%m-%d"),
                          "start_date": start_date,
                          "end_date": end_date,
                          "card_id": card_id
                          })


@login_required
def exchange_entity_card_summary_detail_ajax(request):
    per_page = request.POST.get("per_page")
    cur_page = request.POST.get("cur_page")
    start_date = request.POST.get("start_date")
    end_date = request.POST.get("end_date")
    card_id = request.POST.get("card_id")
    cursor = connections['order'].cursor()
    cursor.execute("call `SP_T_RP_D_ENTITY_CARD_REPORT_DETAIL`(%s, %s, %s)",[start_date, end_date, card_id])
    vip_data = cursor.fetchall()

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
def exchange_entity_card_summary_detail_csv(request):
    pt_user_id = request.GET.get("pt_user_id")
    vip_card_id = request.GET.get("vip_card_id")
    filename = '%s(%s).csv' % ("葡萄实体卡-子订单统计", str(pt_user_id))
    csv_data = [["实体卡序号",
                 "卡片名称",
                 "卡片次数",
                 "剩余次数",
                 "实际有效期",
                 "绑定手机号",
                 "订单状态",
                 "订单单号",
                 "服务商",
                 "商品名称",
                 "下单时间",
                 "服务时间",
                 "预约人帐号",
                 "预约人手机号",
                 ]]
    csv_data.extend(v_data)
    return get_csv_response(filename, csv_data)


def update_order_detail_info(orders, cur_page, per_page):
    vip_orders = []
    for obj in orders:
        vip_orders.append(
            [
                str(obj[0]),
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
            ]
        )
    return vip_orders
