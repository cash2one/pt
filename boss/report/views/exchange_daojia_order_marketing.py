#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'putao'
__mtime__ = '1/26/2016'
"""


from report_pub import *

@login_required
@add_common_var
@permission_required(u'man.%s' % ReportConst.BA_TRANSACTION_ANALYSIS_DAOJIA_PRODUCT, raise_exception=True)
def exchange_daojia_order_marketing(request, template_name):
    app = request.GET.get("app")
    report_check_app(request, app)
    vers = get_app_versions(app)
    channels = get_app_channels(app)
    products = get_order_types()
    today = datetime.datetime.now()
    return report_render(request, template_name, {
        "currentdate": get_datestr(0, "%Y-%m-%d"),
        "vers": vers,
        "channels": channels,
        "products": products,
    })

def get_marketing_data(request):
    try:
        data = {}
        start_date = request.POST["start_date"]
        end_date = request.POST["end_date"]
        per_page = int(request.POST.get("per_page",1))
        cur_page = int(request.POST.get("cur_page",1))
        global g_data #返回列表数据
        g_data = []
        cursor = connections['report'].cursor()
        cursor.execute("CALL `pt_biz_report`.`SP_T_RP_D_EXCHANGE_DAOJIA_ORDER_COST` (%s, %s)",[start_date, end_date])
        objs = cursor.fetchall()
        mk_objs = []
        for i in objs:
            mk_objs.append([
                str(i[0]) if i[0] is not None else '',
                str(i[1]),
                str(i[2]),
                str(i[3]),
                str(i[4]),
                str(i[5]),
                str(i[6]),
                str(i[7]),
                str(i[8]),
                str(i[9]),
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
@permission_required(u'man.%s' % ReportConst.BA_TRANSACTION_ANALYSIS_DAOJIA_PRODUCT, raise_exception=True)
def exchange_daojia_order_marketing_ajax(request):
    try:
        data = get_marketing_data(request)
    except Exception as e:
        data = {'code':'-1','msg':e.message}
    return HttpResponse(json.dumps(data))



@login_required
@permission_required(u'man.%s' % ReportConst.BA_TRANSACTION_ANALYSIS_DAOJIA_PRODUCT, raise_exception=True)
def exchange_daojia_order_marketing_csv(request):
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")
    filename = '%s(%s-%s).csv' % ("交易分析-营销费用", str(start_date), str(end_date))
    csv_data = [["CP名称",
                    "新顾客人数",
                    "新顾客成本",
                    "拉新人均成本",
                    "老顾客人数",
                    "老顾客成本",
                    "老顾客人均成本",
                    "优惠券成本",
                    "活动补贴成本",
                    "营销成本总计",
                 ]]
    csv_data.extend(g_data)
    return get_csv_response(filename, csv_data)
