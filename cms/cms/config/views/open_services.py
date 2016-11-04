# coding: utf-8
from __future__ import unicode_literals
# from config.views.config_pub import *
# from config.forms import *
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required, permission_required
import json
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

from common.const import AuthCodeName
from common.views import filter_none
from config.forms import CmsOpenServiceForm
from config.views.config_pub import GetAllActions
from main.models import CmsOpenVersion, CmsOpenChannel, CmsOpenService, CmsViewOpenService
from main.views.main_pub import add_main_var, get_scenes, get_city_list, get_city_group, format_form


@login_required
@add_main_var
def channels(request, template_name):
    ver_channels = []
    vers = CmsOpenVersion.objects.all()
    for ver in vers:
        ver_channels.append([ver.name, CmsOpenChannel.objects.filter(app_version=ver).values_list("name", "id")])
    return render_to_response(template_name,{
        "ver_channels":ver_channels
    }, context_instance=RequestContext(request))


def copy_channel_open_services(source_id, dest):
    """
    拷贝渠道
    :param source_id: 源渠道，id
    :param dest: 目标渠道，obj
    :return:
    """
    opens = CmsOpenService.objects.filter(cmsviewopenservice__channel_id=source_id)
    for open in opens:
        open.pk = None
        open.save()
        CmsViewOpenService(channel=dest, service=open).save()

@login_required
@permission_required(u'%s.%s' % (AuthCodeName.APP_LABEL,AuthCodeName.CONFIG), raise_exception=True)
def new_version(request):
    try:
        version_name = request.POST.get("version_name")
        copy_name = request.POST.get("copy_name")
        new_version = CmsOpenVersion(name=version_name)
        new_version.save()
        if copy_name:
            old_version = CmsOpenVersion.objects.get(name=copy_name)
            channels = CmsOpenChannel.objects.filter(app_version=old_version)
            for old_channel in channels:
                new_channel = CmsOpenChannel(name=old_channel.name, app_version=new_version)
                new_channel.save()
                copy_channel_open_services(old_channel, new_channel)
        return HttpResponse(0)
    except Exception as e:
        return HttpResponse(e.args[1])


@login_required
@permission_required(u'%s.%s' % (AuthCodeName.APP_LABEL,AuthCodeName.CONFIG), raise_exception=True)
def edit_version(request):
    try:
        old_ver = request.POST.get("old_ver")
        new_ver = request.POST.get("new_ver")
        version = CmsOpenVersion.objects.get(name=old_ver)
        version.name = new_ver
        version.save()
        return HttpResponse(0)
    except Exception as e:
        return HttpResponse(e.args[1])


@login_required
@permission_required(u'%s.%s' % (AuthCodeName.APP_LABEL,AuthCodeName.CONFIG), raise_exception=True)
def new_channel(request):
    try:
        version_name = request.POST.get("version_name")
        channel_name = request.POST.get("channel_name")
        channel_id = request.POST.get("channel_id", "")
        new_channel = CmsOpenChannel(name=channel_name, app_version=CmsOpenVersion.objects.get(name=version_name))
        new_channel.save()
        if channel_id:
            copy_channel_open_services(channel_id, new_channel)
        return HttpResponse(0)
    except Exception as e:
        return HttpResponse(e.args[1])


@login_required
@permission_required(u'%s.%s' % (AuthCodeName.APP_LABEL,AuthCodeName.CONFIG), raise_exception=True)
def edit_channel(request):
    try:
        old_channel = request.POST.get("old_channel")
        new_channel = request.POST.get("new_channel")
        channel = CmsOpenChannel.objects.get(name=old_channel)
        channel.name = new_channel
        channel.save()
        return HttpResponse(0)
    except Exception as e:
        return HttpResponse(e.args[1])


def del_channel_open_services(channel_id):
    CmsOpenService.objects.filter(cmsviewopenservice__channel__id=channel_id).delete()
    CmsOpenChannel.objects.get(id=channel_id).delete()


@login_required
@permission_required(u'%s.%s' % (AuthCodeName.APP_LABEL,AuthCodeName.CONFIG), raise_exception=True)
def del_ver_channels(request):
    """
    data: {
        vers:'["xyz", "woshi"]',
        channels:'{"nihao": ["zhong"],"0": ["putao_h5", "weixin_h5"]}'
    },
    删除版本渠道，版本渠道底下的数据也要删除掉
    :param request:
    :return:
    """
    vers = json.loads(request.POST.get("vers"))
    ver_channels = json.loads(request.POST.get("channels"))
    for ver in vers:
        channels = CmsOpenChannel.objects.filter(app_version__name=ver)
        for channel in channels:
            del_channel_open_services(channel.id)
        CmsOpenVersion.objects.get(name=ver).delete()
    for ver, channels in ver_channels.items():
        for channel in channels:
            channel_id = CmsOpenChannel.objects.get(name=channel, app_version__name=ver).id
            del_channel_open_services(channel_id)
    return HttpResponse(0)


