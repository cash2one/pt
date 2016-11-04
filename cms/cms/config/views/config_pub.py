# coding: utf-8
import time

from cms.settings import CMS_CHECK_ON
from common.const import CmsModule, CONFIG_ITEMS, CheckOpType, CheckStatu
# from main.views.main_pub import *
from common.views import get_relate_channel_list, checked_results

# 返回服务列表
from main.models import CmsServices, CmsGoods, CmsCoupon, CmsCategoryItembean, CmsCheck, CmsViewActivity, CmsViewAd, \
    CmsViewNavi, CmsViewChoicenessCategory, CmsViewService, CmsViewOpconfig, CmsViewCoupon, CmsViewFindTopic, \
    CmsViewHomepageTopic, CmsViewLike, CmsViewStream, CmsViewCategoryitem, CmsViewScreenads, CmsViewNativeActivity, \
    CmsSecKillViewTemp, CmsSpecialTopic, CmsViewPush, CmsActions, CmsCP, CmsActivityV37
from main.views.main_pub import GetAllCities
from main.views.main_pub import RemoveShiCity


def get_services():
    services = CmsServices.objects.filter(parent_id=0, type=0).order_by("name").values_list('id', 'name', 'memo',
                                                                                            'srv_id')
    results = checked_results('CmsServices', services, 0)
    return results


# 返回商品列表
def get_goods():
    goods = CmsGoods.objects.filter(parent_id=-1).order_by("name").values_list('id', 'name', 'memo')
    results = checked_results('CmsGoods', goods, 0)
    return results


# 返回优惠券列表
def get_coupons():
    coupons = CmsCoupon.objects.filter(parent_id=-1).order_by("name").values_list('id', 'name')
    results = checked_results('CmsCoupon', coupons, 0)
    return results


# 返回商家列表
def get_shops():
    shops = CmsCategoryItembean.objects.filter(parent_id=-1).order_by("name").values_list("id", "name")
    results = checked_results('CmsCategoryItembean', shops, 0)
    return results


