#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author sunq
import time
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q

from common.base_cursor import BaseCursor
from main.models import CmsQuickOrderGoods


class QuickOrderGoods():
    @classmethod
    def create_or_get(cls, quick_id, goods_id, operation_desc, create_uid, sort):
        try:
            obj = CmsQuickOrderGoods.objects.filter(Q(quick_order_id=quick_id) & Q(goods_id=goods_id)).get()
        except ObjectDoesNotExist:
            obj = CmsQuickOrderGoods()
            obj.create_date = time.time()
            obj.create_uid = create_uid
        obj.quick_order_id = quick_id
        obj.goods_id = goods_id
        obj.operation_desc = operation_desc
        obj.sort = sort
        obj.save()
        return obj

    @classmethod
    def create_schedule(cls, goods, current_user, quick_id):
        exist_id = cls.get_goods_ids(quick_id)
        result = []
        for index, item in enumerate(goods):
            qg = QuickOrderGoods.create_or_get(quick_id, item['goodsid'], item['desc'], current_user,
                                               len(goods) - index)
            result.append(qg)
        new_id = set()
        for i in result:
            new_id.add(i.id)
        deleting_ids = exist_id-new_id
        cls.delete(deleting_ids)
        return result
    @classmethod
    def get_goods_ids(cls,quick_id):
        sql = "SELECT id FROM cms_quick_order_goods where quick_order_id={0}".format(quick_id)
        ids = BaseCursor.get_all(sql)
        result = set()
        for i in ids:
            result.add(i[0])
        return result

    @classmethod
    def delete(cls, deleting_ids):
        for i in deleting_ids:
            CmsQuickOrderGoods.objects.filter(id=i).delete()
    @classmethod
    def get_goods_simple(cls, quick_id):
        sql = "select g.cp_name,g.name from cms_quick_order_goods qog inner join view_cms_goods_formal g on g.goods_id = qog.goods_id and g.parent_id=-1 where qog.quick_order_id={0}".format(
            quick_id)
        result = BaseCursor.get_all(sql=sql)
        return list(map(cls.quick_order_simple_format, result))

    @classmethod
    def get_goods_simple_str(cls, quick_id):
        result = cls.get_goods_simple(quick_id)
        return ';'.join(result)

    @classmethod
    def quick_order_simple_format(cls, item):
        return '-'.join(item)

    @classmethod
    def get_goods(cls, quick_order_id):
        sql = "select qg.goods_id,qg.operation_desc,g.cp_name,g.city,g.name from cms_quick_order_goods qg inner join view_cms_goods_formal g on g.goods_id = qg.goods_id and g.parent_id=-1 where qg.quick_order_id={0} order by qg.sort desc".format(
            quick_order_id)
        result = BaseCursor.get_all(sql)
        return result
