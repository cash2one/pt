# -*- coding: utf-8 -*-
# Author:songroger
# Aug.1.2016
from __future__ import unicode_literals
from __future__ import division
import json
import traceback
import logging
from ..models import Tags, TagGoods, TagGroup
from main.models import CmsNaviCategory
from django.core.paginator import Paginator
from django.db import connection, IntegrityError
from pttools.ptformat import check_name_exists


log = logging.getLogger("main.app")

__all__ = ["get_tags_list", "get_tag", "add_tag", "delete_tags",
           "up_tag", "delete_tag", "get_tag_goods_list", "tag_to_goods",
           "tag_to_group", "delete_group_tag", "get_third_category_list",
           "cats_get_goods", "set_tag_sort", "get_all_skus"]


def get_tags_list(page, limit, full):
    if full == 1:
        tags = Tags.objects.all().only("id", "name", "remark").order_by("-id")
        return [dict(id=t.id, name=str((t.remark or "") + "_" + t.name))
                for t in tags]
    data = {}
    data['tags'] = []
    # tags = Tags.objects.all().order_by('-id')
    tags = _get_tags_data()

    p = Paginator(tags, limit)
    if page > p.num_pages:
        return data
    tags = p.page(page)
    data['tags'] = [
        dict(id=t[0],
             name=t[1],
             remark=t[2],
             goods_name=t[4],
             logo=t[5],
             desc=t[6]
             ) for t in tags]

    data["total"] = p.count
    data['page'] = page
    data["totalpage"] = p.num_pages
    data["hasNext"] = tags.has_next()
    return data


def _get_tags_data():
    cur = connection.cursor()
    sql = '''
        SELECT  a.id
                ,a.name
                ,a.remark
                ,t.sort
                #,GROUP_CONCAT(DISTINCT s.sku_name SEPARATOR '、') AS sku_names
                ,GROUP_CONCAT(DISTINCT v.name SEPARATOR '、') AS goods_names
                ,a.logo
                ,a.description
        FROM cms_tag a
        LEFT JOIN cms_tag_group_tag t
        ON a.id= t.tag_id
        LEFT JOIN cms_goods_sku_tag c
        ON a.id = c.tag_id
        LEFT JOIN cms_sku s
        ON s.sku_id = c.sku_id AND s.goods_id=c.goods_id
        LEFT JOIN view_cms_goods_formal v
        ON v.goods_id= c.goods_id
        GROUP BY a.id,a.name,a.remark
        ORDER BY a.id DESC;
    '''
    cur.execute(sql)
    row = cur.fetchall()
    return row


def get_tag(tid):
    data = {}
    try:
        tag = Tags.objects.get(id=tid)
        data["data"] = {"id": tag.id,
                        "name": tag.name,
                        "remark": tag.remark,
                        "logo": tag.logo,
                        "desc": tag.description,
                        }
        data["code"] = 0
    except Tags.DoesNotExist:
        data = {"msg": u"标签不存在", "code": 1}

    return data


def add_tag(request):
    data = {}
    # c_user = request.user.username
    json_string = request.body.decode('utf-8')
    try:
        request_data = json.loads(json_string)
        if request_data:
            remark = request_data.get('remark', None)
            name = request_data.get('name', "")
            logo = request_data.get('logo', None)
            desc = request_data.get('desc', None)
            name_exists = check_name_exists('cms_tag', 'name', name)
            if name_exists:
                return {"msg": u"名称与其他标签重复，请修改名称", "code": 1}
            Tags.objects.create(name=name, remark=remark,
                                logo=logo, description=desc)
            return {"msg": u"添加成功", "code": 0}
        data = {"msg": u"缺少参数", "code": 1}
    except:
        data = {"msg": u"添加失败", "code": 1}

    return data


def up_tag(request, tid):
    data = {}
    # c_user = request.user.username
    json_string = request.body.decode('utf-8')
    try:
        request_data = json.loads(json_string)
        if request_data:
            tag = Tags.objects.filter(id=tid)
            remark = request_data.get('remark', tag[0].remark)
            name = request_data.get('name')
            logo = request_data.get('logo', tag[0].logo)
            desc = request_data.get('desc', tag[0].description)
            tag.update(name=name, remark=remark, logo=logo, description=desc)
            return {"msg": u"修改成功", "code": 0}
        data = {"msg": u"缺少参数", "code": 1}
    except IndexError:
        data = {"msg": u"标签不存在", "code": 1}
    except IntegrityError:
        data = {"msg": u"名称与其他标签重复，请修改名称", "code": 1}
    except:
        data = {"msg": u"修改失败", "code": 1}

    return data


def delete_tag(tid):
    try:
        tag = Tags.objects.get(id=tid)
        tag.delete()
        TagGoods.objects.filter(tag_id=tid).delete()
        TagGroup.objects.filter(tag_id=tid).delete()
        data = {"msg": u"删除成功", "code": 0}
    except Tags.DoesNotExist:
        data = {"msg": u"标签不存在", "code": 1}

    return data


def get_tag_goods_list(page, limit, tag):
    # todo: 取标签商品列表详情
    data = {}
    data['tag_goods'] = []
    tag_goods = _get_tag_goods(tag)

    p = Paginator(tag_goods, limit)
    if page > p.num_pages:
        return data
    tag_goods = p.page(page)
    data['tag_goods'] = [
        dict(id=t[0],
             sku_id=t[1],
             name=t[2],
             icon_url=t[3],
             cp_name=t[4],
             desc=t[5],
             city=t[6],
             sku_name=t[7],
             gid=t[8],
             ) for t in tag_goods]

    data["total"] = p.count
    data['page'] = page
    data["totalpage"] = p.num_pages
    data["hasNext"] = tag_goods.has_next()
    return data


