#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author sunq
from django.core.exceptions import ObjectDoesNotExist

from common.views import make_timestamp
from main.models import CmsAdbeans


class Adbeans():
    @classmethod
    def create_or_update(cls, id, img_url, start, end, location, action_id, city, name):
        open_type = 0
        id = int(id)
        if id > 0:
            try:
                obj = CmsAdbeans.objects.filter(id=id).get()
            except ObjectDoesNotExist:
                obj = CmsAdbeans()
            obj.img_url = img_url
            obj.start = make_timestamp(start)
            obj.end = make_timestamp(end)
            obj.location = location
            obj.city = city
            obj.action_id = action_id
            obj.name = name
            obj.open_type = open_type
            obj.save()
        else:
            obj = CmsAdbeans()
            obj.img_url = img_url
            obj.start = make_timestamp(start)
            obj.end = make_timestamp(end)
            obj.location = location
            obj.action_id = action_id
            obj.city = city
            obj.name = name
            obj.open_type = open_type
            obj.save()

        return obj

    @classmethod
    def create_schedule(cls, banners):
        result = []
        for (index, item) in enumerate(banners):
            obj = cls.create_or_update(item['adbean_id'], item['image'], item['start'], item['end'],
                                       len(banners) - index, item['action_id'], item['active_city'],
                                       item['adbean_name'])
            result.append(obj)
        return result
