# -*- coding: utf-8 -*-
# Author:songroger
# Jun.17.2016
from __future__ import unicode_literals

from django.db import models
from datetime import datetime
from activity.settings import icon_img


class Activity(models.Model):

    name = models.CharField(u"名称", max_length=255)
    remark = models.CharField(u"描述", max_length=255, blank=True, null=True)
    start_time = models.DateTimeField(
        u"开始时间", default=datetime.now, blank=True)
    end_time = models.DateTimeField(u"结束时间", default=datetime.now, blank=True)
    type = models.IntegerField(u"类型")
    c_time = models.DateTimeField(u"创建时间", blank=True, null=True)
    m_time = models.DateTimeField(u"修改时间", blank=True, null=True)
    c_user = models.CharField(u"创建人", max_length=50, blank=True, null=True)
    m_user = models.CharField(u"修改人", max_length=50, blank=True, null=True)
    provider = models.CharField(
        u"活动提供方", max_length=100, blank=True, null=True)

    class Meta:
        db_table = 'activity'


class ActivityGiftRule(models.Model):

    gift_name = models.CharField(u"礼品名称", max_length=50, blank=True, null=True)
    is_entity = models.IntegerField(u"是否实物礼品", blank=True, null=True)
    entity_id = models.BigIntegerField(u"实物礼品id", blank=True, null=True)
    is_need_consume = models.IntegerField(u"是否消费", blank=True, null=True)
    consume_type = models.IntegerField(u"消费类型", blank=True, null=True)
    min_consume = models.IntegerField(u"消费下限", blank=True, null=True)
    max_consume = models.IntegerField(u"消费上限", blank=True, null=True)
    start_time = models.DateTimeField(u"礼品释放时间", blank=True, null=True)
    is_combine_pkg = models.IntegerField(u"是否组合礼品", blank=True, null=True)
    lottery_rule = models.CharField(
        u"组合礼品id和比率", max_length=255, blank=True, null=True)
    gift_description = models.CharField(
        u"礼品描述", max_length=255, blank=True, null=True)
    daily_amount_limit = models.IntegerField(
        u"礼品单日发放上线", blank=True, null=True)
    max_amount = models.IntegerField(u"礼品上限", blank=True, null=True)
    ratio = models.IntegerField(u"百分比", blank=True, null=True)
    activity_id = models.BigIntegerField(u"活动id", blank=True, null=True)
    extends_col = models.TextField(u"扩展json串", blank=True, null=True)

    class Meta:
        db_table = 'activity_gift_rule'


class ActivityJoinRule(models.Model):

    activity_id = models.BigIntegerField(u"规则关联的活动id")
    is_need_login = models.IntegerField(u"活动是否需要登录")
    default_times = models.IntegerField(u"默认参与次数")
    daily_times = models.IntegerField(u"单日参与次数限制")
    personal_times = models.IntegerField(u"单人参数次数限制")
    total_num = models.IntegerField(u"活动参与总名额限制")
    is_need_consume = models.IntegerField(u"是否需要消费")
    consume_type = models.IntegerField(u"消费的产品的类型")
    min_consume = models.IntegerField(u"最低消费额")
    gifts = models.CharField(u"礼品串", max_length=255, blank=True, null=True)
    extends_col = models.TextField(u"预留扩展json串", blank=True, null=True)

    class Meta:
        db_table = 'activity_join_rule'


class ActivityLotteryRecord(models.Model):

    activity_id = models.BigIntegerField(u"活动id")
    resource_id = models.BigIntegerField(u"资源id")
    resource_type = models.IntegerField(u"获得的资源类型")
    c_time = models.DateTimeField(u"获取时间", blank=True, null=True)
    uid = models.CharField(u"中奖的用户", max_length=50)
    mobile = models.CharField(u"手机号", max_length=11, blank=True, null=True)
    remark = models.CharField(u"中奖描述", max_length=100)

    class Meta:
        db_table = 'activity_lottery_record'


class CouponAllot(models.Model):
    """
    status:使用状态 1已使用，0 未使用
    is_del:是否删除，1是 0否
    """
    cid = models.BigIntegerField(u"券id")
    uid = models.CharField(u"用户id", max_length=50)
    allot_time = models.DateTimeField(u"领取时间", auto_now_add=True)
    status = models.IntegerField(u"使用状态", default=0)
    consume_time = models.DateTimeField(u"使用时间", blank=True, null=True)
    m_time = models.DateTimeField(
        u"修改时间", auto_now_add=True, blank=True, null=True)
    activity_id = models.BigIntegerField(u"活动id", blank=True, null=True)
    exchange_code_id = models.BigIntegerField(u"兑换码id", blank=True, null=True)
    name = models.CharField(u"券展示名称", max_length=50, blank=True, null=True)
    reason = models.CharField(u"发券理由", max_length=255, blank=True, null=True)
    start_time = models.DateTimeField(
        u"有效开始时间", blank=True, null=True)
    end_time = models.DateTimeField(u"有效结束时间", blank=True, null=True)
    is_del = models.IntegerField(u"是否删除", default=0, blank=True, null=True)
    c_user = models.CharField(u"创建人", max_length=50, blank=True, null=True)
    channel = models.CharField(u"领券渠道", max_length=50, blank=True, null=True)
    mobile = models.CharField(u"用户电话", max_length=11, blank=True, null=True)

    class Meta:
        db_table = 'coupon_allot'


