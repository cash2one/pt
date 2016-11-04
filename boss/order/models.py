# -*- coding: utf-8 -*-
from django.db import models


class PtDaojiaOrder(models.Model):
    subject = models.CharField(max_length=192)
    goodsid = models.BigIntegerField(db_column='goodsId')  # Field name made lowercase.
    cpgoodsid = models.CharField(max_length=192, db_column='cpGoodsId', blank=True)  # Field name made lowercase.
    order_no = models.CharField(max_length=150)
    cporderno = models.CharField(max_length=300, db_column='cpOrderNo', blank=True)  # Field name made lowercase.
    provider = models.CharField(max_length=192, blank=True)
    providermobile = models.CharField(max_length=48, db_column='providerMobile',
                                      blank=True)  # Field name made lowercase.
    payway = models.IntegerField(db_column='payWay')  # Field name made lowercase.
    service_time = models.DateTimeField()
    service_length = models.IntegerField()
    city = models.CharField(max_length=96)
    service_address = models.CharField(max_length=768)
    longtitude = models.FloatField()
    latitude = models.FloatField()
    staffid = models.CharField(max_length=300, db_column='staffId', blank=True)  # Field name made lowercase.
    staffname = models.CharField(max_length=96, db_column='staffName', blank=True)  # Field name made lowercase.
    staffphone = models.CharField(max_length=48, db_column='staffPhone', blank=True)  # Field name made lowercase.
    staffheadurl = models.CharField(max_length=1536, db_column='staffHeadUrl', blank=True)  # Field name made lowercase.
    consumer = models.CharField(max_length=96)
    consumermobile = models.CharField(max_length=48, db_column='consumerMobile')  # Field name made lowercase.
    pt_username = models.CharField(max_length=48, db_column='pt_username')  # Field name made lowercase.
    quantity = models.IntegerField()
    price = models.IntegerField()
    comment = models.CharField(max_length=3072, blank=True)
    pay_price = models.BigIntegerField()
    create_time = models.CharField(max_length=48)
    modify_time = models.DateTimeField()
    appid = models.BigIntegerField(db_column='appId')  # Field name made lowercase.
    goodsname = models.CharField(max_length=192, db_column='goodsName')  # Field name made lowercase.
    status = models.IntegerField(null=True, blank=True)
    cancel_by = models.IntegerField(null=True, blank=True)
    cancel_msg = models.CharField(max_length=1536, blank=True)
    amount = models.BigIntegerField(null=True, blank=True)
    simple_address = models.CharField(max_length=384, blank=True)
    service_type = models.IntegerField(null=True, blank=True)
    extrainfo = models.CharField(max_length=768, db_column='extraInfo', blank=True)  # Field name made lowercase.
    sku = models.CharField(max_length=768, blank=True)
    staff_sex = models.IntegerField(null=True, blank=True)
    promotion_activity_info = models.CharField(max_length=3072, blank=True)
    trade_no = models.CharField(max_length=150)  # payment transaction no
    vip_price = models.IntegerField()
    channel_no = models.CharField(max_length=60, db_column='channel_no')  # Field name made lowercase.
    favo_price = models.IntegerField()
    user_pay_price = models.IntegerField()
    service_time_show = models.DateTimeField()
    diff_price = models.IntegerField()
    u_id = models.CharField(max_length=1536, blank=True)


    class Meta:
        db_table = u'vw_pt_daojia_order'
        ordering = ["-modify_time"]


