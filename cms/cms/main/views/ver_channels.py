# coding: utf-8

"""
    版本渠道列表
"""
# from main.forms import *
# from .main_pub import *
import time
from django.views.decorators.http import require_POST

from common.views import get_relate_channel_list
from main.forms import NewVerForm, NewChannelForm
from main.models import CmsChannelsAppVersion, CmsCheck, CmsChannels
from main.views.op_channel import OpChannel
from main.views.del_channel import DelChannel
from audioop import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
import json
from django.http import HttpResponse, HttpResponseRedirect
from cms.settings import CMS_CHECK_ON
from common.const import AuthCodeName, CheckStatu, CheckOpType, CmsModule, get_nav_text, CONFIG_ITEMS

"""
    app_version 版本名字
    type_id 应用id
    src_ver_id 源版本id 要复制哪个版本
"""


@login_required
@permission_required(u'%s.%s' % (AuthCodeName.APP_LABEL, AuthCodeName.CONFIG), raise_exception=True)
@require_POST
def new_version(request):
    type_id = request.POST["type_id"]
    src_ver_id = request.POST.get('src_ver_id')
    form = NewVerForm(request.POST)
    if form.is_valid():
        channelsappversion = form.save()
        remark = ""
        if src_ver_id:
            src_ver = CmsChannelsAppVersion.objects.get(id=src_ver_id)
            src_ver_text = src_ver.app_version
            src_type_text = get_nav_text(src_ver.type_id)
            type_text = get_nav_text(type_id)
            remark = "在%s下新建了版本%s，它是由%s%s版本复制而来" % (
                type_text, channelsappversion.app_version, src_type_text, src_ver_text)
        if CMS_CHECK_ON:
            CmsCheck(module=CmsModule.MAIN_CHANNEL,
                     table_name='CmsChannelsAppVersion',
                     data_id=channelsappversion.id,
                     op_type=CheckOpType.NEW,
                     remark=remark,
                     alter_person=request.user.username,
                     alter_date=time.strftime("%Y-%m-%d %X", time.localtime())).save()
        if src_ver_id:
            copy_version(src_ver_id, channelsappversion.id, request)
    return HttpResponseRedirect(reverse('main_index') + "?t=%s" % type_id)


@login_required
@permission_required(u'%s.%s' % (AuthCodeName.APP_LABEL, AuthCodeName.CONFIG), raise_exception=True)
def edit_version(request):
    try:
        type_id = request.POST["type_id"]
        old_ver = request.POST["old_ver"]
        new_ver = request.POST["new_ver"]
        ver_obj = CmsChannelsAppVersion.objects.get(type_id=type_id, app_version=old_ver)
        ver_obj.app_version = new_ver
        ver_obj.save()
        if CMS_CHECK_ON:
            CmsCheck(module=CmsModule.MAIN_CHANNEL,
                     table_name='CmsChannelsAppVersion',
                     data_id=ver_obj.id,
                     op_type=CheckOpType.EDIT,
                     alter_person=request.user.username,
                     alter_date=time.strftime("%Y-%m-%d %X", time.localtime())).save()
        return HttpResponse(0)
    except:
        return HttpResponse(1)


# 复制版本
def copy_version(source_version_id, target_version_id, request):
    # 复制到
    channels = CmsChannels.objects.filter(app_version_id=source_version_id)
    for channel in channels:
        channel.app_version_id = target_version_id
        src_channel_id = channel.id
        channel.id = None
        channel.save()
        if CMS_CHECK_ON:
            CmsCheck(module=CmsModule.MAIN_CHANNEL,
                     table_name='CmsChannels',
                     data_id=channel.id,
                     op_type=CheckOpType.NEW,
                     is_show=0,
                     alter_person=request.user.username,
                     alter_date=time.strftime("%Y-%m-%d %X", time.localtime())).save()
        ocmschannelchannel = OpChannel(src_channel_id).copy_asso(channel.id)
        if CMS_CHECK_ON:
            CmsCheck(module=CmsModule.MAIN_CHANNEL,
                     table_name='CmsChannelChannel',
                     data_id=ocmschannelchannel.id,
                     op_type=CheckOpType.NEW,
                     is_show=0,
                     alter_person=request.user.username,
                     alter_date=time.strftime("%Y-%m-%d %X", time.localtime())).save()


