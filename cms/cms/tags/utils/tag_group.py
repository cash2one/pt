# -*- coding: utf-8 -*-
# Author:songroger
# Aug.1.2016
from __future__ import unicode_literals
from __future__ import division
from ..models import Groups, TagBooking, TagGroup
import json
from django.db import connection, IntegrityError
from django.core.paginator import Paginator
import traceback
import logging
from pttools.ptformat import check_name_exists, ptlog

log = logging.getLogger("main.app")

__all__ = ["get_tag_group_list", "get_tag_group", "get_tag_group_tags",
           "add_tag_group", "up_tag_group", "delete_tag_group",
           "get_booking_tag_groups", "get_booking_groups", "tag_to_booking",
           "delete_tag_booking", "set_group_sort"]


def get_tag_group_list(page, limit, full):
    if full == 1:
        groups = Groups.objects.all().order_by("-id")
        return [dict(id=t.id,
                     name=str((t.remark or "") + "_" + t.tag_group_name))
                for t in groups]
    data = {}
    data['groups'] = []
    # groups = Groups.objects.all().order_by('-id')
    groups = _get_groups_data()

    p = Paginator(groups, limit)
    if page > p.num_pages:
        return data
    groups = p.page(page)
    data['groups'] = [
        dict(id=t[0],
             name=t[1],
             remark=t[2],
             tags_name=t[3]
             ) for t in groups]

    data["total"] = p.count
    data['page'] = page
    data["totalpage"] = p.num_pages
    data["hasNext"] = groups.has_next()
    return data


def _get_groups_data():
    cur = connection.cursor()
    sql = '''
        SELECT  a.id
                ,a.tag_group_name
                ,a.remark
                ,GROUP_CONCAT(c.name SEPARATOR '、') AS tag_name
        FROM cms_tag_group a
        LEFT JOIN cms_tag_group_tag t
        ON a.id= t.tag_group_id
        LEFT JOIN cms_tag c
        ON t.tag_id = c.id
        GROUP BY a.id,a.tag_group_name,a.remark
        ORDER BY a.id DESC;
    '''
    cur.execute(sql)
    row = cur.fetchall()
    return row


def get_tag_group(gid):
    data = {}
    try:
        group = Groups.objects.get(id=gid)
        data["data"] = {"id": group.id,
                        "name": group.tag_group_name,
                        "remark": group.remark,
                        }
        data["code"] = 0
    except Groups.DoesNotExist:
        data = {"msg": u"标签组不存在", "code": 1}

    return data


def add_tag_group(request):
    data = {}
    # c_user = request.user.username
    json_string = request.body.decode('utf-8')
    try:
        request_data = json.loads(json_string)
        if request_data:
            remark = request_data.get('remark', None)
            name = request_data.get('name', '')
            bid = request_data.get('bid', None)
            name_exists = check_name_exists(
                "cms_tag_group", 'tag_group_name', name)
            if name_exists:
                return {"msg": u"名称与其他标签组重复，请修改名称", "code": 1}
            group = Groups.objects.create(tag_group_name=name, remark=remark)

            # 在快捷入口处新建group组，直接添加进：快捷入口-标签组
            if bid:
                TagBooking.objects.create(
                    quick_order_id=bid, tag_group_id=group.id)
            return {"msg": u"添加成功", "code": 0}
        data = {"msg": u"缺少参数", "code": 1}
    except:
        ptlog()
        data = {"msg": u"添加失败", "code": 1}

    return data


def up_tag_group(request, gid):
    data = {}
    # c_user = request.user.username
    json_string = request.body.decode('utf-8')
    try:
        request_data = json.loads(json_string)
        if request_data:
            group = Groups.objects.filter(id=gid)
            remark = request_data.get('remark', group[0].remark)
            name = request_data.get('name')
            group.update(tag_group_name=name, remark=remark)
            return {"msg": u"修改成功", "code": 0}
        data = {"msg": u"缺少参数", "code": 1}
    except IndexError:
        data = {"msg": u"标签组不存在", "code": 1}
    except IntegrityError:
        data = {"msg": u"名称与其他重复，请修改名称", "code": 1}
    except:
        ptlog()
        data = {"msg": u"添加失败", "code": 1}

    return data


def delete_tag_group(gid):
    try:
        group = Groups.objects.get(id=gid)
        group.delete()
        TagGroup.objects.filter(tag_group_id=gid).delete()
        data = {"msg": u"删除成功", "code": 0}
    except Groups.DoesNotExist:
        data = {"msg": u"标签组不存在", "code": 1}

    return data


def get_tag_group_tags(page, limit, gid):
    data = {}
    data['tags'] = []
    tags = _get_tags_by_gid(gid)

    p = Paginator(tags, limit)
    if page > p.num_pages:
        return data
    tags = p.page(page)
    data['tags'] = [
        dict(id=t[0],
             name=t[1],
             remark=t[2],
             sort=t[3],
             sku_names=t[4],
             logo=t[5],
             desc=t[6]
             ) for t in tags]

    data["total"] = p.count
    data['page'] = page
    data["totalpage"] = p.num_pages
    data["hasNext"] = tags.has_next()
    return data


