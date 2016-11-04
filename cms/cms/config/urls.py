# coding: utf-8

from django.conf.urls import patterns, url
from config.views import common_services, ads, config_item, category_pages_services, config_operation, invite_gift, \
    new_invite
from config.views import homepage_specialtopic, foundpage_specialtopic, streams, likes, activity, choiceness_category
from config.views import coupons, second_category, native_activities, screen_ads, open_services, activity_list, coupons_list, new_coupons,grant_coupons,generate_code
from config.views import coupon_activity, cp, share_coupon
from config.views import seckills, pcard_list
from config.apis import pcard


#配置项
urlpatterns = [
    url(r'^config_item/$', config_item.config_item, {"template_name": "config_item.html"}, name='config_item'),
]


#广告
urlpatterns += [
    url(r'^ads/$', ads.ads, {"template_name": "ads/ads.html"}, name='ads'),
    url(r'^ads/search/$', ads.search_ads, name='search_ads'),
    url(r'^ads/delete_group/$', ads.delete_ad, name='delete_ad'),
    url(r'^ads/delete/$', ads.delete_bean, name='delete_bean'),
    url(r'^ads/new_group/$', ads.new_adgroup, {"template_name": "ads/new_group.html"}, name='new_adgroup'),
    url(r'^ads/edit_group/$', ads.edit_adgroup, {"template_name": "ads/edit_group.html"}, name='edit_adgroup'),
    url(r'^new_ads/$', ads.new_ads, {"template_name": "ads/new_ad.html"}, name='new_ads'),
    url(r'^edit_ads/$', ads.edit_ads, {"template_name": "ads/edit_ad.html"}, name='edit_ads'),
]


#常用服务、商品、广告
urlpatterns += [
    url(r'^common_services/$', common_services.common_services, {"template_name": "common_services/common_services.html"}, name='common_services'),
    url(r'^common_services/search/$', common_services.search_common_services, name='search_common_services'),
    url(r'^common_services/exchange/$', common_services.exchange_common_service, name='exchange_common_service'),
    url(r'^common_services/new_service/$', common_services.new_common_service, name='new_common_service'),
    url(r'^common_services/new_goods/$', common_services.new_common_goods, name='new_common_goods'),
    url(r'^common_services/new_category/$', common_services.new_common_category, name='new_common_category'),
    url(r'^common_services/edit_service/$', common_services.edit_common_service, {"template_name": "common_services/edit_service.html"}, name='edit_common_service'),
    url(r'^common_services/edit_goods/$', common_services.edit_common_goods, {"template_name": "common_services/edit_goods.html"}, name='edit_common_goods'),
    url(r'^common_services/edit_category_first/$', common_services.edit_common_category_first, {"template_name": "common_services/edit_category_first.html"}, name='edit_common_category_first'),
    url(r'^common_services/edit_category_second/$', common_services.edit_common_category_second, {"template_name": "common_services/edit_category_second.html"}, name='edit_common_category_second'),
    url(r'^common_services/delete_goods/$', common_services.delete_common_goods, name='delete_common_goods'),
    url(r'^common_services/delete_category/$', common_services.delete_common_category, name='delete_common_category'),
    url(r'^common_services/delete_service/$', common_services.delete_common_service, name='delete_common_service'),

    #新增到家服务
    url(r'^common_services/new_home_cate/$', common_services.new_home_cate, name='common_service_new_home_cate'),
    url(r'^common_services/edit_home_cate/$', common_services.edit_home_cate,{"template_name": "common_services/edit_home_service_cate.html"}, name='common_service_edit_home_cate'),
]