@login_required
@permission_required(u'%s.%s' % (AuthCodeName.APP_LABEL, AuthCodeName.CONFIG), raise_exception=True)
def del_ver_channels(request):
    """
    data: {
        type_id: 4,
        vers:'["xyz", "woshi"]',
        channels:'{"nihao": ["zhong"],"0": ["putao_h5", "weixin_h5"]}'
    },
    删除版本渠道，版本渠道底下的数据也要删除掉
    :param request:
    :return:
    """
    type_id = request.POST.get("type_id")
    vers = json.loads(request.POST.get("vers"))
    ver_channels = json.loads(request.POST.get("channels"))
    for ver in vers:
        DelChannel.del_index_version(CmsChannelsAppVersion.objects.get(type_id=type_id, app_version=ver).id, request)
    for ver, channels in ver_channels.items():
        for channel in channels:
            channel_id = CmsChannels.objects.get(
                app_version=CmsChannelsAppVersion.objects.get(type_id=type_id, app_version=ver), channel_no=channel).id
            DelChannel.del_index_channel(channel_id)
            if CMS_CHECK_ON:
                CmsCheck(
                    module=CmsModule.MAIN_CHANNEL,
                    table_name='CmsChannels',
                    data_id=channel_id,
                    op_type=CheckOpType.DELETE,
                    status=CheckStatu.WAIT_SUBMIT,
                    is_show=1,
                    alter_person=request.user.username,
                    alter_date=time.strftime("%Y-%m-%d %X", time.localtime())).save()
    return HttpResponse(0)


"""
url :{% url 'new_channel' %}
channel_type_id :类型
input_app_version
channel_no
order
source_channel_id : 要复制的渠道id
channel_op_type ： 值为 'copy' or 'associate'
config_items :配置项列表 格式：['activity','ads','category_pages_services','choiceness_category','common_services',\
'config_operation','coupons','foundpage_specialtopic','homepage_specialtopic','likes','streams']
"""


@login_required
@permission_required(u'%s.%s' % (AuthCodeName.APP_LABEL, AuthCodeName.CONFIG), raise_exception=True)
def new_channel(request):
    try:
        form = NewChannelForm(request.POST)
        type_id = request.POST.get("channel_type_id")
        source_channel_id = request.POST.get("source_channel_id")
        config_items = request.POST.get("config_items")
        config_items = json.loads(config_items)
        channel_op_type = request.POST.get("channel_op_type")
        if form.is_valid():
            channel_no = request.POST.get("channel_no")
            app_version = request.POST.get("input_app_version")
            if request.POST.get("order") == "1":
                order = 1
            else:
                order = 2
            app_obj = CmsChannelsAppVersion.objects.get(type_id=type_id, app_version=app_version)
            channel = CmsChannels(app_version=app_obj, channel_no=channel_no, user_id=1, order=order)
            channel.save()
            if CMS_CHECK_ON:
                CmsCheck(module=CmsModule.MAIN_CHANNEL,
                         table_name='CmsChannels',
                         data_id=channel.id,
                         op_type=CheckOpType.NEW,
                         alter_person=request.user.username,
                         alter_date=time.strftime("%Y-%m-%d %X", time.localtime())).save()
            if channel_op_type and source_channel_id and config_items:
                ocmschannelchannel = OpChannel(source_channel_id).copy_asso(channel.id, config_items=config_items,
                                                                            channel_op_type=channel_op_type)
                if CMS_CHECK_ON:
                    CmsCheck(module=CmsModule.MAIN_CHANNEL,
                             table_name='CmsChannelChannel',
                             data_id=ocmschannelchannel.id,
                             op_type=CheckOpType.NEW,
                             alter_person=request.user.username,
                             alter_date=time.strftime("%Y-%m-%d %X", time.localtime())).save()
            return HttpResponse(0)
        else:
            errors = ""
            for item in form.errors:
                errors += (item + ":" + form.errors[item][0] + "\n")
            return HttpResponse(json.loads(errors))
    except Exception as ex:
        return HttpResponse(ex.args[0])


@login_required
@permission_required(u'%s.%s' % (AuthCodeName.APP_LABEL, AuthCodeName.CONFIG), raise_exception=True)
def edit_channel(request):
    try:
        type_id = request.POST["type_id"]
        ver = request.POST["ver"]
        old_channel = request.POST["old_channel"]
        new_channel = request.POST["new_channel"]
        ver_obj = CmsChannelsAppVersion.objects.get(type_id=type_id, app_version=ver)
        channel_obj = CmsChannels.objects.get(app_version=ver_obj, channel_no=old_channel)
        channel_obj.channel_no = new_channel
        channel_obj.save()
        if CMS_CHECK_ON:
            CmsCheck(module=CmsModule.MAIN_CHANNEL,
                     table_name='CmsChannels',
                     data_id=channel_obj.id,
                     op_type=CheckOpType.EDIT,
                     alter_person=request.user.username,
                     alter_date=time.strftime("%Y-%m-%d %X", time.localtime())).save()
        return HttpResponse(0)
    except:
        return HttpResponse(1)


def ver_channels_test(request):
    print ("==============", get_relate_channel_list(1000, CONFIG_ITEMS.AD))
    return HttpResponse(0)