@login_required
@add_main_var
def open_services(request, template_name):
    v = request.GET.get("v")
    c = request.GET.get("c")
    channel = CmsOpenChannel.objects.get(name=c, app_version__name=v).id
    return render_to_response(template_name,{
        "v": v,
        "c": c,
        "channel": channel
    }, context_instance=RequestContext(request))



@login_required
def search_services(request):
    channel_id = request.GET.get('channel')
    objs = CmsOpenService.objects.filter(cmsviewopenservice__channel_id=channel_id).order_by('-id')
    result = []
    distribute_dic ={"0":"无条件","1":"时间条件","2":"地狱条件"}
    for obj in objs:
        distribute = distribute_dic[str(obj.distribute)]
        result.append([obj.id, obj.action_id, obj.show_name, obj.icon, "不限" if obj.city=="*" else obj.city, distribute])
    # result.sort(key=lambda o: (o[0], o[1]))
    filter_none(result)
    return HttpResponse(json.dumps(result))



@login_required
@add_main_var
@permission_required(u'%s.%s' % (AuthCodeName.APP_LABEL,AuthCodeName.CONFIG), raise_exception=True)
def new_open_services(request,template_name):
    """
    配置库新建开放服务
    url :{% url 'open_services_new' %}?channel={{ channel }}
    :请求方式: Get
    :请求参数：channel
    :返回数据：fields errors actions(id,标题,备注) citygroups cities
    :例如：

    :请求方式：Post
    :请求参数：
    """
    channel_id = request.GET.get('channel')
    open_channel = CmsOpenChannel.objects.get(id=channel_id)
    c = open_channel.name
    v = open_channel.app_version.name
    if request.method =='POST':
        form = CmsOpenServiceForm(request.POST)
        if form.is_valid():
            openServieIns = form.save()
            channelIns = CmsOpenChannel.objects.get(id=channel_id)
            CmsViewOpenService(channel=channelIns,service=openServieIns).save()
            return HttpResponseRedirect(reverse("open_services_list")+"?c=%s&v=%s" % (c,v))
    else:
        form = CmsOpenServiceForm()
    actions = GetAllActions()
    cities = get_city_list()
    citygroups = get_city_group()
    errors,fields = format_form(form)
    return render_to_response(template_name,{
        "actions": actions,
        "fields": fields,
        "errors":errors,
        "cities":cities,
        "citygroups":citygroups,
        "c":c,
        "v":v,
        "channel":channel_id
    },context_instance=RequestContext(request))


@login_required
@add_main_var
@permission_required(u'%s.%s' % (AuthCodeName.APP_LABEL,AuthCodeName.CONFIG), raise_exception=True)
def edit_open_services(request, template_name):
    """
    配置库新建开放服务
    url :{% url 'open_services_edit' %}?channel={{ channel }}&id={{ id }}
    :请求方式: Get
    :请求参数：channel,id
    :返回数据：fields errors actions(id,标题,备注) citygroups cities
    :例如：

    :请求方式：Post
    :请求参数：
    """
    id= request.GET.get("id")
    channel_id = request.GET.get('channel')
    open_channel = CmsOpenChannel.objects.get(id=channel_id)
    c = open_channel.name
    v = open_channel.app_version.name
    openServieIns = CmsOpenService.objects.get(id=id)
    if request.method =='POST':
        form = CmsOpenServiceForm(request.POST,instance=openServieIns)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("open_services_list")+"?c=%s&v=%s" % (c,v))
    else:
        form = CmsOpenServiceForm(instance=openServieIns)
    actions = GetAllActions()
    cities = get_city_list()
    citygroups = get_city_group()
    errors,fields = format_form(form)
    return render_to_response(template_name,{
        "actions": actions,
        "fields": fields,
        "errors":errors,
        "cities":cities,
        "citygroups":citygroups,
        "c":c,
        "v":v,
        "channel":channel_id,
        "id":id
    },context_instance=RequestContext(request))


@login_required
@permission_required(u'%s.%s' % (AuthCodeName.APP_LABEL,AuthCodeName.CONFIG), raise_exception=True)
def delete_open_services(request):
    id = request.POST.get("id")
    CmsOpenService.objects.get(id=id).delete()
    return HttpResponse(0)