#分类页服务
urlpatterns+=[
    url(r'^category_pages_services/$',category_pages_services.category_pages_services,{"template_name": "category_pages_services/category_pages_services.html"},name="category_pages_services"),
    url(r'^search_category_pages_services/$',category_pages_services.search_category_pages_services,name="search_category_pages_services"),
    #分类页服务组 一级分类
    url(r'^category_pages_services/new_group/$',category_pages_services.new_group,{"template_name": "category_pages_services/new_group.html"},name="category_pages_services_new_group"),
    url(r'^category_pages_services/edit_group/$',category_pages_services.edit_group,{"template_name": "category_pages_services/edit_group.html"},name="category_pages_services_edit_group"),
    url(r'^category_pages_services/delete_group/$',category_pages_services.delete_group,name="category_pages_services_delete_group"),
    #分类页服务下面：商品
    url(r'^category_pages_services/new_goods/$',category_pages_services.new_goods,name="category_pages_services_new_goods"),
    url(r'^category_pages_services/edit_goods/$',category_pages_services.edit_goods,{"template_name": "category_pages_services/edit_goods.html"},name="category_pages_services_edit_goods"),
    url(r'^category_pages_services/delete_goods/$',category_pages_services.delete_goods,name="category_pages_services_delete_goods"),
    #分类页服务下面：服务
    url(r'^category_pages_services/new_service/$',category_pages_services.new_service,name="category_pages_services_new_service"),
    url(r'^category_pages_services/edit_service/$',category_pages_services.edit_service,{"template_name": "category_pages_services/edit_service.html"},name="category_pages_services_edit_service"),
    url(r'^category_pages_services/delete_service/$',category_pages_services.delete_service,name="category_pages_services_delete_service"),
    #分类页服务下面：二级分类
    url(r'^category_pages_services/new_category/$',category_pages_services.new_category,name="category_pages_services_new_category"),
    url(r'^category_pages_services/edit_category/$',category_pages_services.edit_category,{"template_name": "category_pages_services/edit_category.html"},name="category_pages_services_edit_category"),
    url(r'^category_pages_services/delete_category/$',category_pages_services.delete_category,name="category_pages_services_delete_category"),

    url(r'^category_pages_services/exchange_category/$',category_pages_services.exchange_category,name="category_pages_services_exchange"),
    url(r'^category_pages_services/get_second_category/$',category_pages_services.get_second_category,name="category_pages_services_get_second_category"),

    #新增到家分类
    url(r'^category_pages_services/new_home_cate/$', category_pages_services.new_home_cate, name='category_pages_services_new_home_cate'),
    url(r'^category_pages_services/edit_home_cate/$', category_pages_services.edit_home_cate,{"template_name": "category_pages_services/edit_home_service_cate.html"}, name='category_pages_services_edit_home_cate'),
    url(r'^category_pages_services/del_home_cate/$', category_pages_services.del_home_cate, name='category_pages_services_del_home_cate'),
]


#首页专题
urlpatterns += [
    url(r'^homepage_specialtopic/$',homepage_specialtopic.homepage_specialtopic , {"template_name": "homepage/homepage.html"}, name='homepage_specialtopic'),
    url(r'^search_homepage_specialtopic/$', homepage_specialtopic.search_homepage_specialtopic, name='search_homepage_specialtopic'),
    url(r'^delete_homepage_specialtopic/$', homepage_specialtopic.delete_homepage_specialtopic, name='delete_homepage_specialtopic'),
    url(r'^new_homepage_specialtopic/$', homepage_specialtopic.new_homepage_specialtopic, name='new_homepage_specialtopic'),
    url(r'^edit_homepage_specialtopic/$', homepage_specialtopic.edit_homepage_specialtopic, {"template_name": "homepage/edit_homepage.html"}, name='edit_homepage_specialtopic'),
]


#发现页专题
urlpatterns += [
    url(r'^foundpage_specialtopic/$',foundpage_specialtopic.foundpage_specialtopic , {"template_name": "foundpage/foundpage.html"}, name='foundpage_specialtopic'),
    url(r'^search_foundpage_specialtopic/$', foundpage_specialtopic.search_foundpage_specialtopic, name='search_foundpage_specialtopic'),
    url(r'^delete_foundpage_specialtopic/$', foundpage_specialtopic.delete_foundpage_specialtopic, name='delete_foundpage_specialtopic'),
    url(r'^top_foundpage_specialtopic/$', foundpage_specialtopic.top_foundpage_specialtopic, name='top_foundpage_specialtopic'),
    url(r'^mark_info_foundpage/$', foundpage_specialtopic.mark_info_foundpage, name='mark_info_foundpage'),
    url(r'^new_foundpage_specialtopic/$', foundpage_specialtopic.new_foundpage_specialtopic, name='new_foundpage_specialtopic'),
    url(r'^edit_foundpage_specialtopic/$', foundpage_specialtopic.edit_foundpage_specialtopic, {"template_name": "foundpage/edit_foundpage.html"}, name='edit_foundpage_specialtopic'),
]


