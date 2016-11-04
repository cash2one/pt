# coding: utf-8
"""
    审核中心
1.审核之后才能拿过来用


2.已提交的不能编辑和删除

3.审核表记录新增什么，就要记录删除什么。

"""

# from main.views.op_channel import *
import json

import time
from django.contrib.auth.decorators import login_required, permission_required
from django.core.mail import send_mail
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

from cms.settings import EMAIL_HOST_USER
from common.const import AuthCodeName, get_2array_value, check_status, CheckStatu, CheckOpType
from common.views import filter_none
from main.models import AuthUser, CmsCheck, CmsCheckHistory, CmsChannelChannel, CmsChannels, CmsViewActivity, \
    CmsActivities, CmsViewAd, CmsAds, CmsAdsBeans, CmsAdbeans, CmsViewNavi, CmsNavicategories, CmsNavicatesCategory, \
    CmsNavicatesServices, CmsServices, CmsNavicatesGoods, CmsGoods, CmsViewChoicenessCategory, CmsChoicenessCategory, \
    CmsViewService, CmsViewOpconfig, CmsOpconfig, CmsViewCoupon, CmsCoupon, CmsViewFindTopic, CmsViewHomepageTopic, \
    CmsViewLike, CmsLikes, CmsLikesGoods, CmsLikesServices, CmsViewStream, CmsStreamcontent, CmsStreamcontentsBeans, \
    CmsStreamcontentbeans, CmsStreamcontentsGoods, CmsViewCategoryitem, CmsCategoryItem, CmsCategoryitemItembean, \
    CmsCategoryItembean, CmsViewScreenads, CmsScreenads, CmsViewNativeActivity, CmsNativeActivity
from main.views.del_channel import DelChannel
from main.views.main_pub import add_main_var, show_cvt, set_id_into_records, get_record_detail
from main.views.op_channel import OpChannel


@login_required
@permission_required(u'%s.%s' % (AuthCodeName.APP_LABEL, AuthCodeName.CHECK), raise_exception=True)
@add_main_var
def check(request, template_name):
    users = AuthUser.objects.filter(is_staff=0).values_list('username', 'email')
    return render_to_response(template_name, {
        "users": users
    }, context_instance=RequestContext(request))


def split_checks(records):
    result = []
    for record in records:
        try:
            type, version, channel_no = show_cvt(record.channel_id, record.module)
            last_check = CmsCheck.objects.filter(channel_id=record.channel_id, module=record.module,
                                                 status=record.status).last()
            data = [
                last_check.submit_person,
                type,
                version,
                channel_no,
                record.module,
                str(last_check.submit_date)
            ]
            set_id_into_records(result, data, record.id)
        except:
            continue
    result.sort(key=lambda o: o["record"][5], reverse=True)
    filter_none(result)
    return result


@login_required
@permission_required(u'%s.%s' % (AuthCodeName.APP_LABEL, AuthCodeName.CHECK), raise_exception=True)
def check_handle(request):
    records = CmsCheck.objects.filter(status=CheckStatu.SUBMIT)
    result = split_checks(records)
    return HttpResponse(json.dumps(result))


@login_required
@permission_required(u'%s.%s' % (AuthCodeName.APP_LABEL, AuthCodeName.CHECK), raise_exception=True)
@add_main_var
def check_detail(request, template_name):
    return render_to_response(template_name, context_instance=RequestContext(request))


@login_required
@permission_required(u'%s.%s' % (AuthCodeName.APP_LABEL, AuthCodeName.CHECK), raise_exception=True)
def check_detail_data(request):
    ids_str = request.GET.get("ids")
    ids = ids_str.split(",")
    result = get_record_detail(ids)
    return HttpResponse(json.dumps(result))


@login_required
@permission_required(u'%s.%s' % (AuthCodeName.APP_LABEL, AuthCodeName.CHECK), raise_exception=True)
def check_history(request):
    hs = CmsCheckHistory.objects.all()
    result = []
    for h in hs:
        item = [
            h.status,
            h.check_person,
            h.check_date,
            h.type,
            h.version,
            h.channel_no,
            h.module,
            h.submit_person,
            h.submit_date,
            h.id
        ]
        result.append(item)
    return HttpResponse(json.dumps(result))


