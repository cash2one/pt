#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author sunq
import time
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

from common.base_cursor import BaseCursor
from main.model.quick_order_category import QuickOrderCategory
from main.model.quick_order_goods import QuickOrderGoods
from main.models import CmsQuickOrder, CmsQuickOrderCategory, CmsQuickOrderGoods, CmsCategoryIndexQuickOrder


class QuickOrderModel():
    @classmethod
    def create_or_get_quick_order(cls, name, desc, image_url, order_style, background_style, create_uid, is_h5, h5_url, id=0):
        if id:
            try:
                obj = CmsQuickOrder.objects.filter(id=id).get()
            except ObjectDoesNotExist:
                obj = CmsQuickOrder()
                obj.create_uid = create_uid
                obj.create_date = time.time()
            obj.cms_quick_name = name
            obj.cms_quick_desc = desc
            obj.order_style = order_style
            obj.background_style = background_style
            obj.image_url = image_url
            obj.is_h5 = is_h5
            obj.h5_url = h5_url
            obj.save()
        else:
            obj = CmsQuickOrder()
            obj.cms_quick_desc = desc
            obj.cms_quick_name = name
            obj.order_style = order_style
            obj.background_style = background_style
            obj.image_url = image_url
            obj.create_date = time.time()
            obj.create_uid = create_uid
            obj.is_h5 = is_h5
            obj.h5_url = h5_url
            obj.save()
        return obj

    @classmethod
    def search_quick_order(cls, page, per_page, key=None):
        sql = "select qo.id,c.name,qo.cms_quick_name,qo.cms_quick_desc from cms_quick_order qo inner join cms_quick_order_category qoc on qoc.quick_order_id = qo.id inner join cms_navi_category c on c.id=qoc.category_id order by qo.id desc"
        total_page, result = BaseCursor.get_pageinate(page, per_page, sql)
        return total_page, result

    @classmethod
    def delete_quick_order(cls, quick_order_id):
        # 删除管理的分类首页关系
        try:
            with transaction.atomic():
                CmsCategoryIndexQuickOrder.objects.filter(quick_order_id=quick_order_id).delete()
                CmsQuickOrderGoods.objects.filter(quick_order_id=quick_order_id).delete()
                CmsQuickOrderCategory.objects.filter(quick_order_id=quick_order_id).delete()
                CmsQuickOrder.objects.filter(id=quick_order_id).delete()
            return True
        except Exception:
            return False

    @classmethod
    def get_update_data(cls, id):
        try:
            quick_order = CmsQuickOrder.objects.filter(id=id).get()
            category = QuickOrderCategory.get_category(quick_order.id)
            if not category:
                return False
            goods = QuickOrderGoods.get_goods(quick_order.id)
            cp_names = [x[2] for x in goods]
            goods_ids = [x[0] for x in goods]
            return {'goods': goods, "goods_ids": goods_ids,
                    "cp_names": cp_names, "category_id": category[1],
                    "category_name": category[0], "quick_order_name": quick_order.cms_quick_name,
                    "background_style": quick_order.background_style,
                    "order_style": quick_order.order_style,
                    "image_url": quick_order.image_url,
                    "is_h5": quick_order.is_h5,
                    "h5_url": quick_order.h5_url,
                    "quick_order_desc": quick_order.cms_quick_desc}
        except ObjectDoesNotExist:
            return False
