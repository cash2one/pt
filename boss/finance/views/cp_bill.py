#coding: utf-8

"""
    所有订单状态报表
"""

import time, datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.db import transaction, connections
from django.http import HttpResponse

from common.views import get_datestr, add_common_var
from finance.views.finance_pub import FinanceConst,add_report_var, get_cp_types, report_render

@login_required
@permission_required(u'man.%s' % FinanceConst.FINANCE_EVENT_UPLOAD_CP_BILL, raise_exception=True)
@add_common_var
def upload_cp_bill(request, template_name):
    cur_cp_type = request.GET.get("cp_type") or -1
    cp_types = get_cp_types()
    return report_render(request, template_name, {
        "cp_types": cp_types,
        "cur_cp_type": cur_cp_type,
        "currentdate": get_datestr(1, "%Y-%m-%d")
    })


@login_required
@permission_required(u'man.%s' % FinanceConst.FINANCE_EVENT_UPLOAD_CP_BILL, raise_exception=True)
def upload_cp_csv(request):
    cp_type = int(request.GET.get("cp_type"))
    product_type = int(request.GET.get("product_type"))
    start_date = request.GET.get("start_date")

    if cp_type == -1:
        return HttpResponse("failed")
    csv_data = request.FILES["file_data"].read()

    try :
        filter_data = filter_cp_data(csv_data, cp_type)
        result = dump_cp_data(filter_data, cp_type)
        notify_cp_refreshed(start_date, cp_type, product_type)
        return HttpResponse(result)
    except Exception, e:
        print("in excepct", e)
        return HttpResponse(e)

def notify_cp_refreshed(start_date, cp_type, product_type):
    print("notify_cp_refreshed begin")
    print(start_date)
    print(cp_type)
    print(product_type)
    time_stamp = int(time.mktime(datetime.datetime.now().timetuple()))
    print(time_stamp)
    cursor = connections['report'].cursor()
    cursor.execute("call `SP_T_LD_CP_ALL_UPLOAD`(%s, %s, %s, %s)",
                    [start_date, cp_type, product_type, str(time_stamp)])
    cursor.execute("commit")
    #cursor.fetchall()
    print("notify_cp_refreshed end")

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
    if cp_type == 20:
        for single_data in a:
            single_list = single_data.split(',')
            single_list = map(formate_data,single_list)
            com_data.append(single_list)
    else:
        for single_data in a:
            single_list = single_data.split(',')
            com_data.append(single_list)

    return com_data

