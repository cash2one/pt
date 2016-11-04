# -*- coding: utf-8 -*-
# Author:songroger
# Aug.30.2016
from __future__ import unicode_literals
from django.core.cache import cache
from .models import ChannelCoverAds
from datetime import datetime


def make_ads_cache_key(cid, city):
    return str(cid) + str(city)


def get_ads_data(cid, city):
    ads = ChannelCoverAds.objects.filter(channel_id=cid,
                                         city__city_name__startswith=city,
                                         ads__end_time__gte=datetime.now())\
        | ChannelCoverAds.objects.filter(channel_id=cid,
                                         city__city_name=u"全国",
                                         ads__end_time__gte=datetime.now())
    return [dict(logo=a.ads.logo,
                 display_time=a.ads.display_time,
                 action=a.ads.action_string,
                 start_time=a.ads.tutime()[0],
                 end_time=a.ads.tutime()[1]
                 ) for a in ads] if ads else []


def set_ads_cache(key, value, timeout=24 * 60 * 60):
    cache.set(key, value, timeout)


def get_ads_cache(cid, city):
    ads = cache.get(make_ads_cache_key(cid, city))
    if ads is None:
        ads = get_ads_data(cid, city)
        # set_ads_cache(make_ads_cache_key(cid, city), ads)
        # ads = cache.get(make_ads_cache_key(cid, city))

    return ads


def delete_ads_cache(cid, city):
    cache.delete(make_ads_cache_key(cid, city))


def delete_many_ads_cache(dkeys):
    cache.delete_many(dkeys)


def cache_clear():
    cache.clear()
