# -*- coding: utf-8 -*-
# Author:wrd
import datetime
import json

import sys
from django.contrib.auth.decorators import login_required, permission_required
from django.db import connection, connections
from django.views.decorators.http import require_http_methods

from common.views import get_csv_response, add_common_var
from report.views.report_pub import ReportConst, add_report_var, report_render, get_datestr, get_invite_table, \
    get_invite_table_b, get_invite_detail, PtHttpResponse, pag, Const


def update_order_info(orders, who):
    # 0 表示邀请人,1表示被邀请人
    try:
        recharge_orders = []
        if who == 0:
            for obj in orders:
                recharge_orders.append(
                    [
                        str(obj[0]),
                        str(obj[1]) if obj[1] and obj[1] is not None else '--',
                        str(obj[2]),
                        str(obj[3]),
                        str(obj[4]),
                        str(obj[5]),
                        obj[6].strftime("%Y-%m-%d %H:%M:%S") if obj[6] and obj[6] is not None else '--',
                    ]
                )
        else:
            for obj in orders:
                recharge_orders.append(
                    [
                        str(obj[0]),
                        str(obj[1]) if obj[1] and obj[1] is not None else '--',
                        obj[2].strftime("%Y-%m-%d %H:%M:%S") if obj[2] and obj[2] is not None else '--',
                        obj[3].strftime("%Y-%m-%d %H:%M:%S") if obj[3] and obj[3] is not None else '--',
                        obj[4].strftime("%Y-%m-%d %H:%M:%S") if obj[4] and obj[4] is not None else '--',
                        str(obj[5]),
                        str(obj[6]) if obj[6] and obj[6] is not None else '--',
                    ]
                )
        if not recharge_orders:
            recharge_orders.append([Const.NONE] * 7)
        return recharge_orders
    except Exception as err:
        raise Exception(err.message)


def update_order_detail_info(orders):
    try:
        recharge_orders = []
        for obj in orders:
            if obj[1] and obj[1] is not None:
                cids = filter_allot_name(obj[1])
            else:
                cids = '--'
            if obj[5] and obj[5] is not None:
                new_cids = filter_allot_name(obj[5])
            else:
                new_cids = '--'
            recharge_orders.append(
                [
                    str(obj[0]),
                    cids,
                    str(obj[2]),
                    obj[3].strftime("%Y-%m-%d %H:%M:%S") if obj[3] and obj[3] is not None else '--',
                    str(obj[4]),
                    new_cids,
                    obj[6].strftime("%Y-%m-%d %H:%M:%S") if obj[6] and obj[6] is not None else '--',
                ]
            )
        if not recharge_orders:
            recharge_orders.append([Const.NONE] * 7)
        return recharge_orders
    except Exception as err:
        raise Exception(err.message)


def filter_allot_name(cids):
    try:
        cursor = connections['activity'].cursor()
        sql = "SELECT name FROM pt_activity_coupon.coupon_allot where id in (" + cids + ");"
        cursor.execute(sql)
        return ','.join([i[0] for i in cursor.fetchall()])
    except Exception as err:
        raise Exception(err.message)


