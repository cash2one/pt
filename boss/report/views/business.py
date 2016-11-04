#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'putao'
__mtime__ = '1/26/2016'
"""


from report_pub import *
from django.db.models import Sum

g_data =[]

@login_required
@add_common_var
def bussiness_summary(request, template_name):
    app = request.GET.get("app")
    report_check_app(request, app)
    vers = get_app_versions(app)
    channels = get_app_channels(app)
    products = get_order_types()
    today = datetime.datetime.now()
    if not app:
        app = 'PLUS99'
    summary = TongjiRpDTurnoverBusinessSummary.objects.filter(app_id=app, app_version='PLUS99',
    channel_no='PLUS99', product_type='PLUS99', statdate=today.strftime("%Y-%m-%d"))
    if summary:
        summary = summary[0]
    last_summary = TongjiRpDTurnoverBusinessSummary.objects.filter(app_id=app, app_version='PLUS99',
    channel_no='PLUS99', product_type='PLUS99', statdate=get_datestr(1,"%Y-%m-%d"))
    if last_summary:
        last_summary = last_summary[0]
    print(today.strftime("%Y-%m-%d"))
    return report_render(request, template_name, {
        "currentdate": today.strftime("%Y-%m-%d"),
        "vers": vers,
        "channels": channels,
        "products": products,
        "summary": summary,
        "last_summary": last_summary
    })


def search_bussiness_summary(request):
    ot, app, ver, channel = get_app_ver_channel(request)
    today_summary = []
    last_summary_result = []
    today = datetime.datetime.now()
    summary = TongjiRpDTurnoverBusinessSummary.objects.filter(app_id=app, app_version=ver,
    channel_no=channel,product_type=ot, statdate=today.strftime("%Y-%m-%d"))
    if summary:
        summary = summary[0]
        today_summary.append(str(summary.total_order_count))  #订单总数
        today_summary.append(str(summary.total_pay_price))   #今日交易单数
        today_summary.append(str(summary.total_user_count))   #今日交易用户数
        today_summary.append(str(summary.avg_user_order_count)) #今日人均笔数
        today_summary.append(str(summary.avg_order_pay))  #今日客单价
        today_summary.append(str(summary.arpu)) #今日ARPU值
    else:
        today_summary =[0, 0, 0, 0, 0, 0, 0]
    last_summary = TongjiRpDTurnoverBusinessSummary.objects.filter(app_id=app, app_version=ver,
    channel_no=channel, product_type=ot, statdate=get_datestr(1,"%Y-%m-%d"))
    if last_summary:
        last_summary = last_summary[0]
        last_summary_result.append(str(last_summary.total_order_count))  #订单总数
        last_summary_result.append(str(last_summary.total_pay_price))   #今日交易单数
        last_summary_result.append(str(last_summary.total_user_count))   #今日交易用户数
        last_summary_result.append(str(last_summary.avg_user_order_count)) #今日人均笔数
        last_summary_result.append(str(last_summary.avg_order_pay))  #今日客单价
        last_summary_result.append(str(last_summary.arpu)) #今日ARPU值
    else:
        last_summary_result =[0, 0, 0, 0, 0, 0, 0]
    return HttpResponse(json.dumps([today_summary,last_summary_result]))


def get_bussiness_line_data(request):
    today = datetime.datetime.now()
    start_date = request.POST["start_date"]
    end_date = request.POST["end_date"]
    ot, app, ver, channel = get_app_ver_channel(request)
    total_order_count_result = []      #订单总数
    total_pay_price_result = []        #订单总金额
    total_user_count_result = []       #用户数
    avg_user_order_count_result = []   #人均笔数
    avg_order_pay_result=[]            #客单价
    arpu_result = []                   #ARPU
    global g_data #返回列表数据
    g_data = []
    x_axis = []
    result=[]
    not_show = []
    if start_date and end_date and start_date != end_date:
        pass
    else:
        start_date = get_datestr(60, "%Y-%m-%d")
        end_date = today.strftime("%Y-%m-%d")
    if not request.POST.get("type"):
        summaries = TongjiRpDTurnoverBusinessSummary.objects.filter(app_id=app, app_version=ver,
        channel_no=channel, product_type=ot, statdate__gte=start_date, statdate__lte=end_date)
        for summary in summaries:
            total_order_count_result.append(int(summary.total_order_count))
            total_pay_price_result.append(float(summary.total_pay_price))
            total_user_count_result.append(int(summary.total_user_count))
            avg_user_order_count_result.append(float(summary.avg_user_order_count))
            avg_order_pay_result.append(float(summary.avg_order_pay))
            arpu_result.append(float(summary.arpu))
            g_data.append([summary.statdate.strftime("%Y-%m-%d"), int(summary.total_order_count),
                           float(summary.total_pay_price), int(summary.total_user_count),
                           str(summary.avg_user_order_count),
                           float(summary.avg_order_pay), float(summary.arpu)])
            x_axis.append(summary.statdate.strftime("%Y-%m-%d"))
        result.append({"data":total_order_count_result,"type":"line","name":"订单总数"})
        result.append({"data":total_pay_price_result,"type":"line","name":"订单总金额"})
        result.append({"data":total_user_count_result,"type":"line","name":"用户数"})
        result.append({"data":avg_user_order_count_result,"type":"line","name":"人均笔数"})
        result.append({"data":avg_order_pay_result,"type":"line","name":"客单价"})
        result.append({"data":arpu_result,"type":"line","name":"ARPU"})
        not_show = ["订单总数","订单总金额","用户数","人均笔数"]
        x_axis = sorted(x_axis)
    else:
        x_axis, result = get_channel_summary(app,request.POST.get("type"),start_date, end_date)
    return HttpResponse(json.dumps([result, x_axis, not_show, g_data]))


def get_channel_summary(app, type, start_date, end_date):
    x_axis = []
    total_order_count_result = []      #订单总数
    total_pay_price_result = []        #订单总金额
    total_user_count_result = []       #用户数
    avg_user_order_count_result = []   #人均笔数
    avg_order_pay_result=[]            #客单价
    arpu_result = []                   #ARPU
    business_sumamries = TongjiRpDTurnoverBusinessSummary.objects.filter(app_id=app,statdate__gte=start_date, statdate__lte=end_date).values(type).\
    annotate(Sum("total_order_count")).annotate(Sum("total_pay_price")).annotate(Sum("total_user_count")).\
    annotate(Sum("avg_user_order_count")).annotate(Sum("avg_order_pay")).annotate(Sum("arpu"))
    for business_sumamry in business_sumamries:
        # print(business_sumamry)
        if type == u'product_type':
            if business_sumamry[type] == u'PLUS99':
                x_axis.append("全部业务")
            else:
                obj = TongjiPayProduct.objects.get(type=int(business_sumamry[type]))
                x_axis.append(str(obj.name))
        else:
            x_axis.append(str(business_sumamry[type]))
        total_order_count_result.append(0 if not business_sumamry['total_order_count__sum'] else int(business_sumamry['total_order_count__sum']))
        total_pay_price_result.append(0 if not business_sumamry['total_pay_price__sum'] else float(business_sumamry['total_pay_price__sum']))
        total_user_count_result.append(0 if not business_sumamry['total_user_count__sum'] else int(business_sumamry['total_user_count__sum']))
        avg_user_order_count_result.append(0 if not business_sumamry['avg_user_order_count__sum'] else float(business_sumamry['avg_user_order_count__sum']))
        avg_order_pay_result.append(0 if not business_sumamry['avg_order_pay__sum'] else float(business_sumamry['avg_order_pay__sum']))
        arpu_result.append(0 if not business_sumamry['arpu__sum'] else float(business_sumamry['arpu__sum']))
    result=[]
    result.append({"data":total_order_count_result,"type":"bar","name":"订单总数"})
    result.append({"data":total_pay_price_result,"type":"bar","name":"订单总金额"})
    result.append({"data":total_user_count_result,"type":"bar","name":"用户数"})
    result.append({"data":avg_user_order_count_result,"type":"bar","name":"人均笔数"})
    result.append({"data":avg_order_pay_result,"type":"bar","name":"客单价"})
    result.append({"data":arpu_result,"type":"bar","name":"ARPU"})
    return x_axis, result


def get_app_ver_channel(request):
    ot = request.POST.get("ot")
    if not ot:
        ot = "PLUS99"
    app = request.POST.get("app")
    report_check_app(request, app)
    if not app:
        app = "PLUS99"
    ver = request.POST.get("ver") #数据有问题
    if not ver:
        ver = "PLUS99"
    channel = request.POST.get("channel")
    if not channel:
        channel = "PLUS99"
    return ot, app, ver, channel


@login_required
# @permission_required(u'man.%s' % ReportConst.ORDER_REPORTS, raise_exception=True)
def exchange_business_reports_csv(request):
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")
    filename = '%s(%s-%s).csv' % ("业务分析", str(start_date), str(end_date))
    csv_data = [["日期",
                "交易单数",
                "交易总额",
                "交易用户数",
                "人均笔数",
                "客单价",
                "ARPU"]]
    csv_data.extend(g_data)
    return get_csv_response(filename, csv_data)