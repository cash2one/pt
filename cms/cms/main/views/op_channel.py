#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'rong'
__mtime__ = '2015/10/15'
"""
import time
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
import json
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.http import require_POST

from cms.settings import CMS_CHECK_ON
from common.const import CONFIG_ITEMS, AuthCodeName, CmsModule, CheckOpType
# from main.views.main_pub import *
# from common.views import CONFIG_ITEMS
from main.views.del_channel import DelChannel
from main.models import CmsCheck, CmsChannelChannel, CmsChannels, CmsViewActivity, \
    CmsActivities, CmsViewAd, CmsAds, CmsAdbeans, CmsViewNavi, CmsNavicategories, \
    CmsServices, CmsGoods, CmsViewChoicenessCategory, CmsChoicenessCategory, \
    CmsViewService, CmsViewOpconfig, CmsOpconfig, CmsViewCoupon, CmsCoupon, CmsViewFindTopic, CmsViewHomepageTopic, \
    CmsViewLike, CmsLikes, CmsViewStream, CmsStreamcontent, \
    CmsStreamcontentbeans, CmsViewCategoryitem, CmsCategoryItem, \
    CmsCategoryItembean, CmsViewScreenads, CmsScreenads, CmsViewNativeActivity, CmsNativeActivity, CmsCpdisplay, \
    CmsActivityV37, CmsShareCoupon, CmsSecKill, CmsHomeCP, CmsViewActivity37, CmsViewShareCoupon, CmsSecKillViewTemp, \
    CmsActivityGoods, CmsActivityCP, CmsAdsBeans, CmsNavicatesServices, CmsNavicatesGoods, CmsNaviCategory, \
    CmsNavicatesCategory, CmsLikesServices, CmsLikesGoods, CmsStreamcontentsGoods, CmsStreamcontentsBeans, \
    CmsCategoryitemItembean
from main.views.main_pub import add_main_var, get_type_ver_channels


class OpChannel(object):
    def __init__(self, source_channel_id, database="default"):
        self.database = database
        self.source_channel_id = source_channel_id
        self.config_item_dic = {value: key.lower() for key, value in CONFIG_ITEMS.__dict__.items() if
                                key.find("__") == -1}

    def copy_asso(self, target_channel_id, config_items=None, channel_op_type="copy"):
        self.target_channel_id = target_channel_id
        self.target_channel = CmsChannels.objects.using(self.database).get(id=target_channel_id)
        if config_items == None:
            config_items = self.config_item_dic.keys()
        for config_item in config_items:
            fun = getattr(self, channel_op_type + "_" + self.config_item_dic[config_item])
            fun()
        op_type = 0
        if channel_op_type == 'associate':
            self.associate_others(config_items)
        else:
            op_type = 1
        ocmschannelchannel = CmsChannelChannel(channel_id1=self.source_channel_id, channel_id2=self.target_channel_id,
                                               config_items="," + ",".join(config_items) + ",", op_type=op_type)
        ocmschannelchannel.save(using=self.database)
        return ocmschannelchannel

    def associate_others(self, config_items):
        channel_channels = CmsChannelChannel.objects.using(self.database).filter(
            Q(channel_id1=self.source_channel_id) | Q(channel_id2=self.source_channel_id), op_type=0)
        for channel_channel in channel_channels:
            if channel_channel.channel_id1 == int(self.source_channel_id):
                new_config_items = set(config_items) & set(channel_channel.config_items.split(',')[1:-1])
                if len(new_config_items) > 0:
                    new_config_items = "," + ",".join(new_config_items) + ","
                    CmsChannelChannel(channel_id1=channel_channel.channel_id2, channel_id2=self.target_channel_id,
                                      config_items=new_config_items).save(using=self.database)
            else:
                new_config_items = set(config_items) & set(channel_channel.config_items.split(',')[1:-1])
                if len(new_config_items) > 0:
                    new_config_items = "," + ",".join(new_config_items) + ","
                    CmsChannelChannel(channel_id1=channel_channel.channel_id1, channel_id2=self.target_channel_id,
                                      config_items=new_config_items).save(using=self.database)

    # 复制品牌
    def copy_cp(self):
        cms_cpdises = CmsCpdisplay.objects.using(self.database).filter(cmshomecp__channel_id=self.source_channel_id)
        for cms_cpdis in cms_cpdises:
            cms_cpdis.id = None
            cms_cpdis.save(using=self.database)
            CmsHomeCP(cp=cms_cpdis, channel=self.target_channel).save(using=self.database)

    # 关联品牌
    def associate_cp(self):
        cms_cpdises = CmsCpdisplay.objects.using(self.database).filter(cmshomecp__channel_id=self.source_channel_id)
        for cms_cpdis in cms_cpdises:
            CmsHomeCP(cp=cms_cpdis, channel=self.target_channel).save(using=self.database)

    # 复制业务活动
    def copy_coupon_activity(self):
        coupon_activities = CmsActivityV37.objects.using(self.database).filter(
            cmsviewactivity37__channel_id=self.source_channel_id)
        for coupon_activity in coupon_activities:
            cps = coupon_activity.cp.all()
            goods = coupon_activity.goods.all()
            coupon_activity.id = None
            coupon_activity.save(using=self.database)
            CmsViewActivity37(channel=self.target_channel, activity=coupon_activity).save(using=self.database)
            for good in goods:
                acitvitygoods_ins, status = CmsActivityGoods.objects.using(self.database).get_or_create(
                    activity=coupon_activity, goods=good)
                acitvitygoods_ins.save(using=self.database)
            for cp in cps:
                activitycp_ins, status = CmsActivityCP.objects.using(self.database).get_or_create(
                    activity=coupon_activity, cp=cp)
                activitycp_ins.save(using=self.database)

    # 关联业务活动
    def associate_coupon_activity(self):
        coupon_activities = CmsActivityV37.objects.using(self.database).filter(
            cmsviewactivity37__channel_id=self.source_channel_id)
        for coupon_activity in coupon_activities:
            CmsViewActivity37(channel=self.target_channel, activity=coupon_activity).save(using=self.database)

    # 复制本地活动
    def copy_native_activity(self):
        native_activities = CmsNativeActivity.objects.using(self.database).filter(
            cmsviewnativeactivity__channel_id=self.source_channel_id)
        for native_activity in native_activities:
            native_activity.id = None
            native_activity.save(using=self.database)
            CmsViewNativeActivity(nactivity=native_activity, channel=self.target_channel).save(using=self.database)

    # 关联本地活动
    def associate_native_activity(self):
        native_activities = CmsNativeActivity.objects.using(self.database).filter(
            cmsviewnativeactivity__channel_id=self.source_channel_id)
        for native_activity in native_activities:
            CmsViewNativeActivity(nactivity=native_activity, channel=self.target_channel).save(using=self.database)

    # 复制开屏广告
    def copy_screen_ad(self):
        screen_ads = CmsScreenads.objects.using(self.database).filter(
            cmsviewscreenads__channel_id=self.source_channel_id)
        for screen_ad in screen_ads:
            screen_ad.id = None
            screen_ad.save(using=self.database)
            CmsViewScreenads(screenad=screen_ad, channel=self.target_channel).save(using=self.database)

    # 关联开屏广告
    def associate_screen_ad(self):
        screen_ads = CmsScreenads.objects.using(self.database).filter(
            cmsviewscreenads__channel_id=self.source_channel_id)
        for screen_ad in screen_ads:
            CmsViewScreenads(screenad=screen_ad, channel=self.target_channel).save(using=self.database)

    # 复制活动
    def copy_activity(self):
        activities = CmsActivities.objects.using(self.database).filter(
            cmsviewactivity__channel_id=self.source_channel_id)
        for activity in activities:
            # 复制活动
            activity.id = None
            activity.save(using=self.database)
            CmsViewActivity(activity=activity, channel=self.target_channel).save(using=self.database)

    # 关联活动
    def associate_activity(self):
        activities = CmsActivities.objects.using(self.database).filter(
            cmsviewactivity__channel_id=self.source_channel_id)
        for activity in activities:
            CmsViewActivity(activity=activity, channel=self.target_channel).save(using=self.database)

    def copy_ad(self):
        # 广告
        ads = CmsAds.objects.using(self.database).filter(cmsviewad__channel_id=self.source_channel_id)
        for ad in ads:
            # 保存原来的id
            ad_id = ad.id
            # 复制广告组
            ad.id = None
            ad.save(using=self.database)
            CmsViewAd(ad=ad, channel=self.target_channel).save(using=self.database)
            beans = CmsAdbeans.objects.using(self.database).filter(cmsadsbeans__ad_id=ad_id)
            for bean in beans:
                # 复制广告
                bean.id = None
                bean.save(using=self.database)
                CmsAdsBeans(ad=ad, bean=bean).save(using=self.database)

    def associate_ad(self):
        ads = CmsAds.objects.using(self.database).filter(cmsviewad__channel_id=self.source_channel_id)
        for ad in ads:
            CmsViewAd(ad=ad, channel=self.target_channel).save(using=self.database)

    # 复制分类页服务
    def copy_category_page_services(self):
        # 分类页服务(导航)
        groups = CmsNavicategories.objects.using(self.database).filter(cmsviewnavi__channel_id=self.source_channel_id)
        for group in groups:
            # 复制分类页服务组
            cate_id = group.id
            group.id = None
            group.save(using=self.database)
            CmsViewNavi(navicat=group, channel=self.target_channel, status=0).save(using=self.database)
            services = CmsServices.objects.using(self.database).filter(cmsnavicatesservices__cate_id=cate_id)
            for service in services:
                service.id = None
                service.save(using=self.database)
                CmsNavicatesServices(cate=group, service=service).save(using=self.database)
            goods = CmsGoods.objects.using(self.database).filter(cmsnavicatesgoods__cate_id=cate_id)
            for good in goods:
                good.id = None
                good.save(using=self.database)
                CmsNavicatesGoods(cate=group, goods=good).save(using=self.database)
            categories = CmsNaviCategory.objects.using(self.database).filter(cmsnavicatescategory__cate_id=cate_id)
            for category in categories:
                # 所有渠道共用分类基础库数据
                CmsNavicatesCategory(cate=group, category=category).save(using=self.database)

    # 关联分类页服务
    def associate_category_page_services(self):
        groups = CmsNavicategories.objects.using(self.database).filter(cmsviewnavi__channel_id=self.source_channel_id)
        for group in groups:
            # 关联分类页服务组
            CmsViewNavi(navicat=group, channel=self.target_channel, status=0).save(using=self.database)

    # 复制精品分类
    def copy_choiceness_category(self):
        choicenesscategories = CmsChoicenessCategory.objects.using(self.database).filter(
            cmsviewchoicenesscategory__channel_id=self.source_channel_id)
        for choicenesscategory in choicenesscategories:
            choicenesscategory.id = None
            choicenesscategory.save(using=self.database)
            CmsViewChoicenessCategory(choiceness_category=choicenesscategory, channel=self.target_channel).save(
                using=self.database)

    # 关联精品分类
    def associate_choiceness_category(self):
        choicenesscategories = CmsChoicenessCategory.objects.using(self.database).filter(
            cmsviewchoicenesscategory__channel_id=self.source_channel_id)
        for choicenesscategory in choicenesscategories:
            CmsViewChoicenessCategory(choiceness_category=choicenesscategory, channel=self.target_channel).save(
                using=self.database)

    # 复制常用服务
    def copy_common_services(self):
        view_services = CmsViewService.objects.using(self.database).filter(channel_id=self.source_channel_id)
        for view_service in view_services:
            try:
                if view_service.open_type == 0:
                    serviceobj = CmsServices.objects.using(self.database).get(id=view_service.service_id)
                    serviceobj.id = None
                    serviceobj.save(using=self.database)
                    CmsViewService(service_id=serviceobj.id, channel=self.target_channel,
                                   open_type=view_service.open_type).save(using=self.database)
                elif view_service.open_type == 1:
                    goodobj = CmsGoods.objects.using(self.database).get(id=view_service.service_id)
                    goodobj.id = None
                    goodobj.save(using=self.database)
                    CmsViewService(service_id=goodobj.id, channel=self.target_channel,
                                   open_type=view_service.open_type).save(using=self.database)
                else:
                    CmsViewService(service_id=view_service.service_id, channel=self.target_channel,
                                   open_type=view_service.open_type).save(using=self.database)
            except Exception as ex:
                print(ex)
                continue

    # 关联常用服务
    def associate_common_services(self):
        view_services = CmsViewService.objects.using(self.database).filter(channel_id=self.source_channel_id)
        for view_service in view_services:
            view_service.channel_id = self.target_channel_id
            view_service.id = None
            view_service.save(using=self.database)

    # 复制运营配置
    def copy_config_operation(self):
        opconfigs = CmsOpconfig.objects.using(self.database).filter(cmsviewopconfig__channel_id=self.source_channel_id)
        for opconfig in opconfigs:
            opconfig.id = None
            opconfig.save(using=self.database)
            CmsViewOpconfig(opconfig=opconfig, channel=self.target_channel).save(using=self.database)

    # 关联运营配置
    def associate_config_operation(self):
        opconfigs = CmsOpconfig.objects.using(self.database).filter(cmsviewopconfig__channel_id=self.source_channel_id)
        for opconfig in opconfigs:
            CmsViewOpconfig(opconfig=opconfig, channel=self.target_channel).save(using=self.database)

    def copy_coupons(self):
        coupons = CmsCoupon.objects.using(self.database).filter(cmsviewcoupon__channel_id=self.source_channel_id)
        for coupon in coupons:
            coupon.id = None
            coupon.save(using=self.database)
            CmsViewCoupon(coupon=coupon,
                          channel=CmsChannels.objects.using(self.database).get(id=self.target_channel_id)).save(
                using=self.database)

    def associate_coupons(self):
        coupons = CmsCoupon.objects.using(self.database).filter(cmsviewcoupon__channel_id=self.source_channel_id)
        for coupon in coupons:
            CmsViewCoupon(coupon=coupon,
                          channel=CmsChannels.objects.using(self.database).get(id=self.target_channel_id)).save(
                using=self.database)

    def copy_foundpage(self):
        viewfoundpages = CmsViewFindTopic.objects.using(self.database).filter(channel_id=self.source_channel_id)
        for viewfoundpage in viewfoundpages:
            viewfoundpage.id = None
            viewfoundpage.channel_id = self.target_channel_id
            viewfoundpage.save(using=self.database)

    def associate_foundpage(self):
        viewfoundpages = CmsViewFindTopic.objects.using(self.database).filter(channel_id=self.source_channel_id)
        for viewfoundpage in viewfoundpages:
            viewfoundpage.id = None
            viewfoundpage.channel_id = self.target_channel_id
            viewfoundpage.save(using=self.database)

    def copy_homepage(self):
        viewhomepages = CmsViewHomepageTopic.objects.using(self.database).filter(channel_id=self.source_channel_id)
        for viewhomepage in viewhomepages:
            viewhomepage.id = None
            viewhomepage.channel_id = self.target_channel_id
            viewhomepage.save(using=self.database)

    def associate_homepage(self):
        viewhomepages = CmsViewHomepageTopic.objects.using(self.database).filter(channel_id=self.source_channel_id)
        for viewhomepage in viewhomepages:
            viewhomepage.id = None
            viewhomepage.channel_id = self.target_channel_id
            viewhomepage.save(using=self.database)

    def copy_likes(self):
        likes = CmsLikes.objects.using(self.database).filter(cmsviewlike__channel_id=self.source_channel_id)
        for like in likes:
            like_id = like.id
            like.id = None
            like.save(using=self.database)
            CmsViewLike(like=like, channel=self.target_channel).save(using=self.database)
            services = CmsServices.objects.using(self.database).filter(cmslikesservices__like_id=like_id)
            for service in services:
                service.id = None
                service.save(using=self.database)
                CmsLikesServices(service=service, like=like).save(using=self.database)
            goods = CmsGoods.objects.using(self.database).filter(cmslikesgoods__like_id=like_id)
            for good in goods:
                good.id = None
                good.save(using=self.database)
                CmsLikesGoods(goods=good, like=like).save(using=self.database)

    def associate_likes(self):
        likes = CmsLikes.objects.using(self.database).filter(cmsviewlike__channel_id=self.source_channel_id)
        for like in likes:
            CmsViewLike(like=like, channel=self.target_channel).save(using=self.database)

    def copy_streams(self):
        streamcontents = CmsStreamcontent.objects.using(self.database).filter(
            cmsviewstream__channel_id=self.source_channel_id)
        for streamcontent in streamcontents:
            streamcontent_id = streamcontent.id
            streamcontent.id = None
            streamcontent.save(using=self.database)
            CmsViewStream(streamcontent=streamcontent, channel=self.target_channel, status=0).save(using=self.database)
            goods = CmsGoods.objects.using(self.database).filter(
                cmsstreamcontentsgoods__streamcontent_id=streamcontent_id)
            for good in goods:
                good.id = None
                good.save(using=self.database)
                CmsStreamcontentsGoods(streamcontent=streamcontent, goods=good).save(using=self.database)
            streambeans = CmsStreamcontentbeans.objects.using(self.database).filter(
                cmsstreamcontentsbeans__streamcontent_id=streamcontent_id)
            for streambean in streambeans:
                streambean.id = None
                streambean.save(using=self.database)
                CmsStreamcontentsBeans(streamcontent=streamcontent, bean=streambean).save(using=self.database)

    def associate_streams(self):
        streamcontents = CmsStreamcontent.objects.using(self.database).filter(
            cmsviewstream__channel_id=self.source_channel_id)
        for streamcontent in streamcontents:
            CmsViewStream(streamcontent=streamcontent, channel=self.target_channel, status=0).save(using=self.database)

    def copy_second_category(self):
        categoryitems = CmsCategoryItem.objects.using(self.database).filter(
            cmsviewcategoryitem__channel_id=self.source_channel_id)
        for categoryitem in categoryitems:
            categoryitem_id = categoryitem.id
            categoryitem.id = None
            categoryitem.save(using=self.database)
            CmsViewCategoryitem(category_item=categoryitem, channel=self.target_channel).save(using=self.database)
            categoryitembeans = CmsCategoryItembean.objects.using(self.database).filter(
                cmscategoryitemitembean__category_item_id=categoryitem_id)
            for categoryitembean in categoryitembeans:
                categoryitembean.id = None
                categoryitembean.save(using=self.database)
                CmsCategoryitemItembean(category_item=categoryitem, item_bean=categoryitembean).save(
                    using=self.database)

    def associate_second_category(self):
        categoryitems = CmsCategoryItem.objects.using(self.database).filter(
            cmsviewcategoryitem__channel_id=self.source_channel_id)
        for categoryitem in categoryitems:
            CmsViewCategoryitem(category_item=categoryitem, channel=self.target_channel).save(using=self.database)

    # 复制分享券
    def copy_share_coupon(self):
        coupons = CmsShareCoupon.objects.using(self.database).filter(
            cmsviewsharecoupon__channel_id=self.source_channel_id)
        for coupon in coupons:
            coupon.id = None
            coupon.save(using=self.database)
            CmsViewShareCoupon(share_coupon=coupon, channel=self.target_channel).save(using=self.database)

    # 关联分享券
    def associate_share_coupon(self):
        coupons = CmsShareCoupon.objects.using(self.database).filter(
            cmsviewsharecoupon__channel_id=self.source_channel_id)
        for coupon in coupons:
            CmsViewShareCoupon(share_coupon=coupon, channel=self.target_channel).save(using=self.database)

    # 复制秒杀活动
    def copy_seckills(self):
        seckills = CmsSecKill.objects.using(self.database).filter(cmsseckillviewtemp__channel_id=self.source_channel_id)
        for sk in seckills:
            sk.id = None
            sk.save(using=self.database)
            CmsSecKillViewTemp(seckill=sk, channel=self.target_channel, status=0).save(using=self.database)

    # 关联秒杀活动
    def associate_seckills(self):
        seckills = CmsSecKill.objects.using(self.database).filter(cmsseckillviewtemp__channel_id=self.source_channel_id)
        for sk in seckills:
            CmsSecKillViewTemp(seckill=sk, channel=self.target_channel, status=0).save(using=self.database)


"""
 渠道关联和复制
 url :{% url 'channel_op' %}