@login_required
@permission_required(u'%s.%s' % (AuthCodeName.APP_LABEL, AuthCodeName.CHECK), raise_exception=True)
def check_history_detail(request):
    id = request.GET.get("id")
    content = CmsCheckHistory.objects.get(id=id).content
    return HttpResponse(content)


@login_required
@permission_required(u'%s.%s' % (AuthCodeName.APP_LABEL, AuthCodeName.CHECK), raise_exception=True)
def check_pass(request):
    """
    审核通过
    :param url: {% url 'check_pass' %}
    :param ids: 审核表id列表
    :return: 0 表示成功
    """

    ids = json.loads(request.POST.get("ids"))
    check_time = time.strftime("%Y-%m-%d %X", time.localtime())
    records = CmsCheck.objects.filter(id__in=ids)
    result = split_checks(records)
    try:
        for r in result:
            history = CmsCheckHistory(
                status=get_2array_value(check_status, CheckStatu.PASS),
                check_person=request.user.username,
                check_date=check_time,
                type=r["record"][1],
                version=r["record"][2],
                channel_no=r["record"][3],
                module=r["record"][4],
                submit_person=r["record"][0],
                submit_date=r["record"][5],
                content=json.dumps(get_record_detail(r["ids"])),
            )
            history.save()

        for id in ids:
            oCmsCheck = CmsCheck.objects.get(id=id)
            # 如果是新建和编辑的话直接同步到正式库，删除就直接删除
            if oCmsCheck.op_type == int(CheckOpType.NEW):
                if oCmsCheck.table_name == "CmsChannelChannel":
                    pass_channelchannel(oCmsCheck.data_id, oCmsCheck.is_show)
                else:
                    table_obj = eval(oCmsCheck.table_name).objects.get(id=oCmsCheck.data_id)
                    table_obj.save(using="online")
            elif oCmsCheck.op_type == int(CheckOpType.EDIT):
                table_obj = eval(oCmsCheck.table_name).objects.get(id=oCmsCheck.data_id)
                table_obj.save(using="online")
            else:
                if oCmsCheck.table_name == "CmsChannels":
                    DelChannel.del_index_channel(oCmsCheck.data_id, db="online")
                elif oCmsCheck.table_name == "CmsViewFindTopic":
                    table_obj = eval(oCmsCheck.table_name).objects.get(id=oCmsCheck.data_id)
                    table_obj.save(using="online")
                else:
                    eval(oCmsCheck.table_name).objects.using("online").filter(id=oCmsCheck.data_id).delete()
            oCmsCheck.status = CheckStatu.PASS
            oCmsCheck.check_person = request.user.username
            oCmsCheck.check_date = check_time
            if oCmsCheck.op_type == int(CheckOpType.DELETE):
                CmsCheck.objects.filter(table_name=oCmsCheck.table_name, data_id=oCmsCheck.data_id).delete()
            else:
                oCmsCheck.save()

    except Exception as ex:
        for r in result:
            history = CmsCheckHistory(
                status=get_2array_value(check_status, CheckStatu.CHECK_ERROR),
                check_person=request.user.username,
                check_date=check_time,
                type=r["record"][1],
                version=r["record"][2],
                channel_no=r["record"][3],
                module=r["record"][4],
                submit_person=r["record"][0],
                submit_date=r["record"][5],
                content=json.dumps(get_record_detail(r["ids"])),
            )
            history.save()

        for id in ids:
            oCmsCheck = CmsCheck.objects.get(id=id)
            oCmsCheck.status = CheckStatu.SUBMIT
            oCmsCheck.check_person = request.user.username
            oCmsCheck.check_date = check_time
            oCmsCheck.remark = "exception:%s" % ex.args[0]
            oCmsCheck.save()
    return HttpResponse(0)


# 关联表审核通过 对正式库做关联或者复制操作
def pass_channelchannel(data_id, is_show=1):
    oCmsChannelChannel = CmsChannelChannel.objects.get(id=data_id)
    config_items = oCmsChannelChannel.config_items.split(",")[1:-1]
    op_channel = OpChannel(oCmsChannelChannel.channel_id1, "online")
    # 判断是否是首页复制还是渠道关联
    if is_show and CmsChannels.objects.using("online").filter(id=oCmsChannelChannel.channel_id2):
        DelChannel.del_config_channel(oCmsChannelChannel.channel_id2, config_items, "online")
    op_type = "copy" if oCmsChannelChannel.op_type else "associate"
    op_channel.copy_asso(oCmsChannelChannel.channel_id2, config_items=config_items, channel_op_type=op_type)


