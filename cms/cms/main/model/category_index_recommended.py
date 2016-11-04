#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author sunq
import time
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q

from common.base_cursor import BaseCursor
from common.views import make_timestamp, timestamp2str
from main.models import CmsCategoryIndexRecommendedGoods


class CategoryIndexRecommended():
    @classmethod
    def create_or_update(cls, category_index_id, goods_id, sort, start_date, end_date, create_uid):
        try:
            obj = CmsCategoryIndexRecommendedGoods.objects.filter(
                Q(category_index_id=category_index_id) & Q(goods_id=goods_id)).get()
            obj.sort = sort
            obj.start_date = make_timestamp(start_date)
            obj.end_date = make_timestamp(end_date)
            obj.save()
        except ObjectDoesNotExist:
            obj = CmsCategoryIndexRecommendedGoods()
            obj.category_index_id = category_index_id
            obj.goods_id = goods_id
            obj.sort = sort
            obj.start_date = make_timestamp(start_date)
            obj.end_date = make_timestamp(end_date)
            obj.create_date = time.time()
            obj.create_uid = create_uid
            obj.save()
        return obj

    @classmethod
    def create_schedule(cls, category_index_id, recommendeds, current_uid):
        exist_ids = cls.get_recommended_ids(category_index_id)
        result = []
        for (index, item) in enumerate(recommendeds):
            obj = cls.create_or_update(category_index_id, item['goods_id'], len(recommendeds) - index, item['start'],
                                       item['end'],
                                        current_uid)
            result.append(obj)
        new_id = set()
        for i in result:
            new_id.add(i.id)
        deleting_ids = exist_ids - new_id
        cls.delete(deleting_ids)
        return result

    @classmethod
    def delete(cls, deleting_ids):
        for i in deleting_ids:
            CmsCategoryIndexRecommendedGoods.objects.filter(id=i).delete()

    @classmethod
    def get_recommended_ids(cls, category_index_id):
        sql = "SELECT id FROM cms_category_index_recommended_goods where category_index_id={0}".format(
            category_index_id)
        ids = BaseCursor.get_all(sql)
        result = set()
        for i in ids:
            result.add(i[0])
        return result

    @classmethod
    def get_recommended(cls, category_index_id):
        sql = "select cg.goods_id,g.name,cg.start_date,cg.end_date from cms_category_index_recommended_goods cg inner join view_cms_goods_formal g on g.goods_id = cg.goods_id and g.parent_id=-1 where cg.category_index_id={0} ORDER BY cg.sort DESC".format(
            category_index_id)
        result = BaseCursor.get_all(sql=sql)

        def _format(item):
            item[-1] = timestamp2str(item[-1])
            item[-2] = timestamp2str(item[-2])
            return item

        result = list(map(_format, result))
        return result