#内容流
urlpatterns += [
    url(r'^streams/$',streams.streams, {"template_name": "streams/streams.html"}, name='streams'),
    url(r'^streams/search/$', streams.search_streams, name='search_streams'),
    url(r'^streams/new_group/$', streams.new_streamsgroup, {"template_name": "streams/new_group.html"}, name='new_streamsgroup'),
    url(r'^streams/edit_group/$', streams.edit_streamsgroup, {"template_name": "streams/edit_group.html"}, name='edit_streamsgroup'),
    url(r'^streams/new_goods/$', streams.new_goods, name='streams_new_goods'),
    url(r'^streams/edit_goods/$', streams.edit_goods, {"template_name": "streams/edit_goods.html"}, name='streams_edit_goods'),
    url(r'^streams/new_stream/$', streams.new_content_stream, {"template_name": "streams/new_stream.html"},name='new_content_stream'),
    url(r'^streams/edit_stream/$', streams.edit_content_stream, {"template_name": "streams/edit_stream.html"},name='edit_content_stream'),
    url(r'^streams/delete_group/$', streams.delete_streamsgroup,name='delete_streamsgroup'),
    url(r'^streams/delete_stream/$', streams.delete_content_stream,name='delete_content_stream'),
    url(r'^streams/delete_goods/$', streams.delete_goods,name='delete_goods'),
    url(r'^streams/exchange/$', streams.streams_exchange,name='streams_exchange'),
    #品牌
    url(r'^streams/new_cp/$', streams.new_cp, name='streams_new_cp'),
    url(r'^streams/edit_cp/$', streams.edit_cp,{"template_name": "streams/edit_cp.html"}, name='streams_edit_cp'),
    url(r'^streams/del_cp/$', streams.del_cp, name='streams_del_cp'),

]

#运营配置
urlpatterns += [
    url(r'^config_operation/$',config_operation.config_operation,{"template_name": "config_operation/config_operation.html"},name='config_operation'),
    url(r'^config_operation/search/$',config_operation.search_config_operation, name='search_config_operation'),
    url(r'^new_config_operation/$',config_operation.new_config_operation,name='new_config_operation'),
    url(r'^edit_config_operation/$',config_operation.edit_config_operation,name='edit_config_operation'),
    url(r'^delete_config_operation/$', config_operation.delete_config_operation, name='delete_config_operation'),
]

#猜你喜欢
urlpatterns += [
    url(r'^likes/$',likes.likes, {"template_name": "likes/likes.html"}, name='likes'),
    url(r'^likes/search/$', likes.search_likes,name='search_likes'),
    url(r'^likes/exchange/$', likes.exchange_likes,name='exchange_likes'),
    #新增 编辑和删除组
    url(r'^likes/new_group/$', likes.new_group, {"template_name": "likes/new_group.html"}, name='new_likes_group'),
    url(r'^likes/edit_group/$', likes.edit_group, {"template_name": "likes/edit_group.html"}, name='edit_likes_group'),
    url(r'^likes/delete_group/$', likes.delete_group, name='delete_likes_group'),
    #新增 编辑和删除商品
    url(r'^likes/new_goods/$', likes.new_goods, name='likes_new_goods'),
    url(r'^likes/edit_goods/$', likes.edit_goods, {"template_name": "likes/edit_goods.html"},name='likes_edit_goods'),
    url(r'^likes/delete_goods/$', likes.delete_goods,name='likes_delete_goods'),
    #新增 编辑和删除服务
    url(r'^likes/new_service/$', likes.new_service, name='likes_new_service'),
    url(r'^likes/edit_service/$', likes.edit_service, {"template_name": "likes/edit_service.html"},name='likes_edit_service'),
    url(r'^likes/delete_service/$', likes.delete_service,name='likes_delete_service'),
]


#活动
urlpatterns += [
    url(r'^activities/$', activity.activities, {"template_name": "activities/activities.html"}, name='activities'),
    url(r'^activities/search/$', activity.search_activities,name='search_activities'),
    url(r'^activities/exchange/$', activity.exchange_activities,name='exchange_activities'),
    url(r'^activities/new_activity/$', activity.new_activity, {"template_name": "activities/new_activity.html"}, name='new_activity'),
    url(r'^activities/edit_activity/$', activity.edit_activity, {"template_name": "activities/edit_activity.html"}, name='edit_activity'),
    url(r'^activities/delete_activity/$', activity.delete_activity, name='delete_activity'),
]


#精品分类
urlpatterns += [
    url(r'^choiceness_categories/$', choiceness_category.choiceness_categories, {"template_name": "choiceness_categories/choiceness_categories.html"}, name='choiceness_categories'),
    url(r'^search_choiceness_categories/$', choiceness_category.search_choiceness_categories, name='search_choiceness_categories'),
    url(r'^exchange_choiceness_categories/$', choiceness_category.exchange_choiceness_categories, name='exchange_choiceness_categories'),
    url(r'^new_choiceness_category/$', choiceness_category.new_choiceness_category, {"template_name": "choiceness_categories/new_choiceness_category.html"}, name='new_choiceness_category'),
    url(r'^edit_choiceness_category/$', choiceness_category.edit_choiceness_category, {"template_name": "choiceness_categories/edit_choiceness_category.html"}, name='edit_choiceness_category'),
    url(r'^delete_choiceness_category/$', choiceness_category.delete_choiceness_category, name='delete_choiceness_category'),
]