def new_associate(channel_id, id, config_type, request, open=0):
    channels = get_relate_channel_list(channel_id, config_type)
    for channel in channels:
        if config_type == CONFIG_ITEMS.ACTIVITY:
            oCmsViewActivity = CmsViewActivity(activity_id=id, channel_id=channel)
            oCmsViewActivity.save()
            if CMS_CHECK_ON:
                CmsCheck(channel_id=channel_id,
                         module=CmsModule.CONFIG_ACTIVITY,
                         table_name='CmsViewActivity',
                         data_id=oCmsViewActivity.id,
                         op_type=CheckOpType.NEW,
                         is_show=0,
                         alter_person=request.user.username,
                         alter_date=time.strftime("%Y-%m-%d %X", time.localtime())).save()
        if config_type == CONFIG_ITEMS.AD:
            oCmsViewAd = CmsViewAd(ad_id=id, channel_id=channel)
            oCmsViewAd.save()
            if CMS_CHECK_ON:
                CmsCheck(channel_id=channel_id,
                         module=CmsModule.CONFIG_AD,
                         table_name='CmsViewAd',
                         data_id=oCmsViewAd.id,
                         op_type=CheckOpType.NEW,
                         is_show=0,
                         alter_person=request.user.username,
                         alter_date=time.strftime("%Y-%m-%d %X", time.localtime())).save()
        if config_type == CONFIG_ITEMS.CATEGORY_PAGE_SERVICES:
            oCmsViewNavi = CmsViewNavi(navicat_id=id, channel_id=channel, status=0)
            oCmsViewNavi.save()
            if CMS_CHECK_ON:
                CmsCheck(channel_id=channel_id,
                         module=CmsModule.CONFIG_PAGE,
                         table_name='CmsViewNavi',
                         data_id=oCmsViewNavi.id,
                         op_type=CheckOpType.NEW,
                         is_show=0,
                         alter_person=request.user.username,
                         alter_date=time.strftime("%Y-%m-%d %X", time.localtime())).save()
        if config_type == CONFIG_ITEMS.CHOICENESS_CATEGORY:
            oCmsViewChoicenessCategory = CmsViewChoicenessCategory(choiceness_category_id=id, channel_id=channel)
            oCmsViewChoicenessCategory.save()
            if CMS_CHECK_ON:
                CmsCheck(channel_id=channel_id,
                         module=CmsModule.CONFIG_CHOICENESS,
                         table_name='CmsViewChoicenessCategory',
                         data_id=oCmsViewChoicenessCategory.id,
                         op_type=CheckOpType.NEW,
                         is_show=0,
                         alter_person=request.user.username,
                         alter_date=time.strftime("%Y-%m-%d %X", time.localtime())).save()
        if config_type == CONFIG_ITEMS.COMMON_SERVICES:
            oCmsViewService = CmsViewService(service_id=id, channel_id=channel, open_type=open)
            oCmsViewService.save()
            if CMS_CHECK_ON:
                CmsCheck(channel_id=channel_id,
                         module=CmsModule.CONFIG_COMMON_SERVICES,
                         table_name='CmsViewService',
                         data_id=oCmsViewService.id,
                         op_type=CheckOpType.NEW,
                         is_show=0,
                         alter_person=request.user.username,
                         alter_date=time.strftime("%Y-%m-%d %X", time.localtime())).save()
        if config_type == CONFIG_ITEMS.CONFIG_OPERATION:
            oCmsViewOpconfig = CmsViewOpconfig(opconfig_id=id, channel_id=channel)
            oCmsViewOpconfig.save()
            if CMS_CHECK_ON:
                CmsCheck(channel_id=channel_id,
                         module=CmsModule.CONFIG_OPERATION,
                         table_name='CmsViewOpconfig',
                         data_id=oCmsViewOpconfig.id,
                         op_type=CheckOpType.NEW,
                         is_show=0,
                         alter_person=request.user.username,
                         alter_date=time.strftime("%Y-%m-%d %X", time.localtime())).save()
        if config_type == CONFIG_ITEMS.COUPONS:
            oCmsViewCoupon = CmsViewCoupon(coupon_id=id, channel_id=channel)
            oCmsViewCoupon.save()
            if CMS_CHECK_ON:
                CmsCheck(channel_id=channel_id,
                         module=CmsModule.CONFIG_COUPON,
                         table_name='CmsViewCoupon',
                         data_id=oCmsViewCoupon.id,
                         op_type=CheckOpType.NEW,
                         is_show=0,
                         alter_person=request.user.username,
                         alter_date=time.strftime("%Y-%m-%d %X", time.localtime())).save()
        if config_type == CONFIG_ITEMS.FOUNDPAGE:
            oCmsViewFindTopic = CmsViewFindTopic(topic_id=id, channel_id=channel)
            oCmsViewFindTopic.save()
            push_foundpage(channel, id)
            if CMS_CHECK_ON:
                CmsCheck(channel_id=channel_id,
                         module=CmsModule.CONFIG_FOUNDPAGE,
                         table_name='CmsViewFindTopic',
                         data_id=oCmsViewFindTopic.id,
                         op_type=CheckOpType.NEW,
                         is_show=0,
                         alter_person=request.user.username,
                         alter_date=time.strftime("%Y-%m-%d %X", time.localtime())).save()
        if config_type == CONFIG_ITEMS.HOMEPAGE:
            oCmsViewHomepageTopic = CmsViewHomepageTopic(topic_id=id, channel_id=channel)
            oCmsViewHomepageTopic.save()
            if CMS_CHECK_ON:
                CmsCheck(channel_id=channel_id,
                         module=CmsModule.CONFIG_HOMEPAGE,
                         table_name='CmsViewHomepageTopic',
                         data_id=oCmsViewHomepageTopic.id,
                         op_type=CheckOpType.NEW,
                         is_show=0,
                         alter_person=request.user.username,
                         alter_date=time.strftime("%Y-%m-%d %X", time.localtime())).save()
        if config_type == CONFIG_ITEMS.LIKES:
            oCmsViewLike = CmsViewLike(like_id=id, channel_id=channel)
            oCmsViewLike.save()
            if CMS_CHECK_ON:
                CmsCheck(channel_id=channel_id,
                         module=CmsModule.CONFIG_LIKE,
                         table_name='CmsViewLike',
                         data_id=oCmsViewLike.id,
                         op_type=CheckOpType.NEW,
                         is_show=0,
                         alter_person=request.user.username,
                         alter_date=time.strftime("%Y-%m-%d %X", time.localtime())).save()
        if config_type == CONFIG_ITEMS.STREAMS:
            oCmsViewStream = CmsViewStream(streamcontent_id=id, channel_id=channel, status=0)
            oCmsViewStream.save()
            if CMS_CHECK_ON:
                CmsCheck(channel_id=channel_id,
                         module=CmsModule.CONFIG_STREAM,
                         table_name='CmsViewStream',
                         data_id=oCmsViewStream.id,
                         op_type=CheckOpType.NEW,
                         is_show=0,
                         alter_person=request.user.username,
                         alter_date=time.strftime("%Y-%m-%d %X", time.localtime())).save()
        if config_type == CONFIG_ITEMS.SECOND_CATEGORY:
            oCmsViewCategoryitem = CmsViewCategoryitem(category_item_id=id, channel_id=channel)
            oCmsViewCategoryitem.save()
            if CMS_CHECK_ON:
                CmsCheck(channel_id=channel_id,
                         module=CmsModule.CONFIG_SECOND_CATEGORY,
                         table_name='CmsViewCategoryitem',
                         data_id=oCmsViewCategoryitem.id,
                         op_type=CheckOpType.NEW,
                         is_show=0,
                         alter_person=request.user.username,
                         alter_date=time.strftime("%Y-%m-%d %X", time.localtime())).save()
        if config_type == CONFIG_ITEMS.SCREEN_AD:
            oCmsViewScreenads = CmsViewScreenads(screenad_id=id, channel_id=channel)
            oCmsViewScreenads.save()
            if CMS_CHECK_ON:
                CmsCheck(channel_id=channel_id,
                         module=CmsModule.CONFIG_SCREEN_AD,
                         table_name='CmsViewScreenads',
                         data_id=oCmsViewScreenads.id,
                         op_type=CheckOpType.NEW,
                         is_show=0,
                         alter_person=request.user.username,
                         alter_date=time.strftime("%Y-%m-%d %X", time.localtime())).save()
        if config_type == CONFIG_ITEMS.NATIVE_ACTIVITY:
            oCmsViewNativeActivity = CmsViewNativeActivity(nactivity_id=id, channel_id=channel)
            oCmsViewNativeActivity.save()
            if CMS_CHECK_ON:
                CmsCheck(channel_id=channel_id,
                         module=CmsModule.CONFIG_NATIVE_ACTIVITY,
                         table_name='CmsViewNativeActivity',
                         data_id=oCmsViewNativeActivity.id,
                         op_type=CheckOpType.NEW,
                         is_show=0,
                         alter_person=request.user.username,
                         alter_date=time.strftime("%Y-%m-%d %X", time.localtime())).save()
        if config_type == CONFIG_ITEMS.SECKILLS:
            oCmsSecKillViewTemp = CmsSecKillViewTemp(channel_id=channel, seckill_id=id, status=0)
            oCmsSecKillViewTemp.save()
            if CMS_CHECK_ON:
                CmsCheck(channel_id=channel_id,
                         module=CmsModule,
                         table_name='CmsViewNativeActivity',
                         data_id=oCmsViewNativeActivity.id,
                         op_type=CheckOpType.NEW,
                         is_show=0,
                         alter_person=request.user.username,
                         alter_date=time.strftime("%Y-%m-%d %X", time.localtime())).save()


