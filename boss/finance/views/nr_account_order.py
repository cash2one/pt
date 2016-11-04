#coding: utf-8

"""
    所有订单状态报表
"""

from finance.models import TongjiPayProduct
from finance_pub import *


def get_nr_account_data(start_date, end_date):
    """
    获取所有订单状态报表汇总数据
    :param start_date: 开始日期
    :param end_date: 结束日期
    :param order_type: 订单种类
    :param app: 应用id
    :param ver: 版本
    :param channel: 渠道
    :return:
    """

    if not start_date:
        start_date = None
    if not end_date:
        end_date = None

    cursor = connections['report'].cursor()
    cursor.execute("call `SP_T_RP_D_NR_ACCOUNT_CHECKING`(%s, %s, %s, %s, %s, %s)",
                    [start_date, end_date, None, None, None, 1])
    objs = cursor.fetchall()
    data = []

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
            ]
        )

    if not data:
        data.append([Const.NONE] * 8)
    else:
        data.sort(key=lambda o: o[0], reverse=True)
    return data



@login_required
@permission_required(u'man.%s' % FinanceConst.FINANCE_DETAIL_NR_ORDER_DETAIL, raise_exception=True)
@add_common_var
def nr_account_order(request, template_name):
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
@permission_required(u'man.%s' % FinanceConst.FINANCE_DETAIL_NR_ORDER_DETAIL, raise_exception=True)
def nr_account_order_ajax(request):
    start_date = request.POST["start_date"]
    end_date = request.POST["end_date"]
    result = get_nr_account_data(start_date, end_date)
    return HttpResponse(json.dumps(result))



@login_required
@permission_required(u'man.%s' % FinanceConst.FINANCE_DETAIL_NR_ORDER_DETAIL, raise_exception=True)
def nr_account_order_csv(request):
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")
    name = "非匹配订单对账对账明细表"
    filename = '%s(%s-%s).csv' % (name, str(start_date), str(end_date))
    csv_data = [["订单号",
                "订单创建时间",
                "实收款",
                "实际退款",
                "交易服务费",
                "实际付款",
                "是否异常",
                "异常原因"]]
    csv_data.extend(get_nr_account_data(start_date, end_date))
    return get_csv_response(filename, csv_data)