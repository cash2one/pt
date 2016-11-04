# coding: utf-8

from django.db import models

# Create your models here.


class CmsImageInfo(models.Model):
    image_name = models.CharField(verbose_name="图片名称", unique=True, max_length=200)
    image_category = models.CharField(verbose_name="图片分类", max_length=200)
    image_sec_category = models.CharField(verbose_name="图片二级分类", max_length=200)
    image_url = models.CharField(verbose_name="图片URL", max_length=200)
    mark = models.CharField(verbose_name="备注", max_length=500)
    deal_time = models.DateTimeField(verbose_name="上传时间", blank=True, null=True,auto_now=True)


    def get_check_title(self):
        return "image_name"

    class Meta:
        db_table = 'cms_image_info'
        ordering = ['-deal_time']  # 按上传时间逆序

class PtCard(models.Model):
    # 葡萄卡
    id = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name="卡名称", max_length=20)
    remark = models.CharField(verbose_name="备注", max_length=200,blank=True,null=True)
    click_action = models.CharField(verbose_name="跳转", max_length=2506,blank=True,null=True)
    icon = models.URLField(verbose_name="图片URL")
    icon_inactive = models.URLField(verbose_name="底图url")
    retail_price = models.BigIntegerField(verbose_name="零售价")
    usable_times = models.BigIntegerField(verbose_name="可用次数")
    service_length = models.BigIntegerField(verbose_name="服务时长,单位:分钟")
    cancel_minutes = models.IntegerField(verbose_name="子订单次数取消时间限制(单位：分钟)",blank=True,null=True)
    instruction = models.CharField(verbose_name="使用说明)", max_length=3000)
    expire_dates = models.BigIntegerField(verbose_name="自购买后X天内有效，单位为天)")
    is_app_sale = models.SmallIntegerField(verbose_name="该葡萄卡在APP内是否可售,0:不可售 1:可售")
    c_time = models.DateTimeField(verbose_name="上传时间", auto_now_add=True)
    m_time = models.DateTimeField(verbose_name="修改时间", auto_now=True)

    class Meta:
        db_table = 'pt_card'
        ordering = ['-m_time']  # 按上传时间逆序

class PtCardScope(models.Model):
    #　葡萄卡范围
    id = models.AutoField(primary_key=True)
    card_id = models.BigIntegerField(verbose_name="卡id")
    positive_second_category_id = models.CharField(verbose_name="正选二级分类id,多个用逗号分隔)", max_length=2000)
    reverse_second_category_id = models.CharField(verbose_name="反选二级分类id,多个用逗号分隔)",blank=True,null=True, max_length=2000)
    positive_category_id = models.CharField(verbose_name="正选三级分类id,多个用逗号分隔)", max_length=2000)
    reverse_category_id = models.CharField(verbose_name="反选三级分类id,多个用逗号分隔)",blank=True,null=True, max_length=2000)
    positive_cpid = models.CharField(verbose_name="正选cpid,多个用逗号分隔)",blank=True,null=True, max_length=2000)
    reverse_cpid = models.CharField(verbose_name="反选cpid,多个用逗号分隔)",blank=True,null=True, max_length=2000)
    positive_gid = models.CharField(verbose_name="正选商品id,多个用逗号分隔)",blank=True,null=True, max_length=2000)
    reverse_gid = models.CharField(verbose_name="反选商品id,多个用逗号分隔)", max_length=2000)
    positive_skuid = models.CharField(verbose_name="正选规格id,多个用逗号分隔)", max_length=2000)
    reverse_skuid = models.CharField(verbose_name="反选规格id,多个用逗号分隔)", max_length=2000)
    c_time = models.DateTimeField(verbose_name="上传时间", auto_now_add=True)
    m_time = models.DateTimeField(verbose_name="修改时间", auto_now=True)

    class Meta:
        db_table = 'pt_card_scope'


class PtEntityCard(models.Model):
    # 实体卡
    id = models.AutoField(primary_key=True)
    card_id = models.BigIntegerField(verbose_name="葡萄卡id,连接pt_card.id")
    expire_date_begin = models.DateTimeField(verbose_name="激活期起始时间",blank=True,null=True)
    expire_date_end = models.DateTimeField(verbose_name="激活期截止时间",blank=True,null=True)
    c_time = models.DateTimeField(verbose_name="上传时间", auto_now_add=True)
    m_time = models.DateTimeField(verbose_name="修改时间", auto_now=True)

    class Meta:
        db_table = 'pt_entity_card'


class CmsNaviCategory(models.Model):
    name = models.CharField(verbose_name="分类名称", max_length=255)
    name_style = models.CharField(verbose_name="名称颜色", max_length=256)
    fatherid = models.IntegerField(verbose_name="", db_column='fatherId')  # Field name made lowercase.
    search_keyword = models.TextField(verbose_name="搜索关键词", blank=True, null=True)
    used_by_op = models.IntegerField(default=1, verbose_name="是否为开放平台使用")
    desc = models.CharField(verbose_name="描述", max_length=256, blank=True, null=True)
    desc_style = models.CharField(verbose_name="描述颜色", max_length=256)
    small_icon_url = models.CharField(verbose_name="小图标", max_length=1024, blank=True, null=True)
    icon_url = models.CharField(verbose_name="大图标", max_length=1024, blank=True, null=True)
    location = models.IntegerField(verbose_name="分类页排序")
    action_id = models.IntegerField(verbose_name="动作")
    dot_info = models.CharField(verbose_name="打点信息", max_length=2048, blank=True, null=True)
    strategy = models.IntegerField(verbose_name="", blank=True, null=True, default=0)
    valid_time = models.CharField(verbose_name="有效时间", max_length=256)
    city = models.TextField(verbose_name="城市")
    memo = models.CharField(verbose_name="备注", max_length=256, blank=True, null=True)
    scene_id = models.IntegerField(verbose_name="场景")
    parent_id = models.IntegerField(verbose_name="")
    show_style = models.IntegerField(verbose_name="展现形式")
    background = models.CharField(verbose_name="底色", max_length=256, blank=True, null=True)
    # 新增
    location2 = models.IntegerField(verbose_name="首页排序", default=0, blank=True, null=True)
    # 0是3.7以下，1是3.7以上
    type = models.IntegerField(verbose_name="分类类型", blank=True, null=True, default=0)
    # v4.3 新增分类首页描述,新增分类首页标签
    category_index_remark = models.CharField(verbose_name="分类首页描述", max_length=256, blank=True, null=True)
    category_index_icon = models.CharField(verbose_name="分类首页标签", max_length=256, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'cms_navi_category'
        ordering = ["-id"]



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


class PtCardGoods(models.Model):
    # 葡萄卡商品

    id = models.AutoField(primary_key=True)
    goods_name = models.CharField(verbose_name="商品名称", max_length=200)
    pt_cids = models.CharField(verbose_name="与葡萄卡关联的id", max_length=2000)

    class Meta:
        ordering = ["-id"]
        db_table = 'pt_card_goods'