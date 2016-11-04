#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'putao'
__mtime__ = '1/26/2016'
"""
import json

from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator
from django.db import connections
from django.http import HttpResponse

from common.views import add_common_var, get_datestr, get_csv_response
from finance.views.finance_pub import FinanceConst
from main.views.main_pub import report_render
from order.views.order_pub import get_full_cp_names

@login_required
@add_common_var
@permission_required(u'man.%s' % FinanceConst.FINANCE_DETAIL_DAOJIA_COUPON, raise_exception=True)
def daojia_coupon_detail(request, template_name):
    cps = get_full_cp_names()
    return report_render(request, template_name, {
        "currentdate": get_datestr(0, "%Y-%m-%d"),
        'cps':cps,
    })

def get_marketing_data(request):
    try:
        data = {}
        start_date = request.POST["start_date"]
        end_date = request.POST["end_date"]
        per_page = int(request.POST.get("per_page",1))
        cur_page = int(request.POST.get("cur_page",1))
        cp_id = request.POST.get("cp_id") if request.POST.get("cp_id") else None
        global g_data #返回列表数据
        g_data = []
        cursor = connections['report'].cursor()
        cursor.execute("CALL `pt_biz_report`.`SP_T_RP_D_OPERATION_COST_COUPON_DETAIL` (%s, %s, %s)",[start_date, end_date,cp_id])
        objs = cursor.fetchall()
        mk_objs = []
        for i in objs:
            mk_objs.append([
                str(i[0]) if i[0] is not None else '--',
                str(i[1]),
                str(i[2]),
                str(i[3]),
                str(i[4]),
                str(i[5]) if i[5] is not None else '--',
                str(i[6]),
                str(i[7]) if i[7] is not None else '--',
            ])
        g_data = mk_objs
        p = Paginator(mk_objs, per_page)
        num_pags = p.num_pages
        if cur_page > num_pags:
            return {'code': '-1', 'msg': '页数太大'}
        r_data = p.page(cur_page)
        data['data'] = r_data.object_list
        data['page'] = num_pags
        data['code'] = '0'
        return data
    except Exception as e:
        return {'code':'-1','msg':e.message}

@login_required
@permission_required(u'man.%s' % FinanceConst.FINANCE_DETAIL_DAOJIA_COUPON, raise_exception=True)
def daojia_coupon_detail_ajax(request):
    try:
        data = get_marketing_data(request)
    except Exception as e:
        data = {'code':'-1','msg':e.message}
    return HttpResponse(json.dumps(data))



@login_required
@permission_required(u'man.%s' % FinanceConst.FINANCE_DETAIL_DAOJIA_COUPON, raise_exception=True)
def daojia_coupon_detail_csv(request):
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")
    filename = '%s(%s-%s).csv' % ("到家优惠券明细", str(start_date), str(end_date))
    csv_data = [[   "CP名称",
                    "CP_ID",
                    "订单号",
                    "优惠券编号",
                    "活动名称",
                    "优惠券实耗",
                    "葡萄承担成本",
                    "CP承担成本",
                 ]]
    csv_data.extend(g_data)
    return get_csv_response(filename, csv_data)