class PtDaojiaOrderNewUser(models.Model):
    subject = models.CharField(max_length=192)
    goodsid = models.BigIntegerField(db_column='goodsId')  # Field name made lowercase.
    cpgoodsid = models.CharField(max_length=192, db_column='cpGoodsId', blank=True)  # Field name made lowercase.
    order_no = models.CharField(max_length=150)
    cporderno = models.CharField(max_length=300, db_column='cpOrderNo', blank=True)  # Field name made lowercase.
    provider = models.CharField(max_length=192, blank=True)
    providermobile = models.CharField(max_length=48, db_column='providerMobile',
                                      blank=True)  # Field name made lowercase.
    payway = models.IntegerField(db_column='payWay')  # Field name made lowercase.
    service_time = models.DateTimeField()
    service_length = models.IntegerField()
    city = models.CharField(max_length=96)
    service_address = models.CharField(max_length=768)
    longtitude = models.FloatField()
    latitude = models.FloatField()
    staffid = models.CharField(max_length=300, db_column='staffId', blank=True)  # Field name made lowercase.
    staffname = models.CharField(max_length=96, db_column='staffName', blank=True)  # Field name made lowercase.
    staffphone = models.CharField(max_length=48, db_column='staffPhone', blank=True)  # Field name made lowercase.
    staffheadurl = models.CharField(max_length=1536, db_column='staffHeadUrl', blank=True)  # Field name made lowercase.
    consumer = models.CharField(max_length=96)
    consumermobile = models.CharField(max_length=48, db_column='consumerMobile')  # Field name made lowercase.
    pt_username = models.CharField(max_length=48, db_column='pt_username')  # Field name made lowercase.
    quantity = models.IntegerField()
    price = models.IntegerField()
    comment = models.CharField(max_length=3072, blank=True)
    pay_price = models.BigIntegerField()
    create_time = models.CharField(max_length=48)
    modify_time = models.DateTimeField()
    appid = models.BigIntegerField(db_column='appId')  # Field name made lowercase.
    goodsname = models.CharField(max_length=192, db_column='goodsName')  # Field name made lowercase.
    status = models.IntegerField(null=True, blank=True)
    cancel_by = models.IntegerField(null=True, blank=True)
    cancel_msg = models.CharField(max_length=1536, blank=True)
    amount = models.BigIntegerField(null=True, blank=True)
    simple_address = models.CharField(max_length=384, blank=True)
    service_type = models.IntegerField(null=True, blank=True)
    extrainfo = models.CharField(max_length=768, db_column='extraInfo', blank=True)  # Field name made lowercase.
    sku = models.CharField(max_length=768, blank=True)
    staff_sex = models.IntegerField(null=True, blank=True)
    promotion_activity_info = models.CharField(max_length=3072, blank=True)
    vip_price = models.IntegerField()
    channel_no = models.CharField(max_length=60, db_column='channel_no')  # Field name made lowercase.
    is_first_order = models.CharField(max_length=60, db_column='is_first_order')  # Field name made lowercase.
    order_source = models.CharField(max_length=60, db_column='order_source')  # Field name made lowercase.
    ditui_responser = models.CharField(max_length=60, db_column='ditui_responser')  # Field name made lowercase.
    ditui_action_time = models.CharField(max_length=60, db_column='ditui_action_time')  # Field name made lowercase.
    ditui_area = models.CharField(max_length=60, db_column='ditui_area')  # Field name made lowercase.
    activity_channel = models.CharField(max_length=60, db_column='activity_channel')  # Field name made lowercase.
    user_pay_price = models.IntegerField(db_column='user_pay_price')
    prod_price = models.IntegerField(db_column='prod_price')
    coupon_real_cost = models.IntegerField(db_column='coupon_real_cost')
    promotion_favo_price = models.IntegerField(db_column='promotion_favo_price')
    pt_cost = models.IntegerField(db_column='pt_cost')
    cp_cost = models.IntegerField(db_column='cp_cost')


    class Meta:
        db_table = u'vw_tongji_daojia_order_detail'
        ordering = ["-modify_time"]


class PtDaojiaOrderGuarantee(models.Model):
    order_no = models.CharField(max_length=150)
    g_type = models.IntegerField()
    status = models.IntegerField()
    g_status = models.IntegerField()
    order_create_time = models.CharField(max_length=48)
    order_modify_time = models.DateTimeField()
    order_service_time = models.DateTimeField()
    check_status = models.IntegerField()
    pt_comment = models.CharField(max_length=3072, blank=True)
    c_time = models.DateTimeField()
    m_time = models.DateTimeField()

    class Meta:
        db_table = u'pt_daojia_order_guarantee'
        ordering = ["-order_create_time"]


class PtVoucherResource(models.Model):
    id = models.BigIntegerField(primary_key=True)
    voucher_code = models.CharField(max_length=50, null=True)
    voucher_face_value = models.CharField(max_length=50, null=True)
    status = models.IntegerField()

    class Meta:
        db_table = u'phone_voucher_resource'


class VmPtVipOrder(models.Model):
    id = models.BigIntegerField(primary_key=True)
    order_no = models.CharField(max_length=50)
    goods_name = models.CharField(max_length=100)
    user_mobile = models.CharField(max_length=1000)
    cost_price = models.DecimalField(max_digits=14, decimal_places=4)
    pay_price = models.DecimalField(max_digits=23, decimal_places=4)
    order_status = models.CharField(max_length=4)
    app_id = models.CharField(max_length=20)
    app_version = models.CharField(max_length=16)
    channel_no = models.CharField(max_length=60)
    pt_u_id = models.CharField(max_length=50)
    c_time = models.CharField(max_length=48)
    favo_price = models.DecimalField(max_digits=24, decimal_places=4)

    class Meta:
        db_table = u'vw_pt_vip_order'


