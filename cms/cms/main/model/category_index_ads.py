#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author sunq
import time

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q

from common.views import timestamp2str
from main.models import CmsCategoryIndexAds
from common.base_cursor import BaseCursor


class CategoryIndexAds():
    @classmethod
    def create_or_update(cls, category_index_id, adbean_id, create_uid, sort):
        try:
            obj = CmsCategoryIndexAds.objects.filter(Q(category_index_id=category_index_id) & Q(adbean_id=adbean_id)).get()
            obj.sort = sort
            obj.save()
        except ObjectDoesNotExist:

            obj = CmsCategoryIndexAds()
            obj.category_index_id = category_index_id
            obj.adbean_id = adbean_id
            obj.sort = sort
            obj.create_uid = create_uid
            obj.create_date = time.time()
            obj.save()
        return obj

    @classmethod
    def create_schedule(cls, category_index_id, adbean_ids, create_uid):
        exist_id = cls.get_ads_id(category_index_id)
        result = []
        for (index, i) in enumerate(adbean_ids):
            obj = cls.create_or_update(category_index_id, i, create_uid, len(adbean_ids) - index)
            result.append(obj)
        new_id = set()
        for i in result:
            new_id.add(i.id)
        deleting_ids = exist_id - new_id
        cls.delete(deleting_ids)
        return result

    @classmethod
    def delete(cls, deleting_ids):
        for i in deleting_ids:
            CmsCategoryIndexAds.objects.filter(id=i).delete()

    @classmethod
    def get_ads_id(cls, category_index_id):
        sql = "SELECT id FROM cms_category_index_ads where category_index_id={0}".format(category_index_id)
        ids = BaseCursor.get_all(sql)
        result = set()
        for i in ids:
            result.add(i[0])
        return result

    @classmethod
    def get_ads(cls, category_index_id):
        sql = "SELECT ad.id AS adbean_id, ad.name AS adbean_name, ad.img_url AS image, ad.start, ad.end, ad.action_id, ifnull(ac.memo,'') AS action_name, ad.city FROM cms_adbeans ad LEFT JOIN cms_actions ac ON ac.id = ad.action_id INNER JOIN cms_category_index_ads cad ON cad.adbean_id = ad.id WHERE cad.category_index_id = {0} ORDER BY cad.sort DESC ".format(
            category_index_id)
        result = BaseCursor.get_all(sql=sql)

        def _format(item):
            item[3] = timestamp2str(item[3])
            item[4] = timestamp2str(item[4])
            if item[6]:
                item[6] = "%d(%s)" % (item[5], item[6])
            else:
                item[6] = "%d" % (item[5])
            return item

        result = list(map(_format, result))
        return result
