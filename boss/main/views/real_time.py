#coding: utf-8

"""
    实时统计
"""


from django.shortcuts import render_to_response
import json
from main.models import TRpHAppuseSum, VRpDRealtimeStat
from main_pub import *


def __get_data_by_date(type, app_key, date):
    if not app_key:
        app_key = Const.PLUS99
    objs = TRpHAppuseSum.objects.filter(
        app_key=app_key,
        channel_no=Const.PLUS99,
        app_version=Const.PLUS99,
        statdate=date)
    result = [0] * 24
    if type == "un":
        for obj in objs:
            result[obj.stathour] = Cal.int(obj.c_usernew)
    elif type == "ua":
        for obj in objs:
            result[obj.stathour] = Cal.int(obj.c_useapp)
    elif type == "ur":
        user = [0] * 24
        for obj in objs:
            user[obj.stathour] = Cal.int(obj.c_user)
        for i in range(len(user)):
            result[i] = sum(user[:i+1])
    return result



@login_required
@permission_required(u'man.%s' % MainConst.USER_ON, raise_exception=True)
@add_common_var
def real_time(request, template_name):
    app_key = request.GET.get("app")
    if not app_key:
        app_key = Const.PLUS99
    #获取实时统计的基本数据
    try:
        sumobj = VRpDRealtimeStat.objects.filter(app_key=app_key).order_by("-statdate")[0]
        sum_un = Cal.int(sumobj.c_usernew)
        rate_un = Cal.precision(sumobj.c_usernew_change_rate)
        sum_ua = Cal.int(sumobj.c_useapp)
        rate_ua = Cal.precision(sumobj.c_useapp_change_rate)
        sum_ur = Cal.int(sumobj.c_user)
        rate_ur = Cal.precision(sumobj.c_user_change_rate)
    except Exception as e:
        sum_un = rate_un = sum_ua = rate_ua = sum_ur = rate_ur = Const.NONE
    return report_render(request,template_name, {
        "currentdate": get_datestr(0, "%Y-%m-%d"),
        "sum_un": sum_un,
        "rate_un": rate_un,
        "sum_ua": sum_ua,
        "rate_ua": rate_ua,
        "sum_ur": sum_ur,
        "rate_ur": rate_ur
    })


@login_required
@permission_required(u'man.%s' % MainConst.USER_ON, raise_exception=True)
def real_time_ajax(request):
    app = request.POST["app"]
    type = request.POST["type"]
    date = request.POST["date"]
    #获取实时统计详细数据
    result = []
    result.append({
        "name": "今日",
        "type": "line",
        "data": __get_data_by_date(type, app, get_datestr(0, "%Y%m%d"))
    })
    result.append({
        "name": "昨日",
        "type": "line",
        "data": __get_data_by_date(type, app, get_datestr(1, "%Y%m%d"))
    })
    result.append({
        "name": "7天前",
        "type": "line",
        "data": __get_data_by_date(type, app, get_datestr(7, "%Y%m%d"))
    })
    result.append({
        "name": "30天前",
        "type": "line",
        "data": __get_data_by_date(type, app, get_datestr(30, "%Y%m%d"))
    })
    if date:
        date = date.split(",")
        for d in date:
            result.append({
                "name": d,
                "type": "line",
                "data": __get_data_by_date(type, app, d)
            })
    return HttpResponse(json.dumps(result))


@login_required
@permission_required(u'man.%s' % MainConst.USER_ON, raise_exception=True)
def real_time_csv(request):
    app_key = request.GET.get("app")
    other_date = request.GET.get("date")
    type = request.GET.get("type")
    if not app_key:
        app_key = Const.PLUS99
    app_name = TSysApp.objects.get(app_key=app_key)
    if type == "un":
        type_name = "新增用户"
    elif type == "ua":
        type_name = "启动次数"
    elif type == "ur":
        type_name = "时段累计日活"
    else:
        type_name = ""
    filename = '实时统计(%s-%s-%s).csv' % (app_name, type_name, get_datestr(0, "%Y%m%d"))
    head = [""]
    data = []
    date = [
        get_datestr(0, "%Y%m%d"),
        get_datestr(1, "%Y%m%d"),
        get_datestr(7, "%Y%m%d"),
        get_datestr(30, "%Y%m%d")
    ]
    if other_date:
        date.extend(other_date.split(","))
    for d in date:
        head.append(d)
        data.append(__get_data_by_date(type, app_key, d))
    #arr = [[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]]
    #转为[[1, 4, 7, 10], [2, 5, 8, 11], [3, 6, 9, 12]]
    temp = map(list, zip(*data))
    #添加时间
    m = 0
    for x in temp:
        x.insert(0, "%d:00" % m)
        m += 1
    csv_data = [head]
    csv_data.extend(temp)
    return get_csv_response(filename, csv_data)