def get_topics():
    """获取专题列表"""
    topics = CmsSpecialTopic.objects.filter().order_by('title').values_list('id', 'title', 'subtitle')
    results = checked_results('CmsSpecialTopic', topics, 0)
    return results


def exchange_obj(classobj1, id1, classobj2, id2, channel_id, module, request, word1="location", word2="location"):
    obj1 = classobj1.objects.get(id=id1)
    obj2 = classobj2.objects.get(id=id2)
    value1 = getattr(obj1, word1)
    value2 = getattr(obj2, word2)
    setattr(obj1, word1, value2)
    setattr(obj2, word2, value1)
    obj1.save()
    obj2.save()
    if CMS_CHECK_ON:
        check = CmsCheck(
            channel_id=channel_id,
            module=module,
            table_name=classobj1.__name__,
            data_id=id1,
            op_type=CheckOpType.EDIT,
            status=CheckStatu.WAIT_SUBMIT,
            is_show=1,
            alter_person=request.user.username,
            alter_date=time.strftime("%Y-%m-%d %X", time.localtime()))
        check.save()
        check = CmsCheck(
            channel_id=channel_id,
            module=module,
            table_name=classobj2.__name__,
            data_id=id2,
            op_type=CheckOpType.EDIT,
            status=CheckStatu.WAIT_SUBMIT,
            is_show=1,
            alter_person=request.user.username,
            alter_date=time.strftime("%Y-%m-%d %X", time.localtime()))
        check.save()


def push_foundpage(channel_id, specialtopic_id):
    ospecialtopic = CmsSpecialTopic.objects.get(id=specialtopic_id)
    citys = RemoveShiCity(ospecialtopic.city)
    if citys == "*":
        allcities = GetAllCities()
        for city in allcities:
            obj, created = CmsViewPush.objects.get_or_create(city=city, channel_id=channel_id)
            if created:
                data_version = 1
            else:
                data_version = obj.data_version + 1
            obj.data_version = data_version
            obj.save()
    else:
        for city in citys.split(","):
            obj, created = CmsViewPush.objects.get_or_create(city=city, channel_id=channel_id)
            if created:
                data_version = 1
            else:
                data_version = obj.data_version + 1
            obj.data_version = data_version
            obj.save()


def GetAllActions():
    actions = CmsActions.objects.all().values_list("id", 'dest_title', 'memo')
    return actions


def get_all_cps():
    cps = CmsCP.objects.all().values_list("id", "name", "desc")
    return cps


# 获取所有活动
def get_all_coupon_activities():
    coupon_activities = CmsActivityV37.objects.all().values_list("id", "name")
    return coupon_activities
