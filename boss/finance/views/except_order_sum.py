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
    print("objs is ", objs)
    return objs


def get_sum_data(start_date, end_date, app):
    if not start_date:
        start_date = None
    if not end_date:
        end_date = None

    print("app is ", app)

    cursor = connections['report'].cursor()

    cursor.execute("call `SP_T_RP_D_ACCOUNT_CHECK_SUMMARY_APP`(%s, %s, %s)",
                    [start_date, end_date, app])
    objs = cursor.fetchall()
    str_objs = string_objs(objs, 2)
    except_sum = []
    for obj in str_objs:
        temp_data = ['','','','','','','','']
        temp_data[0] = obj[0]
        #temp_data[0] = obj[0]
        t_datas = obj[1].split('|')
        except_result = []
        for data in t_datas:
            t_data = data.split(':')
            except_result.append(t_data)
        for data in except_result:
            if data[0] in except_type.keys():
                t_str = data[2]+' ('+data[1]+'笔)'
                temp_data[except_type[data[0]]] = t_str
            else:
                print("except_type except")
                print(obj)
                print(data[0])
        except_sum.append(temp_data)
    return except_sum

@login_required
@permission_required(u'man.%s' % FinanceConst.FINANCE_DETAIL_ABNORMAL_ORDER_SUMMARY, raise_exception=True)
@add_common_var
def except_order_sum(request, template_name):
    app = request.GET.get("app")
    print(app)
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
@permission_required(u'man.%s' % FinanceConst.FINANCE_DETAIL_ABNORMAL_ORDER_SUMMARY, raise_exception=True)
def except_order_sum_ajax(request):
    start_date = request.POST["start_date"]
    end_date = request.POST["end_date"]

    app = request.POST.get("app")
    report_check_app(request, app)
    if app:
        app = "^%s$" % app
    else:
        app = get_user_apps(request.user)

    result = get_sum_data(start_date, end_date, app)
    return HttpResponse(json.dumps(result))


@login_required
@permission_required(u'man.%s' % FinanceConst.FINANCE_DETAIL_ABNORMAL_ORDER_SUMMARY, raise_exception=True)
def except_order_sum_csv(request):
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")

    app = request.GET.get("app")
    report_check_app(request, app)
    if app:
        app = "^%s$" % app
    else:
        app = get_user_apps(request.user)

    name = "异常订单汇总表"
    filename = '%s(%s-%s).csv' % (name, str(start_date), str(end_date))
    csv_data = [['业务类型', '无支付平台数据,CP数据', '无支付平台数据', '无CP数据', '实收价格不等于实付价格', 'PT退款,CP未退款', 'CP退款,PT未退款', '未知']]
    csv_data.extend(get_sum_data(start_date, end_date))
    return get_csv_response(filename, csv_data)