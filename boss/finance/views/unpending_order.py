#coding: utf-8

"""
    无压单对账明细
"""

from finance_pub import *

def get_unpending_data(start_date, end_date, order_type, cp_type, payment_type, finance_result, order_state, ver, channel, app, daojia_cp_type):
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
    if order_type:
        if int(order_type) == 110:
            if daojia_cp_type:
                cp_type = daojia_cp_type;
    cursor = connections['report'].cursor()
    cursor.execute("call `SP_T_RP_D_ACCOUNT_CHECKING`(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
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
                str(obj[18]),
                str(obj[19]),
				str(obj[20]),
            ]
        )
    if not data:
        data.append([Const.NONE] * 21)
    else:
        data.sort(key=lambda o: o[0], reverse=True)
    return data

@login_required
@permission_required(u'man.%s' % FinanceConst.FINANCE_DETAIL_NO_OV_ORDER_DETAIL, raise_exception=True)
@add_common_var
def unpending_order(request, template_name):
    app = request.GET.get("app")
    report_check_app(request, app)
    vers = get_app_versions(app)
    channels = get_app_channels(app)
    products = get_order_types()
    order_states = get_order_states()
    finance_results = get_finance_result_type()
    cp_types = get_cp_types()
    daojia_cp_types = get_full_cp_names()
    payment_types = get_payment_types()
    cur_order_type = None
    cur_cp_type = None
    cur_daojia_cp_type = None
    try:
        cur_order_type = int(request.GET.get("order_type"))
    except:
        pass
    try:
        cur_cp_type = int(request.GET.get("cp_type"))
    except:
        pass
    try:
        if int(cur_order_type) == 110:
            if cur_cp_type:
                cur_daojia_cp_type = cur_cp_type
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
        "cur_daojia_cp_type":cur_daojia_cp_type,
        "daojia_cp_types":daojia_cp_types,
    })

@login_required
@permission_required(u'man.%s' % FinanceConst.FINANCE_DETAIL_NO_OV_ORDER_DETAIL, raise_exception=True)
def unpending_order_ajax(request):
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
    daojia_cp_type = request.POST.get("daojia_cp_type")
    payment_type = request.POST.get("payment_type")
    result = get_unpending_data(start_date, end_date, order_type, cp_type, payment_type, finance_result, order_state, ver, channel, app, daojia_cp_type)
    return HttpResponse(json.dumps(result))


@login_required
@permission_required(u'man.%s' % FinanceConst.FINANCE_DETAIL_NO_OV_ORDER_DETAIL, raise_exception=True)
def unpending_order_csv(request):
    print("unpending_order_csv")
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
    daojia_cp_type = request.GET.get("daojia_cp_type")
    payment_type = request.GET.get("payment_type")
    if order_type:
        name = "%s无压单对账明细表" % str(TongjiPayProduct.objects.get(type=order_type).name)
    else:
        name = "无压单对账明细表"
    filename = '%s(%s-%s).csv' % (name, str(start_date), str(end_date))
    csv_data = [["订单号",
                "订单创建时间",
                "商品名字",
                "内容商名称",
                "支付方式",
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
                 "异常原因",
				 "订单来源"]]
    csv_data.extend(get_unpending_data(start_date, end_date, order_type, cp_type, payment_type, finance_result, order_state, ver, channel, app, daojia_cp_type))
    return get_csv_response(filename, csv_data)