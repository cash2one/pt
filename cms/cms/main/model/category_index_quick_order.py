#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author sunq
import time
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q

from common.base_cursor import BaseCursor
from main.models import CmsCategoryIndexQuickOrder


class CategoryIndexQuickOrder():
    @classmethod
    def create_or_update(cls, quick_order_id, category_index_id, sort, create_uid):
        try:
            obj = CmsCategoryIndexQuickOrder.objects.filter(
                Q(quick_order_id=quick_order_id) & Q(category_index_id=category_index_id)).get()
            obj.sort = sort
            obj.save()
        except ObjectDoesNotExist:

            obj = CmsCategoryIndexQuickOrder()
            obj.quick_order_id = quick_order_id
            obj.category_index_id = category_index_id
            obj.create_date = time.time()
            obj.sort = sort
            obj.create_uid = create_uid
            obj.save()
        return obj

    @classmethod
    def create_schedule(cls, category_index_id, quick_orders, current_uid):
        exist_id = cls.get_quick_order_ids(category_index_id)
        result = []
        for (index, item) in enumerate(quick_orders):
            obj = cls.create_or_update(item['quick_order_id'], category_index_id, len(quick_orders) - index,
                                       current_uid)
            result.append(obj)
        new_id = set()
        for i in result:
            new_id.add(i.id)
        delting_ids = exist_id - new_id
        cls.delete(delting_ids)
        return result

    @classmethod
    def delete(cls, deleting_ids):
        for i in deleting_ids:
            CmsCategoryIndexQuickOrder.objects.filter(id=i).delete()

    @classmethod
    def get_quick_order_ids(cls, category_index_id):
        sql = "SELECT id FROM cms_category_index_quick_order where category_index_id={0}".format(category_index_id)
        ids = BaseCursor.get_all(sql)
        result = set()
        for i in ids:
            result.add(i[0])
        return result

    @classmethod
    def get_quick_orders(cls, category_index_id):
        sql = "select ciqo.quick_order_id,qo.cms_quick_desc,qo.cms_quick_name from cms_category_index_quick_order ciqo inner join cms_quick_order qo on qo.id = ciqo.quick_order_id where ciqo.category_index_id={0} ORDER BY ciqo.sort DESC".format(
            category_index_id)
        result = BaseCursor.get_all(sql=sql)
        return result
