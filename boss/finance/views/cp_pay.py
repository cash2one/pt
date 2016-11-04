# coding: utf-8

"""
    所有订单状态报表
"""

import time, datetime

from django.contrib.auth.decorators import login_required, permission_required
from django.db import transaction, connections
from django.http import HttpResponse
from common.views import get_datestr, add_common_var
from finance.views.finance_pub import FinanceConst, add_report_var, get_pay_types, report_render


@login_required
@permission_required(u'man.%s' % FinanceConst.FINANCE_EVENT_UPLOAD_CP_BILL, raise_exception=True)
@add_common_var
def upload_cp_pay(request, template_name):
    cur_cp_type = request.GET.get("cp_type") or -1
    cp_types = get_pay_types()
    return report_render(request, template_name, {
        "cp_types": cp_types,
        "cur_cp_type": cur_cp_type,
        "currentdate": get_datestr(1, "%Y-%m-%d")
    })



@login_required
@permission_required(u'man.%s' % FinanceConst.FINANCE_EVENT_UPLOAD_CP_BILL, raise_exception=True)
def upload_cp_pay_csv(request):
    cp_type = int(request.GET.get("cp_type"))
    product_type = int(request.GET.get("product_type"))
    start_date = request.GET.get("start_date")

    if cp_type == -1:
        return HttpResponse("failed")
    csv_data = request.FILES.getlist("file_data")
    try:
        filter_data = filter_csv(csv_data,cp_type)
        result = dump_cp_data(filter_data, cp_type)
        notify_cp_refreshed(start_date, cp_type, product_type)
        return HttpResponse(result)
    except Exception as e:
        print("in excepct", e)
        return HttpResponse(e)


def notify_cp_refreshed(start_date, cp_type, product_type):
    print("notify_zf_refreshed begin")
    print(start_date)
    print(cp_type)
    print(product_type)
    time_stamp = int(time.mktime(datetime.datetime.now().timetuple()))
    print(time_stamp)
    cursor = connections['report'].cursor()
    cursor.execute("call `SP_T_LD_ZF_ALL_UPLOAD`(%s, %s)",
                   [start_date, str(time_stamp)])
    cursor.execute("commit")
    # cursor.fetchall()
    print("notify_zf_refreshed end")


def filter_csv(csv_data,cp_type):
    if cp_type in (8,9):
        if csv_data.__len__() == 2:
            filter_data = []
            if csv_data[0]._name == u'gionee_pay.csv' and csv_data[1]._name == u'gionee_refund.csv':
                pay_data = csv_data[0].read().decode('gbk').encode('utf-8')
                pay_list = filter_cp_data(pay_data, cp_type)
                refund_data = csv_data[1].read().decode('gbk').encode('utf-8')
                refund_list = filter_cp_data(refund_data, cp_type)
                filter_data.append(pay_list[1:])
                filter_data.append(refund_list[1:])
            elif csv_data[1]._name == u'gionee_pay.csv' and csv_data[0]._name == u'gionee_refund.csv':
                pay_data = csv_data[1].read().decode('gbk').encode('utf-8')
                pay_list = filter_cp_data(pay_data, cp_type)
                refund_data = csv_data[0].read().decode('gbk').encode('utf-8')
                refund_list = filter_cp_data(refund_data, cp_type)
                filter_data.append(pay_list[1:])
                filter_data.append(refund_list[1:])
            else:
                raise Exception('no gionee_pay.csv or gionee_refund.csv')
        else:
            raise Exception('no gionee_pay.csv or gionee_refund.csv')
    else:
        csv_data = csv_data.read().decode('gbk').encode('utf-8')
        filter_data = filter_cp_data(csv_data, cp_type)
    return filter_data


def formate_data(data):
    f_data = data.replace("\t", "")
    f_data = f_data.replace('"', "")
    f_data = f_data.replace("'", "")
    f_data = f_data.strip()
    return f_data


def filter_cp_data(data, cp_type):
    f_data = data.replace("\r", "")
    fl_data = f_data.replace("﻿", "")
    ff_data = fl_data.replace("'", "")
    a = ff_data.split('\n')
    com_data = []
    for single_data in a:
        single_list = single_data.split(',')
        single_list = map(formate_data, single_list)
        if len(single_list) != 1:
            com_data.append(single_list)

    return com_data

