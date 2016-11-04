# -*- coding: utf-8 -*-
# Author:songroger
# Aug.29.2016
from __future__ import unicode_literals
from pttools.pthttp import PtHttpResponse, get_requests_json, get_response_json
from ads.ads_cache import get_ads_cache
from main.models import CmsChannels
from django.db import connection
from ads.settings import GET_BOUGHT_URL, REQ_ENV, GET_GOODS_INFO,\
    GET_GOODS_PROMOTION
from pttools.ptformat import to_unixtime
from datetime import datetime
# import time
import json
from pttools.ptapps import check_range, safe_distance
from pttools.ptformat import md5str, uniquenum


def get_ads(request):
    data = {"msg": u"获取成功",
            "code": 0,
            "server_time": to_unixtime(datetime.now())}
    city = request.GET.get('city')
    app_version = request.GET.get('app_version', None)
    channel_no = request.GET.get('channel_no', None)
    if app_version and channel_no:
        try:
            ch = CmsChannels.objects.get(
                channel_no=channel_no, app_version__app_version=app_version)
        except CmsChannels.DoesNotExist:
            try:
                ch = CmsChannels.objects.get(
                    order=1, app_version__app_version=app_version)
            except CmsChannels.DoesNotExist:
                data.update({"msg": u"无该渠道配置内容", "code": 1, "data": []})
                return PtHttpResponse(data)
        data["data"] = get_ads_cache(ch.id, city) if city else []
        data["data_version"] = uniquenum(md5str(json.dumps(data["data"])))
    else:
        data.update({"msg": u"URL缺少必传参数", "code": 1, "data": []})

    return PtHttpResponse(data)


def ptcard_list(request):
    data = {"msg": u"获取成功",
            "code": 0,
            "data": {},
            "server_time": to_unixtime(datetime.now())}
    page = int(request.GET.get('page', 1))
    limit = int(request.GET.get('page_size', 10))
    start = (int(page) - 1) * limit
    tag_id = int(request.GET.get('tag_id')) if request.GET.get(
        'tag_id') else -10000
    city = request.GET.get('city', '')
    pt_token = request.GET.get('pt_token', '')
    location = request.GET.get('location', '')
    longitude = location.split(",")[1] if location else ""
    latitude = location.split(",")[0] if location else ""
    district = request.GET.get('district', '')
    data["data"]["tags"] = _get_tags_data(city)
    data["data"]["goods_list"] = _get_goods(
        tag_id, start, limit, city, pt_token, longitude, latitude, district)
    data["data"]["current_tag_id"] = tag_id

    return PtHttpResponse(data)


def _get_tags_data(city):
    cur = connection.cursor()
    sql = '''
        SELECT DISTINCT IFNULL(v.`new_second_category`,-9999) AS nav_id
               ,IFNULL(n.name,"其他") AS nav_name
               ,IFNULL(n.location,9999) AS sort
        FROM `view_cms_goods_formal` v
        LEFT JOIN `cms_navi_category` AS n
        ON v.`new_second_category` = n.id
        WHERE card_type !=0
        AND v.sale_status=1
    '''
    if city:
        c_like = '%' + city + '%'
        sql += '''
        AND (v.city = '*' OR v.city like %s)
        '''
    sql += '''
        ORDER BY sort
        '''
    if city:
        cur.execute(sql, c_like)
    else:
        cur.execute(sql)
    row = cur.fetchall()
    tags = [dict(id=-10000, name=u"全部", sort=-1, is_available=1)]
    tags.extend([dict(id=d[0],
                      name=d[1],
                      sort=d[2],
                      is_available=1) for d in row])
    return tags


