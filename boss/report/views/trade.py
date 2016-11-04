#coding: utf-8

"""
    营销费用报表
"""


from report_pub import *


def get_trade_data(start_date, end_date, product_type, ver, channel, app):
    """
    获取营销费用报表数据
    :param start_date: 开始日期
    :param end_date: 结束日期
    :param product_type: 订单业务类型，"假" 表示全部
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
    if not product_type:
        product_type = None
    cursor = connections['report'].cursor()
    cursor.execute("call `SP_T_RP_D_OPERATION_COST`(%s, %s, %s, %s, %s, %s)",
                    [start_date, end_date, product_type, ver, channel, app])
    objs = cursor.fetchall()
    data = []
    for obj in objs:
        data.append(
            [
                str(obj[0]),
                '%0.2f' % obj[1],
                '%0.2f' % obj[2],
                '%0.2f' % obj[3],
                '%0.2f' % obj[4],
                '%0.2f' % obj[5]
            ]
        )
    if not data:
        data.append([Const.NONE] * 6)
    else:
        data.sort(key=lambda o: o[0], reverse=True)
    return list(data)



@login_required
@permission_required(u'man.%s' % ReportConst.TRADE, raise_exception=True)
@add_common_var
def trade(request, template_name):
    app = request.GET.get("app")
    report_check_app(request, app)
    vers = get_app_versions(app)
    channels = get_app_channels(app)
    objs = TongjiPayProduct.objects.all()
    products = [[obj.type, obj.name] for obj in objs]
    return report_render(request, template_name, {
        "currentdate": get_datestr(1, "%Y-%m-%d"),
        "vers": vers,
        "channels": channels,
        "products": products
    })


@login_required
@permission_required(u'man.%s' % ReportConst.TRADE, raise_exception=True)
def trade_ajax(request):
    start_date = request.POST["start_date"]
    end_date = request.POST["end_date"]
    product_type = request.POST["pt"]
    app = request.POST.get("app")
    report_check_app(request, app)
    ver = request.POST.get("ver")
    channel = request.POST.get("channel")
    result = get_trade_data(start_date, end_date, product_type, ver, channel, app)
    return HttpResponse(json.dumps(result))


@login_required
@permission_required(u'man.%s' % ReportConst.TRADE, raise_exception=True)
def trade_csv(request):
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")
    product_type = request.GET.get("pt")
    app = request.GET.get("app")
    report_check_app(request, app)
    ver = request.GET.get("ver")
    channel = request.GET.get("channel")
    name = TongjiPayProduct.objects.get(type=product_type).name
    filename = '营销费用报表(%s-%s-%s-%s).csv' % (str(get_app_name(app)), str(name), str(start_date), str(end_date))
    csv_data = [["日期",
                "优惠券",
                "总成交额",
                "CP扣款",
                "CP退款",
                "运营成本"]]
    csv_data.extend(get_trade_data(start_date, end_date, product_type, ver, channel, app))
    return get_csv_response(filename, csv_data)