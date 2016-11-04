#coding: utf-8

"""
    渠道列表
"""

from django.shortcuts import render_to_response
import json
from main.models import TRpDAppuseCombine, TRpDAppuseUsetimes
from main_pub import *


class ChannelListType(object):
    """
    渠道列表，今日/昨日
    """
    TODAY = 1
    YESTERDAY = 2


def get_channel_list_data(app_key, type):
    """
    获取渠道列表的所有数据，全部应用无法查看渠道列表
    :param app_key: 应用ID
    :param type: 今日、周日、最近7天
    :return:
    """
    #设置一些默认值
    if not type:
        type = ChannelListType.TODAY
    data = []
    if type == ChannelListType.TODAY:
        #今日
        objs = TRpDAppuseCombine.objects.filter(
            app_key=app_key,
            app_version=Const.PLUS99,
            statdate=get_datestr(0, "%Y%m%d"))\
            .exclude(channel_no=Const.PLUS99)\
            .order_by("-c_useracc")
        c_useracc_total = get_objp_sum(objs, "c_useracc")
        for obj in objs:
            if obj.c_useracc is not None:
                c_useracc_per = "%d (%s)" % (Cal.int(obj.c_useracc), Cal.percent(obj.c_useracc, c_useracc_total))
            else:
                c_useracc_per = Const.NONE
            data.append([str(obj.channel_no), Cal.int(obj.c_usernew), Cal.int(obj.c_user), c_useracc_per])
        if not data:
            data.append([Const.NONE] * 4)
    elif type == ChannelListType.YESTERDAY:
        #昨日
        objs = TRpDAppuseCombine.objects.filter(
            app_key=app_key,
            app_version=Const.PLUS99,
            statdate=get_datestr(1, "%Y%m%d"))\
            .exclude(channel_no=Const.PLUS99)\
            .order_by("-c_useracc")
        c_useracc_total = get_objp_sum(objs, "c_useracc")
        for obj in objs:
            if obj.c_useracc is not None:
                c_useracc_per = "%d (%s)" % (Cal.int(obj.c_useracc), Cal.percent(obj.c_useracc, c_useracc_total))
            else:
                c_useracc_per = Const.NONE
            try:
                """
                SELECT
                statdate
                ,round((sum(s_usetime)/sum(c_usetime))/60,2) as '平均使用时长'
                ,round(sum(c_useapp),0) as '启动次数'
                ,round(sum(c_usernew),0) as '新增用户'
                ,round(sum(c_user),0) as '活跃用户'
                FROM pt_op_total.t_rp_d_appuse_usetimes
                where app_key='8479f31753834d7989eaa5a8fb69c618' and channel_no='tencent' and app_version='PLUS99'
                group by statdate
                ORDER BY STATDATE DESC
                """
                usetimeobjs = TRpDAppuseUsetimes.objects.filter(
                    app_key=app_key,
                    app_version=Const.PLUS99,
                    channel_no=obj.channel_no,
                    statdate=obj.statdate)
                s_usetime_total = get_objp_sum(usetimeobjs, 's_usetime')
                c_usetime_total = get_objp_sum(usetimeobjs, 'c_usetime')
                usetime = Cal.sec2time(s_usetime_total / c_usetime_total)
            except:
                usetime = Const.NONE
            data.append([str(obj.channel_no), Cal.int(obj.c_usernew), Cal.int(obj.c_user), Cal.int(obj.c_useapp),
                         usetime, c_useracc_per])
        if not data:
            data.append([Const.NONE] * 6)
    return data



@login_required
@permission_required(u'man.%s' % MainConst.USER_ON, raise_exception=True)
@add_common_var
def channel_list(request, template_name):
    app_key = request.GET.get("app")
    if not app_key or app_key == Const.PLUS99:
        return report_render(request,Const.TEMPLATE_PLUS99, {"zh":"渠道列表", "en":"channel_list"})
    data = get_channel_list_data(app_key, ChannelListType.TODAY)
    channels, versions = get_channels_versions(app_key)
    return report_render(request,template_name, {
        "data": data,
        "currentdate": get_datestr(0, "%Y-%m-%d"),
        "channels": channels
    })


@login_required
@permission_required(u'man.%s' % MainConst.USER_ON, raise_exception=True)
def channel_list_ajax(request):
    app_key = request.POST["app"]
    type = int(request.POST["type"])
    result = get_channel_list_data(app_key, type)
    return HttpResponse(json.dumps(result))


@login_required
@permission_required(u'man.%s' % MainConst.USER_ON, raise_exception=True)
def channel_list_csv(request):
    app_key = request.GET.get("app")
    type = int(request.GET.get("type"))
    app_name = TSysApp.objects.get(app_key=app_key)
    filename = '渠道列表数据表(%s-%s).csv' % (app_name, get_datestr(0, "%Y%m%d"))
    if type == ChannelListType.TODAY:
        csv_data = [["渠道名", "新增用户", "活跃用户", '累计用户(占比)']]
    else:
        csv_data = [["渠道名", "新增用户", "活跃用户", '启动次数', '单次使用时长', '累计用户(占比)']]
    csv_data.extend(get_channel_list_data(app_key, type))
    return get_csv_response(filename, csv_data)