def filter_invite_list(start_date, end_date_d, key, who):
    try:
        if who == 0:
            cursor = connections['activity'].cursor()
            sql = "SELECT i.old_u_id ,u.name,COUNT(DISTINCT i.new_u_id) AS new_user_count ," \
                  "COUNT(DISTINCT d.order_no) AS new_user_order_count" \
                  ",SUM(CASE WHEN d.status = 15 THEN 1 ELSE 0 END) AS new_user_order_finish_count" \
                  ",SUM(IFNULL(ROUND(i.money/100,2),0)) AS old_user_get_money " \
                  ",MAX(i.m_time) AS m_time " \
                  "FROM pt_biz_db.pt_invite_union i " \
                  "LEFT JOIN pt_db.p_relate_user u ON i.old_u_id = u.u_id " \
                  "LEFT JOIN pt_biz_db.pt_daojia_order d ON i.new_u_id = d.pt_u_id  "
            if key:
                sql = sql + "WHERE i.old_u_id  = %s or u.name = %s and (m_time>=%s and m_time<=%s) GROUP BY i.old_u_id,u.name order by m_time desc; "
                cursor.execute(sql, [key, key,start_date,end_date_d])
            else:
                sql += "WHERE m_time>=%s and m_time<=%s GROUP BY i.old_u_id,u.name order by m_time desc; "
                cursor.execute(sql,[start_date,end_date_d])
        else:
            cursor = connections['activity'].cursor()
            sql = "SELECT R1.new_u_id,R1.new_mobile,MIN(R1.c_time) AS c_time,MIN(d.create_time) AS f_order_time," \
                  "MIN(CASE WHEN d.status = 15 THEN d.modify_time END) AS f_finished_order_time," \
                  "SUM(new_user_get_money) AS new_user_get_money,MAX(old_mobile) AS old_mobile " \
                  "FROM (SELECT i.new_u_id,i.new_mobile,i.c_time AS c_time,CAST(t.id AS CHAR) AS c_id,c.id AS coupon_id," \
                  "IFNULL(c.amount,0) AS new_user_get_money,u.name AS old_mobile " \
                  "FROM pt_biz_db.pt_invite_union i " \
                  "LEFT JOIN pt_activity_coupon.coupon_allot t ON find_in_set(t.id,i.new_cids) " \
                  "LEFT JOIN pt_activity_coupon.coupon_resource c  ON t.cid = c.id " \
                  "LEFT JOIN pt_db.p_relate_user u ON i.old_u_id = u.u_id " \

            if key:
                sql += "WHERE i.new_u_id = %s OR i.new_mobile = %s and (i.c_time>=%s and i.c_time<=%s) )R1 " \
                       "LEFT JOIN pt_biz_db.pt_pay_order o ON R1.c_id = o.coupon_ids " \
                        "LEFT JOIN pt_biz_db.pt_daojia_order d ON o.order_no = d.order_no " \
                        "GROUP BY R1.new_u_id,R1.new_mobile;"
                cursor.execute(sql, [key, key,start_date,end_date_d])
            else:
                sql += "WHERE i.c_time>=%s and i.c_time<=%s )R1 " \
                       "LEFT JOIN pt_biz_db.pt_pay_order o ON R1.c_id = o.coupon_ids " \
                        "LEFT JOIN pt_biz_db.pt_daojia_order d ON o.order_no = d.order_no " \
                        "GROUP BY R1.new_u_id,R1.new_mobile;"
                cursor.execute(sql,[start_date,end_date_d])
        return [list(i) for i in cursor.fetchall()]
    except Exception as err:
        raise Exception(err.message)


def get_invite_list(request):
    try:
        re_data = json.loads(request.body.decode('utf-8'))
        per_page = re_data.get("per_page")
        cur_page = re_data.get("cur_page")
        who = int(re_data.get("who"))
        start_date = re_data.get("start_date")
        end_date = re_data.get("end_date")
        end_date_d = datetime.datetime.strptime(end_date, "%Y-%m-%d") + datetime.timedelta(days=1) \
            if end_date is not None else ''
        key = re_data.get("key")
        key = key.strip(' ')
        key = key.strip('\t')
        orders = filter_invite_list(start_date, end_date_d, key, who)
        global csv_da
        csv_da = []
        csv_da = orders
        orders, num_pages = pag(orders, per_page, cur_page)
        result = update_order_info(orders, who)
        return [result, num_pages]
    except Exception as err:
        raise Exception(err.message)


def cursor_data(ptuid):
    try:
        cursor = connections['activity'].cursor()
        sql = "SELECT i.old_u_id,i.cids,SUM(IFNULL(amount, 0)) AS old_user_coupon_amount," \
              "CASE WHEN i.status = 'SUCCESS' THEN i.m_time END AS old_user_get_coupon_time,i.new_mobile,i.new_cids, " \
              "i.c_time AS new_user_get_coupon_time " \
              "FROM pt_biz_db.pt_invite_union i " \
              "LEFT JOIN pt_activity_coupon.coupon_allot t ON FIND_IN_SET(t.id, i.cids) " \
              "LEFT JOIN pt_activity_coupon.coupon_resource c ON t.cid = c.id " \
              "LEFT JOIN pt_db.p_relate_user u ON i.old_u_id = u.u_id " \
              "WHERE old_u_id = %s GROUP BY i.id;"
        cursor.execute(sql, [ptuid])
        return [list(i) for i in cursor.fetchall()]
    except Exception as err:
        raise Exception(err.message)