class CouponAllot(models.Model):
    id = models.AutoField(primary_key=True)
    cid = models.BigIntegerField(u"券id", blank=True, null=True)
    mobile = models.CharField(u"用户电话", max_length=11)
    uid = models.CharField(u"用户id", max_length=50, blank=True, null=True)
    allot_time = models.CharField(u"领取时间", blank=True, null=True, max_length=50)
    status = models.SmallIntegerField(u"0未使用，1使用", blank=True, null=True)
    consume_time = models.CharField(u"使用时间", blank=True, null=True, max_length=50)
    m_time = models.CharField(u"修改时间", blank=True, null=True, max_length=50)
    activity_id = models.BigIntegerField(u"活动id,如果是活动获得券，记录活动的id", blank=True, null=True)
    exchange_code_id = models.BigIntegerField(u"通过此兑换码获取的优惠券，如果不是兑换码得到的券，此处为空", blank=True, null=True)
    name = models.CharField(u"券展示名称", max_length=100, blank=True, null=True)
    reason = models.CharField(u"发券理由", max_length=100, blank=True, null=True)
    start_time = models.CharField(u"用户领取的这张券的有效开始时间", blank=True, null=True, max_length=50)
    end_time = models.CharField(u"用户领取的这张券的有效结束时间", blank=True, null=True, max_length=50)
    is_del = models.SmallIntegerField(u"是否删除，1是 0否", blank=True, null=True)
    c_user = models.CharField(u"创建人", max_length=100, blank=True, null=True)
    channel = models.CharField(u"领券渠道", max_length=100, blank=True, null=True)
    activity_type = models.SmallIntegerField(u"活动主体类型，现在 1-->activity,2-->sahre-activity", blank=True, null=True)
    activity_name = models.CharField(u"活动名称", max_length=100)

    class Meta:
        db_table = 'coupon_allot'


class CouponResource(models.Model):
    """
    is_mutex:0不互斥，1互斥
    cost_type:1 cp成本，2 葡萄成本，3 合作
    effect_type:0 是固定开始和结束时间，1 是从领券时间算起固定时间长度
    biz_type: 券类型，0 金额，1 流量，2 折扣
    """
    name = models.CharField(u"名称", max_length=255, blank=True, null=True)
    remark = models.CharField(u"描述", max_length=255, blank=True, null=True)
    amount = models.IntegerField(u"券面数值", blank=True, null=True)
    biz_type = models.IntegerField(u"券类型", blank=True, null=True)
    effect_type = models.IntegerField(u"生效类型", blank=True, null=True)
    start_time = models.DateTimeField(u"开始有效时间", blank=True, null=True)
    end_time = models.DateTimeField(u"结束有效时间", blank=True, null=True)
    effect_days = models.IntegerField(u"有效天数", blank=True, null=True)
    min_consume = models.IntegerField(u"最低消费", blank=True, null=True)
    consume_remark = models.CharField(u"最低消费说明", max_length=255, blank=True, null=True)
    cost_type = models.IntegerField(u"成本类型", blank=True, null=True)
    cp_cost = models.IntegerField(u"cp成本金额", blank=True, null=True)
    putao_cost = models.IntegerField(u"葡萄成本金额", blank=True, null=True)
    c_time = models.DateTimeField(u"创建时间", auto_now_add=True, blank=True, null=True)
    m_time = models.DateTimeField(u"修改时间", auto_now=True, blank=True, null=True)
    c_user = models.CharField(u"创建人", max_length=50, blank=True, null=True)
    m_user = models.CharField(u"修改人", max_length=50, blank=True, null=True)
    is_mutex = models.IntegerField(u"是否互斥", blank=True, null=True)
    scope = models.CharField(u"使用范围", max_length=50, blank=True, null=True)
    gids = models.TextField(u"老版优惠券商品列表", blank=True, null=True)
    click_action = models.CharField(u"app导航连接", max_length=255, blank=True, null=True)
    icon = models.CharField(u"券图标", max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'coupon_resource'


class PtPayOrder(models.Model):
    name = models.CharField(u"名称", max_length=255, blank=True, null=True)
    coupon_ids = models.CharField(u"id", max_length=100, blank=True, null=True)
    channel_no = models.CharField(u"渠道", max_length=100, blank=True, null=True)
    app_version = models.CharField(u"创单的版本", max_length=100, blank=True, null=True)
    class Meta:
        db_table = 'pt_pay_order'

