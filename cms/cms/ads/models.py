# -*- coding: utf-8 -*-
# Author:songroger
# Aug.29.2016
from __future__ import unicode_literals

from django.db import models
from main.models import PtYellowCitylist, CmsActions
from pttools.ptformat import to_unixtime


class CoverAds(models.Model):

    name = models.CharField(u"名称", max_length=100)
    logo = models.URLField(u"广告图片")
    display_time = models.IntegerField(u"显示时间", default=2)
    action = models.ForeignKey(CmsActions, null=True, blank=True)
    start_time = models.DateTimeField(u"开始日期")
    end_time = models.DateTimeField(u"结束日期")

    def __str__(self):
        return self.name

    def tutime(self):
        return to_unixtime(self.start_time), to_unixtime(self.end_time)

    @property
    def action_string(self):
        data = None
        if self.action:
            data = dict(key=self.action.dest_activity,
                        params=dict(click_link=self.action.dest_url,
                                    show_title=self.action.dest_title,
                                    cp_info=self.action.cp_info,
                                    expend_params=self.action.action_params,
                                    action_id=self.action.id)
                        )
        return data

    class Meta:
        db_table = 'cms_cover_ads'


class ChannelCoverAds(models.Model):

    channel_id = models.IntegerField(u"渠道ID")
    ads = models.ForeignKey(CoverAds)
    city = models.ForeignKey(PtYellowCitylist)

    def save(self, *args, **kwargs):
        super(ChannelCoverAds, self).save(*args, **kwargs)

    def delete(self):
        super(ChannelCoverAds, self).delete()

    class Meta:
        db_table = 'cms_channel_cover_ads'
