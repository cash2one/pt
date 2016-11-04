# -*- coding: utf-8 -*-
# Author:songroger
# Jul.28.2016
from __future__ import unicode_literals

from django.db import models
from config.models import TimeModel, StateModel


class Groups(models.Model):

    tag_group_name = models.CharField(u"名称", max_length=100)
    remark = models.CharField(u"描述", max_length=255, blank=True, null=True)

    def __str__(self):
        return self.tag_group_name

    class Meta:
        db_table = 'cms_tag_group'


class Tags(models.Model):

    name = models.CharField(u"名称", max_length=255, unique=True)
    remark = models.CharField(u"备注", max_length=255, blank=True, null=True)
    logo = models.URLField(u"标签图", blank=True, null=True)
    description = models.CharField(
        u"描述", max_length=255, blank=True, null=True)
    # groups = models.ManyToManyField(Groups)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'cms_tag'


class TagGoods(models.Model):
    """
    sku_id:若商品没有SKU，则该SKU_ID为0
    """

    goods_id = models.BigIntegerField(u"商品id")
    sku_id = models.BigIntegerField(u"规格id")
    sort = models.BigIntegerField(u"排序", default=0)
    tag_id = models.IntegerField(u"标签id")

    class Meta:
        db_table = 'cms_goods_sku_tag'


class TagGroup(models.Model):
    """
    标签-标签组
    """

    tag_group_id = models.BigIntegerField(u"标签组id")
    tag_id = models.BigIntegerField(u"标签id")
    sort = models.BigIntegerField(u"排序", default=0)

    class Meta:
        managed = False
        db_table = 'cms_tag_group_tag'
        unique_together = ("tag_group_id", "tag_id")


class TagBooking(models.Model):
    """
    快捷入口-标签组
    """

    quick_order_id = models.BigIntegerField(u"快捷入口id")
    tag_group_id = models.BigIntegerField(u"标签组id")
    level = models.BigIntegerField(u"排序", default=0)

    class Meta:
        managed = False
        db_table = 'cms_quick_order_taggroup'
        unique_together = ("quick_order_id", "tag_group_id")
