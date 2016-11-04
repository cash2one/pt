#coding: utf-8

"""
    服务质量追踪-电影票
"""

from report_pub import *



@login_required
@permission_required(u'man.%s' % ReportConst.MOVIE, raise_exception=True)
@add_common_var
def movie(request, template_name):
    app = request.GET.get("app")
    report_check_app(request, app)
    vers = get_app_versions(app)
    channels = get_app_channels(app)
    product_type = get_product_type(ReportConst.MOVIE)
    cps = get_cp_info(product_type)
    return report_render(request, template_name,{
        "currentdate": get_datestr(1, "%Y-%m-%d"),
        "cps": cps,
        "vers": vers,
        "channels": channels
    })


@login_required
@permission_required(u'man.%s' % ReportConst.MOVIE, raise_exception=True)
def movie_ajax(request):
    start_date = request.POST.get("start_date")
    end_date = request.POST.get("end_date")
    app = request.POST.get("app")
    report_check_app(request, app)
    ver = request.POST.get("ver")
    channel = request.POST.get("channel")
    cp = request.POST.get("cp")
    result = get_service_quality_data(start_date, end_date, app, ver, channel, None, None, None, cp, ReportConst.MOVIE)
    return HttpResponse(json.dumps(result))


@login_required
@permission_required(u'man.%s' % ReportConst.MOVIE, raise_exception=True)
def movie_csv(request):
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")
    app = request.GET.get("app")
    report_check_app(request, app)
    ver = request.GET.get("ver")
    channel = request.GET.get("channel")
    cp = request.GET.get("cp")
    filename = '%s-质量追踪(%s-%s-%s).csv' % (ReportConst.MOVIE, str(get_app_name(app)), str(start_date), str(end_date))
    csv_data = [["日期",
                "总单数",
                "成功数",
                "失败数",
                "失败率",
                "1分钟到账数",
                "1分钟到账率",
                "3分钟到账数",
                "3分钟到账率",
                "10分钟到账数",
                "10分钟到账率",
                "30分钟到账数",
                "30分钟到账率",
                "30分钟以上到账数",
                "30分钟以上到账率"]]
    csv_data.extend(get_service_quality_data(start_date, end_date, app, ver, channel, None, None, None, cp, ReportConst.MOVIE))
    return get_csv_response(filename, csv_data)