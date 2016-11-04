#coding: utf-8

"""
    所有订单状态报表
"""

from finance.models import TongjiPayProduct
from finance_pub import *


def get_pending_order_data(start_date, end_date, order_type, cp_type, payment_type, finance_result, order_state, ver, channel, app):
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
    if not app:
        app = None
    if not ver:
        ver = None
    if not channel:
        channel = None
    if not order_type:
        order_type = None
    if not order_state:
        order_state = None
    if not finance_result:
        finance_result = None
    if not cp_type:
        cp_type = None
    if not payment_type:
        payment_type = None
    cursor = connections['report'].cursor()
    cursor.execute("call `SP_T_RP_D_OV_ACCOUNT_CHECKING`(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                    [start_date, end_date, order_type, cp_type, payment_type, finance_result, order_state, ver, channel, app])
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
                str(obj[8]),
                str(obj[9]),
                str(obj[10]),
                str(obj[11]),
                str(obj[12]),
                str(obj[13]),
                str(obj[14]),
                str(obj[15]),
                str(obj[16]),
                str(obj[17]),
            ]
        )

    if not data:
        data.append([Const.NONE] * 18)
    else:
        data.sort(key=lambda o: o[0], reverse=True)
    return data

def get_pending_order_detail(order_no):
    print("get_pending_order_detail", order_no)
    cursor = connections['report'].cursor()
    cursor.execute("call `SP_T_RP_OV_ORDER_DETAIL`(%s)",
                    [order_no])
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
                str(obj[8]),
                str(obj[9]),
                str(obj[10]),
                str(obj[11]),
                str(obj[12]),
                str(obj[13]),
                str(obj[14]),
                str(obj[15]),
                str(obj[16]),
            ]
        )
    if not data:
        data.append([Const.NONE] * 17)
    else:
        data.sort(key=lambda o: o[0], reverse=True)
    return data



@login_required
@permission_required(u'man.%s' % FinanceConst.FINANCE_DETAIL_OV_ORDER_DETAIL, raise_exception=True)
@add_common_var
def pending_order(request, template_name):
    app = request.GET.get("app")
    report_check_app(request, app)
    vers = get_app_versions(app)
    channels = get_app_channels(app)
    products = get_order_types()
    order_states = get_order_states()
    finance_results = get_finance_result_type()
    cp_types = get_cp_types()
    payment_types = get_payment_types()
    cur_order_type = None
    cur_cp_type = None
    try:
        cur_order_type = int(request.GET.get("order_type"))
    except:
        pass
    try:
        cur_cp_type = int(request.GET.get("cp_type"))
    except:
        pass
    return report_render(request, template_name, {
        "currentdate": get_datestr(1, "%Y-%m-%d"),
        "vers": vers,
        "channels": channels,
        "products": products,
        "order_states":order_states,
        "finance_results":finance_results,
        "cp_types":cp_types,
        "payment_types":payment_types,
        "cur_order_type":cur_order_type,
        "cur_cp_type":cur_cp_type,
    })


@login_required
@permission_required(u'man.%s' % FinanceConst.FINANCE_DETAIL_OV_ORDER_DETAIL, raise_exception=True)
def pending_order_ajax(request):
    start_date = request.POST["start_date"]
    end_date = request.POST["end_date"]
    order_type = request.POST["ot"]
    app = request.POST.get("app")
    report_check_app(request, app)
    if app:
        app = "^%s$" % app
    else:
        app = get_user_apps(request.user)
    ver = request.POST.get("ver")
    channel = request.POST.get("channel")
    order_state = request.POST.get("order_state")
    finance_result = request.POST.get("finance_result")
    cp_type = request.POST.get("cp_type")
    payment_type = request.POST.get("payment_type")
    result = get_pending_order_data(start_date, end_date, order_type, cp_type, payment_type, finance_result, order_state, ver, channel, app)
    return HttpResponse(json.dumps(result))

@login_required
@permission_required(u'man.%s' % FinanceConst.FINANCE_DETAIL_OV_ORDER_DETAIL, raise_exception=True)
def pending_order_detail_ajax(request):
    order_no = request.POST["order_no"]
    result = get_pending_order_detail(order_no)
    return HttpResponse(json.dumps(result))


@login_required
@permission_required(u'man.%s' % FinanceConst.FINANCE_DETAIL_OV_ORDER_DETAIL, raise_exception=True)
def pending_order_csv(request):
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")
    order_type = request.GET.get("ot")
    app = request.GET.get("app")
    report_check_app(request, app)
    if app:
        app = "^%s$" % app
    else:
        app = get_user_apps(request.user)
    ver = request.GET.get("ver")
    channel = request.GET.get("channel")
    order_state = request.GET.get("order_state")
    finance_result = request.GET.get("finance_result")
    cp_type = request.GET.get("cp_type")
    payment_type = request.GET.get("payment_type")
    if order_type:
        name = "%s有压单对账明细表" % str(TongjiPayProduct.objects.get(type=order_type).name)
    else:
        name = "有压单对账明细表"
    filename = '%s(%s-%s).csv' % (name, str(start_date), str(end_date))
    csv_data = [["订单号",
                "订单创建时间",
                "商品名字",
                "商品定价(应收款)",
                "商品成本价(应付款)",
                "营销策略编号",
                "营销减免金额",
                "优惠券编号",
                "优惠券面值",
                "优惠券消耗价格",
                "交易状态",
                "应退款",
                "实收款",
                "实际退款",
                "交易服务费",
                "实际付款",
                "是否异常",
                "异常原因"]]
    csv_data.extend(get_pending_order_data(start_date, end_date, order_type, cp_type, payment_type, finance_result, order_state, ver, channel, app))
    return get_csv_response(filename, csv_data)