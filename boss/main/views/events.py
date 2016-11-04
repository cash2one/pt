#coding: utf-8

"""
    事件
"""


from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django import forms
import json
from main.models import PtTotalEventWeb
from main_pub import *


class EventForm(forms.ModelForm):
    event_id = forms.CharField(label=u"事件ID*")
    event_name = forms.CharField(label=u"事件名称", required=False)
    event_type = forms.ChoiceField(label=u'事件类型',
                                   choices=((u'计数事件', u'计数事件（用于统计字符串型变量的消息数及触发设备数）'), (u'计算事件', u'计算事件')),
                                   initial=u'计数事件',
                                   widget=forms.RadioSelect())
    app_key = forms.CharField(widget=forms.HiddenInput())
    business_type = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    class Meta:
        model = PtTotalEventWeb


def get_total_event(app_key):
    objs = PtTotalEventWeb.objects.filter(app_key=app_key)
    data = []
    for obj in objs:
        if obj.business_type:
            business_type = obj.business_type
            business_name = TSysEventCategory.objects.get(id=obj.business_type).sub_category
        else:
            business_type = ""
            business_name = Const.NONE
        data.append([str(obj.event_id), str(obj.event_name), str(obj.event_type), str(business_name), str(business_type)])
    return data



@login_required
@permission_required(u'man.%s' % MainConst.USER_ON, raise_exception=True)
@add_common_var
def events(request, template_name):
    app_key = request.GET.get("app")
    if not app_key or app_key == Const.PLUS99:
        return report_render(request,Const.TEMPLATE_PLUS99, {"zh":"设置事件", "en":"events"})
    if request.method == 'POST':
        eventform = EventForm(request.POST)
        if eventform.is_valid():
            eventform.save()
            return HttpResponseRedirect("%s?app=%s" % (reverse("events"), app_key))
    else:
        eventform = EventForm()
    categorys = get_categorys()
    return report_render(request,template_name,{
        "eventform": eventform,
        "app": app_key,
        "categorys": categorys
    },context_instance=RequestContext(request))


@login_required
@permission_required(u'man.%s' % MainConst.USER_ON, raise_exception=True)
def events_ajax(request):
    app_key = request.POST["app"]
    result = get_total_event(app_key)
    return HttpResponse(json.dumps(result))


@login_required
@permission_required(u'man.%s' % MainConst.USER_ON, raise_exception=True)
def del_event(request):
    app_key = request.POST["app"]
    eventid = request.POST["eventid"]
    PtTotalEventWeb.objects.get(app_key=app_key, event_id=eventid).delete()
    data = get_total_event(app_key)
    return HttpResponse(json.dumps(data))


@login_required
@permission_required(u'man.%s' % MainConst.USER_ON, raise_exception=True)
def clear_event(request):
    app_key = request.POST["app"]
    PtTotalEventWeb.objects.filter(app_key=app_key).delete()
    data = get_total_event(app_key)
    return HttpResponse(json.dumps(data))



@login_required
@permission_required(u'man.%s' % MainConst.USER_ON, raise_exception=True)
@add_common_var
def edit_event(request, template_name):
    app_key = request.GET.get("app")
    obj = PtTotalEventWeb.objects.get(app_key=app_key, event_id=request.POST["event_id"])
    eventform = EventForm(request.POST, instance=obj)
    if eventform.is_valid():
        eventform.save()
        return HttpResponseRedirect("%s?app=%s" % (reverse("events"), app_key))
    data = get_total_event(app_key)
    categorys = get_categorys()
    return render_to_response(template_name,{
        "data": json.dumps(data),
        "eventform": eventform,
        "app": app_key,
        "categorys": categorys
    },context_instance=RequestContext(request))


@login_required
@permission_required(u'man.%s' % MainConst.USER_ON, raise_exception=True)
def upload_event_file(request):
    """csv文件导入"""
    app_key = request.GET.get("app")
    csv_data = request.FILES["file_data"].read()
    #有BOM标记，要把它去掉
    if csv_data.startswith("\xEF\xBB\xBF"):
        csv_data = csv_data[3:]
    items = csv_data.split("\n")
    objs = []
    for item in items:
        #过滤一些无效行
        if(len(item) > 10):
            temp = item.split(",")
            business_type = None
            if len(temp) >= 3:
                event_id = temp[0]
                event_name = temp[1]
                event_type = temp[2]
                if temp[3].strip():
                    business_type = int(temp[3].strip())
            elif len(temp) == 3:
                event_id, event_name, event_type = temp
            else:
                continue
            objs.append(PtTotalEventWeb(
                app_key=app_key,
                event_id=event_id,
                event_name=event_name,
                event_type=event_type,
                business_type=business_type))
    PtTotalEventWeb.objects.bulk_create(objs)
    #一定要返回json格式，否则file input控件会报错
    return HttpResponse(json.dumps("ok"))

