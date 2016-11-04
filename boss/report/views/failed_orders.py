#coding: utf-8

"""
    所有失败订单
"""

from report.models import VwPtTongjiPayFailedList
from report_pub import *


def get_failed_orders_data(order_type, app, ver, channel, start_date, end_date):
    """
    获取所有失败订单汇总数据
    :param order_type: 订单业务类型，"假" 表示全部
    :param app: 应用id
    :param ver: 版本
    :param channel: 渠道
    :return:
    """
    query = {}
    if app:
        query["app_id"] = app
    if ver:
        query["app_version"] = ver
    if channel:
        query["channel_no"] = channel
    if order_type:
        query["product_type"] = order_type
    end_date_d = datetime.datetime.strptime(end_date, "%Y-%m-%d")+datetime.timedelta(days=1)
    objs = VwPtTongjiPayFailedList.objects.filter(**query).filter(c_time__gte=start_date,c_time__lte=end_date_d)
    data = []
    for obj in objs:
        #退款状态翻译
        refund_status = obj.refund_status
        if refund_status == "REFUND_PROCESS":
            refund_status = "处理中"
        elif refund_status == "REFUND_FAIL":
            refund_status = "退款失败"
        data.append(
            [
                obj.order_no,
                obj.product,
                obj.name,
                '%0.2f' % obj.price,
                str(obj.c_time),
                obj.status,
                refund_status
            ]
        )
    if not data:
        data.append([Const.NONE] * 7)
    return data


@login_required
@permission_required(u'man.%s' % ReportConst.FAILED_ORDERS, raise_exception=True)
@add_common_var
def failed_orders(request, template_name):
    app = request.GET.get("app")
    report_check_app(request, app)
    vers = get_app_versions(app)
    channels = get_app_channels(app)
    products = get_order_types()
    return report_render(request, template_name, {
        "currentdate": get_datestr(0, "%Y-%m-%d"),
        "vers": vers,
        "channels": channels,
        "products": products
    })


@login_required
@permission_required(u'man.%s' % ReportConst.FAILED_ORDERS, raise_exception=True)
def failed_orders_ajax(request):
    order_type = request.POST["ot"]
    app = request.POST.get("app")
    start_date = request.POST.get("start_date")
    end_date = request.POST.get("end_date")
    report_check_app(request, app)
    ver = request.POST.get("ver")
    channel = request.POST.get("channel")
    result = get_failed_orders_data(order_type, app, ver, channel, start_date, end_date)
    return HttpResponse(json.dumps(result))


@login_required
@permission_required(u'man.%s' % ReportConst.FAILED_ORDERS, raise_exception=True)
def failed_orders_csv(request):
    order_type = request.GET.get("ot")
    app = request.GET.get("app")
    start_date = request.POST.get("start_date")
    end_date = request.POST.get("end_date")
    report_check_app(request, app)
    ver = request.GET.get("ver")
    channel = request.GET.get("channel")
    if order_type:
        name = "失败订单分表-%s" % (str(order_type))
    else:
        name = "所有失败订单汇总"
    filename = '%s(%s-%s).csv' % (name, str(get_app_name(app)), str(get_datestr(0, "%Y-%m-%d")))
    csv_data = [["订单号",
                "订单种类",
                "订单详情",
                "支付金额",
                "创建时间",
                "订单状态",
                "退款状态"]]
    csv_data.extend(get_failed_orders_data(order_type, app, ver, channel, start_date, end_date))
    return get_csv_response(filename, csv_data)

