#coding: utf-8

"""
    自定义事件
"""


from django.shortcuts import render_to_response
import json
from main.models import PtTotalEventWeb, TRpDAppuseEventSum
from main_pub import *


def geteventsum(app_key, ver, event_id, a):
    date = get_datestr(a, "%Y%m%d")
    try:
        return TRpDAppuseEventSum.objects.get(app_key=app_key,
                                              event_id=event_id,
                                              statdate=date,
                                              channel_no=Const.PLUS99,
                                              app_version=ver).c_event
    except:
        return Const.NONE


def get_custom_event_data(app_key, ver, cid = None):
    """
    获取自定义事件的所有数据
    :param app_key: 应用ID
    :param ver: 版本
    :param cid: 业务类型
    :return:
    """
    #设置一些默认值
    if not app_key:
        app_key = Const.PLUS99
    if not ver:
        ver = Const.PLUS99
    data = []
    if cid:
        objs = PtTotalEventWeb.objects.filter(app_key=app_key, business_type=cid)
    else:
        objs = PtTotalEventWeb.objects.filter(app_key=app_key)
    for obj in objs:
        data.append([
            str(obj.event_id),
            str(obj.event_name),
            Cal.int(geteventsum(app_key, ver, obj.event_id, 1)),
            Cal.int(geteventsum(app_key, ver, obj.event_id, 0)),
        ])
    return data



@login_required
@permission_required(u'man.%s' % MainConst.USER_ON, raise_exception=True)
@add_common_var
def custom_event(request, template_name):
    app_key = request.GET.get("app")
    if not app_key or app_key == Const.PLUS99:
        return report_render(request,Const.TEMPLATE_PLUS99, {"zh":"自定义事件", "en":"custom_event"})
    channels, versions = get_channels_versions(app_key)
    data = get_custom_event_data(app_key, Const.PLUS99)
    categorys = get_categorys()
    return report_render(request,template_name, {
        "data": json.dumps(data),
        "versions": versions,
        "categorys": categorys
    })


@login_required
@permission_required(u'man.%s' % MainConst.USER_ON, raise_exception=True)
def custom_event_ajax(request):
    app_key = request.POST["app"]
    ver = request.POST["ver"]
    cid = request.POST["cid"]
    result = get_custom_event_data(app_key, ver, cid)
    return HttpResponse(json.dumps(result))


@login_required
@permission_required(u'man.%s' % MainConst.USER_ON, raise_exception=True)
def custom_event_csv(request):
    app_key = request.GET.get("app")
    ver = request.GET.get("ver")
    cid = request.GET.get("cid")
    app_name = TSysApp.objects.get(app_key=app_key)
    filename = '事件列表(%s-%s).csv' % (app_name, get_datestr(0, "%Y%m%d"))
    csv_data = [["事件ID", "事件名称", "昨日消息数", "今日消息数"]]
    csv_data.extend(get_custom_event_data(app_key, ver, cid))
    return get_csv_response(filename, csv_data)