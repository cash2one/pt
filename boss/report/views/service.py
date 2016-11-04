#coding: utf-8

"""
    用户交易报表-业务情况
"""


from report_pub import *


def get_products():
    """获取所有的业务数据"""
    objs = TongjiPayProduct.objects.all()
    return [[o.type, o.name] for o in objs]


def get_service_data(start_date, end_date, app, ver, channel, product):
    """
    获取业务情况数据
    :param start_date: 开始日期
    :param end_date: 结束日期
    :param app: 应用id
    :param ver: 版本
    :param channel: 渠道
    :param product: 产品名称，充话费、充流量等
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
    if not product:
        product = None
    cursor = connections['report'].cursor()
    cursor.execute("call `SP_T_RP_D_USER_TRADE`(%s, %s, %s, %s, %s, %s)",
                    [start_date, end_date, product, ver, channel, app])
    objs = cursor.fetchall()
    data = []
    for obj in objs:
        data.append([
            str(obj[0]),
            int(obj[1]),
            int(obj[4]),
            int(obj[3]),
            int(obj[6]),
            '%0.2f%%' % float(obj[8] * 100),
            int(obj[2]),
            int(obj[5]),
            '%0.2f%%' % float(obj[7] * 100),
            '%0.2f' % float(obj[10]),
            '%0.2f' % float(obj[9])
        ])
    if not data:
        data.append([Const.NONE] * 11)
    else:
        data.sort(key=lambda o: o[0], reverse=True)
    return data



@login_required
@permission_required(u'man.%s' % ReportConst.SERVICE, raise_exception=True)
@add_common_var
def service(request, template_name):
    app = request.GET.get("app")
    report_check_app(request, app)
    vers = get_app_versions(app)
    channels = get_app_channels(app)
    products = get_products()
    return report_render(request, template_name,{
        "currentdate": get_datestr(1, "%Y-%m-%d"),
        "products": products,
        "vers": vers,
        "channels": channels
    })


@login_required
@permission_required(u'man.%s' % ReportConst.SERVICE, raise_exception=True)
def service_ajax(request):
    start_date = request.POST.get("start_date")
    end_date = request.POST.get("end_date")
    app = request.POST.get("app")
    report_check_app(request, app)
    ver = request.POST.get("ver")
    channel = request.POST.get("channel")
    product = request.POST.get("product")
    result = get_service_data(start_date, end_date, app, ver, channel, product)
    return HttpResponse(json.dumps(result))


@login_required
@permission_required(u'man.%s' % ReportConst.SERVICE, raise_exception=True)
def service_csv(request):
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")
    app = request.GET.get("app")
    report_check_app(request, app)
    ver = request.GET.get("ver")
    channel = request.GET.get("channel")
    product = request.GET.get("product")
    filename = '业务情况(%s-%s-%s).csv' % (str(get_app_name(app)), str(start_date), str(end_date))
    csv_data = [["日期",
                 "总用户数",
                 "总支付数",
                 "老用户数",
                 "老用户支付数",
                 "老用户支付占比",
                 "新用户数",
                 "新用户支付数",
                 "新用户支付占比",
                 "人均笔数",
                 "人均成交额"]]
    csv_data.extend(get_service_data(start_date, end_date, app, ver, channel, product))
    return get_csv_response(filename, csv_data)