#配置库优惠券
urlpatterns += [
    url(r'^coupons/$', coupons.coupons, {"template_name": "config_coupons/coupons.html"}, name='config_coupons'),
    url(r'^coupons/search/$', coupons.search_coupons, name='search_config_coupons'),
    url(r'^coupons/exchange/$', coupons.exchange_coupons, name='exchange_config_coupons'),
    url(r'^coupons/new_coupons/$', coupons.new_coupons, name='new_config_coupons'),
    url(r'^coupons/edit_coupons/$', coupons.edit_coupons, {"template_name": "config_coupons/edit_coupons.html"}, name='edit_config_coupons'),
    url(r'^coupons/delete_coupons/$', coupons.delete_coupons, name='delete_config_coupons'),
]


#二级分类
urlpatterns += [
    url(r'^second_category/$', second_category.second_category, {"template_name": "second_category/second_category.html"}, name='second_category'),
    url(r'^second_category/exchange/$', second_category.exchange, name='exchange_second_category'),
    url(r'^second_category/search_second_category/$', second_category.search_second_category, name='search_second_category'),
    url(r'^second_category/new_second_category/$', second_category.new_second_category, {"template_name": "second_category/new_second_category.html"}, name='sc_new_second_category'),
    url(r'^second_category/edit_second_category/$', second_category.edit_second_category, {"template_name": "second_category/edit_second_category.html"}, name='sc_edit_second_category'),
    url(r'^second_category/new_shop/$', second_category.new_shop, name='sc_new_shop'),
    url(r'^second_category/edit_shop/$', second_category.edit_shop, {"template_name": "second_category/edit_shop.html"}, name='sc_edit_shop'),
    url(r'^second_category/delete_second_category/$', second_category.delete_second_category, name='sc_delete_second_category'),
    url(r'^second_category/delete_shop/$', second_category.delete_shop, name='sc_delete_shop'),
]


#配置Native活动
urlpatterns += [
    url(r'^native_activities/$', native_activities.native_activities, {"template_name": "native_activities/native_activities.html"}, name='native_activities'),
    url(r'^native_activities/search/$', native_activities.search_activities, name='search_native_activities'),
    url(r'^native_activities/exchange/$', native_activities.exchange_activities, name='exchange_native_activities'),
    url(r'^native_activities/new_activity/$', native_activities.new_activity, {"template_name": "native_activities/new_activity.html"}, name='new_native_activity'),
    url(r'^native_activities/edit_activity/$', native_activities.edit_activity, {"template_name": "native_activities/edit_activity.html"}, name='edit_native_activity'),
    url(r'^native_activities/delete_activity/$', native_activities.delete_activity, name='delete_native_activity'),
]


# 配置开屏广告
urlpatterns += [
    url(r'^screen_ads/$', screen_ads.screen_ads, {"template_name": "screen_ads/screen_ads.html"}, name='screen_ads'),
    url(r'^screen_ads/search/$', screen_ads.search_screen_ads, name='search_screen_ads'),
    url(r'^screen_ads/new_ad/$', screen_ads.new_ad, {"template_name": "screen_ads/new_ad.html"}, name='new_screen_ad'),
    url(r'^screen_ads/edit_ad/$', screen_ads.edit_ad, {"template_name": "screen_ads/edit_ad.html"}, name='edit_screen_ad'),
    url(r'^screen_ads/delete_ad/$', screen_ads.delete_ad, name='delete_screen_ad'),
]

# 开放服务
urlpatterns += [
    url(r'^open_services_channel/list/$', open_services.channels, {"template_name": "open_services/channels.html"}, name='open_services_channels'),
    url(r'^open_services_version/new/$', open_services.new_version, name='open_services_version_new'),
    url(r'^open_services_version/edit/$', open_services.edit_version, name='open_services_version_edit'),
    url(r'^open_services_version/delete/$', open_services.del_ver_channels, name='open_services_version_delete'),

    url(r'^open_services_channel/new/$', open_services.new_channel, name='open_services_channel_new'),
    url(r'^open_services_channel/edit/$', open_services.edit_channel, name='open_services_channel_edit'),

    url(r'^open_services/list/$', open_services.open_services, {"template_name": "open_services/open_services.html"}, name='open_services_list'),
    url(r'^search_open_services/$', open_services.search_services, name='search_open_services'),
    url(r'^open_services/new/$', open_services.new_open_services, {"template_name": "open_services/new_open_service.html"}, name='open_services_new'),
    url(r'^open_services/edit/$', open_services.edit_open_services, {"template_name": "open_services/edit_open_service.html"}, name='open_services_edit'),
    url(r'^open_services/delete/$', open_services.delete_open_services, name='open_services_delete'),
]


