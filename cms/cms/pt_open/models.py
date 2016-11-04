# -*- coding: utf-8 -*-
# Author:songroger
# Jun.27.2016
from __future__ import unicode_literals

from django.db import models


class PAppInfo(models.Model):
    pid = models.BigIntegerField(primary_key=True)
    cpid = models.BigIntegerField()
    name = models.CharField(max_length=64)
    icon96 = models.CharField(max_length=255, blank=True, null=True)
    icon144 = models.CharField(max_length=255, blank=True, null=True)
    topic_image = models.CharField(max_length=255)
    entry_url = models.CharField(max_length=512, blank=True, null=True)
    service_phone = models.CharField(max_length=16)
    desc = models.CharField(max_length=512, blank=True, null=True)
    type_id = models.IntegerField(blank=True, null=True)
    appkey = models.CharField(max_length=64, blank=True, null=True)
    appsecret = models.CharField(max_length=64, blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    visible = models.IntegerField(blank=True, null=True)
    introduction = models.CharField(max_length=512, blank=True, null=True)
    security_domains = models.CharField(max_length=512, blank=True, null=True)
    account_server_ip = models.CharField(max_length=512, blank=True, null=True)
    order_server_ip = models.CharField(max_length=512, blank=True, null=True)
    c_time = models.DateTimeField(blank=True, null=True)
    testing_mobile = models.CharField(max_length=256, blank=True, null=True)
    second_category_id = models.IntegerField(blank=True, null=True)
    join_up_type = models.CharField(max_length=16, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'p_app_info'


class PCoupon(models.Model):
    pid = models.BigIntegerField(primary_key=True)
    parent_id = models.BigIntegerField(blank=True, null=True)
    app_id = models.BigIntegerField()
    gids = models.TextField(blank=True, null=True)
    name = models.CharField(max_length=64)
    desc = models.CharField(max_length=255, blank=True, null=True)
    instruction = models.CharField(max_length=2000)
    money = models.FloatField()
    amount = models.IntegerField()
    allot_amount = models.IntegerField()
    consume_amount = models.IntegerField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    notify_url = models.CharField(max_length=255)
    logo_url = models.CharField(max_length=255, blank=True, null=True)
    link_url = models.CharField(max_length=255, blank=True, null=True)
    link_title = models.CharField(max_length=64, blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    visible = models.IntegerField(blank=True, null=True)
    c_time = models.DateTimeField()
    m_time = models.DateTimeField(blank=True, null=True)
    coupon_type = models.IntegerField(blank=True, null=True)
    flag = models.IntegerField(blank=True, null=True)
    scope = models.CharField(max_length=64, blank=True, null=True)
    min_money = models.FloatField(blank=True, null=True)
    biz = models.IntegerField(blank=True, null=True)
    consume_remark = models.CharField(max_length=255, blank=True, null=True)
    all_gids = models.CharField(max_length=2000, blank=True, null=True)
    is_mutex = models.IntegerField()
    is_cp_cost = models.IntegerField()
    cp_cost = models.FloatField()
    pt_cost = models.FloatField()
    reason = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'p_coupon'


class PGoodsCity(models.Model):
    id = models.BigIntegerField(primary_key=True)
    gid = models.BigIntegerField(blank=True, null=True)
    city = models.CharField(max_length=64)

    class Meta:
        managed = False
        db_table = 'p_goods_city'


class PGoodsInfo(models.Model):
    pid = models.BigIntegerField(primary_key=True)
    appid = models.BigIntegerField()
    source_id = models.CharField(max_length=64)
    name = models.CharField(max_length=64)
    icon = models.CharField(max_length=64, blank=True, null=True)
    thumbnail = models.CharField(max_length=64, blank=True, null=True)
    desc = models.CharField(max_length=256, blank=True, null=True)
    price = models.FloatField(blank=True, null=True)
    fav_price = models.FloatField(blank=True, null=True)
    price_unit = models.CharField(max_length=8, blank=True, null=True)
    num = models.IntegerField(blank=True, null=True)
    c_time = models.DateField()
    start_time = models.DateField(blank=True, null=True)
    end_time = models.DateField(blank=True, null=True)
    trade_url = models.CharField(max_length=512, blank=True, null=True)
    type_id = models.IntegerField(blank=True, null=True)
    detail_images = models.CharField(max_length=256, blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    visible = models.IntegerField(blank=True, null=True)
    big_icon = models.CharField(max_length=512, blank=True, null=True)
    charge_desc = models.CharField(max_length=1024, blank=True, null=True)
    function_desc = models.CharField(max_length=1024, blank=True, null=True)
    service_duration = models.IntegerField(blank=True, null=True)
    service_unit = models.CharField(max_length=8, blank=True, null=True)
    service_type = models.IntegerField(blank=True, null=True)
    pay_way = models.IntegerField(blank=True, null=True)
    is_support_choose_amount = models.IntegerField(blank=True, null=True)
    is_limit_purchase_amount = models.IntegerField(blank=True, null=True)
    minimum_purchase_amount = models.IntegerField(blank=True, null=True)
    maximum_purchase_amount = models.IntegerField(blank=True, null=True)
    is_need_user_address = models.IntegerField(blank=True, null=True)
    is_need_user_time = models.IntegerField(blank=True, null=True)
    is_need_user_extra_remark = models.IntegerField(blank=True, null=True)
    user_extra_remark = models.CharField(max_length=256, blank=True, null=True)
    cp_order_create_url = models.CharField(
        max_length=512, blank=True, null=True)
    cp_order_modify_url = models.CharField(
        max_length=512, blank=True, null=True)
    cp_order_paied_url = models.CharField(
        max_length=512, blank=True, null=True)
    cp_service_staff_url = models.CharField(
        max_length=512, blank=True, null=True)
    cp_book_service_staff_url = models.CharField(
        max_length=512, blank=True, null=True)
    cp_service_time_url = models.CharField(
        max_length=512, blank=True, null=True)
    second_category_id = models.IntegerField(blank=True, null=True)
    topic = models.CharField(max_length=64, blank=True, null=True)
    has_sku = models.IntegerField(blank=True, null=True)
    remind_msg = models.CharField(max_length=64, blank=True, null=True)
    remind_position = models.CharField(max_length=8, blank=True, null=True)
    support_info = models.CharField(max_length=8, blank=True, null=True)
    remind_time = models.CharField(max_length=16, blank=True, null=True)
    additional_charge = models.IntegerField(blank=True, null=True)
    is_need_service_staff = models.IntegerField(blank=True, null=True)
    gorder = models.IntegerField(blank=True, null=True)
    is_post_paid = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'p_goods_info'


class Sku(models.Model):
    """
    商户开放平台同步过来的sku表
    price：原价，单位为分
    fav_price: 售价，分为单位
    is_order_h5:是否H5下单: 1为h5,0为正常本地实现下单
    """
    sku_id = models.BigIntegerField(u"规格id")
    goods_id = models.BigIntegerField(u"商品id")
    source_id = models.CharField(u"CP映射ID", max_length=255)
    sku_name = models.CharField(u"SKU名字", max_length=255)
    price = models.DecimalField(
        u"原价", max_digits=10, decimal_places=2, default='0.00')
    fav_price = models.DecimalField(
        u"售价", max_digits=10, decimal_places=2, default='0.00')
    price_unit = models.CharField(
        u"价格单位", max_length=255, blank=True, null=True)
    is_order_h5 = models.IntegerField(u"是否H5下单")
    order_h5 = models.CharField(
        u"下单H5URL", max_length=255, blank=True, null=True)
    service_length = models.IntegerField(u"服务时长", blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cms_sku'
