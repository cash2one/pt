# -*- coding: utf-8 -*-
# Author:wrd
import datetime
import json
from itertools import chain
from django.contrib.auth.decorators import login_required, permission_required
from django.db import connections
from django.views.decorators.http import require_http_methods

from common.views import get_csv_response, add_common_var
from order.models import CouponAllot, CouponResource, PtPayOrder
from order.views.order_pub import get_coupons_table_columns, pag, Const
from report.models import VwPtAppVersionFilter, VwPtAppChannelNoFilter
from report.views.report_pub import add_report_var, ReportConst, report_render, get_datestr, PtHttpResponse, \
    get_app_versions, get_app_channels


def update_order_info(orders, cur_page, per_page):
    recharge_orders = []
    try:
        for obj in orders:
            if obj[10] == 0:
                money = str(obj[9] / 100) + '元'
            else:
                money = str(obj[9]) + 'M'
            recharge_orders.append(
                [
                    str(obj[0]),
                    str(obj[1]),
                    str(obj[2]) if obj[2] and obj[2] is not None else '--',
                    str(obj[3]),
                    str(obj[8]) if obj[8] and obj[8] is not None else '--',
                    money,
                    str(obj[11]) if obj[11] and obj[11] is not None else '--',
                    str(obj[12]) if obj[12] and obj[12] is not None else '--',
                    str(obj[4]) if obj[4] and obj[4] is not None else '--',
                    obj[5].strftime("%Y-%m-%d %H:%M:%S") if obj[5] else '--',
                    obj[6].strftime("%Y-%m-%d %H:%M:%S") if obj[6] else '--',
                    obj[7].strftime("%Y-%m-%d %H:%M:%S") if obj[7] and obj[7] is not None else '--',
                    str(obj[14]) if obj[14] and obj[14] is not None else '--',
                    str(obj[13]) if obj[13] and obj[13] is not None else '--',
                ]
            )
    except Exception as e:
        pass
    if not recharge_orders:
        recharge_orders.append([Const.NONE] * 14)
    return recharge_orders


def show_selected_columns(result, selected_columns):
    coupon_table_columns = get_coupons_table_columns()
    show_columns = []
    show_result = []
    row = []
    for col in selected_columns:
        for d_col in coupon_table_columns:
            if col == d_col[1]:
                show_columns.append(d_col[0])
    for obj in result:
        for s_col in show_columns:
            row.append(obj[s_col])
        show_result.append(row)
        row = []
    return show_result


# def filter_coupons_list(app_channel,app_version,start_date,end_date_d,mobile='',ptuid=''):
#     try:
#         if mobile:
#             couponallot = list(CouponAllot.objects.using('activity').filter(allot_time__gte=start_date,allot_time__lte=end_date_d,mobile=mobile)\
#                 .values_list('id','uid','mobile','cid','activity_name','allot_time','end_time','consume_time'))
#         elif ptuid:
#             couponallot = list(CouponAllot.objects.using('activity').filter(allot_time__gte=start_date, allot_time__lte=end_date_d,uid=ptuid) \
#                 .values_list('id', 'uid', 'mobile', 'cid', 'activity_name', 'allot_time', 'consume_time', 'end_time'))
#         else:
#             return []
#         couponresourse = [CouponResource.objects.using('activity').filter(id=i[3])
#                               .values_list('name','amount','biz_type','consume_remark','remark') for i in couponallot]
#         ptpayorder = [PtPayOrder.objects.using('order')
#                         .filter(coupon_ids=i[0])
#                         .values_list('name') for i in couponallot]
#         filter_data =[]
#         for i in range(len(couponallot)):
#             ca = list(couponallot[i])
#             cs = list(couponresourse[i][0])
#             po = list(ptpayorder[i][0]) if ptpayorder[i] else ['']
#             filter_data.append(ca+cs+po)
#
#         return filter_data
#     except Exception as e:
#         return []
#
def filter_coupons_list(app_channel, app_version, start_date, end_date_d,key):
    try:
        cursor = connections['activity'].cursor()
        sql = "SELECT " \
              "a.id AS id,a.uid AS uid,a.mobile AS mobile,a.cid AS cid,a.activity_name AS activity_name,a.allot_time as allot_time,a.end_time as end_time,a.consume_time as consume_time," \
              "b.name AS name,b.amount AS amount,b.biz_type as biz_type,b.consume_remark as consume_remark,b.remark as remark," \
              "c.name AS name,c.order_no " \
              "FROM pt_activity_coupon.coupon_allot AS a " \
              "LEFT JOIN pt_activity_coupon.coupon_resource AS b ON a.cid = b.id " \
              "LEFT JOIN pt_biz_db.pt_pay_order AS c ON CAST(a.id AS CHAR) = c.coupon_ids " \
              "WHERE (a.mobile = %s or a.uid = %s) and a.allot_time >= %s and a.allot_time <= %s;"
        cursor.execute(sql,[key,key,start_date,end_date_d])
        return [list(i) for i in cursor.fetchall()]
    except Exception as e:
        return []