def get_invite_detail_list(request):
    try:
        re_data = json.loads(request.body.decode('utf-8'))
        per_page = re_data.get("per_page")
        cur_page = re_data.get("cur_page")
        ptuid = re_data.get("pt_uid")
        orders = cursor_data(ptuid)
        orders, num_pages = pag(orders, per_page, cur_page)
        result = update_order_detail_info(orders)
        return [result, num_pages]
    except Exception as err:
        raise Exception(err.message)


@login_required
@permission_required(u'man.%s' % ReportConst.INVITE_BUSINESS_ANALY, raise_exception=True)
@add_common_var
def invite_index(request, template_name, who):
    """
    显示首页
    :param request:
    :param template_name:
    :param who:0表示邀请人,1表示被邀请人
    :return:
    """
    if who == '0':
        invite_table = get_invite_table()
    elif who == '1':
        invite_table = get_invite_table_b()
    else:
        return PtHttpResponse({'msg': 'no this who', 'code': 1})
    return report_render(request, template_name,
                         {"currentdate": get_datestr(0, "%Y-%m-%d"),
                          'invite_table': invite_table,
                          'who': who,
                          })


@login_required
@permission_required(u'man.%s' % ReportConst.INVITE_BUSINESS_ANALY, raise_exception=True)
@add_common_var
def invite_detail(request, template_name):
    """
    显示详情
    :param request:
    :param template_name:
    :return:
    """
    pt_uid = request.GET.get('pt_uid')
    invite_detail_table = get_invite_detail()
    return report_render(request, template_name,
                         {'invite_detail_table': invite_detail_table, 'pt_uid': pt_uid})


@login_required
@permission_required(u'man.%s' % ReportConst.INVITE_BUSINESS_ANALY, raise_exception=True)
@require_http_methods(['POST'])
def invite_list(request):
    if request.method == 'POST':
        try:
            data = get_invite_list(request)
            return PtHttpResponse(data)
        except Exception as err:
            return PtHttpResponse({'msg': err.message, 'code': 1})
    return PtHttpResponse({'msg': u'错误方法', 'code': 1})


@login_required
@permission_required(u'man.%s' % ReportConst.INVITE_BUSINESS_ANALY, raise_exception=True)
@require_http_methods(['POST'])
def invite_detail_list(request):
    if request.method == 'POST':
        try:
            data = get_invite_detail_list(request)
            return PtHttpResponse(data)
        except Exception as err:
            return PtHttpResponse({'msg': err.message, 'code': 1})
    return PtHttpResponse({'msg': u'错误方法', 'code': 1})


@login_required
@permission_required(u'man.%s' % ReportConst.INVITE_BUSINESS_ANALY, raise_exception=True)
def invite_csv(request):
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")
    key = request.GET.get("key")
    key = key.strip(' ')
    key = key.strip('\t')
    whos = request.GET.get("who")
    end_date_d = datetime.datetime.strptime(end_date, "%Y-%m-%d") + datetime.timedelta(days=1)
    # csv_da = filter_invite_list(start_date, end_date_d, key, int(whos))
    if whos == '0':
        who = '邀请人'
        csv_data = [["PTUID",
                 "用户手机号",
                 "邀请注册成功人数",
                 "首单下单成功人数",
                 "首单服务完成人数",
                 "获券总额",
                 "修改时间",
                ]]
    elif whos == '1':
        who = '被邀请人'
        csv_data = [["PTUID",
                     "被邀请人手机号",
                     "获券/注册时间",
                     "首单下单成功时间",
                     "首单服务完成时间",
                     "获券总额",
                     "邀请人手机号"]]
    else:
        return
    filename = '%s%s(%s-%s).csv' % (str(who),str(key), str(start_date), str(end_date))
    csv_data.extend(csv_da)
    return get_csv_response(filename, csv_data)


@login_required
@permission_required(u'man.%s' % ReportConst.INVITE_BUSINESS_ANALY, raise_exception=True)
def invite_detail_csv(request):
    ptuid = request.GET.get("pt_uid")
    csv_d = cursor_data(ptuid)
    csv_data = [["PTUID",
                 "邀请人获券",
                 "被邀请人获券面值",
                 "被邀人获券时间",
                 "被邀人手机号",
                 "被邀人获券",
                 "被邀人获券时间"]]
    filename = '邀请人详情(%s).csv' % (str(ptuid))
    csv_data.extend(csv_d)
    return get_csv_response(filename, csv_data)