def _get_tag_goods(tag):
    cur = connection.cursor()
    sql = '''
        SELECT  v.id
                ,a.sku_id
                ,v.name
                ,v.icon_url
                ,v.cp_name
                ,v.desc
                ,v.city
                ,s.sku_name
                ,a.goods_id
        FROM cms_goods_sku_tag a
        LEFT JOIN view_cms_goods_formal v
        ON a.goods_id= v.goods_id
        LEFT JOIN cms_sku s
        ON a.goods_id= s.goods_id AND a.sku_id=s.sku_id
        WHERE a.tag_id = %s
        ORDER BY a.id DESC;
    '''
    cur.execute(sql, tag)
    row = cur.fetchall()
    return row


def tag_to_goods(tag_id, goods_id):
    """
    给商品打标签
    """
    try:
        if tag_id and goods_id:
            # sku_dict = _get_sku_dict(goods_id)
            ca_objects = [TagGoods(goods_id=g.get("cid"),
                                   sku_id=g.get("sid", 0),
                                   tag_id=tag_id) for g in goods_id]
            TagGoods.objects.bulk_create(ca_objects)
        data = {"msg": u"添加成功", "code": 0}
    except IntegrityError:
        data = {"msg": u"部分商品已存在,不能重复添加", "code": 1}
    except:
        data = {"msg": u"添加失败", "code": 1}
    return data


def _get_sku_dict(goods_id):
    return {}


def delete_tags(tag_id, goods_id, sku_id):
    try:
        t = TagGoods.objects.get(
            goods_id=goods_id, tag_id=tag_id, sku_id=sku_id)
        t.delete()
        data = {"msg": u"删除成功", "code": 0}
    except TagGoods.DoesNotExist:
        data = {"msg": u"数据不存在", "code": 1}
    return data


def tag_to_group(tag_group_id, tags_id):
    """
    给标签组添加标签
    """
    try:
        # with transaction.atomic():
        if tag_group_id and tags_id:
            ca_objects = [TagGroup(tag_group_id=tag_group_id,
                                   tag_id=t
                                   ) for t in tags_id]
            TagGroup.objects.bulk_create(ca_objects)
        return {"msg": u"添加成功", "code": 0}
    except IntegrityError:
        return {"msg": u"部分标签已存在,不能重复添加", "code": 1}
    except:
        return {"msg": u"添加失败", "code": 1}


def delete_group_tag(group_id, tag_id):
    try:
        t = TagGroup.objects.get(tag_group_id=group_id, tag_id=tag_id)
        t.delete()
        data = {"msg": u"删除成功", "code": 0}
    except TagGroup.DoesNotExist:
        data = {"msg": u"数据不存在", "code": 1}
    return data


def get_third_category_list(cat_ids):
    """
    获取分类列表
    """
    cnc = CmsNaviCategory.objects.filter(fatherid__in=cat_ids, type=0).only(
        "id", "name").distinct().order_by("-id")
    return [dict(id=c.id, name=c.name) for c in cnc]


def cats_get_goods(tid, thd_cat_ids, sec_cat_ids):
    """
    获取商品列表
    @para: thd_cat_ids:三级分类ID列表, sec_cat_ids:二级分类
    @return 商品列表
    """
    sql = '''
        SELECT a.goods_id
               ,a.name
               ,IFNULL(s.sku_name,"") AS sku_name
               ,a.cp_name
               ,a.city
               ,IFNULL(s.sku_id,0) AS sku_id
        FROM view_cms_goods_formal a
        LEFT JOIN cms_sku s
        ON s.goods_id=a.goods_id
        LEFT JOIN (
            SELECT  a.goods_id
                ,a.sku_id
            FROM cms_goods_sku_tag a
            LEFT JOIN view_cms_goods_formal v
            ON a.goods_id= v.goods_id
            LEFT JOIN cms_sku s
            ON a.goods_id= s.goods_id AND a.sku_id=s.sku_id
            WHERE a.tag_id = %s
            ORDER BY a.id DESC
            ) b
        ON a.goods_id = b.goods_id
        AND b.sku_id = IFNULL(s.sku_id,0)
        WHERE (new_second_category IN (%s) OR new_category IN (%s))
        AND b.goods_id IS NULL
        ORDER BY a.id DESC;
    '''
    cur = connection.cursor()
    sql_exe = sql % (tid, ",".join(map(str, thd_cat_ids)) or "''",
                     ",".join(map(str, sec_cat_ids)) or "''")
    cur.execute(sql_exe)
    row = cur.fetchall()
    data = [dict(cid=r[0],
                 name="-".join([r[1], r[2], r[3], r[4]]),
                 sku_id=r[5]) for r in row]
    return data


def set_tag_sort(tid, gid, sort):
    try:
        TagGroup.objects.filter(tag_group_id=gid, tag_id=tid).update(sort=sort)
        data = {"msg": u"设置成功", "code": 0}
    except:
        data = {"msg": u"设置失败", "code": 1}
    return data


def get_all_skus():
    """
    获取全部商品sku列表
    @return 商品sku列表
    """
    sql = '''
        SELECT a.goods_id
               ,a.name
               ,IFNULL(s.sku_name,"") AS sku_name
               ,a.cp_name
               ,a.city
               ,IFNULL(s.sku_id,0) AS sku_id
        FROM view_cms_goods_formal a
        LEFT JOIN cms_sku s
        ON s.goods_id=a.goods_id
        ORDER BY a.id DESC;
    '''
    cur = connection.cursor()
    cur.execute(sql)
    row = cur.fetchall()
    data = [dict(cid=r[0],
                 name="-".join([r[1], r[2], r[3], r[4]]),
                 sku_id=r[5]) for r in row]
    return data