def dump_cp_data(data, cp_type):

    cursor = connections['report'].cursor()
    if cp_type == 2:
        print("gwl")
        for single_data in data:
            sql = "replace into finance_cp_movie_gwl(gwl_trade_no, putao_order_no, add_time, paid_time, mp_id, gwl_user_id, cinema_name, movie_name, paid_amount, quantity) values ('" + str(single_data[0]) + "', '" + str(single_data[1]) + "', '" + str(single_data[2]) + "', '" + str(single_data[3]) + "', '" + str(single_data[4]) + "', '" + str(single_data[5]) + "', '" + str(single_data[6]) + "', '" + str(single_data[7]) + "', '" + str(single_data[8]) + "', '" + str(single_data[9])  + "');"
            #print(sql)
            cursor.execute(sql)
            transaction.commit_unless_managed(using='report')
    elif cp_type == 3:
        print("zhongyin")
        for single_data in data:
            sql = "replace into finance_cp_movie_zy(zy_trade_no, zy_user_id, zy_order_no, mobile, distributor, channel, city_name, cinema_name, business_type, quantity, paid_amount, add_time, status, payment_status, ticketing_status, refund_amount) values ('" + str(single_data[0]) + "', '" + str(single_data[1]) + "', '" + str(single_data[2]) + "', '" + str(single_data[3]) + "', '" + str(single_data[4]) + "', '" + str(single_data[5]) + "', '" + str(single_data[6]) + "', '" + str(single_data[7]) + "', '" + str(single_data[8]) + "', '" + str(single_data[9]) + "', '" + str(single_data[10]) + "', '" + str(single_data[11]) + "', '" + str(single_data[12]) + "', '" + str(single_data[13]) + "', '" + str(single_data[14]) + "', '" + str(single_data[15]) + "');"
            #print(sql)
            cursor.execute(sql)
            transaction.commit_unless_managed(using='report')
    elif cp_type == 5:
        print("maizuo")
        for single_data in data:
            sql = "replace into finance_cp_movie_mz(mz_order_no, mz_trade_no, cinema_name, city_name, movie_name, ticket_type, movie_type, quantity, unit_price, paid_amount, mobile, add_time, play_time) values ('" + str(single_data[0]) + "', '" + str(single_data[1]) + "', '" + str(single_data[2]) + "', '" + str(single_data[3]) + "', '" + str(single_data[4]) + "', '" + str(single_data[5]) + "', '" + str(single_data[6]) + "', '" + str(single_data[7]) + "', '" + str(single_data[8]) + "', '" + str(single_data[9]) + "', '" + str(single_data[10]) + "', '" + str(single_data[11]) + "', '" + str(single_data[12])  + "');"
            #print(sql)
            cursor.execute(sql)
            transaction.commit_unless_managed(using='report')
    elif cp_type == 7:
        print("gaoyangfee")
        for single_data in data:
            if str(single_data[8]) == "":
                single_data[8] = 0
            if str(single_data[10]) == "":
                single_data[10] = 0
            if str(single_data[11]) == "":
                single_data[11] = 0
            if str(single_data[12]) == "":
                single_data[12] = 0
            if str(single_data[13]) == "":
                single_data[13] = 0
            sql = "replace into finance_cp_pf_gaoyang(`key`, log_time, platform_order, putao_order, pay_order, province, service_provide, account_type, face_value, moblie, single_value, actual_pay, transfer_account, refund, order_state) values ('" + str(single_data[0]) + "', '" + str(single_data[1]) + "', '" + str(single_data[2]) + "', '" + str(single_data[3]) + "', '" + str(single_data[4]) + "', '" + str(single_data[5]) + "', '" + str(single_data[6]) + "', '" + str(single_data[7]) + "', '" + str(single_data[8]) + "', '" + str(single_data[9]) + "', '" + str(single_data[10]) + "', '" + str(single_data[11]) + "', '" + str(single_data[12])  + "', '" + str(single_data[13])  + "', '" + str(single_data[14])  + "');"
            #print(sql)
            cursor.execute(sql)
            transaction.commit_unless_managed(using='report')
    elif cp_type == 8:
        print("gaoyangflow")
        for single_data in data:
            if str(single_data[8]) == "":
                single_data[8] = 0
            if str(single_data[10]) == "":
                single_data[10] = 0
            if str(single_data[11]) == "":
                single_data[11] = 0
            if str(single_data[12]) == "":
                single_data[12] = 0
            if str(single_data[13]) == "":
                single_data[13] = 0
            sql = "replace into finance_cp_flow_gaoyang(`key`, log_time, platform_order, putao_order, pay_order, province, service_provide, account_type, face_value, moblie, single_value, actual_pay, transfer_account, refund, order_state) values ('" + str(single_data[0]) + "', '" + str(single_data[1]) + "', '" + str(single_data[2]) + "', '" + str(single_data[3]) + "', '" + str(single_data[4]) + "', '" + str(single_data[5]) + "', '" + str(single_data[6]) + "', '" + str(single_data[7]) + "', '" + str(single_data[8]) + "', '" + str(single_data[9]) + "', '" + str(single_data[10]) + "', '" + str(single_data[11]) + "', '" + str(single_data[12])  + "', '" + str(single_data[13])  + "', '" + str(single_data[14])  + "');"
            #print(sql)
            cursor.execute(sql)
            transaction.commit_unless_managed(using='report')
    elif cp_type == 11:
        print("福禄")
        for single_data in data:
            sql = "replace into finance_cp_game_fulu(fulu_trade_no, putao_order_no, goods_id, goods_name, goods_type, quantity, sell_price, account, order_status, trans_time, refund_status) values ('" + str(single_data[0]) + "', '" + str(single_data[1]) + "', '" + str(single_data[2]) + "', '" + str(single_data[3]) + "', '" + str(single_data[4]) + "', '" + str(single_data[5]) + "', '" + str(single_data[6]) + "', '" + str(single_data[7]) + "', '" + str(single_data[8]) + "', '" + str(single_data[9]) + "', '" + str(single_data[9]) + "');"
            #print(sql)
            cursor.execute(sql)
            transaction.commit_unless_managed(using='report')
    elif cp_type == 115:
        print("weidianyin", data)
        for single_data in data:
            sql = "replace into finance_cp_movie_wp(channel, wp_trade_no, cinema_id, cinema_name, movie_name, unit_price, quantity, paid_amount, wp_service_fee, add_time, paid_time, wp_order_no) values ('" + str(single_data[0]) + "', '" + str(single_data[1]) + "', '" + str(single_data[2]) + "', '" + str(single_data[3]) + "', '" + str(single_data[4]) + "', '" + str(single_data[5]) + "', '" + str(single_data[6]) + "', '" + str(single_data[7]) + "', '" + str(single_data[8]) + "', '" + str(single_data[9]) + "', '" + str(single_data[10]) + "', '" + str(single_data[11]) + "');"
            #print(sql)
            cursor.execute(sql)
            transaction.commit_unless_managed(using='report')
    elif cp_type == 116:
        print("koudianyin")
        for single_data in data:
            sql = "replace into finance_cp_movie_kdy(kdy_trade_no, add_time, mobile, cinema_name, movie_name, play_time, room_name, quantity, unit_price, paid_amount, status) values ('" + str(single_data[0]) + "', '" + str(single_data[1]) + "', '" + str(single_data[2]) + "', '" + str(single_data[3]) + "', '" + str(single_data[4]) + "', '" + str(single_data[5]) + "', '" + str(single_data[6]) + "', '" + str(single_data[7]) + "', '" + str(single_data[8]) + "', '" + str(single_data[9]) + "', '" + str(single_data[10]) + "');"
            #print(sql)
            cursor.execute(sql)
            transaction.commit_unless_managed(using='report')
    elif cp_type == 120:
        print("易赛水电煤")
        for single_data in data:
            sql = "replace into finance_cp_wec_esai(`id`, `ip`, `app_type`, `s_code`, `esai_user_id`, `province`, `city`, `carrier`, `esai_trade_no`, `putao_order_no`, `recharge_type`, `account`, `expire_date`, `recharge_amount`, `paid_amount`, `sell_price`, `start_time`, `timeout`, `status`, `recharge_result`) values ('" + str(single_data[0]) + "', '" + str(single_data[1]) + "', '" + str(single_data[2]) + "', '" + str(single_data[3]) + "', '" + str(single_data[4]) + "', '" + str(single_data[5]) + "', '" + str(single_data[6]) + "', '" + str(single_data[7]) + "', '" + str(single_data[8]) + "', '" + str(single_data[9]) + "', '" + str(single_data[10]) + "', '" + str(single_data[11]) + "', '" + str(single_data[12])+ "', '"+ str(single_data[13]) + "', '" + str(single_data[14]) + "', '" + str(single_data[15]) +  "', '" + str(single_data[16]) + "', '" + str(single_data[17]) + "', '" + str(single_data[18]) + "', '" + str(single_data[19]) + "');"
            #print(sql)
            cursor.execute(sql)
            transaction.commit_unless_managed(using='report')
    elif cp_type == 20:
        print("西城")
        data=data[1:]
        for single_data in data:
            if len(single_data) != 16:
                if len(single_data) == 1:
                    continue
                msg = single_data[14]
                for i in range(len(single_data)-16):
                    msg += single_data[15+i]
                msg = msg.encode('utf-8')
            else:
                msg = single_data[14]
            sql = "replace into finance_cp_flow_xicheng(`putao_order_no`, `sdk`, `add_time`, `moblie`, `provider`, `district`, `face_value`, `unit_price`, `order_state`, `discount`, `actual_pay`, `response_time`, `error_desc`) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
            #　print sql
            cursor.execute(sql,[str(single_data[2]),str(single_data[3]),str(single_data[4]),str(single_data[5]),str(single_data[6]),str(single_data[7]),
                                str(single_data[8]), str(single_data[9]), str(single_data[10]), str(single_data[11]),
                                str(single_data[12]),str(single_data[13]),str(msg)])
            transaction.commit_unless_managed(using='report')
    else:
        return "cp_type not exsit"

    return "success"


@login_required
@permission_required(u'man.%s' % FinanceConst.FINANCE_EVENT_UPLOAD_CP_BILL, raise_exception=True)
def upload_balance_ajax(request):
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
def refresh_cp_summary(request):
    start_date = request.POST.get("start_date")
    end_date = request.POST.get("end_date")

    try:
        cursor = connections['report'].cursor()
        cursor.execute("CALL `SP_T_LD_RP_D_CASH_SUMMARY_APP`(%s, %s)",
                   [start_date, end_date])
        cursor.execute("CALL `SP_T_LD_RP_D_OPERATION_DATA_SUMMARY_APP`(%s, %s)",
                   [start_date, end_date])
        cursor.execute("CALL `SP_T_LD_RP_D_DAOJIA_OPERATION_DATA_SUMMARY_APP`(%s, %s)",
                   [start_date, end_date])
        cursor.execute("commit")
        return HttpResponse('Update Successfully!')
    except Exception, e:
        return HttpResponse(e)
