# -*- coding: utf-8 -*-
# Author:songroger
# Aug.1.2016
from django.conf.urls import url

from tags import api

urlpatterns = [

    url(r'^tags/list/$', api.tag_list, name='tags_list'),
    url(r'^tag/$', api.tag, name='tag'),
    url(r'^tag/group/list/$', api.tag_group_list, name='tags_group_list'),
    url(r'^tag/group/$', api.tag_group, name='tag_group'),
    url(r'^tag/goods/list/$', api.tag_goods_list, name='tag_goods_list'),
    url(r'^tag/goods/$', api.tag_goods, name='tag_goods'),
    url(r'^tag_group/tags/list/$', api.tag_group_tags, name='tag_group_tags'),
    url(r'^tag/group/tags/$', api.manage_tag_group_tags,
        name='manage_tag_group_tags'),
    url(r'^third/category/list/$', api.third_category_list,
        name='third_category_list'),
    url(r'^third/category/goods/$', api.cats_to_get_goods_list,
        name='third_category_goods'),
    url(r'^booking/tag/group/list/$',
        api.booking_tag_groups, name='booking_tag_groups'),
    url(r'^booking/tag/groups/$',
        api.booking_groups, name='booking_groups'),
    url(r'^tag/booking/groups/$',
        api.tag_booking, name='tag_booking_groups'),
    url(r'^tag/sort/$', api.tag_sort, name='tag_sort'),
    url(r'^group/sort/$', api.group_sort, name='group_sort'),
    url(r'^all/goods/sku/$', api.all_skus, name='all_skus'),
]
