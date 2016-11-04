# -*- coding: utf-8 -*-
# Author:songroger
# Aug.29.2016
from django.conf.urls import url
from apis import ptcms, ptclient

urlpatterns = [

    url(r'^cover/ads/$', ptcms.cover_ads, name='cover_ads'),
    url(r'^cover/ads/list/$', ptcms.cover_ads_list, name='cover_ads_list'),
    url(r'^common/coverads$', ptclient.get_ads, name='common_cover_ads'),
    url(r'^common/ptcard$', ptclient.ptcard_list, name='common_ptcard_list'),
]


# todo
# 3.缓存处理，如增删过程中
# 4.同一城市下的广告有效期不允许有交叉
