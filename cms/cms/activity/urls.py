# -*- coding: utf-8 -*-
# Author:songroger
# Jun.22.2016
from django.conf.urls import url

from activity import api

urlpatterns = [

    url(r'^coupon/list/$', api.coupon_list, name='coupon_list'),
    url(r'^coupon/$', api.coupon, name='coupon'),
    url(r'^cps/list/$', api.cps_list, name='cps_list'),
    url(r'^goods/list/$', api.goods_list, name='goods_list'),
    url(r'^coupons/$', api.coupons_list, name='coupons_list'),
    url(r'^coupons_valid/$', api.coupons_list_valid,
        name='coupons_list_valid'),
    url(r'^codes/$', api.create_codes, name='create_codes'),
    url(r'^allotted_coupon/list/$', api.coupon_created_list,
        name='allotted_coupon_list'),
    url(r'^allot/coupon/$', api.allot_coupon, name='allot_coupon'),
    url(r'^codes/down/$', api.download_codes, name='download_codes'),
    url(r'^codes/list/$', api.codes_list, name='codes_list'),
    url(r'^category/list/$', api.category_list, name='category_list'),
    url(r'^invite_gift_api/list/$', api.invite_gift_list,
        name='invite_gift_api'),
    url(r'^invite_gift_api/updown/$',
        api.invite_gift_updown, name='invite_gift_updown'),
    url(r'^invite_gift_api/down/$',
        api.invite_gift_down, name='invite_gift_down'),
    url(r'^invite_gift/$', api.invite_gift, name='invite_gift_change'),
    url(r'^share/activity/list/$', api.share_activity_list,
        name='share_activity_list'),
    url(r'^vip/list/$', api.vip_list,
        name='vip_list'),
]
