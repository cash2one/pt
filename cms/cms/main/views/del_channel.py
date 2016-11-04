# coding: utf-8

"""
    删除渠道
"""

# from common.views import *
import time
from django.db.models import Q

from cms.settings import CMS_CHECK_ON
from common.const import CONFIG_ITEMS, CmsModule, CheckOpType, CheckStatu
from common.views import get_relate_channel_list
from main.models import CmsCheck, CmsChannelChannel, CmsChannels, CmsViewActivity, \
    CmsActivities, CmsViewAd, CmsAds, CmsAdbeans, CmsViewNavi, CmsNavicategories, \
    CmsServices, CmsGoods, CmsViewChoicenessCategory, CmsChoicenessCategory, \
    CmsViewService, CmsViewOpconfig, CmsOpconfig, CmsViewCoupon, CmsCoupon, CmsViewFindTopic, CmsViewHomepageTopic, \
    CmsViewLike, CmsLikes, CmsViewStream, CmsStreamcontent, \
    CmsStreamcontentbeans, CmsViewCategoryitem, CmsCategoryItem, \
    CmsCategoryItembean, CmsViewScreenads, CmsScreenads, CmsViewNativeActivity, CmsNativeActivity, CmsCpdisplay, \
    CmsActivityV37, CmsShareCoupon, CmsSecKill, CmsHomeCP, CmsViewActivity37, CmsViewShareCoupon, CmsSecKillViewTemp, \
    CmsChannelsAppVersion