def _get_goods(tag_id, start, limit, city, pt_token,
               longitude, latitude, district):
    data = []
    cur = connection.cursor()
    sql = '''
        SELECT v.`goods_id`
               ,v.`name`
               ,v.`cp_name`
               ,v.`icon_url`
               ,v.`fav_price`
               ,v.`price`
               ,v.`fav_price_desc`
               ,v.`desc`
               ,v.`is_support_cart_i`
               ,v.`recommend_icon`
               ,UNIX_TIMESTAMP(o.activityBeginDate) * 1000 AS unix_begin_time
               ,UNIX_TIMESTAMP(o.activityEndDate) * 1000 AS unix_end_time
               ,o.promotionMsg  #r[12]
               ,o.applyUser
               ,o.activityCity
               ,o.activityPrice
               ,v.mark
               ,v.serviceRangeGraph #r[17]
               ,v.serviceRangeJson
               ,v.citysJson
               ,v.tag1
               ,v.tag1_style
               ,v.tag2
               ,v.tag2_style
               ,v.tag3
               ,v.tag3_style
        FROM `view_cms_goods_formal` v
        LEFT JOIN `cms_navi_category` AS n
        ON v.`new_second_category` = n.id
        left join op_goods_activity o
        on v.`goods_id`= o.`goodsId`
        WHERE card_type !=0
        AND v.sale_status=1
    '''
    if tag_id == -9999:
        sql += '''
            AND v.`new_second_category` IS NULL
        '''
    elif tag_id and tag_id != -10000:
        sql += '''
            AND v.`new_second_category`=%s
        ''' % tag_id
    if city:
        c_like = '%' + city + '%'
        sql += '''
        AND (v.city = '*' OR v.city like %s)
        '''
    sql += '''
        ORDER BY v.`goods_id` DESC
    '''
    if city:
        cur.execute(sql, c_like)
    else:
        cur.execute(sql)
    row = cur.fetchall()
    gids = [t[0] for t in row]
    seckill_gids, seckill_time = _get_seckill_goods(city)
    goods_info = _get_goods_info_by_req(gids, pt_token, city)
    goods_promotion = _get_goods_promotion_by_req(gids, pt_token, city)
    for t in row:
        is_seckill = _get_seckill_status(seckill_gids, t[0])
        # promotion_msg = _get_promotion_msg(
        #     t[12], t[13], t[14], t[15], t[4], pt_token, t[0])
        promotion_msg = goods_info.get(
            str(t[0]))["promotionMsg"] if goods_info.get(str(t[0])) else t[12]
        operation_msg = goods_info.get(
            str(t[0]))["operationMsg"] if goods_info.get(str(t[0])) else ""
        activity_price = goods_info.get(
            str(t[0]))["promotionPrice"] / 100 if goods_info.get(str(t[0])) else None
        is_within_range = _get_is_within_range_status(
            t[17], t[18], t[19], longitude, latitude, city, district)
        comment_count = goods_promotion.get(
            t[0], {}).get("comment_count", None)
        data.append(dict(id=t[0],
                         cpname=t[2],
                         icon=t[3],
                         fav_price=float(t[4]),
                         price=float(t[5]),
                         price_unit=t[6],
                         name=t[1],
                         goods_desc=t[7],
                         is_support_cart=t[8],
                         recommend_icon=t[9],
                         sold_count=-1,
                         promotion_msg=promotion_msg,
                         activity_price=activity_price,
                         operation_msg=operation_msg,
                         operation_tag=t[16],
                         op_tag=_op_tag_list(t[20], t[21], t[22], t[23], t[24], t[25]),
                         is_seckill=is_seckill,
                         is_within_range=is_within_range,
                         commentCount=u"好评数%s" % comment_count if comment_count else None,
                         start_time=seckill_time.get(
                             t[0])["start_time"] if is_seckill else None,
                         end_time=seckill_time.get(
                             t[0])["end_time"] if is_seckill else None))
    return sorted(data, key=lambda k: k['is_within_range'], reverse=True)[start: start + limit]


def _op_tag_list(t1, t1s, t2, t2s, t3, t3s):
    op_tags = []
    if t1:
        op_tags.append(dict(tag=t1, tag_style=t1s))
    if t2:
        op_tags.append(dict(tag=t2, tag_style=t2s))
    if t3:
        op_tags.append(dict(tag=t3, tag_style=t3s))
    return op_tags


