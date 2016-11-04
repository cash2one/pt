#coding: utf-8

"""
    服务质量追踪-电影票
"""

from report_pub import *


def get_movie_sum_data(start_date, end_date, app, ver, channel):
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
    cursor = connections['report'].cursor()
    cursor.execute("call `SP_T_RP_D_MOVIE_RANKS`(%s, %s, %s, %s, %s)",
                    [start_date, end_date, ver, channel, app])
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
                str(obj[7]),
            ]
        )
    if not data:
        data.append([Const.NONE] * 8)
    else:
        data.sort(key=lambda o: o[0], reverse=True)
    return data

@login_required
@permission_required(u'man.%s' % ReportConst.BA_PRODUCT_ANALYSIS_MOVIE_REPORT, raise_exception=True)
@add_common_var
def movie_sum(request, template_name):
    app = request.GET.get("app")
    report_check_app(request, app)
    vers = get_app_versions(app)
    channels = get_app_channels(app)
    product_type = get_product_type(ReportConst.MOVIE)
    cps = get_cp_info(product_type)
    return report_render(request, template_name,{
        "currentdate": get_datestr(0, "%Y-%m-%d"),
        "vers": vers,
        "channels": channels
    })


@login_required
@permission_required(u'man.%s' % ReportConst.BA_PRODUCT_ANALYSIS_MOVIE_REPORT, raise_exception=True)
def movie_sum_ajax(request):
    start_date = request.POST.get("start_date")
    end_date = request.POST.get("end_date")
    app = request.POST.get("app")
    report_check_app(request, app)
    ver = request.POST.get("ver")
    channel = request.POST.get("channel")
    result = get_movie_sum_data(start_date, end_date, app, ver, channel)
    return HttpResponse(json.dumps(result))


@login_required
@permission_required(u'man.%s' % ReportConst.BA_PRODUCT_ANALYSIS_MOVIE_REPORT, raise_exception=True)
def movie_sum_csv(request):
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")
    app = request.GET.get("app")
    report_check_app(request, app)
    ver = request.GET.get("ver")
    channel = request.GET.get("channel")
    filename = '电影票汇总报表(%s-%s).csv' % (str(start_date), str(end_date))
    csv_data = [["电影名称",
                "订单总数",
                "订单支付数",
                "订单支付率",
                "订单支付成功数",
                "订单支付成功率",
                "订单支付失败数",
                "订单支付失败率"]]
    csv_data.extend(get_movie_sum_data(start_date, end_date, app, ver, channel))
    return get_csv_response(filename, csv_data)