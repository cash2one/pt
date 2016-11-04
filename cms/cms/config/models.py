# -*- coding: utf-8 -*-
# Author:songroger
# Jul.6.2016
from __future__ import unicode_literals

from django.db import models


class TimeModel(models.Model):
    '''
    class: 包含创建和修改时间的基础类
    '''
    c_time = models.DateTimeField(
        u"创建时间", auto_now_add=True, blank=True, null=True)
    m_time = models.DateTimeField(
        u"修改时间", auto_now_add=True, blank=True, null=True)

    class Meta:
        abstract = True


class StateModel(models.Model):
    '''
    class: 是否删除的基础类
    @para is_del:是否删除，1是 0否
    '''
    is_del = models.IntegerField(u"是否删除", default=0, blank=True, null=True)

    class Meta:
        abstract = True


class CreatedModel(models.Model):
    '''
    class: 创建人和修改人的基础类
    '''
    c_user = models.CharField(u"创建人", max_length=50, blank=True, null=True)
    m_user = models.CharField(u"修改人", max_length=50, blank=True, null=True)

    class Meta:
        abstract = True


class CmsCategoryHotGoods(models.Model):
    category_id = models.BigIntegerField()
    goods_id = models.BigIntegerField()
    sort_id = models.IntegerField()

    class Meta:
        db_table = 'cms_category_hot_goods'


class CmsPackageGoods(models.Model):
    package_goods_id = models.BigIntegerField()
    goods_id = models.BigIntegerField()
    sort = models.IntegerField(default=0)

    class Meta:
        db_table = 'cms_package_goods'