def _get_seckill_status(seckill_gids, gid):
    if gid in seckill_gids:
        return 1
    return 0


def _get_promotion_msg(msg, apluser, city, actprice, fav_price, pt_token, gid):
    if pt_token:
        bought_status = _get_bought_status(pt_token, gid)
        if bought_status and apluser == "0" or apluser == "2":
            return ""
    else:
        return msg


def _get_bought_status(pt_token, gid):
    stat, rsp = get_requests_json(GET_BOUGHT_URL.get(REQ_ENV) % pt_token)
    if stat == 200:
        return True
    return False


def _get_operation_msg():
    return ""


def _get_operation_tag(tag):
    return tag


def _get_activity_price():
    return None


def _get_is_within_range_status(graph, rangejson, citiesjson,
                                longitude, latitude, city, district):
    if not graph and not rangejson and not city:
        return 1
    status = 0
    if graph:
        status = _check_gragh(graph, longitude, latitude)
        if status != 1 and rangejson:
            status = _check_rangejson(rangejson, longitude, latitude)

    elif status != 1 and rangejson:
        status = _check_rangejson(rangejson, longitude, latitude)
    if status != 1 and citiesjson:
        status = _check_city(citiesjson, city, district)

    return status


def _get_comment_count(gid):
    return ""


def _get_goods_info_by_req(gids, pt_token, city):
    payload = dict(pt_token=pt_token, gids=gids, city=city)
    stat, rsp = get_response_json(GET_GOODS_INFO.get(REQ_ENV), params=payload)
    if stat == 200 and rsp.get("data"):
        return rsp["data"]
    return {}


def _check_gragh(graph, longitude, latitude):
    if graph and longitude and latitude:
        position_tmp = dict(lat=float(latitude), lng=float(longitude))
        for m in json.loads(graph):
            if check_range(position_tmp, m):
                return 1
        return 0
    else:
        return 0


def _check_rangejson(rangejson, longitude, latitude):
    if rangejson and latitude:
        for r in json.loads(rangejson):
            if safe_distance(float(latitude), float(longitude), float(r["latitude"]), float(r["longitude"])) <= r["radius"]:
                return 1
        return 0
    else:
        return 0


def _check_city(citiesjson, city, district):
    if citiesjson and city:
        for c in json.loads(citiesjson):
            if (c.get("city") is None or c.get("city") == u"全国" or c.get("city").find(city) != -1 or c.get("city") == "") and (c.get("districts") is None or c.get("districts") == u"全市" or district and c.get("districts").find(district) != -1):
                return 1
        return 0
    else:
        return 0


def _get_seckill_goods(city):
    cur = connection.cursor()
    sql = '''
    SELECT goodsId
           ,UNIX_TIMESTAMP(activityBeginDate) * 1000 AS unix_begin_time
           ,UNIX_TIMESTAMP(activityEndDate) * 1000 AS unix_end_time
    FROM op_goods_activity_act
    WHERE is_seckill=1
        AND activityBeginDate<NOW()
        AND activityEndDate>NOW()
        AND (activityCity='全国' OR activityCity LIKE %s)
    '''
    c_like = '%' + city + '%'
    cur.execute(sql, c_like)
    row = cur.fetchall()
    data = {}
    for r in row:
        data.update({r[0]: dict(start_time=r[1], end_time=r[2])})
    return [r[0] for r in row], data


def _get_goods_promotion_by_req(gids, pt_token, city):
    data = {}
    payload = dict(pt_token=pt_token, gids=gids, city=city)
    stat, rsp = get_response_json(
        GET_GOODS_PROMOTION.get(REQ_ENV), params=payload)
    if stat == 200 and rsp.get("data"):
        for d in rsp.get("data"):
            data.update({d["gid"]: dict(comment_count=d[
                        "commentCount"], promotion_msg=d["promotionMsg"])})
    return data