@login_required
@permission_required(u'%s.%s' % (AuthCodeName.APP_LABEL, AuthCodeName.CHECK), raise_exception=True)
def check_reject(request):
    """
    审核拒绝
    :param url: {% url 'check_reject' %}
    :param  ids: 审核表id列表
            message:审核不通过的信息
            recipient_list 收件人列表
    """

    ids = json.loads(request.POST.get("ids"))
    message = request.POST.get("message")
    recipient_list = json.loads(request.POST.get("recipient_list"))
    check_time = time.strftime("%Y-%m-%d %X", time.localtime())
    subject = "审核不通过 审核人：%s 审核时间：%s" % (request.user.username, check_time)
    send_mail(subject=subject, message=message, from_email=EMAIL_HOST_USER, recipient_list=recipient_list)
    for id in ids:
        CmsCheck.objects.filter(id=id).update(status=CheckStatu.WAIT_SUBMIT)
    return HttpResponse(0)


# @login_required
# @permission_required(u'%s.%s' % (AuthCodeName.APP_LABEL,AuthCodeName.CHECK), raise_exception=True)
# def check_reject(request):
#     """
#     审核拒绝
#     :param url: {% url 'check_reject' %}
#     :param  ids: 审核表id列表
#             message:审核不通过的信息
#             recipient_list 收件人列表
#     """
#
#     ids = json.loads(request.POST.get("ids"))
#     message = request.POST.get("message")
#     recipient_list = json.loads(request.POST.get("recipient_list"))
#     check_time = time.strftime("%Y-%m-%d %X",time.localtime())
#     subject = "审核不通过 审核人：%s 审核时间：%s" % (request.user.username,check_time)
#     send_mail(subject=subject,message=message,from_email=EMAIL_HOST_USER,recipient_list=recipient_list)
#
#     for id in ids:
#         #新增这条然后删除
#         oCmsChecks=CmsCheck.objects.filter(id=id)
#         for oCmsCheck in oCmsChecks:
#             #审核不通过新建的直接干掉
#             try:
#                 if oCmsCheck.op_type==int(CheckOpType.NEW):
#                     if oCmsCheck.table_name=="CmsChannelChannel":
#                         revert_channelchannel(oCmsCheck.data_id)
#                     else:
#                         #驳回新增：要删除这条新增的，删除审核表中后续对这表数据所做的修改
#                         eval(oCmsCheck.table_name).objects.get(id=oCmsCheck.data_id).delete()
#                         # delobjs = CmsCheck.objects.filter(channel_id=oCmsCheck.channel_id,table_name=oCmsCheck.table_name,data_id=oCmsCheck.data_id)
#                         oCmsCheck.delete()
#                         # delobjs.delete()
#                 #正式库覆盖默认库
#                 elif oCmsCheck.op_type==int(CheckOpType.EDIT):
#                     #判断此备份库的修改对象是否存在第二次修改，若无第二次修改，就直接拿正式库覆盖默认库。
#                     #若有第二次更改就不做任何操作
#                     # if CmsCheck.objects.filter(id>oCmsCheck.id,channel_id=oCmsCheck.channel_id,table_name = oCmsCheck.table_name,data_id=oCmsCheck.data_id):
#                     #     pass
#                     # else:
#                     table_obj = eval(oCmsCheck.table_name).objects.using("online").get(id=oCmsCheck.data_id)
#                     table_obj.save(using="default")
#                 else:
#                     #删除首页下面的渠道进行驳回
#                     if oCmsCheck.table_name=='CmsChannels':
#                         recovery_channel(oCmsCheck.data_id)
#                     table_obj = eval(oCmsCheck.table_name).objects.using("online").get(id=oCmsCheck.data_id)
#                     table_obj.save(using="default")
#                 oCmsCheck.status=CheckStatu.REJECT
#                 oCmsCheck.check_person = request.user.username
#                 oCmsCheck.check_date = check_time
#                 oCmsCheck.save()
#             except Exception as ex:
#                 print(ex)
#                 oCmsCheck.status=CheckStatu.CHECK_ERROR
#                 oCmsCheck.check_person = request.user.username
#                 oCmsCheck.check_date = check_time
#                 oCmsCheck.save()
#     return HttpResponse(0)