class DelChannel(object):
    @classmethod
    def del_ads(cls, channel_id, db="default"):
        """删除广告-非关联关系"""
        ads = CmsAds.objects.using(db).filter(cmsviewad__channel_id=channel_id)
        for ad in ads:
            CmsAdbeans.objects.using(db).filter(cmsadsbeans__ad=ad).delete()
        ads.delete()

    @classmethod
    def del_common_services(cls, channel_id, db="default"):
        """删除常用服务-非关联关系"""
        view_services = CmsViewService.objects.using(db).filter(open_type=0, channel_id=channel_id)
        for view_service in view_services:
            try:
                CmsServices.objects.using(db).get(id=view_service.service_id).delete()
            except Exception as ex:
                print(ex)
                continue
        view_goods = CmsViewService.objects.using(db).filter(open_type=1, channel_id=channel_id)
        for view_good in view_goods:
            try:
                CmsGoods.objects.using(db).get(id=view_good.service_id).delete()
            except Exception as ex:
                print(ex)
                continue

    @classmethod
    def del_cate_page_services(cls, channel_id, db="default"):
        """删除分类页-非关联关系"""
        groups = CmsNavicategories.objects.using(db).filter(cmsviewnavi__channel_id=channel_id)
        for group in groups:
            CmsServices.objects.using(db).filter(cmsnavicatesservices__cate=group).delete()
            CmsGoods.objects.using(db).filter(cmsnavicatesgoods__cate=group).delete()
        groups.delete()

    @classmethod
    def del_streams(cls, channel_id, db="default"):
        """删除内容流-非关联关系"""
        groups = CmsStreamcontent.objects.using(db).filter(cmsviewstream__channel_id=channel_id)
        for group in groups:
            CmsGoods.objects.using(db).filter(cmsstreamcontentsgoods__streamcontent=group).delete()
            CmsStreamcontentbeans.objects.using(db).filter(cmsstreamcontentsbeans__streamcontent=group).delete()
        groups.delete()

    @classmethod
    def del_op_config(cls, channel_id, db="default"):
        """删除运营配置-非关联关系"""
        CmsOpconfig.objects.using(db).filter(cmsviewopconfig__channel=channel_id).delete()

    @classmethod
    def del_cp(cls, channel_id, db="default"):
        """删除品牌-非关联关系"""
        CmsCpdisplay.objects.using(db).filter(cmshomecp__channel_id=channel_id).delete()

    @classmethod
    def del_coupon_activity(cls, channel_id, db="default"):
        """删除业务活动-非关联关系"""
        CmsActivityV37.objects.using(db).filter(cmsviewactivity37__channel_id=channel_id).delete()

    @classmethod
    def del_likes(cls, channel_id, db="default"):
        """删除猜你喜欢-非关联关系"""
        groups = CmsLikes.objects.using(db).filter(cmsviewlike__channel_id=channel_id)
        for group in groups:
            CmsGoods.objects.using(db).filter(cmslikesgoods__like=group).delete()
            CmsServices.objects.using(db).filter(cmslikesservices__like=group).delete()
        groups.delete()

    @classmethod
    def del_activity(cls, channel_id, db="default"):
        """删除活动-非关联关系"""
        CmsActivities.objects.using(db).filter(cmsviewactivity__channel_id=channel_id).delete()

    @classmethod
    def del_choiceness(cls, channel_id, db="default"):
        """删除精品分类-非关联关系"""
        CmsChoicenessCategory.objects.using(db).filter(cmsviewchoicenesscategory__channel_id=channel_id).delete()

    @classmethod
    def del_coupon(cls, channel_id, db="default"):
        """删除优惠券-非关联关系"""
        CmsCoupon.objects.using(db).filter(cmsviewcoupon__channel_id=channel_id).delete()

    @classmethod
    def del_homepage(cls, channel_id, db="default"):
        """删除首页专题-非关联关系"""
        pass

    @classmethod
    def del_findpage(cls, channel_id, db="default"):
        """删除发现页专题-非关联关系"""
        # find_topics = CmsViewFindTopic.objects.using(db).filter(channel_id=channel_id)
        # for find_topic in find_topics:
        #     find_topic.is_deleted = 1
        #     find_topic.delete_time = timezone.now()
        #     find_topic.save()

        CmsViewFindTopic.objects.using(db).filter(channel_id=channel_id).delete()

    @classmethod
    def del_second_category(cls, channel_id, db="default"):
        """删除二级分类-非关联关系"""
        groups = CmsCategoryItem.objects.using(db).filter(cmsviewcategoryitem__channel_id=channel_id)
        for group in groups:
            CmsCategoryItembean.objects.using(db).filter(cmscategoryitemitembean__category_item=group).delete()
        groups.delete()

    @classmethod
    def del_screen_ads(cls, channel_id, db="default"):
        """删除开屏广告-非关联关系"""
        CmsScreenads.objects.using(db).filter(cmsviewscreenads__channel=channel_id).delete()

    @classmethod
    def del_native_activity(cls, channel_id, db="default"):
        """删除Native活动-非关联关系"""
        CmsNativeActivity.objects.using(db).filter(cmsviewnativeactivity__channel_id=channel_id).delete()

    @classmethod
    def del_share_coupon(cls, channel_id, db="default"):
        """删除分享券-非关联关系"""
        CmsShareCoupon.objects.using(db).filter(cmsviewsharecoupon__channel=channel_id).delete()

    @classmethod
    def del_seckills(cls, channel_id, db="default"):
        """删除秒杀活动-非关联关系"""
        CmsSecKill.objects.using(db).filter(cmsseckillviewtemp__channel=channel_id).delete()

    @classmethod
    def del_index_channel(cls, channel_id, db="default"):
        """
        首页删除渠道，就要删除渠道下面的所有配置内容
        :param channel_id:
        :return:
        """
        if CMS_CHECK_ON:
            CmsCheck.objects.filter(channel_id=channel_id).delete()
        channel = CmsChannels.objects.using(db).get(id=channel_id)
        # 广告
        if not get_relate_channel_list(channel_id, CONFIG_ITEMS.AD, db):
            cls.del_ads(channel_id, db)
        # 常用服务
        if not get_relate_channel_list(channel_id, CONFIG_ITEMS.COMMON_SERVICES, db):
            cls.del_common_services(channel_id, db)
        # 分类页服务
        if not get_relate_channel_list(channel_id, CONFIG_ITEMS.CATEGORY_PAGE_SERVICES, db):
            cls.del_cate_page_services(channel_id, db)
        # 内容流
        if not get_relate_channel_list(channel_id, CONFIG_ITEMS.STREAMS, db):
            cls.del_streams(channel_id, db)
        # 运营配置
        if not get_relate_channel_list(channel_id, CONFIG_ITEMS.CONFIG_OPERATION, db):
            cls.del_op_config(channel_id, db)
        # 猜你喜欢
        if not get_relate_channel_list(channel_id, CONFIG_ITEMS.LIKES, db):
            cls.del_likes(channel_id, db)
        # 活动
        if not get_relate_channel_list(channel_id, CONFIG_ITEMS.ACTIVITY, db):
            cls.del_activity(channel_id, db)
        # 精品分类
        if not get_relate_channel_list(channel_id, CONFIG_ITEMS.CHOICENESS_CATEGORY, db):
            cls.del_choiceness(channel_id, db)
        # 优惠券
        if not get_relate_channel_list(channel_id, CONFIG_ITEMS.COUPONS, db):
            cls.del_coupon(channel_id, db)
        # 二级分类
        if not get_relate_channel_list(channel_id, CONFIG_ITEMS.SECOND_CATEGORY, db):
            cls.del_second_category(channel_id, db)
        # 开屏广告
        if not get_relate_channel_list(channel_id, CONFIG_ITEMS.SCREEN_AD, db):
            cls.del_screen_ads(channel_id, db)
        # Native活动
        if not get_relate_channel_list(channel_id, CONFIG_ITEMS.NATIVE_ACTIVITY, db):
            cls.del_native_activity(channel_id, db)
        # 品牌
        if not get_relate_channel_list(channel_id, CONFIG_ITEMS.CP, db):
            cls.del_cp(channel_id, db)
        # 业务活动
        if not get_relate_channel_list(channel_id, CONFIG_ITEMS.COUPON_ACTIVITY, db):
            cls.del_coupon_activity(channel_id, db)
        # 分享券
        if not get_relate_channel_list(channel_id, CONFIG_ITEMS.SHARE_COUPON, db):
            cls.del_share_coupon(channel_id, db)

        # 秒杀
        if not get_relate_channel_list(channel_id, CONFIG_ITEMS.SECKILLS, db):
            cls.del_seckills(channel_id, db)
            pass

        # 首页专题
        cls.del_homepage(channel_id, db)
        # 发现页专题
        cls.del_findpage(channel_id, db)
        # 删除渠道关联表
        channel_channels = CmsChannelChannel.objects.using(db).filter(
            Q(channel_id1=channel_id) | Q(channel_id2=channel_id))
        if CMS_CHECK_ON:
            if db == "default":
                for channel_channel in channel_channels:
                    check = CmsCheck(
                        module=CmsModule.MAIN_CHANNEL,
                        table_name="CmsChannelChannel",
                        data_id=channel_channel.id,
                        op_type=CheckOpType.DELETE,
                        status=CheckStatu.WAIT_SUBMIT,
                        is_show=0,
                        alter_person="",
                        alter_date=time.strftime("%Y-%m-%d %X", time.localtime()))
                    check.save()
        channel_channels.delete()
        channel.delete()

    @classmethod
    def del_config_channel(cls, channel_id, config_items, db="default"):
        """
        关联/复制，删除渠道，根据配置项删除
        :param channel_id:
        :param config_items: 配置项，类型[ ]
        :return:
        """
        # 广告
        if CONFIG_ITEMS.AD in config_items:
            if not get_relate_channel_list(channel_id, CONFIG_ITEMS.AD, db):
                cls.del_ads(channel_id, db)
            else:
                CmsViewAd.objects.using(db).filter(channel_id=channel_id).delete()
        # 常用服务
        if CONFIG_ITEMS.COMMON_SERVICES in config_items:
            if not get_relate_channel_list(channel_id, CONFIG_ITEMS.COMMON_SERVICES, db):
                cls.del_common_services(channel_id, db)
                CmsViewService.objects.using(db).filter(channel_id=channel_id, open_type=3).delete()
                CmsViewService.objects.using(db).filter(channel_id=channel_id, open_type=4).delete()
            else:
                CmsViewService.objects.using(db).filter(channel_id=channel_id).delete()
        # 分类页服务
        if CONFIG_ITEMS.CATEGORY_PAGE_SERVICES in config_items:
            if not get_relate_channel_list(channel_id, CONFIG_ITEMS.CATEGORY_PAGE_SERVICES, db):
                cls.del_cate_page_services(channel_id, db)
            else:
                CmsViewNavi.objects.using(db).filter(channel_id=channel_id).delete()
        # 内容流
        if CONFIG_ITEMS.STREAMS in config_items:
            if not get_relate_channel_list(channel_id, CONFIG_ITEMS.STREAMS, db):
                cls.del_streams(channel_id, db)
            else:
                CmsViewStream.objects.using(db).filter(channel_id=channel_id).delete()
        # 运营配置
        if CONFIG_ITEMS.CONFIG_OPERATION in config_items:
            if not get_relate_channel_list(channel_id, CONFIG_ITEMS.CONFIG_OPERATION, db):
                cls.del_op_config(channel_id, db)
            else:
                CmsViewOpconfig.objects.using(db).filter(channel_id=channel_id).delete()
        # 猜你喜欢
        if CONFIG_ITEMS.LIKES in config_items:
            if not get_relate_channel_list(channel_id, CONFIG_ITEMS.LIKES, db):
                cls.del_likes(channel_id, db)
            else:
                CmsViewLike.objects.using(db).filter(channel_id=channel_id).delete()
        # 活动
        if CONFIG_ITEMS.ACTIVITY in config_items:
            if not get_relate_channel_list(channel_id, CONFIG_ITEMS.ACTIVITY, db):
                cls.del_activity(channel_id, db)
            else:
                CmsViewActivity.objects.using(db).filter(channel_id=channel_id).delete()
        # 精品分类
        if CONFIG_ITEMS.CHOICENESS_CATEGORY in config_items:
            if not get_relate_channel_list(channel_id, CONFIG_ITEMS.CHOICENESS_CATEGORY, db):
                cls.del_choiceness(channel_id, db)
            else:
                CmsViewChoicenessCategory.objects.using(db).filter(channel_id=channel_id).delete()
        # 优惠券
        if CONFIG_ITEMS.COUPONS in config_items:
            if not get_relate_channel_list(channel_id, CONFIG_ITEMS.COUPONS, db):
                cls.del_coupon(channel_id, db)
            else:
                CmsViewCoupon.objects.using(db).filter(channel_id=channel_id).delete()
        # 首页专题
        if CONFIG_ITEMS.HOMEPAGE in config_items:
            CmsViewHomepageTopic.objects.using(db).filter(channel_id=channel_id).delete()
        # 二级分类
        if CONFIG_ITEMS.SECOND_CATEGORY in config_items:
            if not get_relate_channel_list(channel_id, CONFIG_ITEMS.SECOND_CATEGORY, db):
                cls.del_second_category(channel_id, db)
            else:
                CmsViewCategoryitem.objects.using(db).filter(channel_id=channel_id).delete()
        # 发现页专题
        if CONFIG_ITEMS.FOUNDPAGE in config_items:
            cls.del_findpage(channel_id, db)
        # 开屏广告
        if CONFIG_ITEMS.SCREEN_AD in config_items:
            if not get_relate_channel_list(channel_id, CONFIG_ITEMS.SCREEN_AD, db):
                cls.del_screen_ads(channel_id, db)
            else:
                CmsViewScreenads.objects.using(db).filter(channel_id=channel_id).delete()
        # Native活动
        if CONFIG_ITEMS.NATIVE_ACTIVITY in config_items:
            if not get_relate_channel_list(channel_id, CONFIG_ITEMS.NATIVE_ACTIVITY, db):
                cls.del_native_activity(channel_id, db)
            else:
                CmsViewNativeActivity.objects.using(db).filter(channel_id=channel_id).delete()
        # 品牌
        if CONFIG_ITEMS.CP in config_items:
            if not get_relate_channel_list(channel_id, CONFIG_ITEMS.CP, db):
                cls.del_cp(channel_id, db)
            else:
                CmsHomeCP.objects.using(db).filter(channel_id=channel_id).delete()
        # 业务活动
        if CONFIG_ITEMS.COUPON_ACTIVITY in config_items:
            if not get_relate_channel_list(channel_id, CONFIG_ITEMS.COUPON_ACTIVITY, db):
                cls.del_coupon_activity(channel_id, db)
            else:
                CmsViewActivity37.objects.using(db).filter(channel_id=channel_id).delete()
        # 分享券
        if CONFIG_ITEMS.SHARE_COUPON in config_items:
            if not get_relate_channel_list(channel_id, CONFIG_ITEMS.SHARE_COUPON, db):
                cls.del_share_coupon(channel_id, db)
            else:
                CmsViewShareCoupon.objects.using(db).filter(channel_id=channel_id).delete()

        # 秒杀
        if CONFIG_ITEMS.SECKILLS in config_items:
            if not get_relate_channel_list(channel_id, CONFIG_ITEMS.SECKILLS, db):
                cls.del_seckills(channel_id, db)
            else:
                CmsSecKillViewTemp.objects.using(db).filter(channel_id=channel_id).delete()
        # 重置关联表
        channel_channels = CmsChannelChannel.objects.using(db).filter(
            Q(channel_id1=channel_id) | Q(channel_id2=channel_id))
        for channel_channel in channel_channels:
            items_str = channel_channel.config_items
            if not items_str:
                continue
            old_items = items_str.split(",")
            new_items = set(old_items) - set(config_items + [""])
            new_items_str = ",".join(new_items)
            if new_items_str:
                new_items_str = "," + new_items_str + ","
                channel_channel.config_items = new_items_str
                channel_channel.save()
            else:
                channel_channel.delete()

    @classmethod
    def del_index_version(cls, ver_id, request, db="default"):
        # 按照渠道删除步骤，删除该版本下的所有渠道
        channels = CmsChannels.objects.using(db).filter(app_version_id=ver_id)
        for channel in channels:
            cls.del_index_channel(channel.id, db)
            if CMS_CHECK_ON:
                CmsCheck(
                    module=CmsModule.MAIN_CHANNEL,
                    table_name='CmsChannels',
                    data_id=channel.id,
                    op_type=CheckOpType.DELETE,
                    status=CheckStatu.WAIT_SUBMIT,
                    is_show=0,
                    alter_person=request.user.username,
                    alter_date=time.strftime("%Y-%m-%d %X", time.localtime())).save()
        # 删除该版本信息
        CmsChannelsAppVersion.objects.using(db).get(id=ver_id).delete()
        if CMS_CHECK_ON:
            CmsCheck(
                module=CmsModule.MAIN_CHANNEL,
                table_name='CmsChannelsAppVersion',
                data_id=ver_id,
                op_type=CheckOpType.DELETE,
                status=CheckStatu.WAIT_SUBMIT,
                is_show=1,
                alter_person=request.user.username,
                alter_date=time.strftime("%Y-%m-%d %X", time.localtime())).save()