# sort   list , 拼接顺序
# data   list , 数据
def sql_splice(sort,data=[]):
    sql = ''
    result = ''
    for i in data:
        if len(i) == 1:
            result += result.rstrip(',') + ';'
            return result
        for j in sort:
            if j == '':
                sql_data = ''
            else:
                sql_data = i[j]
            sql += '"' + sql_data + '",'
        result += '(' + sql.rstrip(',') + '),'
    result += result.rstrip(',') + ';'
    return result


def dump_cp_data(data, cp_type):
    cursor = connections['report'].cursor()
    if cp_type == 8 or cp_type == 9:
        print("金立支付宝")
        # ssql_0 = sql_splice([1,2,3,'',4,5],data[0])
        # ssql_1 = sql_splice([1,2,3,'',4,5],data[1])
        for single_data in data[0]:
            sql = "replace into finance_zf_source_gionee(`gionee_order_no`, `goods_name`, `trade_time`, `third_party_order_no`, `putao_order_no`, `channel`, `order_state`, `payment_type`, `income`, `gionee_refund_no`, `refund`, `refund_reason`, `approver`, `close_time`) " \
                  "values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
            # 　print sql
            cursor.execute(sql, [str(single_data[0]), str(single_data[6]), str(single_data[2]), str(''),
                                 str(single_data[1]), str(single_data[4]),str(single_data[9]), str(single_data[7]),
                                 single_data[8], str(''),0, str(''),
                                 str(''), str(single_data[11])])
            transaction.commit_unless_managed(using='report')
        for single_data in data[1]:
            sql = "replace into finance_zf_source_gionee(`gionee_order_no`, `goods_name`, `trade_time`, `third_party_order_no`, `putao_order_no`, `channel`, `order_state`, `payment_type`, `income`, `gionee_refund_no`, `refund`, `refund_reason`, `approver`, `close_time`) " \
                  "values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
            # 　print sql
            cursor.execute(sql, [str(single_data[3]), str(''), str(single_data[1]),str(single_data[2]),
                                 str(single_data[4]),str(single_data[5]), str(single_data[6]), str(single_data[7]),
                                 0,str(single_data[0]), str(single_data[8]), '',
                                 str(single_data[10]), str('')])
            transaction.commit_unless_managed(using='report')
    else:
        return "cp_type not exsit"

    return "success"


@login_required
@permission_required(u'man.%s' % FinanceConst.FINANCE_EVENT_UPLOAD_CP_BILL, raise_exception=True)
def upload_balance_pay_ajax(request):
    print("in upload_balance_ajax")
    cp_id = request.POST.get('cp_id')
    print(cp_id)
    balance = request.POST.get('balance')
    print(balance)

    try:
        cursor = connections['report'].cursor()
        sql = "update finance_cp_accounts set account_balance = " + str(balance) + " where cp_id = " + str(cp_id) + ";"
        print(sql)
        cursor.execute(sql)
        transaction.commit_unless_managed(using='report')
        return HttpResponse('success')
    except Exception, e:
        return HttpResponse(e)


@login_required
@permission_required(u'man.%s' % FinanceConst.FINANCE_EVENT_UPLOAD_CP_BILL, raise_exception=True)
def refresh_zf_summary(request):
    start_date = request.POST.get("start_date")
    end_date = request.POST.get("end_date")

    try:
        cursor = connections['report'].cursor()
        cursor.execute("CALL `SP_T_LD_RP_D_CASH_SUMMARY_APP`(%s, %s)",
                   [start_date, end_date])
        cursor.execute("CALL `SP_T_LD_RP_D_OPERATION_DATA_SUMMARY_APP`(%s, %s)",
                   [start_date, end_date])
        cursor.execute("commit")
        cursor.execute("CALL `SP_T_LD_RP_D_DAOJIA_OPERATION_DATA_SUMMARY_APP`(%s, %s)",
                   [start_date, end_date])
        return HttpResponse('Update Successfully!')
    except Exception, e:
        return HttpResponse(e)
