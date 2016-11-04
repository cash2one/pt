#coding: utf-8

"""
    时段详情
"""


from django.shortcuts import render_to_response
import json
from main.models import TRpHAppuseSum
from main_pub import *



def get_period_details_data(app_key, date):
    #设置一些默认值
    if not app_key:
        app_key = Const.PLUS99
    if not date:
        date = get_datestr(0, "%Y%m%d")
    objs = TRpHAppuseSum.objects.filter(
        app_key=app_key,
        app_version=Const.PLUS99,
        statdate=date).all()
    m = 24
    items = {}
    for obj in objs:
        if not items.get(obj.channel_no):
            items[obj.channel_no] = [Const.NONE] * m
        items[obj.channel_no][obj.stathour] = Cal.int(obj.c_usernew)
    data = [[u"时间"]]
    for i in range(0, m):
        data.append(["%.2d:00" % i])
    #对dict进行排序
    items = [(k,items[k]) for k in sorted(items.keys())]
    for channel_no, c_usernew_list in items:
        #全部应用需要显示全部渠道PLUS99，具体应用不需要该选项
        if app_key != Const.PLUS99 and channel_no == Const.PLUS99:
            continue
        data[0].append(str(channel_no))
        for i in range(0, m):
            data[i + 1].append(c_usernew_list[i])
    #按时段进行逆序
    data.sort(reverse=True)
    return data


@login_required
@permission_required(u'man.%s' % MainConst.USER_ON, raise_exception=True)
@add_common_var
def period_details(request, template_name):
    app_key = request.GET.get("app")
    date = request.GET.get("date")
    channels, versions = get_channels_versions(app_key)
    data = get_period_details_data(app_key, date)
    return report_render(request,template_name, {
        "currentdate": get_datestr(0, "%Y-%m-%d"),
        "data": json.dumps(data), #不用json.dumps 时间中文会乱码
        "channels": channels
    })


@login_required
@permission_required(u'man.%s' % MainConst.USER_ON, raise_exception=True)
def period_details_ajax(request):
    date = request.POST["date"]
    app_key = request.POST["app"]
    result = get_period_details_data(app_key, date)
    return HttpResponse(json.dumps(result))


@login_required
@permission_required(u'man.%s' % MainConst.USER_ON, raise_exception=True)
def period_details_csv(request):
    app_key = request.GET.get("app")
    date = request.GET.get("date")
    if not app_key:
        app_key = Const.PLUS99
    app_name = TSysApp.objects.get(app_key=app_key)
    filename = '时段详情数据表(%s-%s).csv' % (app_name, str(date))
    csv_data = get_period_details_data(app_key, date)
    return get_csv_response(filename, csv_data)