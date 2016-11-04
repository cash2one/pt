#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'putao'
__mtime__ = '1/26/2016'
"""
from django.views.decorators.csrf import csrf_exempt

from report_pub import *

g_data =[]

@login_required
@add_common_var
def exchange_daojia_order(request, template_name):
    app = request.GET.get("app")
    report_check_app(request, app)
    vers = get_app_versions(app)
    channels = get_app_channels(app)
    products = get_order_types()
    citys = get_citys
    today = datetime.datetime.now()
    cursor = connections['order'].cursor()
    cursor.execute("call `SP_T_RP_D_TURNOVER_DAOJIA_PRODUCT_SUMMARY`(%s, %s, %s, %s, %s, %s)",
                    [get_datestr(1, "%Y-%m-%d"),today.strftime("%Y-%m-%d"), None, None, None, 4])
    objs = cursor.fetchall()
    summary = []
    for obj in objs:
        summary.append([
            str(obj[0]),#statdate
            str(obj[1]),#new_order_count
            str(obj[2]),#real_order_count
            str(obj[3]),#order_pay_price
            str(obj[4]),#total_user_count
            str(obj[5]),#total_complain_count
            str(obj[6]),#total_order_count
        ])
    return report_render(request, template_name, {
        "currentdate": get_datestr(0, "%Y-%m-%d"),
        "vers": vers,
        "channels": channels,
        "products": products,
        "summary": summary,
        "citys":citys,
    })

def exchange_daojia_order_summaries(request):
    ot, app, ver, channel = get_app_ver_channel(request)
    today_summary = []
    last_summary_result = []
    today = datetime.datetime.now()
    summary = TongjiRpDTurnoverSummary.objects.filter(app_id=app, app_version=ver,
    channel_no=channel,product_type=ot, stathour='PLUS99', statdate=today.strftime("%Y-%m-%d"))
    if summary:
        summary = summary[0]
        today_summary.append(str(summary.total_order_count))  #交易数
        today_summary.append(str(summary.total_prod_price))   #交易额
        today_summary.append(str(summary.total_user_count))   #用户数
        today_summary.append(str(summary.total_coupon_count)) #用券数
        today_summary.append(str(summary.total_coupon_cost))  #用券额
        today_summary.append(str(summary.total_coupon_bring_order)) #券带动消费金额
        today_summary.append(str(summary.coupon_use_ratio))    #交易占比
    else:
        today_summary =[0,0,0,0,0,0,0]
    last_summary = TongjiRpDTurnoverSummary.objects.filter(app_id=app, app_version=ver,
    channel_no=channel, product_type=ot, stathour='PLUS99', statdate=get_datestr(1,"%Y-%m-%d"))
    if last_summary:
        last_summary = last_summary[0]
        last_summary_result.append(str(last_summary.total_order_count))
        last_summary_result.append(str(last_summary.total_prod_price))
        last_summary_result.append(str(last_summary.total_user_count))
    else:
        last_summary_result =[0,0,0]
    return HttpResponse(json.dumps([today_summary,last_summary_result]))


def get_exchange_daojia_order_table_data(request):
    today = datetime.datetime.now()
    start_date = request.POST["start_date"]
    end_date = request.POST["end_date"]
    table_type = request.POST["show_table_type"]
    citys_select = request.POST.get("citys_select") if request.POST.get("citys_select") !='0' else None
    ot, app, ver, channel = get_app_ver_channel(request)
    category_info = get_daojia_goods_category()
    global g_data #返回列表数据
    g_data = []
    cat_data = {}
    cursor = connections['order'].cursor()
    cursor.execute("call `SP_T_RP_D_TURNOVER_DAOJIA_PRODUCT_SUMMARY_CITY`(%s, %s, %s, %s, %s, %s, %s)",
                    [start_date, end_date,citys_select, channel, ver, app, table_type])
    objs = cursor.fetchall()
    for obj in objs:
        data = []
        cg_name = "未获取分类信息"
        if table_type == u"1":
            for cg in category_info:
                if cg[0] == str(obj[0]):
                    print cg[0],obj[0]
                    cg_name = cg[1]
                    break
            data = [
                cg_name,#app_id
                str(obj[1]),#cp_name
                obj[2],#order_count
                str(obj[3]),#order_pay_price
                str(obj[18]),#user_pay_price
                str(obj[19]),#avg_user_pay_price
                str(obj[5]),#total_user_count
                str(obj[17]),#new_user_count
                str(obj[20]),#new_user_rate
                str(obj[21]),#old_user_rate
                str(obj[22]),#cancel_order_rate
                str(obj[7]),#test_order_count
                str(obj[8])+' / '+str(obj[9]),#wait_confirm_order_count / wait_pay_order_count
                str(obj[10])+' / '+str(obj[11]),#cancel_order_count / refund_order_count
                str(obj[12]),#processing_order_count
                str(obj[13]),#success_order_count
                str(obj[14]),#complain_order_count
            ]
        if table_type == u"5":
            for cg in category_info:
                if cg[0] == str(obj[0]):
                    if not cat_data.has_key(cg[1]):
                        data = [
                            obj[2],  # order_count
                            obj[3],  # order_pay_price
                            obj[5],  # total_user_count
                            obj[17],  # new_user_count
                            obj[7],  # test_order_count
                            obj[8],  # wait_confirm_order_count
                            obj[9],  # wait_pay_order_count
                            obj[10], # cancel_order_count
                            obj[11], # refund_order_count
                            obj[12], # processing_order_count
                            obj[13], # success_order_count
                            obj[14], # complain_order_count
                            obj[18],  # user_pay_price

                        ]
                        cat_data[cg[1]] = data
                    else:
                        cat_data[cg[1]][0] += obj[2]
                        cat_data[cg[1]][1] += obj[3]
                        cat_data[cg[1]][2] += obj[5]
                        cat_data[cg[1]][3] += obj[17]
                        cat_data[cg[1]][4] += obj[7]
                        cat_data[cg[1]][5] += obj[8]
                        cat_data[cg[1]][6] += obj[9]
                        cat_data[cg[1]][7] += obj[10]
                        cat_data[cg[1]][8] += obj[11]
                        cat_data[cg[1]][9] += obj[12]
                        cat_data[cg[1]][10] += obj[13]
                        cat_data[cg[1]][12] += obj[18]
                    break
        if table_type == u"2":
            for cg in category_info:
                if cg[0] == str(obj[0]):
                    data = [
                        str(cg[1]),
                        str(cg[2]),
                        str(cg[3]),
                        str(cg[4]),
                        str(cg[5]),
                        str(cg[6]),
                        str(obj[15]),
                        str(obj[16]),
                        "未知",
                    ]
                    break
        if data:
            data.append("详情")
            g_data.append(
                data
            )
    if not g_data:
        if table_type == u"1":
            g_data.append([Const.NONE] * 13)
        if table_type == u"5":
            g_data.append([Const.NONE] * 12)
        if table_type == u"2":
            g_data.append([Const.NONE] * 10)
    elif table_type == u"5":
        g_data = []
        for key, value in cat_data.iteritems():
            g_data.append([
                key,
                value[0],#order_count
                str(value[1]),#order_pay_price
                str(value[12]),#order_pay_price
                str(value[2]),#total_user_count
                str(value[3]),#new_user_count
                str(value[4]),#test_order_count
                str(value[5])+' / '+str(value[6]),#wait_confirm_order_count / wait_pay_order_count
                str(value[7])+' / '+str(value[8]),#cancel_order_count / refund_order_count
                str(value[9]),#processing_order_count
                str(value[10]),#success_order_count
                str(value[11]),#complain_order_count
                "详情",
            ])
        g_data.sort(key=lambda o: o[1], reverse=True)
    else:
        g_data.sort(key=lambda o: o[2], reverse=True)
    return HttpResponse(json.dumps(g_data))



def get_app_ver_channel(request):
    ot = request.POST.get("ot")
    if not ot:
        ot = None
    app = request.POST.get("app")
    report_check_app(request, app)
    if not app:
        app = None
    ver = request.POST.get("ver") #数据有问题
    if not ver:
        ver = None
    channel = request.POST.get("channel")
    if not channel:
        channel = None
    return ot, app, ver, channel


@login_required
# @permission_required(u'man.%s' % ReportConst.ORDER_REPORTS, raise_exception=True)
def exchange_daojia_order_reports_csv(request):
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")
    table_type = request.GET.get("table_type")
    csv_data = []
    filename = '%s(%s-%s).csv' % ("交易分析", str(start_date), str(end_date))
    if table_type == u"1":
        csv_data = [["分类",
                    "服务商名称",
                    "订单总量",
                    "订单销售金额",
                    "订单实付金额",
                    "订单实付均价(客单价)",
                    "交易用户数",
                    "新用户数",
                    "新客占比(首购率)",
                    "老客占比(复购率)",
                    "取消占比",
                    "测试订单数",
                    "待接单 / 待支付订单",
                    "取消 / 退款订单",
                    "进行中订单",
                    "完成订单",
                    "投诉订单",
                    "操作"]]
    elif table_type == u"5":
        csv_data = [["分类",
                    "订单总量",
                    "订单销售金额",
                    "订单实付金额",
                    "交易用户数",
                    "新用户数",
                    "测试订单数",
                    "待接单 / 待支付订单",
                    "取消 / 退款订单",
                    "进行中订单",
                    "完成订单",
                    "投诉订单",
                    "操作"]]
    elif table_type == u"2":
        csv_data = [["分类",
                    "服务商名称",
                    "接入CP数量	",
                    "接入商品数量",
                    "覆盖城市",
                    "平均单价",
                    "接单速度(分)",
                    "服务完成速度(分)",
                    "满意度	",
                    "操作"]]
    csv_data.extend(g_data)
    return get_csv_response(filename, csv_data)


def get_daojia_goods_category():
   cms_cursor = connections['cms'].cursor()
   cms_cursor.execute("""SELECT g.appId
                            ,CASE WHEN c.`name` IS NULL
                                  THEN '未获取分类信息'
                                  ELSE c.`name`
		                      END AS category_name
                            ,g.cp_name
                            ,1 AS cp_count
                            ,g.cp_goods_count
                            ,g.citys
                            ,g.avg_good_price
                      FROM(
                             SELECT cms_goods.new_category as category_id
                                    ,MAX(cms_goods.cp_name) as cp_name
                                    ,cms_goods.open_service_id as appId
                                    ,MAX(cms_goods.city) as citys
                                    ,ROUND(AVG(cms_goods.price),2) as avg_good_price
                                    ,COUNT(DISTINCT cms_goods.goods_id) as cp_goods_count
                             FROM pt_cms_db.cms_goods
                             WHERE cms_goods.new_category IS NOT NULL
                               AND cms_goods.goods_id > 0
                             GROUP BY cms_goods.open_service_id

                             UNION ALL

							 SELECT cms_goods.new_category as category_id
                                    ,MAX(cms_goods.cp_name) as cp_name
                                    ,cms_goods.open_service_id as appId
                                    ,MAX(cms_goods.city) as citys
                                    ,ROUND(AVG(cms_goods.price),2) as avg_good_price
                                    ,COUNT(DISTINCT cms_goods.goods_id) as cp_goods_count
                             FROM pt_cms_db.cms_goods
                             GROUP BY cms_goods.open_service_id
							 HAVING SUM(IFNULL(new_category,0))=0
                      ) g
                      LEFT JOIN pt_cms_db.cms_navi_category AS c
                             ON g.category_id = c.id""")
   goods = cms_cursor.fetchall()
   category_info = []
   for obj in goods:
       category_info.append([
           str(obj[0]),
           str(obj[1]),
           str(obj[2]),
           str(obj[3]),
           str(obj[4]),
           str(obj[5]),
           str(obj[6]),
       ])
   if not category_info:
      category_info.append([Const.NONE] * 7)
   return category_info


def get_every_order(cur_page=1, limit_page=30, all=False, rp_type=1, start_date=None, end_date=None):
    data = {}
    cursor = connections['report'].cursor()
    cursor.execute("call `SP_T_RP_D_EXCHANGE_DAOJIA_ORDER_PERIOD_SUMMARY`(%s, %s, %s)",
                   [start_date, end_date, rp_type])
    evedata = cursor.fetchall()
    if all:
        p_data = evedata
    else:
        p = Paginator(evedata, limit_page)
        num_pags = p.num_pages
        p_data = p.page(cur_page)
        data['page'] = num_pags
        data['code'] = '0'
    every_order = []
    for i in p_data:
        if rp_type == u"1":
            every_order.append([
                str(i[0]) if i[0] is not None else '--',
                str(i[1]) if i[1] is not None else '--',
                str(i[2]) if i[2] is not None else '--',
                str(i[3]) if i[3] is not None else '--',
                float(i[4]) if i[4] is not None and i[4] else '--',
                str(i[5]) if i[5] is not None else '--',
                str(i[6]) if i[6] is not None else '--',
                str(i[7]) if i[7] is not None else '--',
            ])
        if rp_type == u"2":
            every_order.append([
                str(i[0]) if i[0] is not None else '--',
                str(i[1]) if i[1] is not None else '--',
                str(i[2]) if i[2] is not None else '--',
                float(i[3]) if i[3] is not None and i[3] else '--',
                str(i[4]) if i[4] is not None else '--',
                str(i[5]) if i[5] is not None else '--',
            ])
    data['data'] = every_order
    data['code'] = '0'
    print "finish!!!!!!"
    return data

@login_required()
# @csrf_exempt
def exchange_daojia_order_evemonth(request):
    try:
        cur_page = int(request.POST.get('cur_page',1))
        limit_page = int(request.POST.get('limit_page',30))
        start_date = request.POST["start_date"]
        end_date = request.POST["end_date"]
        table_type = request.POST["show_time_table_type"]
        print start_date,end_date,table_type
        data = get_every_order(cur_page, limit_page, rp_type=table_type, start_date=start_date, end_date=end_date)
    except Exception as e:
        data = {'code':'-1','msg':e.message}
    return HttpResponse(json.dumps(data))

@login_required()
# @csrf_exempt
def exchange_daojia_order_evemonth_csv(request):
    csv = get_every_order(all=True)['data']
    name = "到家每月交易分析".encode('utf-8')
    filename = '%s.csv' % (name)
    csv_data = [["年",
                 "月",
                 "总订单量",
                 "总下单用户",
                 "客单价",
                 "首单率",
                 "复购率",
                 "新用户复购率",
                 ]]
    csv_data.extend(csv)
    return get_csv_response(filename, csv_data)