class CouponCodeMain(models.Model):
    """
    is_muti:是否多码 1是，0 否
    """
    cids = models.TextField(u"可兑换券ids")
    amount = models.IntegerField(u"数量")
    is_muti = models.IntegerField(u"是否使用相同兑换码", blank=True, null=True)
    start_time = models.DateTimeField(
        u"兑换有效期开始时间", auto_now_add=True, blank=True, null=True)
    end_time = models.DateTimeField(u"兑换有效期结束时间", blank=True, null=True)
    c_time = models.DateTimeField(
        u"创建时间", auto_now_add=True, blank=True, null=True)
    m_time = models.DateTimeField(
        u"修改时间", auto_now=True, blank=True, null=True)
    c_user = models.CharField(u"创建人", max_length=50, blank=True, null=True)
    m_user = models.CharField(u"修改人", max_length=50, blank=True, null=True)
    user_max_count = models.IntegerField(
        u"单个用户兑换次数上限", default=0, blank=True, null=True)

    class Meta:
        db_table = 'coupon_code_main'


class CouponCodeSub(models.Model):
    """
    status:是否兑换过 1是，0 否
    """

    main_id = models.BigIntegerField(u"兑换码主体id")
    exchange_code = models.CharField(u"兑换码", max_length=20)
    status = models.IntegerField(u"是否兑换过", default=0, blank=True, null=True)
    uid = models.CharField(u"兑换的用户的id", max_length=50, blank=True, null=True)
    c_time = models.DateTimeField(
        u"创建时间", auto_now_add=True, blank=True, null=True)
    m_time = models.DateTimeField(
        u"修改时间", auto_now=True, blank=True, null=True)

    class Meta:
        db_table = 'coupon_code_sub'


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
    consume_remark = models.CharField(
        u"最低消费说明", max_length=255, blank=True, null=True)
    cost_type = models.IntegerField(u"成本类型", blank=True, null=True)
    cp_cost = models.IntegerField(u"cp成本金额", blank=True, null=True)
    putao_cost = models.IntegerField(u"葡萄成本金额", blank=True, null=True)
    c_time = models.DateTimeField(
        u"创建时间", auto_now_add=True, blank=True, null=True)
    m_time = models.DateTimeField(
        u"修改时间", auto_now=True, blank=True, null=True)
    c_user = models.CharField(u"创建人", max_length=50, blank=True, null=True)
    m_user = models.CharField(u"修改人", max_length=50, blank=True, null=True)
    is_mutex = models.IntegerField(u"是否互斥", blank=True, null=True)
    scope = models.CharField(u"使用范围", max_length=50, blank=True, null=True)
    # goods_cat = models.TextField(u"支持的产品分类", blank=True, null=True)
    # goods_cat_x = models.TextField(u"不支持的产品分类", blank=True, null=True)
    # gids = models.TextField(u"支持商品的id", blank=True, null=True)
    # gids_x = models.TextField(u"不支持商品id", blank=True, null=True)
    # cps = models.TextField(u"支持的cp", blank=True, null=True)
    # cps_x = models.TextField(u"不支持的cp", blank=True, null=True)
    gids = models.TextField(u"老版优惠券商品列表", blank=True, null=True)
    click_action = models.CharField(
        u"app导航连接", max_length=255, blank=True, null=True)
    icon = models.CharField(
        u"券图标", default=icon_img, max_length=255, blank=True, null=True)
    reason = models.CharField(u"理由", max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'coupon_resource'


class EntityAllot(models.Model):

    uid = models.CharField(u"用户id", max_length=50)
    eid = models.BigIntegerField(u"实体奖品id")
    allot_time = models.DateTimeField(u"获取时间")
    status = models.IntegerField(u"状态")
    m_time = models.DateTimeField(u"修改时间", blank=True, null=True)
    activity_id = models.BigIntegerField(u"活动id", blank=True, null=True)
    c_user = models.CharField(u"创建人", max_length=50, blank=True, null=True)

    class Meta:
        db_table = 'entity_allot'


class EntityReceiverAddr(models.Model):

    en_alt_id = models.CharField(u"中奖记录id", max_length=50)
    addr = models.CharField(u"收货地址", max_length=255)
    c_time = models.DateTimeField(u"创建时间", blank=True, null=True)
    m_time = models.DateTimeField(u"修改时间", blank=True, null=True)
    mobile = models.CharField(u"收货人手机号", max_length=11, blank=True, null=True)
    receiver = models.CharField(u"收货人地址", max_length=50, blank=True, null=True)

    class Meta:
        db_table = 'entity_receiver_addr'


class EntityResource(models.Model):

    name = models.CharField(u"实物资源名称", max_length=255)
    remark = models.CharField(u"实物资源描述", max_length=255, blank=True, null=True)
    amount = models.IntegerField(u"数量")
    url = models.CharField(u"领取地址", max_length=255, blank=True, null=True)
    c_time = models.DateTimeField(u"创建时间", blank=True, null=True)
    m_time = models.DateTimeField(u"修改时间", blank=True, null=True)
    c_user = models.CharField(u"创建人", max_length=50, blank=True, null=True)
    m_user = models.CharField(u"修改人", max_length=50, blank=True, null=True)
    cost_type = models.IntegerField(u"成本类型")
    cp_cost = models.IntegerField(u"cp成本", blank=True, null=True)
    putao_cost = models.IntegerField(u"葡萄成本", blank=True, null=True)

    class Meta:
        db_table = 'entity_resource'


class CouponResourceScope(models.Model):
    """
    券使用范围
    """
    cid = models.IntegerField(u"券ID")
    goods_cat = models.TextField(u"支持的产品分类", blank=True, null=True)
    goods_cat_x = models.TextField(u"不支持的产品分类", blank=True, null=True)
    gids = models.TextField(u"支持商品的id", blank=True, null=True)
    gids_x = models.TextField(u"不支持商品id", blank=True, null=True)
    cps = models.TextField(u"支持的cp", blank=True, null=True)
    cps_x = models.TextField(u"不支持的cp", blank=True, null=True)

    class Meta:
        db_table = 'coupon_resource_scope'


class ShareActivity(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(u"活动名称", max_length=50)
    description = models.CharField(
        u"活动说明", max_length=255, blank=True, null=True)
    cids = models.TextField(u"活动发放的券的json形式")
    before_vip_charge = models.BigIntegerField(blank=True, null=True)
    after_vip_charge = models.BigIntegerField(blank=True, null=True)
    activity_rule = models.TextField(u"活动规则", blank=True, null=True)
    coupon_count = models.IntegerField(u"活动分享的单个链接参与次数上限")
    start_time = models.DateTimeField(u"活动开始时间", blank=True, null=True)
    end_time = models.DateTimeField(u"活动结束时间", blank=True, null=True)
    c_time = models.DateTimeField(u"创建时间", auto_now_add=True)
    is_use = models.SmallIntegerField(u"是否上架", blank=True, null=True)
    daily_pick_limit = models.IntegerField(
        u"单人单日参与活动次数限制", blank=True, null=True)
    link_valid_days = models.IntegerField(
        u"分享链接有效期，如果为0则与活动时间一致", blank=True, null=True)
    share_coupons = models.TextField(u"回馈给分享人的券json")
    inviter_vip_charge = models.BigIntegerField(blank=True, null=True)
    share_count = models.IntegerField(
        u"分享链接被点击多少次才给分享人发券", blank=True, null=True)
    is_share_award = models.SmallIntegerField(
        u"是否启用给分享人返券，1 是，0否", blank=True, null=True)
    share_type = models.SmallIntegerField(
        u"判断是否邀请有礼的类型,1表示邀请有礼", blank=True, null=True)
    guide_word = models.CharField(u"引导页", max_length=100)

    class Meta:
        db_table = 'share_activity'


class InviteAward(models.Model):
    id = models.AutoField(primary_key=True)
    share_activity_id = models.BigIntegerField()
    number = models.IntegerField()
    cids = models.CharField(max_length=255, blank=True, null=True)
    vip_charge = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'invite_award'


class CouponAllotRecord(models.Model):
    """
    券发放记录
    """
    cids = models.CharField(u"券ID", max_length=255)
    cnames = models.CharField(u"券名", max_length=255)
    count = models.IntegerField(u"发券数")
    ucount = models.IntegerField(u"用户数")
    reason = models.CharField(u"发券理由", max_length=255, blank=True, null=True)
    allot_time = models.DateTimeField(u"领取时间", auto_now_add=True)
    c_user = models.CharField(u"创建人", max_length=50, blank=True, null=True)

    class Meta:
        db_table = 'coupon_allot_record'