# 活动配置
urlpatterns += [
    url(r'^open_activity_channel/list/$', activity_list, {"template_name": "newcoupons/coupons.html"}, name='open_activity_channels'),
    url(r'^open_coupon_create/list/$', coupons_list, {"template_name": "newcoupons/grantcouponlist.html"}, name='open_coupon_create'),
    url(r'^newedit_coupon/$', new_coupons, {"template_name": "newcoupons/new_coupons.html"}, name='newedit_coupon'),
    url(r'^grant_coupon/$', grant_coupons, {"template_name": "newcoupons/grant_coupon.html"}, name='grant_coupon'),
    url(r'^generate_code/$', generate_code, {"template_name": "newcoupons/generate_code.html"}, name='genarate_code'),
    url(r'^invite_gift/list/$', invite_gift, {"template_name": "newcoupons/invite_gift.html"}, name='invite_gift'),
    url(r'^newinvite_gift/$', new_invite, {"template_name": "newcoupons/new_invite.html"}, name='new_invite'),
]

#优惠券活动
urlpatterns += [
    url(r'^coupon_activities/list/$', coupon_activity.coupon_activities, {"template_name": "coupon_activity/coupon_activities.html"}, name='coupon_activities'),
    url(r'^coupon_activity/search/$', coupon_activity.search, name='coupon_search_activity'),
    url(r'^coupon_activity/new/$', coupon_activity.new, {"template_name": "coupon_activity/new_coupon_activity.html"}, name='coupon_new_activity'),
    url(r'^coupon_activity/edit/$', coupon_activity.edit, {"template_name": "coupon_activity/edit_coupon_activity.html"}, name='coupon_edit_activity'),
    url(r'^coupon_activity/delete/$', coupon_activity.delete, name='coupon_del_activity'),
]

#品牌区
urlpatterns +=[
    url(r'^cp/list/$', cp.cps, {"template_name": "cps/cps.html"}, name='config_cp_list'),
    url(r'^cp/search/$', cp.search, name='config_search_cp'),
    url(r'^cp/new/$', cp.new, name='config_new_cp'),
    url(r'^cp/edit/$', cp.edit, {"template_name": "cps/edit_cp.html"}, name='config_edit_cp'),
    url(r'^cp/delelte/$', cp.delelte, name='config_del_cp'),
]

# 分享券
urlpatterns +=[
    url(r'^share_coupon/list/$', share_coupon.share_coupon, {"template_name": "share_coupon/share_coupon.html"}, name='share_coupon'),
    url(r'^share_coupon/search/$', share_coupon.search, name='search_share_coupon'),
    url(r'^share_coupon/new/$', share_coupon.new, {"template_name": "share_coupon/new.html"}, name='new_share_coupon'),
    url(r'^share_coupon/edit/$', share_coupon.edit, {"template_name": "share_coupon/edit.html"}, name='edit_share_coupon'),
    url(r'^share_coupon/delelte/$', share_coupon.delelte, name='del_share_coupon'),
]

# 秒杀活动
urlpatterns +=[
    url(r'^seckills/list/$', seckills.seckills, {"template_name": "seckills/seckills.html"}, name='seckills'),
    url(r'^seckills/search/$',seckills.search,name='search_seckills'),
    url(r'^seckills/new/$', seckills.new, {"template_name": "seckills/new.html"}, name='new_seckill'),
    url(r'^seckills/edit/$', seckills.edit, {"template_name": "seckills/edit.html"}, name='edit_seckill'),
    url(r'^seckills/delelte/$', seckills.delelte, name='del_seckill'),
               ]


# 套餐卡
urlpatterns +=[
    url(r'^pcard/goods/list/$', pcard.pcard_goods_list , name='pcard_goods_list'),
    url(r'^pcard/goods/$', pcard.pcard_goods , name='pcard_goods'),
    url(r'^pcard/common/goods/$', pcard.pcard_common_goods , name='pcard_common_goods'),
    url(r'^pcard/list/$', pcard_list, {"template_name": "pcard/wxh.html"}, name='pcard_list'),
]