def get_coupons_list(request):
    per_page = request.POST.get("per_page")
    cur_page = request.POST.get("cur_page")
    app_version = json.loads(request.POST.get('app_version')) if request.POST.get('app_version') else []
    app_channel = json.loads(request.POST.get('app_channel')) if request.POST.get('app_channel') else []
    start_date = request.POST.get("start_date")
    end_date = request.POST.get("end_date")
    selected_columns = request.POST.getlist("daojia_table[]")
    end_date_d = datetime.datetime.strptime(end_date, "%Y-%m-%d") + datetime.timedelta(days=1)
    key = request.POST.get("key")
    # 获取订单列表下载信息
    global g_data
    g_data = []
    if key == u'' or key is None:
        return [[[Const.NONE] * 14], 1]
    key = key.strip(' ')
    key = key.strip('\t')
    orders = filter_coupons_list(app_channel, app_version, start_date, end_date_d,key)
    g_data = update_order_info(orders, 0, 0)

    # 列表展示信息
    orders, num_pages = pag(orders, per_page, cur_page)
    result = update_order_info(orders, int(cur_page), int(per_page))

    # 仅展示被选中的列表信息
    # show_result = show_selected_columns(result, selected_columns)
    return [result, num_pages]


@login_required
@permission_required(u'man.%s' % ReportConst.ORDER_COUPONS_QUERY, raise_exception=True)
@add_common_var
def order_coupons_query_info(request, template_name):
    """
    显示首页
    :param request:
    :param template_name:
    :return:
    """
    app_id = request.GET.get('app', '')
    coupons_table_columns = get_coupons_table_columns()
    if not app_id:
        apps_version = reduce(lambda x, y: list(set(x + y)), list(
            map(lambda x: list(x), VwPtAppVersionFilter.objects.using('default').values_list('app_version'))))
        apps_channel = reduce(lambda x, y: list(set(x + y)), list(
            map(lambda x: list(x), VwPtAppChannelNoFilter.objects.using('default').values_list('channel_no'))))
    else:
        apps_version = get_app_versions(app_id)
        apps_channel = get_app_channels(app_id)
    return report_render(request, template_name,
                         {"currentdate": get_datestr(0, "%Y-%m-%d"),
                          'apps_version': apps_version,
                          'apps_channel': apps_channel,
                          'coupons_table_columns': coupons_table_columns,
                          })


@require_http_methods(['POST'])
@login_required
@permission_required(u'man.%s' % ReportConst.ORDER_COUPONS_QUERY, raise_exception=True)
def order_coupons_query_list(request):
    """
    获取所有优惠券list
    :param request:
    :return:
    """
    if request.method == 'POST':
        data = get_coupons_list(request)
        return PtHttpResponse(data)
    return PtHttpResponse({'msg': u'错误方法', 'code': 1})


@require_http_methods(['GET'])
@login_required
@permission_required(u'man.%s' % ReportConst.ORDER_COUPONS_QUERY, raise_exception=True)
def order_coupons_query_csv(request):
    """
    获取csv
    :param request:
    :return:
    """
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")
    key = request.GET.get("key")
    csv_data = [["ID",
                 "PTUID",
                 "用户手机号",
                 "优惠券ID",
                 "优惠券名称",
                 "面额",
                 "使用限制",
                 "使用说明",
                 "参与活动",
                 "优惠券领取时间",
                 "优惠券截止日期",
                 "优惠券使用时间",
                 "订单号",
                 "优惠券使用商品名称"]]
    filename = '优惠券列表%s(%s-%s).csv' % (str(key),str(start_date),str(end_date))
    csv_data.extend(g_data)
    return get_csv_response(filename, csv_data)
