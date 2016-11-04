#coding: utf-8

"""
    无压单对账明细
"""

from finance_pub import *

except_type = {
    '无支付平台数据,CP数据':1,
    '无支付平台数据':2,
    '无CP数据':3,
    '实收价格不等于实付价格':4,
    'PT退款,CP未退款':5,
    'CP退款,PT未退款':6,
    '未知':7,
}

def string_objs(fet_objs, num):
    objs = []
    for obj in fet_objs:
        str_obj = []
        for i in range(0, num):
            str_obj.append(str(obj[i]))
        objs.append(str_obj)
    return objs


def get_sum_data(start_date, end_date, app):
    if not start_date:
        start_date = None
    if not end_date:
        end_date = None

    cursor = connections['report'].cursor()
    cursor.execute("call `SP_T_RP_D_ZF_DAOJIA_ORDER_SUMMARY_BY_CP`(%s, %s, %s)",
                    [start_date, end_date, None])
    data = []
    objs = cursor.fetchall()
    for obj in objs:
        data.append(
            [
                str(obj[0]),
                str(obj[1]),
                str(obj[2]),
                str(obj[3]),
                str(obj[4]),
            ]
        )
        print obj
    if not data:
        data.append([Const.NONE] * 5)
    else:
        data.sort(key=lambda o: o[0], reverse=True)
    return data

@login_required
@permission_required(u'man.%s' % FinanceConst.FINANCE_ZF_DAOJIA_REPORT, raise_exception=True)
@add_common_var
def pay_summary_by_daojia_cp(request, template_name):
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
@permission_required(u'man.%s' % FinanceConst.FINANCE_ZF_DAOJIA_REPORT, raise_exception=True)
def pay_summary_by_daojia_cp_ajax(request):
    print("except_order_sum_ajax")
    start_date = request.POST["start_date"]
    end_date = request.POST["end_date"]
    print(start_date, end_date)

    app = request.POST.get("app")
    report_check_app(request, app)
    if app:
        app = "^%s$" % app
    else:
        app = get_user_apps(request.user)

    result = get_sum_data(start_date, end_date, app)
    return HttpResponse(json.dumps(result))


@login_required
@permission_required(u'man.%s' % FinanceConst.FINANCE_ZF_DAOJIA_REPORT, raise_exception=True)
def pay_summary_by_daojia_cp_csv(request):
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")

    app = request.GET.get("app")
    report_check_app(request, app)
    if app:
        app = "^%s$" % app
    else:
        app = get_user_apps(request.user)

    name = "支付数据分业务汇总"
    filename = '%s(%s-%s).csv' % (name, str(start_date), str(end_date))
    csv_data = [['支付渠道', 'CP名称', '业务名称', '订单支付', '订单退款']]
    csv_data.extend(get_sum_data(start_date, end_date, app))
    return get_csv_response(filename, csv_data)