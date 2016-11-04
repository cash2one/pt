#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author sunq
import time
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

from common.base_cursor import BaseCursor
from main.model.category_index_ads import CategoryIndexAds
from main.model.category_index_quick_order import CategoryIndexQuickOrder
from main.model.category_index_recommended import CategoryIndexRecommended
from main.models import CmsCategoryIndex, CmsCategoryIndexAds, CmsCategoryIndexQuickOrder, \
    CmsCategoryIndexRecommendedGoods, CmsNaviCategory


class CategoryIndex():
    @classmethod
    def create_or_update(cls, category_id, city, is_need_all, current_uid, id=0):
        if id > 0:
            try:
                obj = CmsCategoryIndex.objects.filter(id=id).get()
            except ObjectDoesNotExist:
                obj = CmsCategoryIndex()
                obj.create_uid = current_uid
                obj.create_date = time.time()
            obj.city = city
            obj.category_id = category_id
            obj.is_need_all_service = is_need_all
            obj.save()
        else:
            obj = CmsCategoryIndex()
            obj.create_uid = current_uid
            obj.create_date = time.time()
            obj.city = city
            obj.category_id = category_id
            obj.is_need_all_service = is_need_all
            obj.save()
        return obj

    @classmethod
    def search_category_index(cls, page, per_page, key=None):
        sql = "select ci.id,nc.name,ci.city from cms_category_index ci inner join cms_navi_category nc on nc.id = ci.category_id order by ci.id DESC "
        total_page, result = BaseCursor.get_pageinate(page, per_page, sql)
        return total_page, result

    @classmethod
    def delete_category_index(cls, id):
        try:
            with transaction.atomic():
                CmsCategoryIndexAds.objects.filter(category_index_id=id).delete()
                CmsCategoryIndexQuickOrder.objects.filter(category_index_id=id).delete()
                CmsCategoryIndexRecommendedGoods.objects.filter(category_index_id=id).delete()
                CmsCategoryIndex.objects.filter(id=id).delete()
            return True
        except Exception:
            return False

    @classmethod
    def get_update_data(cls, id):
        try:
            category_index = CmsCategoryIndex.objects.filter(id=id).values_list('id', 'category_id', 'city',
                                                                                'is_need_all_service').get()
            category = CmsNaviCategory.objects.filter(id=category_index[1]).values_list('name').get()
            banners = CategoryIndexAds.get_ads(category_index[0])
            quick_orders = CategoryIndexQuickOrder.get_quick_orders(category_index[0])
            recommendeds = CategoryIndexRecommended.get_recommended(category_index[0])
            quick_order_ids = [x[0] for x in quick_orders]
            goods_ids = [x[0] for x in recommendeds]
            return {"category_name":category[0],"category_id":category_index[1],
                    "category_index_id":category_index[0],
                    "category_city":category_index[2],
                    "category_is_need":category_index[3],
                    "banners":banners,
                    "quick_orders":quick_orders,
                    "quick_order_ids":quick_order_ids,
                    "goods":recommendeds,
                    "goods_ids":goods_ids}
        except ObjectDoesNotExist:
            return False
