#coding: utf-8

"""
    用券情况
"""

from report_pub import *



def get_coupon_data(start_date, end_date, app, ver, channel, activity_id, scope):
    """
    获取用券情况数据
    :param start_date: 开始日期
    :param end_date: 结束日期
    :param app: 应用id
    :param ver: 版本
    :param channel: 渠道
    :param activity_id: 活动ID
    :param scope:
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
    if not activity_id:
        activity_id = None
    if not scope:
        scope = None
    cursor = connections['report'].cursor()
    cursor.execute("call `SP_T_RP_D_COUPON_USE`(%s, %s, %s, %s, %s, %s, %s)",
                    [start_date, end_date, activity_id, scope, ver, channel, app])
    objs = cursor.fetchall()
    data = []
    for obj in objs:
        data.append([
            str(obj[0]),
            str(obj[1]),
            int(obj[6]),
            int(obj[7]),
            '%0.2f' % float(obj[4]),
            str(obj[3])
        ])
    if not data:
        data.append([Const.NONE] * 6)
    else:
        data.sort(key=lambda o: o[0], reverse=True)
    return data


@login_required
@permission_required(u'man.%s' % ReportConst.COUPON, raise_exception=True)
@add_common_var
def coupon(request, template_name):
    app = request.GET.get("app")
    report_check_app(request, app)
    vers = get_app_versions(app)
    channels = get_app_channels(app)
    activity_ids = get_report_filters('quan_activity_id')
    keys = get_report_filters('quan_scope')
    scopes = []
    for key in keys:
        text = ""
        if key == "HF":
            text = "话费"
        elif key == "FLOW":
            text = "流量"
        elif key == "MOVIE":
            text = "电影"
        elif key == "LUCK":
            text = "彩票"
        elif key == "QQ":
            text = "腾讯产品充值"
        elif key == "GAME":
            text = "游戏充值"
        elif key == "H5":
            text = "H5业务"
        scopes.append([key, text])
    return report_render(request, template_name,{
        "currentdate": get_datestr(1, "%Y-%m-%d"),
        "activity_ids": activity_ids,
        "scopes": scopes,
        "vers": vers,
        "channels": channels
    })


@login_required
@permission_required(u'man.%s' % ReportConst.COUPON, raise_exception=True)
def coupon_ajax(request):
    start_date = request.POST.get("start_date")
    end_date = request.POST.get("end_date")
    app = request.POST.get("app")
    report_check_app(request, app)
    ver = request.POST.get("ver")
    channel = request.POST.get("channel")
    activity_id = request.POST.get("activity_id")
    scope = request.POST.get("scope")
    result = get_coupon_data(start_date, end_date, app, ver, channel, activity_id, scope)
    return HttpResponse(json.dumps(result))


@login_required
@permission_required(u'man.%s' % ReportConst.COUPON, raise_exception=True)
def coupon_csv(request):
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")
    app = request.GET.get("app")
    report_check_app(request, app)
    ver = request.GET.get("ver")
    channel = request.GET.get("channel")
    activity_id = request.GET.get("activity_id")
    scope = request.GET.get("scope")
    filename = '用券情况(%s-%s-%s).csv' % (str(get_app_name(app)), str(start_date), str(end_date))
    csv_data = [["日期",
                 "活动ID",
                 "发券数",
                 "用券数",
                 "优惠券金额",
                 "优惠券详情"]]
    csv_data.extend(get_coupon_data(start_date, end_date, app, ver, channel, activity_id, scope))
    return get_csv_response(filename, csv_data)