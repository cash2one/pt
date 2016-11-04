# -*- coding: utf-8 -*-
# Author:songroger
# Aug.13.2016
from __future__ import unicode_literals
from django.db import models


class Tabs(models.Model):
    """
    底部菜单栏
    """
    un_check_name = models.CharField(u"uTab名称", max_length=20)
    check_name = models.CharField(u"Tab名称", max_length=20)
    un_check_style = models.CharField(u"u颜色", max_length=20)
    check_style = models.CharField(u"颜色", max_length=20)
    un_check_icon = models.CharField(u"u图标", max_length=100)
    check_icon = models.CharField(u"图标", max_length=100)
    action_id = models.BigIntegerField(u"动作id")
    dot_key = models.CharField(u"打点key", max_length=50)
    sort = models.IntegerField(u"排序", default=0)
    # is_big_icon = models.IntegerField(
    #     u"是否大图片", blank=True, null=True, default=0)

    def __str__(self):
        return self.check_name

    class Meta:
        managed = False
        db_table = 'cms_tab_config'


class TabChannel(models.Model):
    """
    菜单-渠道
    """

    channel_id = models.BigIntegerField(u"渠道id")
    tc = models.ForeignKey(Tabs, db_column='tc_id')

    class Meta:
        managed = False
        db_table = 'cms_view_tab_config'
        # unique_together = ("channel_id", "tc_id")
