#coding: utf-8

"""
    所有订单状态报表
"""

from report.models import TongjiPayProduct
from report_pub import *


def get_order_reports_data(start_date, end_date, order_type, app, ver, channel):
    """
    获取所有订单状态报表汇总数据
    :param start_date: 开始日期
    :param end_date: 结束日期
    :param order_type: 订单种类
    :param app: 应用id
    :param ver: 版本
    :param channel: 渠道
    :return:
    """
    if not start_date:
        start_date = None
    if not end_date:
        end_date = None
    if not app:
        app = None
    if not ver:
        ver = None
    if not channel:
        channel = None
    if not order_type:
        order_type = None
    cursor = connections['report'].cursor()
    cursor.execute("call `SP_T_RP_D_ORDER_REPORT`(%s, %s, %s, %s, %s, %s)",
                    [start_date, end_date, order_type, ver, channel, app])
    objs = cursor.fetchall()
    data = []
    for obj in objs:
        data.append(
            [
                str(obj[0]),
                obj[1],
                '%0.2f' % obj[2],
                '%0.2f' % obj[25],
                int(obj[3]),
                int(obj[4]),
                int(obj[5]),
                int(obj[6]),
                int(obj[7]),
                int(obj[8]),
                int(obj[9]),
                '%0.2f' % obj[10],
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
            ]
        )
    if not data:
        data.append([Const.NONE] * 26)
    else:
        data.sort(key=lambda o: o[0], reverse=True)
    return data


@login_required
@permission_required(u'man.%s' % ReportConst.ORDER_REPORTS, raise_exception=True)
@add_common_var
def order_reports(request, template_name):
    app = request.GET.get("app")
    report_check_app(request, app)
    vers = get_app_versions(app)
    channels = get_app_channels(app)
    products = get_order_types()
    return report_render(request, template_name, {
        "currentdate": get_datestr(1, "%Y-%m-%d"),
        "vers": vers,
        "channels": channels,
        "products": products
    })


@login_required
@permission_required(u'man.%s' % ReportConst.ORDER_REPORTS, raise_exception=True)
def order_reports_ajax(request):
    start_date = request.POST["start_date"]
    end_date = request.POST["end_date"]
    order_type = request.POST["ot"]
    app = request.POST.get("app")
    report_check_app(request, app)
    ver = request.POST.get("ver")
    channel = request.POST.get("channel")
    result = get_order_reports_data(start_date, end_date, order_type, app, ver, channel)
    return HttpResponse(json.dumps(result))


@login_required
@permission_required(u'man.%s' % ReportConst.ORDER_REPORTS, raise_exception=True)
def order_reports_csv(request):
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")
    order_type = request.GET.get("ot")
    app = request.GET.get("app")
    report_check_app(request, app)
    ver = request.GET.get("ver")
    channel = request.GET.get("channel")
    if order_type:
        name = "%s业务分表" % str(TongjiPayProduct.objects.get(type=order_type).name)
    else:
        name = "所有订单状态日报表"
    filename = '%s(%s-%s).csv' % (name, str(start_date), str(end_date))
    csv_data = [["日期",
                # "订单种类",
                "交易是否正常",
                "总成交额",
                "总交易笔数",
                "成功笔数",
                "处理中笔数",
                "失败笔数",
                "退款成功笔数",
                "退款失败笔数",
                "退款中笔数",
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
                "运营成本",
                "运营成本(用券)",
                "营收合计"]]
    csv_data.extend(get_order_reports_data(start_date, end_date, order_type, app, ver, channel))
    return get_csv_response(filename, csv_data)
