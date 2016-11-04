# -*- coding: utf-8 -*-
# Author:songroger
# Aug.31.2016
from __future__ import unicode_literals
import json
import traceback
import logging
from .models import CoverAds, ChannelCoverAds
from django.core.paginator import Paginator
from pttools.pthttp import check_parameter
from pttools.ptformat import ptlog
from django.db import connection
from ads.settings import COVER_ADS_PARAMETERS
from ads.ads_cache import delete_ads_cache, make_ads_cache_key,\
    delete_many_ads_cache, cache_clear
from main.models import PtYellowCitylist
from datetime import datetime


log = logging.getLogger("main.app")


def get_cover_ads_list(page, limit, channel_id):
    data = {}
    ca = _get_ads_data(channel_id)

    p = Paginator(ca, limit)
    if page > p.num_pages:
        return data
    cas = p.page(page)
    data['ads'] = [
        dict(channel_id=t[0],
             ads_id=t[1],
             name=t[2],
             logo=t[3],
             display_time=t[4],
             start_time=t[5].strftime("%Y/%m/%d %H:%M") if t[5] else '',
             end_time=t[6].strftime("%Y/%m/%d %H:%M") if t[6] else '',
             action_id=t[7],
             city_names=t[8].replace(u"市", "").replace(u"县", ""),
             ) for t in cas]

    data["total"] = p.count
    data['page'] = page
    data["totalpage"] = p.num_pages
    data["hasNext"] = cas.has_next()
    return data


def _get_ads_data(cid):
    cur = connection.cursor()
    sql = '''
        SELECT  a.channel_id
                ,c.id AS ads_id
                ,c.name
                ,c.logo
                ,c.display_time
                ,c.start_time
                ,c.end_time
                ,c.action_id
                ,GROUP_CONCAT(DISTINCT t.city_name SEPARATOR '、') AS city_names
        FROM `cms_cover_ads` c
        LEFT JOIN `cms_channel_cover_ads` a
        ON a.ads_id= c.id
        LEFT JOIN `pt_yellow_citylist` t
        ON a.city_id= t.self_id
        WHERE a.channel_id = %s
        GROUP BY a.ads_id
        ORDER BY a.id DESC;
    '''
    cur.execute(sql, cid)
    row = cur.fetchall()
    return row


def add_or_up_cover_ads(request, channel_id, ads_id):
    data = {}
    json_string = request.body.decode('utf-8')
    try:
        request_data = json.loads(json_string)
        if request_data:
            must_result = check_parameter(request_data, COVER_ADS_PARAMETERS)
            if must_result.get("code") == 1:
                return must_result
            update_data = dict(name=request_data.get("name"),
                               logo=request_data.get("logo"),
                               start_time=datetime.strptime(
                                   request_data.get("start_time"), '%Y/%m/%d %H:%M'),
                               end_time=datetime.strptime(
                                   request_data.get("end_time"), '%Y/%m/%d %H:%M'),
                               action_id=request_data.get("action_id"),
                               display_time=request_data.get("display_time"),
                               )
            cities = request_data.get("city_names")
            ads = CoverAds.objects.filter(id=ads_id)
            if ads:
                for c in cities:
                    t1 = ChannelCoverAds.objects.filter(channel_id=channel_id, city__city_name__startswith=c, ads__start_time__lt=update_data[
                                                       "end_time"], ads__end_time__gt=update_data["start_time"]).exclude(ads_id=ads[0].id).exists()
                    t2 = ChannelCoverAds.objects.filter(channel_id=channel_id, city__city_name=u"全国", ads__start_time__lt=update_data[
                                                       "end_time"], ads__end_time__gt=update_data["start_time"]).exclude(ads_id=ads[0].id).exists()
                    t3 = ChannelCoverAds.objects.filter(channel_id=channel_id, ads__start_time__lt=update_data[
                                                       "end_time"], ads__end_time__gt=update_data["start_time"]).exclude(ads_id=ads[0].id).exists() if c==u"全国" else False
                    if t1 or t2 or t3:
                        return {"msg": u"同一城市时间交叉", "code": 1}
                ads.update(**update_data)
                old_cc = ChannelCoverAds.objects.filter(
                    channel_id=channel_id, ads_id=ads[0].id)
                ca_objects = []
                for c in cities:
                    try:
                        city = PtYellowCitylist.objects.get(
                            city_name=c if c == u"全国" else c + u"市")
                    except PtYellowCitylist.DoesNotExist:
                        city = PtYellowCitylist.objects.get(
                            city_name=c + u"县")
                    ca_objects.append(ChannelCoverAds(channel_id=channel_id,
                                                      ads_id=ads[0].id,
                                                      city=city,
                                                      ))
                    delete_ads_cache(channel_id, c)

                delete_many_ads_cache(
                    [make_ads_cache_key(channel_id, c.city.city_name[:-1]) for c in old_cc])
                old_cc.delete()
                ChannelCoverAds.objects.bulk_create(ca_objects)
                cache_clear()
                if u"全国" in cities:
                    cache_clear()
            else:
                ads = CoverAds.objects.create(**update_data)
                ca_objects = []
                for c in cities:
                    try:
                        city = PtYellowCitylist.objects.get(
                            city_name=c if c == u"全国" else c + u"市")
                    except PtYellowCitylist.DoesNotExist:
                        city = PtYellowCitylist.objects.get(
                            city_name=c + u"县")
                    cca1 = ChannelCoverAds.objects.filter(channel_id=channel_id, city=city, ads__start_time__lt=update_data[
                                                       "end_time"], ads__end_time__gt=update_data["start_time"]).exists()
                    cca2 = ChannelCoverAds.objects.filter(channel_id=channel_id, ads__start_time__lt=update_data[
                                                       "end_time"], ads__end_time__gt=update_data["start_time"]).exists() if c==u"全国" else False
                    cca3 = ChannelCoverAds.objects.filter(channel_id=channel_id, city__city_name=u"全国", ads__start_time__lt=update_data[
                                                       "end_time"], ads__end_time__gt=update_data["start_time"]).exists()
                    if cca1 or cca2 or cca3:
                        ads.delete()
                        return {"msg": u"同一城市时间交叉", "code": 1}
                    ca_objects.append(ChannelCoverAds(channel_id=channel_id,
                                                      ads_id=ads.id,
                                                      city=city,
                                                      ))
                    delete_ads_cache(channel_id, c)
                ChannelCoverAds.objects.bulk_create(ca_objects)
                cache_clear()
                if u"全国" in cities:
                    cache_clear()
            return {"msg": u"操作成功", "code": 0}
        data = {"msg": u"缺少参数", "code": 1}
    except:
        ptlog()
        data = {"msg": u"操作失败", "code": 1}

    return data


def delete_ads(channel_id, ads_id):
    cca = ChannelCoverAds.objects.filter(channel_id=channel_id, ads_id=ads_id)
    delete_many_ads_cache(
        [make_ads_cache_key(channel_id, c.city.city_name[:-1]) for c in cca])
    if ChannelCoverAds.objects.filter(channel_id=channel_id, ads_id=ads_id, city_id=-1).exists():
        cache_clear()
    CoverAds.objects.filter(id=ads_id).delete()
    cca.delete()
    return {"msg": u"删除成功", "code": 0}
