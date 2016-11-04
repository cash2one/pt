#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author sunq
import time
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q

from common.base_cursor import BaseCursor
from main.models import CmsQuickOrderCategory


class QuickOrderCategory():
    @classmethod
    def create_or_get(cls, quick_id, category_id, create_uid):
        try:
            obj = CmsQuickOrderCategory.objects.filter(Q(quick_order_id=quick_id) & Q(category_id=category_id)).get()
        except ObjectDoesNotExist:
            obj = CmsQuickOrderCategory()
            obj.create_date = time.time()
            obj.create_uid = create_uid
        obj.category_id = category_id
        obj.quick_order_id = quick_id
        obj.save()
        return obj
    @classmethod
    def get_category(cls,quick_order_id):
        sql = "select c.name,c.id from cms_quick_order_category qoc inner join cms_navi_category c on c.id = qoc.category_id where qoc.quick_order_id={0}".format(quick_order_id)
        result = BaseCursor.get_all(sql)
        if len(result)==1:
            return result[0]
        else:
            return None