def _get_tags_by_gid(gid):
    cur = connection.cursor()
    sql = '''
        SELECT  a.id
                ,a.name
                ,a.remark
                ,t.sort
                ,GROUP_CONCAT(s.sku_name SEPARATOR '、') AS sku_names
                ,a.logo
                ,a.description
        FROM cms_tag a
        LEFT JOIN cms_tag_group_tag t
        ON a.id= t.tag_id
        LEFT JOIN cms_goods_sku_tag c
        ON a.id = c.tag_id
        LEFT JOIN cms_sku s
        ON s.sku_id = c.sku_id AND s.goods_id=c.goods_id
        WHERE t.tag_group_id=%s
        GROUP BY a.id,a.name,a.remark
        ORDER BY t.sort DESC, a.id DESC;
    '''
    cur.execute(sql, gid)
    row = cur.fetchall()
    return row


def get_booking_tag_groups(page, limit):
    data = {}
    data['groups'] = []
    groups = _get_booking_groups()

    p = Paginator(groups, limit)
    if page > p.num_pages:
        return data
    groups = p.page(page)
    data['groups'] = [
        dict(id=t[0],
             cat_name=t[3],
             name=t[1],
             desc=t[2],
             groups_name=t[4]
             ) for t in groups]

    data["total"] = p.count
    data['page'] = page
    data["totalpage"] = p.num_pages
    data["hasNext"] = groups.has_next()
    return data


def _get_booking_groups():
    cur = connection.cursor()
    sql = '''
        SELECT  a.id
               ,a.cms_quick_name
               ,a.cms_quick_desc
               ,c.name AS navi_name
               ,GROUP_CONCAT(g.tag_group_name SEPARATOR '、') AS group_name
        FROM cms_quick_order a
        LEFT JOIN cms_quick_order_category b
               ON a.id = b.quick_order_id
        LEFT JOIN cms_navi_category c
               ON b.category_id = c.id
        LEFT JOIN cms_quick_order_taggroup t
               ON a.id = t.quick_order_id
        LEFT JOIN cms_tag_group g
               ON t.tag_group_id = g.id
        GROUP BY a.cms_quick_name
               ,a.cms_quick_desc
               ,c.name
        ORDER BY id DESC
    '''
    cur.execute(sql)
    row = cur.fetchall()
    return row


def get_booking_groups(page, limit, bid):
    data = {}
    data['groups'] = []
    groups = _bid_get_groups(bid)

    p = Paginator(groups, limit)
    if page > p.num_pages:
        return data
    groups = p.page(page)
    data['groups'] = [
        dict(id=t[0],
             name=t[1],
             remark=t[2],
             tag_names=t[4],
             sort=t[3]
             ) for t in groups]

    data["total"] = p.count
    data['page'] = page
    data["totalpage"] = p.num_pages
    data["hasNext"] = groups.has_next()
    return data


def _bid_get_groups(bid):
    cur = connection.cursor()
    sql = '''
        SELECT  a.id
               ,a.tag_group_name
               ,a.remark
               ,b.level
               ,GROUP_CONCAT(c.name SEPARATOR '、') AS tag_name
        FROM cms_tag_group a
        LEFT JOIN cms_quick_order_taggroup b
               ON a.id = b.tag_group_id
        LEFT JOIN cms_tag_group_tag t
               ON a.id= t.tag_group_id
        LEFT JOIN cms_tag c
               ON t.tag_id = c.id
        WHERE b.quick_order_id = %s
        GROUP BY a.id
       ,a.tag_group_name
       ,a.remark;
    '''
    cur.execute(sql, bid)
    row = cur.fetchall()
    return row


def tag_to_booking(bid, gids):
    try:
        # with transaction.atomic():
        if gids:
            ca_objects = [TagBooking(quick_order_id=bid,
                                     tag_group_id=g
                                     ) for g in gids]
            TagBooking.objects.bulk_create(ca_objects)
        return {"msg": u"添加成功", "code": 0}
    except IntegrityError:
        return {"msg": u"部分标签组已存在,不能重复添加", "code": 1}
    except:
        return {"msg": u"添加失败", "code": 1}


def delete_tag_booking(bid, gid):
    try:
        t = TagBooking.objects.filter(quick_order_id=bid, tag_group_id=gid)
        t.delete()
        data = {"msg": u"删除成功", "code": 0}
    except:
        data = {"msg": u"删除失败", "code": 1}
    return data


def set_group_sort(bid, gid, sort):
    try:
        TagBooking.objects.filter(
            quick_order_id=bid, tag_group_id=gid).update(level=sort)
        data = {"msg": u"设置成功", "code": 0}
    except:
        data = {"msg": u"设置失败", "code": 1}
    return data