:请求方式：ajax Post
:请求参数：source_channel_id 源渠道id
          target_channel_list  目标渠道id 列表[target_channel_id1,target_channel_id2]
          config_items 配置项列表 例如：[activity,ads......]
          channel_op_type 操作类型 copy:渠道复制 associate:渠道关联
:类型 :传数字
返回： 成功：0 错误：错误信息
"""


@login_required
@permission_required(u'%s.%s' % (AuthCodeName.APP_LABEL, AuthCodeName.CONFIG), raise_exception=True)
@require_POST
def channel_op(request):
    if request.method == 'POST':
        data = request.POST.copy()
        error = ""
        for key in data:
            if data[key] == "":
                error += key + " is null \n"
        if error:
            return HttpResponse(error)
        else:
            try:
                config_items = json.loads(request.POST.get("config_items"))
                channel_op_type = request.POST.get("channel_op_type")
                source_channel_id = request.POST.get("source_channel_id")
                target_channel_list = json.loads(request.POST.get("target_channel_list"))
                config_items = sorted(config_items)
                op_channel = OpChannel(source_channel_id)
                for target_channel_id in target_channel_list:
                    # 清空目标渠道的数据
                    DelChannel.del_config_channel(target_channel_id, config_items)
                    ocms_channel_channel = op_channel.copy_asso(target_channel_id, config_items=config_items,
                                                                channel_op_type=channel_op_type)
                    if CMS_CHECK_ON:
                        CmsCheck(module=CmsModule.MAIN_CHANNEL,
                                 table_name='CmsChannelChannel',
                                 data_id=ocms_channel_channel.id,
                                 op_type=CheckOpType.NEW,
                                 alter_person=request.user.username,
                                 alter_date=time.strftime("%Y-%m-%d %X", time.localtime())).save()
                return HttpResponse(0)
            except Exception as ex:
                return HttpResponse(ex.args[0])


@login_required
@permission_required(u'%s.%s' % (AuthCodeName.APP_LABEL, AuthCodeName.CONFIG), raise_exception=True)
@add_main_var
def copy_associate(request, template_name):
    type_ver_channels = get_type_ver_channels()
    return render_to_response(template_name, {
        "CONFIG_ITEMS": CONFIG_ITEMS,
        "type_ver_channels": type_ver_channels
    }, context_instance=RequestContext(request))
