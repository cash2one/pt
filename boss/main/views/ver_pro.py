#coding: utf-8

"""
    版本发布
"""


from django.shortcuts import render_to_response
import json
from django.db.models import Sum
from main.models import TRpDAppuseVersion, TRpDAppuseTrend
from main_pub import *


class VerProType(object):
    """
    版本分布，今日/昨日/最近七天
    """
    TODAY = 1
    YESTERDAY = 2
    LAST7 = 3


def get_ver_pro_data(app_key, type):
    """
    获取版本分布的所有数据
    :param app_key: 应用ID，全部应用无法查看版本分布
    :param period: 今日、昨日、最近7天
    :return:
    """
    #设置一些默认值
    if not type:
        type = VerProType.TODAY
    data = []
    if type == VerProType.TODAY:
        #今日
        objs = TRpDAppuseVersion.objects.filter(
            app_key=app_key,
            channel_no=Const.PLUS99,
            statdate=get_datestr(0, "%Y%m%d"))\
            .order_by("-c_useracc")
        #统计所有版本的累计用户总数
        c_useracc_total = sum(o.c_useracc for o in objs if o.c_useracc and o.app_version != Const.PLUS99)
        for obj in objs:
            if obj.app_version == Const.PLUS99:
                continue
            c_new_and_update = Cal.sum(obj.c_usernew, obj.update_user)
            if obj.c_useracc is not None:
                c_useracc_per = "%d (%s)" % (Cal.int(obj.c_useracc), Cal.percent(obj.c_useracc, c_useracc_total))
            else:
                c_useracc_per = Const.NONE
            data.append([
                str(obj.app_version),
                c_useracc_per,
                Cal.int(obj.c_usernew),
                Cal.int(obj.update_user),
                c_new_and_update,
                Cal.int(obj.c_user),
                Cal.int(obj.c_useapp)
            ])
        if not data:
            data.append([Const.NONE] * 7)
    elif type == VerProType.YESTERDAY:
        #昨日
        objs = TRpDAppuseVersion.objects.filter(
            app_key=app_key,
            channel_no=Const.PLUS99,
            statdate=get_datestr(1, "%Y%m%d"))
        c_useracc_total = 0
        items = []
        for obj in objs:
            if obj.app_version == Const.PLUS99:
                continue
            c_new_and_update = Cal.sum(obj.c_usernew, obj.update_user)
            try:
                obj2 = TRpDAppuseVersion.objects.get(
                    app_key=app_key,
                    app_version=obj.app_version,
                    channel_no=Const.PLUS99,
                    statdate=get_datestr(0, "%Y%m%d"))
                c_useracc_total += obj2.c_useracc
                c_useracc = obj2.c_useracc
            except:
                #为了排序
                c_useracc = None
            items.append([
                obj.app_version,
                c_useracc,
                Cal.int(obj.c_usernew),
                Cal.int(obj.update_user),
                c_new_and_update,
                Cal.int(obj.c_user),
                Cal.int(obj.c_useapp)])
        #按累计用户进行排序
        items.sort(key=lambda o:o[1], reverse=True)
        for item in items:
            if item[1] is not None:
                c_useracc_per = "%d (%s)" % (Cal.int(item[1]), Cal.percent(item[1], c_useracc_total))
            else:
                c_useracc_per = Const.NONE
            data.append([item[0], c_useracc_per, item[2], item[3], item[4], item[5],item[6]])
        if not data:
            data.append([Const.NONE] * 7)
    elif type == VerProType.LAST7:
        objs = TRpDAppuseVersion.objects.filter(
            app_key=app_key,
            channel_no=Const.PLUS99,
            statdate__range=[get_datestr(6, "%Y%m%d"), get_datestr(0, "%Y%m%d")])\
            .values('app_version')\
            .annotate(c_usernew_total=Sum('c_usernew'),
                      update_user_total=Sum('update_user'),
                      c_useapp_total=Sum('c_useapp'))\
            .order_by('app_version')
        for obj in objs:
            if obj["app_version"] == Const.PLUS99:
                continue
            try:
                sumobj = TRpDAppuseTrend.objects.get(
                    app_key=app_key,
                    channel_no=Const.PLUS99,
                    app_version=obj["app_version"],
                    statdate=get_datestr(0, "%Y%m%d"))
                c_user_p7 = Cal.int(sumobj.c_user_p7)
            except:
                c_user_p7 = Const.NONE
            data.append([
                obj["app_version"],
                Cal.int(obj["c_usernew_total"]),
                Cal.int(obj["update_user_total"]),
                Cal.sum(obj["c_usernew_total"], obj["update_user_total"]),
                c_user_p7,
                Cal.int(obj["c_useapp_total"])
            ])
        if not data:
            data.append([Const.NONE] * 6)
    return data



@login_required
@permission_required(u'man.%s' % MainConst.USER_ON, raise_exception=True)
@add_common_var
def ver_pro(request, template_name):
    app_key = request.GET.get("app")
    if not app_key or app_key == Const.PLUS99:
        return report_render(request,Const.TEMPLATE_PLUS99, {"zh":"版本分布", "en":"ver_pro"})
    data = get_ver_pro_data(app_key, VerProType.TODAY)
    return report_render(request,template_name, {
        "currentdate": get_datestr(0, "%Y-%m-%d"),
        "data": data
    })


@login_required
@permission_required(u'man.%s' % MainConst.USER_ON, raise_exception=True)
def ver_pro_ajax(request):
    app_key = request.POST["app"]
    type = int(request.POST["type"])
    result = get_ver_pro_data(app_key, type)
    return HttpResponse(json.dumps(result))


@login_required
@permission_required(u'man.%s' % MainConst.USER_ON, raise_exception=True)
def ver_pro_csv(request):
    app_key = request.GET.get("app")
    type = int(request.GET.get("type"))
    app_name = TSysApp.objects.get(app_key=app_key)
    filename = '版本分布数据表(%s-%s).csv' % (app_name, get_datestr(0, "%Y%m%d"))
    if type == VerProType.TODAY or type == VerProType.YESTERDAY:
        csv_data = [["应用版本", "版本累计用户(%)", "新增用户", '升级用户',
                     '新增+升级', '活跃用户', '启动次数']]
    else:
        csv_data = [["应用版本", "新增用户", '升级用户',
                     '新增+升级', '活跃用户', '启动次数']]
    csv_data.extend(get_ver_pro_data(app_key, type))
    return get_csv_response(filename, csv_data)