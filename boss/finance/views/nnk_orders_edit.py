#coding: utf-8

"""
    所有订单状态报表
"""

from finance.models import FinanceCpPfLlk
from finance_pub import *


def get_nr_account_data():

    nnk_orders = FinanceCpPfLlk.objects.using('report').filter(order_state__contains="处理中")
    data = []

    for orders in nnk_orders:
        data.append(
            [
                str(orders.llk_order_id),
                str(orders.putao_order_no),
                str(orders.add_time),
                str(orders.moblie),
                str(orders.face_value),
                str(orders.actual_pay),
                str(orders.order_state),
                u"",
                u"",
                u"",
            ]
        )

    if not data:
        data.append([Const.NONE] * 10)
    else:
        data.sort(key=lambda o: o[0], reverse=True)
    return data



@login_required
@permission_required(u'man.%s' % FinanceConst.FINANCE_EVENT_UPLOAD_CP_BILL, raise_exception=True)
@add_common_var
def nnk_orders_edit(request, template_name):
    app = request.GET.get("app")
    report_check_app(request, app)
    vers = get_app_versions(app)
    channels = get_app_channels(app)
    products = get_order_types()
    order_states = get_order_states()
    finance_results = get_finance_result_type()
    cp_types = get_cp_types()
    payment_types = get_payment_types()
    return report_render(request, template_name, {
        "currentdate": get_datestr(1, "%Y-%m-%d"),
        "vers": vers,
        "channels": channels,
        "products": products,
        "order_states":order_states,
        "finance_results":finance_results,
        "cp_types":cp_types,
        "payment_types":payment_types,
    })


@login_required
@permission_required(u'man.%s' % FinanceConst.FINANCE_EVENT_UPLOAD_CP_BILL, raise_exception=True)
def nnk_orders_edit_ajax(request):
    result = get_nr_account_data()
    return HttpResponse(json.dumps(result))


@login_required
@permission_required(u'man.%s' % FinanceConst.FINANCE_EVENT_UPLOAD_CP_BILL, raise_exception=True)
def nnk_orders_update_ajax(request):
    start_date = request.POST.get("start_date")
    u_success_orders = request.POST.getlist("u_success_order[]")
    u_refund_orders = request.POST.getlist("u_refund_order[]")
    u_process_orders = request.POST.getlist("u_process_order[]")

    # 更新订单状态
    for success_order in u_success_orders:
        FinanceCpPfLlk.objects.using('report').filter(llk_order_id=success_order).update(order_state=u'成功')
    for refund_order in u_refund_orders:
        FinanceCpPfLlk.objects.using('report').filter(llk_order_id=refund_order).update(order_state=u'已申请退款')
    for process_order in u_process_orders:
        FinanceCpPfLlk.objects.using('report').filter(llk_order_id=process_order).update(order_state=u'处理中')

    #调用存储过程
    cursor = connections['report'].cursor()
    cursor.execute("call `SP_T_LD_CP_ALL`(%s, %s, %s, %s)",
                    [start_date, 16, 3, u"'LLK DUIZHANG'"])
    cursor.close()

    result = get_nr_account_data()
    return HttpResponse(json.dumps(result))



@login_required
@permission_required(u'man.%s' % FinanceConst.FINANCE_EVENT_UPLOAD_CP_BILL, raise_exception=True)
def nnk_orders_edit_csv(request):
    name = "年年卡待定订单列表"
    filename = '%s.csv' % (name)
    csv_data = [["订单号",
                "订单创建时间",
                "实收款",
                "实际退款",
                "交易服务费",
                "实际付款",
                "是否异常",
                "异常原因"]]
    csv_data.extend(get_nr_account_data())
    return get_csv_response(filename, csv_data)