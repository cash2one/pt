#coding: utf-8

"""
    所有订单状态报表
"""

from report.models import TongjiPayProduct
from report_pub import *


def get_order_reports_data(start_date, end_date, order_type, app, ver, channel, status):
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
    if not status:
        status = None
    print start_date, end_date, order_type, ver, channel, app, status
    cursor = connections['order'].cursor()
    cursor.execute("call `SP_T_RP_D_FAILED_ORDER_REPORT`(%s, %s, %s, %s, %s, %s, %s)",
                    [start_date, end_date, order_type, ver, channel, app, status])
    objs = cursor.fetchall()
    data = []
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
                '%0.2f' % obj[7],
                str(obj[8]),
                str(obj[9]),
                str(obj[10]),
                str(obj[11]),
                str(obj[12]),
            ]
        )
    if not data:
        data.append([Const.NONE] * 12)
    else:
        data.sort(key=lambda o: o[0], reverse=True)
    return data


@login_required
@permission_required(u'man.%s' % ReportConst.FAILED_ORDERS, raise_exception=True)
@add_common_var
def abnormal_order_report(request, template_name):
    app = request.GET.get("app")
    report_check_app(request, app)
    vers = get_app_versions(app)
    channels = get_app_channels(app)
    products = get_order_types()
    status = get_order_states()
    return report_render(request, template_name, {
        "currentdate": get_datestr(0, "%Y-%m-%d"),
        "vers": vers,
        "channels": channels,
        "products": products,
        "status": status
    })


@login_required
@permission_required(u'man.%s' % ReportConst.FAILED_ORDERS, raise_exception=True)
def abnormal_order_report_ajax(request):
    start_date = request.POST["start_date"]
    end_date = request.POST["end_date"]
    order_type = request.POST["ot"]
    app = request.POST.get("app")
    report_check_app(request, app)
    ver = request.POST.get("ver")
    channel = request.POST.get("channel")
    status = request.POST.get("status")
    print start_date, end_date, order_type, ver, channel, app, status
    result = get_order_reports_data(start_date, end_date, order_type, app, ver, channel, status)
    return HttpResponse(json.dumps(result))


@login_required
@permission_required(u'man.%s' % ReportConst.FAILED_ORDERS, raise_exception=True)
def abnormal_order_report_csv(request):
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")
    order_type = request.GET.get("ot")
    app = request.GET.get("app")
    report_check_app(request, app)
    ver = request.GET.get("ver")
    channel = request.GET.get("channel")
    status = request.POST.get("status")
    if order_type:
        name = "%s异常订单状态报表" % str(TongjiPayProduct.objects.get(type=order_type).name)
    else:
        name = "异常订单状态报表"
    filename = '%s(%s-%s).csv' % (name, str(start_date), str(end_date))
    csv_data = [["ID",
                "订单日期",
                "订单号",
                "订单创建时间",
                "订单更新时间",
                "商品名称",
                "充值电话",
                "支付价格",
                "业务类型",
                "CP名称",
                "渠道名称",
                "当前订单状态",
                "超时处理标记"]]
    csv_data.extend(get_order_reports_data(start_date, end_date, order_type, app, ver, channel, status))
    return get_csv_response(filename, csv_data)
