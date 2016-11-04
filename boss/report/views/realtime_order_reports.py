#coding: utf-8

"""
    实时订单汇总报表
"""

from report.models import TongjiPayProduct
from report_pub import *
import time



def get_hours():
    return [
        [0, " 00:00:00"],
        [1, " 01:00:00"],
        [2, " 02:00:00"],
        [3, " 03:00:00"],
        [4, " 04:00:00"],
        [5, " 05:00:00"],
        [6, " 06:00:00"],
        [7, " 07:00:00"],
        [8, " 08:00:00"],
        [9, " 09:00:00"],
        [10, " 10:00:00"],
        [11, " 11:00:00"],
        [12, " 12:00:00"],
        [13, " 13:00:00"],
        [14, " 14:00:00"],
        [15, " 15:00:00"],
        [16, " 16:00:00"],
        [17, " 17:00:00"],
        [18, " 18:00:00"],
        [19, " 19:00:00"],
        [20, " 20:00:00"],
        [21, " 21:00:00"],
        [22, " 22:00:00"],
        [23, " 23:00:00"],
    ]

def get_order_sum_data(start_date, end_date, order_type, app, channel, rp_type):
    """
    获取所有订单状态报表汇总数据
    :param start_date: 开始日期
    :param end_date: 结束日期
    :param order_type: 订单种类
    :param app: 应用id
    :param ver: 版本
    :param channel: 渠道
    :param rp_type: 第一个表是1，第二个表是2
    :return:
    """
    if not start_date:
        start_date = None
    if not end_date:
        end_date = None
    if not app:
        app = None
    if not channel:
        channel = None
    if not order_type:
        order_type = None
    #print("start_date is ", start_date)
    #print("end_date is ", end_date)
    cursor = connections['report'].cursor()
    cursor.execute("call `SP_T_RP_H_ALL_ORDER_REPORT_SUMMARY`(%s, %s, %s, %s, %s, %s)",
                    [start_date, end_date, order_type, channel, app, rp_type])
    objs = cursor.fetchall()
    data = []
    if rp_type == 1:
        for obj in objs:
            data.append(
                [
                    str(obj[0]),
                    str(obj[1]),
                    str(obj[2]),
                    str(obj[3]),
                    str(obj[4]),
                    str(obj[5]),
                    str(obj[6]),
                    str(obj[7]),
                    str(obj[8]),
                    str(obj[9]),
                    str(obj[10]),
                    '%0.2f' % obj[11],
                    '%0.2f' % obj[12],
                    '%0.2f' % obj[13],
                    '%0.2f' % obj[14],
                    '%0.2f' % obj[15],
                    '%0.2f' % obj[16],
                    '%0.2f' % obj[17],
                    '%0.2f' % obj[18],
                    '%0.2f' % obj[19],
                    '%0.2f' % obj[20],
                    '%0.2f' % obj[21],
                    '%0.2f' % obj[22],
                    '%0.2f' % obj[23],
                    '%0.2f' % obj[24],
                    '%0.2f' % obj[25],
                ]
            )
        if not data:
            data.append([Const.NONE] * 26)
        else:
            data.sort(key=lambda o: o[0], reverse=True)
    elif rp_type == 2:
        for obj in objs:
            data.append(
                [
                    str(obj[0]),
                    str(obj[1]),
                    str(obj[2]),
                    str(obj[3]),
                    str(obj[4]),
                    str(obj[5]),
                    str(obj[6]),
                    str(obj[7]),
                    str(obj[8]),
                    str(obj[9]),
                    str(obj[10]),
                    str(obj[11]),
                    str(obj[12]),
                    '%0.2f' % obj[13],
                    '%0.2f' % obj[14],
                    '%0.2f' % obj[15],
                    '%0.2f' % obj[16],
                    '%0.2f' % obj[17],
                    '%0.2f' % obj[18],
                    '%0.2f' % obj[19],
                    '%0.2f' % obj[20],
                    '%0.2f' % obj[21],
                    '%0.2f' % obj[22],
                    '%0.2f' % obj[23],
                    '%0.2f' % obj[24],
                    '%0.2f' % obj[25],
                    '%0.2f' % obj[26],
                    '%0.2f' % obj[27],
                ]
            )
        if not data:
            data.append([Const.NONE] * 27)
        else:
            data.sort(key=lambda o: o[0], reverse=True)
    return data


@login_required
@permission_required(u'man.%s' % ReportConst.BA_PRODUCT_ANALYSIS_REAL_TIME_REPORT, raise_exception=True)
@add_common_var
def realtime_order_reports(request, template_name):
    app = request.GET.get("app")
    report_check_app(request, app)
    channels = get_app_channels(app)
    products = get_order_types()
    return report_render(request, template_name, {
        "currentdate": get_datestr(0, "%Y-%m-%d"),
        "channels": channels,
        "products": products,
        "start_hours":get_hours(),
        "end_hours":get_hours(),
        "cur_hour": int(time.strftime('%H', time.localtime(time.time()))),
    })


@login_required
@permission_required(u'man.%s' % ReportConst.BA_PRODUCT_ANALYSIS_REAL_TIME_REPORT, raise_exception=True)
def realtime_order_reports_ajax(request):
    start_date = request.POST["start_date"]
    end_date = request.POST["end_date"]
    start_hour = request.POST["start_hour"]
    if not start_hour:
        start_hour = " 00:00:00"
    end_hour = request.POST["end_hour"]
    if not end_hour:
        end_hour = " 00:00:00"
    start_date = start_date + start_hour
    end_date = end_date + end_hour
    order_type = request.POST["ot"]
    app = request.POST.get("app")
    report_check_app(request, app)
    channel = request.POST.get("channel")
    result1 = get_order_sum_data(start_date, end_date, order_type, app, channel, 1)
    result2 = get_order_sum_data(start_date, end_date, order_type, app, channel, 2)
    return HttpResponse(json.dumps([result1, result2]))


@login_required
@permission_required(u'man.%s' % ReportConst.BA_PRODUCT_ANALYSIS_REAL_TIME_REPORT, raise_exception=True)
def realtime_order_reports_csv(request):
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")
    start_hour = request.GET.get("start_hour")
    if not start_hour:
        start_hour = " 00:00:00"
    end_hour = request.GET.get("end_hour")
    if not end_hour:
        end_hour = " 00:00:00"
    start_date = start_date + start_hour
    end_date = end_date + end_hour
    order_type = request.GET.get("ot")
    app = request.GET.get("app")
    report_check_app(request, app)
    channel = request.GET.get("channel")
    if order_type:
        name = "%s业务分表" % str(TongjiPayProduct.objects.get(type=order_type).name)
    else:
        name = "订单业务渠道实时报表"
    filename = '%s(%s-%s).csv' % (name, str(start_date), str(end_date))
    csv_data = [["订单种类",
                "应用名称",
                "订单是否正常",
                "总用户数",
                "总订单金额",
                "总订单数",
                "总支付金额",
                "总支付订单数",
                "未支付金额",
                "未支付订单数",
                "成功笔数",
                "处理中笔数",
                "失败笔数",
                "支付宝收款",
                "微信收款",
                "其他收款",
                "支付宝退款",
                "微信退款",
                "其他退款",
                "支付宝费率",
                "微信费率",
                "CP应扣",
                "CP实扣",
                "CP退款",
                "CP佣金",
                "运营成本(用券)",
                "运营成本",
                "营收合计"]]
    csv_data.extend(get_order_sum_data(start_date, end_date, order_type, app, channel, 2))
    return get_csv_response(filename, csv_data)