# 渠道关联驳回
# 1.从备份库删除目标渠道
# 2.从正式库恢复目标渠道到备份库
# 3.从正式库中渠道关联表里面和目标渠道关联的，恢复到备份库关联渠道表中
def revert_channelchannel(data_id):
    oCmsChannelChannel = CmsChannelChannel.objects.get(id=data_id)
    config_items = oCmsChannelChannel.config_items.split(",")[1:-1]
    target_channel = oCmsChannelChannel.channel_id2
    # 从渠道关联表中删除这条记录
    oCmsChannelChannel.delete()
    # 从备份库删除目标渠道
    DelChannel.del_config_channel(target_channel, config_items)
    # 从正式库恢复目标渠道到备份库
    recovery_channel(target_channel)


# 正式库的配置项判断这个对应的渠道是否有内容
# 如果该配置项和这个渠道有关联，通过关联表找到这个配置项所在内容的id
# 判断这条数据是否在备份库中，如果不在，就复制回来，如果在不复制
def recovery_channel(channel_id):
    # 活动
    objs = CmsViewActivity.objects.using("online").filter(channel_id=channel_id)
    for obj in objs:
        # 判断备份库里面是否有这条
        oCmsActivities = CmsActivities.objects.filter(id=obj.activity_id)
        # 不存在从正式库中复制到备份库中
        if not oCmsActivities:
            oCmsActivities = CmsActivities.objects.using("online").filter(id=obj.activity_id)
        for oCmsActivity in oCmsActivities:
            oCmsActivity.save(using="default")
            # 活动和渠道的关联关系也需要复制
            obj.save(using="default")

    # 广告
    objs = CmsViewAd.objects.using("online").filter(channel_id=channel_id)
    for obj in objs:
        # 判断备份库中是否存在这条,如果不存在从正式库复制到备份库
        oCmsAds = CmsAds.objects.filter(id=obj.ad_id)
        if not oCmsAds:
            oCmsAds = CmsAds.objects.using("online").filter(id=obj.ad_id)
        for oCmsAd in oCmsAds:
            # 恢复广告组
            oCmsAd.save(using="default")
            # 恢复广告组和广告关联表
            obj.save(using="default")

            # 从正式库中筛选出广告，如果此广告不在备份库中，就从正式库复制到备份库中
            oCmsAdsBeans = CmsAdsBeans.objects.using("online").filter(ad_id=oCmsAd.id)

            for oCmsAdsBean in oCmsAdsBeans:
                if not CmsAdbeans.objects.filter(id=oCmsAdsBean.bean_id):
                    # 恢复广告
                    oCmsAdsBean.bean.save(using="default")
                # 恢复广告和广告组关联表（这条信息存在也许关系不存在同样需要复制）
                oCmsAdsBean.save(using="default")
    # 分类页服务
    objs = CmsViewNavi.objects.using("online").filter(channel_id=channel_id)
    for obj in objs:
        oCmsNavicategories = CmsNavicategories.objects.filter(id=obj.navicat_id)
        # 不在备份库中从正式库中拿出来覆盖
        if not oCmsNavicategories:
            oCmsNavicategories = CmsNavicategories.objects.using("online").filter(id=obj.navicat_id)
        for oCmsNavicategory in oCmsNavicategories:
            # 恢复分类页服务组
            oCmsNavicategory.save(using="default")
            # 恢复分类页服务组和渠道关联
            obj.save(using="default")
            # 查看正式库中的分类页--分类
            oCmsNavicatesCategorys = CmsNavicatesCategory.objects.using("online").filter(cate_id=oCmsNavicategory.id)
            for oCmsNavicatesCategory in oCmsNavicatesCategorys:
                # if not CmsNaviCategory.objects.filter(id=oCmsNavicatesCategory.category_id):
                #     #恢复分类
                #     oCmsNavicatesCategory.category.save(using="default")
                # 恢复分类页组和分类关联
                oCmsNavicatesCategory.save(using="default")
            # 分类页---服务
            oCmsNavicatesServices = CmsNavicatesServices.objects.using("online").filter(cate_id=oCmsNavicategory.id)
            for oCmsNavicatesService in oCmsNavicatesServices:
                if not CmsServices.objects.get(id=oCmsNavicatesService.service_id):
                    oCmsNavicatesService.service.save(using="default")
                oCmsNavicatesService.save(using="default")
            oCmsNavicatesGoods = CmsNavicatesGoods.objects.using("online").filter(cate_id=oCmsNavicategory.id)
            for oCmsNavicatesGood in oCmsNavicatesGoods:
                if not CmsGoods.objects.get(id=oCmsNavicatesGood.goods_id):
                    oCmsNavicatesGood.goods.save(using="default")
                oCmsNavicatesGood.save(using="default")

    # 精品分类
    objs = CmsViewChoicenessCategory.objects.using("online").filter(channel_id=channel_id)
    for obj in objs:
        oCmsChoicenessCategorys = CmsChoicenessCategory.objects.filter(id=obj.choiceness_category_id)
        if not oCmsChoicenessCategorys:
            oCmsChoicenessCategorys = CmsChoicenessCategory.objects.using("online")
        for oCmsChoicenessCategory in oCmsChoicenessCategorys:
            oCmsChoicenessCategory.save(using="default")
            obj.save(using="default")

    # 常用服务
    objs = CmsViewService.objects.using("online").filter(channel_id=channel_id)
    for obj in objs:
        if obj.open_type == 0:
            oCmsServices = CmsServices.objects.filter(id=obj.service_id)
            if not oCmsServices:
                oCmsServices = CmsServices.objects.using("online").filter(id=obj.service_id)
            for oCmsService in oCmsServices:
                oCmsService.save(using="default")
                obj.save(using="default")
        if obj.open_type == 1:
            oCmsGoods = CmsGoods.objects.filter(id=obj.service_id)
            if not oCmsGoods:
                oCmsGoods = CmsGoods.objects.using("online").filter(id=obj.service_id)
            for oCmsGood in oCmsGoods:
                oCmsGood.save(using="default")
                obj.save(using="default")
        if obj.open_type == 3 or obj.open_type == 4:
            obj.save(using="default")
    # 运营配置
    objs = CmsViewOpconfig.objects.using("online").filter(channel_id=channel_id)
    for obj in objs:
        oCmsOpconfigs = CmsOpconfig.objects.filter(id=obj.opconfig_id)
        if not oCmsOpconfigs:
            oCmsOpconfigs = CmsOpconfig.objects.using("online").filter(id=obj.opconfig_id)
        for oCmsOpconfig in oCmsOpconfigs:
            oCmsOpconfig.save(using="default")
            obj.save(using="default")
    # 优惠券
    objs = CmsViewCoupon.objects.using("online").filter(channel_id=channel_id)
    for obj in objs:
        oCmsCoupons = CmsCoupon.objects.filter(id=obj.coupon_id)
        if not oCmsCoupons:
            oCmsCoupons = CmsCoupon.objects.using("online").filter(id=obj.coupon_id)
        for oCmsCoupon in oCmsCoupons:
            oCmsCoupon.save(using="default")
            obj.save(using="default")
    # 发现页专题
    objs = CmsViewFindTopic.objects.using("online").filter(channel_id=channel_id)
    for obj in objs:
        obj.save(using="default")
    # 首页专题
    objs = CmsViewHomepageTopic.objects.using("online").filter(channel_id=channel_id)
    for obj in objs:
        obj.save(using="default")
    # 猜你喜欢
    objs = CmsViewLike.objects.using("online").filter(channel_id=channel_id)
    for obj in objs:
        oCmsLikes = CmsLikes.objects.filter(id=obj.like_id)
        if not oCmsLikes:
            oCmsLikes = CmsLikes.objects.using("online").filter(id=obj.like_id)
        for oCmsLike in oCmsLikes:
            oCmsLike.save(using="default")
            obj.save(using="default")
            # 猜你喜欢--商品
            oCmsLikesGoods = CmsLikesGoods.objects.using("online").filter(like_id=oCmsLike.id)
            for oCmsLikeGood in oCmsLikesGoods:
                if not CmsGoods.objects.get(id=oCmsLikeGood.goods_id):
                    oCmsLikeGood.goods.save(using="default")
                # 存在
                oCmsLikeGood.save(using="default")
            # 猜你喜欢--服务
            oCmsLikesServices = CmsLikesServices.objects.using("online").filter(like_id=oCmsLike.id)
            for oCmsLikesService in oCmsLikesServices:
                if not CmsServices.objects.filter(id=oCmsLikesService.service_id):
                    oCmsLikesService.service.save(using="default")
                oCmsLikesService.save(using="default")
    # 内容流
    objs = CmsViewStream.objects.using("online").filter(channel_id=channel_id)
    for obj in objs:
        oCmsStreamcontents = CmsStreamcontent.objects.filter(id=obj.streamcontent_id)
        if not oCmsStreamcontents:
            oCmsStreamcontents = CmsStreamcontent.objects.using("online").filter(id=obj.streamcontent_id)
        for oCmsStreamcontent in oCmsStreamcontents:
            oCmsStreamcontent.save(using="default")
            obj.save(using="default")
            oCmsStreamcontentsBeans = CmsStreamcontentsBeans.objects.using("online").filter(
                streamcontent_id=oCmsStreamcontent.id)
            for oCmsStreamcontentsBean in oCmsStreamcontentsBeans:
                if not CmsStreamcontentbeans.objects.filter(id=oCmsStreamcontentsBean.bean_id):
                    oCmsStreamcontentsBean.bean.save(using="default")
                oCmsStreamcontentsBean.save(using="default")
            oCmsStreamcontentsGoods = CmsStreamcontentsGoods.objects.using("online").filter(
                streamcontent_id=oCmsStreamcontent.id)
            for oCmsStreamcontentsGood in oCmsStreamcontentsGoods:
                if not CmsGoods.objects.filter(id=oCmsStreamcontentsGood.goods_id):
                    oCmsStreamcontentsGood.goods.save(using="default")
                oCmsStreamcontentsGood.save(using="default")
    # 二级分类
    objs = CmsViewCategoryitem.objects.using("online").filter(channel_id=channel_id)
    for obj in objs:
        oCmsCategoryItems = CmsCategoryItem.objects.filter(id=obj.category_item_id)
        if not oCmsCategoryItems:
            oCmsCategoryItems = CmsCategoryItem.objects.using("online").filter(id=obj.category_item_id)
        for oCmsCategoryItem in oCmsCategoryItems:
            oCmsCategoryItem.save(using="default")
            obj.save(using="default")
            oCmsCategoryitemItembeans = CmsCategoryitemItembean.objects.using("online").filter(
                category_item_id=oCmsCategoryItem.id)
            for oCmsCategoryitemItembean in oCmsCategoryitemItembeans:
                if not CmsCategoryItembean.objects.filter(id=oCmsCategoryitemItembean.item_bean_id):
                    oCmsCategoryitemItembean.item_bean.save(using="default")
                oCmsCategoryitemItembean.save(using="default")
    # 开屏广告
    objs = CmsViewScreenads.objects.using("online").filter(channel_id=channel_id)
    for obj in objs:
        oCmsScreenads = CmsScreenads.objects.filter(id=obj.screenad_id)
        if not oCmsScreenads:
            oCmsScreenads = CmsScreenads.objects.using("online").filter(id=obj.screenad_id)
        for oCmsScreenad in oCmsScreenads:
            oCmsScreenad.save(using="default")
            obj.save(using="default")
    # 本地活动
    objs = CmsViewNativeActivity.objects.using("online").filter(channel_id=channel_id)
    for obj in objs:
        oCmsNativeActivities = CmsNativeActivity.objects.filter(id=obj.nactivity_id)
        if not oCmsNativeActivities:
            oCmsNativeActivities = CmsNativeActivity.objects.using("online").filter(id=obj.nactivity_id)
        for oCmsNativeActivity in oCmsNativeActivities:
            oCmsNativeActivity.save(using="default")
            obj.save(using="default")
    # 从正式库中渠道关联表里面和目标渠道关联的，恢复到备份库渠道关联表中
    channel_channels = CmsChannelChannel.objects.using("online").filter(
        Q(channel_id1=channel_id) | Q(channel_id2=channel_id))
    for channel_channel in channel_channels:
        channel_channel.save(using="default")
