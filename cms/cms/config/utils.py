# -*- coding: utf-8 -*-
# Author:songroger
# Jun.22.2016
from __future__ import unicode_literals
from main.models import CmsGoods
from config.models import CmsPackageGoods, CmsCategoryHotGoods
from django.core.paginator import Paginator
import requests
import json
from config.settings import pcard_goods_url
from django.db import connection


def get_pcard_goods_list(page, limit):
    """
    获取套餐卡商品列表
    """
    data = {}
    pcard_goods = CmsGoods.objects.filter(
        card_type__in=(1, 2), parent_id=-1).only("goods_id", "name")
    p = Paginator(pcard_goods, limit)
    if page > p.num_pages:
        return data
    pcd = p.page(page)
    data['pcards'] = [
        dict(id=c.goods_id,
             name=c.name,
             goods=_get_pcard_goods(c.goods_id),
             ) for c in pcd]

    data["total"] = p.count
    data['page'] = page
    data["totalpage"] = p.num_pages
    data["hasNext"] = pcd.has_next()
    return data


def _get_pcard_goods(pid):
    # cpgs = CmsPackageGoods.objects.filter(package_goods_id=pid)
    sql = """
    SELECT DISTINCT g.goods_id , g.name
    FROM cms_goods AS g
        LEFT JOIN cms_package_goods
        ON g.goods_id=cms_package_goods.goods_id
    WHERE cms_package_goods.package_goods_id=%s;
    """
    cur = connection.cursor()
    cur.execute(sql % pid)
    row = cur.fetchall()
    return [dict(id=r[0], name=r[1]) for r in row]


def _get_goods_name(gid):
    try:
        good = CmsGoods.objects.get(goods_id=gid)
        return good.name
    except:
        pass


def _get_common_goods_list():
    goods = CmsGoods.objects.filter(
        goods_id__gt=0, parent_id=-1).only("goods_id")
    return [dict(id=g.goods_id,
                 name=g.name) for g in goods]


def get_pcard_goods(pcard_id):
    """
    获取套餐卡商品
    @parameter: pcard_id
    """
    return _get_pcard_goods(pcard_id)


def add_pcard_goods(request):
    data = {}
    json_string = request.body.decode('utf-8')
    try:
        request_data = json.loads(json_string)
        if request_data:
            pid = request_data.get('pid', None)
            gid = request_data.get('gid', None)
            payload = {'packageGid': pid, 'gids': gid}
            # rurl = pcard_goods_url + "?packageGid=%s&gids=%s" % (pid, gid)
            r = requests.get(pcard_goods_url, params=payload)
            if r.json().get("code", {}) == 0:
                text = r.json().get("data", {})
                if text.get(str(gid)) == "success":
                    cpg, created = CmsPackageGoods.objects.get_or_create(
                        package_goods_id=pid, goods_id=gid)
                    if not created:
                        return {"msg": u"不能重复添加", "code": 1}
                    return {"msg": u"添加成功", "code": 0}
                return {"msg": text.get(str(gid)), "code": 1}
            else:
                return {"msg": r.json().get("msg", None), "code": 1}
        data = {"msg": u"缺少参数", "code": 1}
    except:
        data = {"msg": u"添加失败", "code": 1}
    return data


def delete_pcard_goods(pid, gid):
    try:
        cpgs = CmsPackageGoods.objects.get(package_goods_id=pid, goods_id=gid)
        cpgs.delete()
        data = {"msg": u"删除成功", "code": 0}
    except CmsPackageGoods.DoesNotExist:
        data = {"msg": u"套餐卡商品不存在", "code": 1}
    return data


def get_common_goods():
    """
    获取可添加商品
    @return:
    """
    return _get_common_goods_list()
