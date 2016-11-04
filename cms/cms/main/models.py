# coding: utf-8
from __future__ import unicode_literals
import time
from django.db import models
from django.db.models import QuerySet
from django.db.models.sql import Query
from django.utils import timezone

# from common.const import *
from common.const import get_nav_text, get_2array_value, open_type, ad_size, ad_type, get_show_style, OP_CONFIG, \
    streams_type, item_modules, screen_ad_times

"""
python manage.py syncdb

注意：Django 1.7.1及以上的版本需要用以下命令
python manage.py makemigrations
python manage.py migrate
"""


class CmsBaseManager(models.Manager):
    pass


class CmsBaseModel(models.Model):
    objects = CmsBaseManager()

    class Meta:
        abstract = True


class CmsScene(CmsBaseModel):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=128)

    class Meta:
        db_table = 'cms_scene'


def get_scene_name(id):
    return CmsScene.objects.get(id=id).name


def get_valid_time(str, s=" | "):
    if "* * * * *" in str:
        return "不限"
    min, hour, day, month, week = str.split(" ")
    valid_time = ""
    if month != "*":
        valid_time += "月：" + month + s
    if day != "*":
        valid_time += "日：" + day + s
    if week != "*":
        valid_time += "周：" + week + s
    if hour != "*":
        valid_time += "小时：" + hour + s
    if min != "*":
        valid_time += "分：" + min + s
    return valid_time


def get_city_str(str):
    return "不限" if "*" in str else str


def timestamp2str_space(timestamp):
    if timestamp:
        t = time.localtime(float(timestamp))
        return time.strftime('%Y-%m-%d %H:%M', t)
    else:
        return ""


# 根据渠道号ID获取渠道号channel_no：c, 版本名称app_version:v，类型id type_id:t
def getCVT(channel_id, db='default'):
    oCmsChannels = CmsChannels.objects.using(db).get(id=channel_id)
    oCmsChannels_app_version = CmsChannelsAppVersion.objects.using(db).get(cmschannels__id=channel_id)
    # oCmsChannels_app_version = CmsChannelsAppVersion.objects.get(id=oCmsChannels.app_version.id)
    return oCmsChannels.channel_no, oCmsChannels_app_version.app_version, oCmsChannels_app_version.type_id


def get_tvc_name(channel_id, db='default'):
    oCmsChannels = CmsChannels.objects.using(db).get(id=channel_id)
    oCmsChannels_app_version = CmsChannelsAppVersion.objects.using(db).get(cmschannels__id=channel_id)
    otype = CmsChannelsType.objects.get(id=oCmsChannels_app_version.type_id)
    return otype.name, oCmsChannels_app_version.app_version, oCmsChannels.channel_no


class DjangoContentType(CmsBaseModel):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class AuthPermission(CmsBaseModel):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey(DjangoContentType)  # content_type_id = models.IntegerField()
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)  # unique_together = (('content_type_id', 'codename'),)


class AuthGroup(CmsBaseModel):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(CmsBaseModel):
    group = models.ForeignKey(AuthGroup)  # group_id = models.IntegerField()
    permission = models.ForeignKey(AuthPermission)  # permission_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)  # unique_together = (('group_id', 'permission_id'),)


class AuthUser(CmsBaseModel):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField(default=0)
    username = models.CharField(unique=True, max_length=30)
    first_name = models.CharField(max_length=30, default="")
    last_name = models.CharField(max_length=30, default="")
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField(default=1)
    date_joined = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.id:
            self.date_joined = timezone.now()
        return super(AuthUser, self).save(*args, **kwargs)

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(CmsBaseModel):
    user = models.ForeignKey(AuthUser)  # user_id = models.IntegerField()
    group = models.ForeignKey(AuthGroup)  # group_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)  # unique_together = (('user_id', 'group_id'),)


class AuthUserUserPermissions(CmsBaseModel):
    user = models.ForeignKey(AuthUser)  # user_id = models.IntegerField()
    permission = models.ForeignKey(AuthPermission)  # permission_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)  # unique_together = (('user_id', 'permission_id'),)


class CmsChannelsType(CmsBaseModel):
    name = models.CharField(verbose_name="应用名称", max_length=256, blank=True, null=True)  # unique=True,

    class Meta:
        managed = False
        db_table = 'cms_channels_type'


class CmsChannelsAppVersion(CmsBaseModel):
    app_version = models.CharField(verbose_name="版本名称", max_length=64)
    type_id = models.IntegerField(verbose_name="应用名称")

    def type_id__text__(self):
        return get_nav_text(self.type_id)

    def get_check_title(self):
        return "app_version"

    class Meta:
        managed = False
        db_table = 'cms_channels_app_version'
        unique_together = (('app_version', 'type_id'),)
        ordering = ['-app_version']  # 按版本逆序


class CmsChannels(CmsBaseModel):
    channel_no = models.CharField(verbose_name="渠道号", max_length=256)
    order = models.IntegerField(verbose_name="是否默认")
    app_version = models.ForeignKey(CmsChannelsAppVersion)  # app_version_id = models.IntegerField()
    user_id = models.CharField(verbose_name="", max_length=256)

    def order__text__(self):
        orders = [[1, "是"], [2, "否"]]
        return get_2array_value(orders, self.order)

    def get_check_title(self):
        return "channel_no"

    class Meta:
        managed = False
        db_table = 'cms_channels'
        unique_together = (('channel_no', 'app_version'),)  # app_version_id
        ordering = ['channel_no']


class PtYellowCitylist(CmsBaseModel):
    city_name = models.CharField(max_length=30, blank=True, null=True)
    city_py = models.CharField(max_length=255, blank=True, null=True)
    id = models.SmallIntegerField(primary_key=True, name="self_id")  # blank=True, null=True,  self_id
    parent_id = models.SmallIntegerField(blank=True, null=True)
    city_type = models.IntegerField(blank=True, null=True)
    district_code = models.CharField(max_length=10, blank=True, null=True)
    city_hot = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pt_yellow_citylist'


class PtCityGroup(CmsBaseModel):
    name = models.CharField(verbose_name="城市分组名称", unique=True, max_length=80)
    remark = models.CharField(verbose_name="备注", max_length=256, blank=True, null=True)

    def get_check_title(self):
        return "name"

    class Meta:
        db_table = 'pt_city_group'
        ordering = ['-id']


class PtCityCityGroups(CmsBaseModel):
    city = models.ForeignKey(PtYellowCitylist)
    group = models.ForeignKey(PtCityGroup)

    class Meta:
        db_table = 'pt_city_city_groups'
        unique_together = (('city', 'group'),)


class CmsServices(CmsBaseModel):
    srv_id = models.IntegerField()
    name = models.CharField(verbose_name="服务名称", max_length=256)
    name_style = models.CharField(verbose_name="名称颜色", max_length=256)
    desc = models.CharField(verbose_name="描述", max_length=2048, blank=True, null=True)
    desc_style = models.CharField(verbose_name="描述颜色", max_length=256, blank=True, null=True)
    search_keyword = models.CharField(verbose_name="搜索关键词", max_length=1024)
    small_icon_url = models.CharField(verbose_name="小图标", max_length=1024)
    icon_url = models.CharField(verbose_name="大图标", max_length=1024)
    location = models.IntegerField(verbose_name="排序")
    action_id = models.IntegerField(verbose_name="动作")
    dot_info = models.CharField(verbose_name="打点信息", max_length=2048, blank=True, null=True)
    strategy = models.IntegerField(verbose_name="", blank=True, null=True, default=0)
    valid_time = models.CharField(verbose_name="有效时间", max_length=256, blank=True, null=True)
    city = models.TextField(verbose_name="城市", blank=True, null=True)
    memo = models.CharField(verbose_name="备注", max_length=256, blank=True, null=True)
    type = models.IntegerField(verbose_name="", blank=True, null=True)
    scene_id = models.IntegerField(verbose_name="场景")
    parent_id = models.IntegerField(verbose_name="")
    open_cp_id = models.IntegerField(verbose_name="")
    open_service_id = models.IntegerField(verbose_name="")
    open_goods_id = models.IntegerField(verbose_name="")
    source_id = models.CharField(verbose_name="", max_length=256, blank=True, null=True)
    action_json = models.TextField(blank=True, null=True)
    mobile = models.CharField(verbose_name="", max_length=256, blank=True, null=True)

    def city__text__(self):
        return get_city_str(self.city)

    def valid_time__text__(self):
        return get_valid_time(self.valid_time)

    def scene_id__text__(self):
        return get_scene_name(self.scene_id)

    def get_check_title(self):
        return "name"

    class Meta:
        managed = False
        db_table = 'cms_services'
        ordering = ['scene_id', 'location']


class CmsActions(CmsBaseModel):
    type = models.IntegerField(verbose_name="类型")
    dest_activity = models.CharField(max_length=256, blank=True, null=True)
    dest_url = models.CharField(max_length=256, blank=True, null=True)
    dest_title = models.CharField(verbose_name="动作标题", max_length=256, blank=True, null=True)
    cp_info = models.CharField(verbose_name="商家信息", max_length=2048, blank=True, null=True)
    action_params = models.CharField(max_length=2048, blank=True, null=True)
    memo = models.CharField(verbose_name="备注", max_length=256, blank=True, null=True)
    pt_h5 = models.IntegerField(verbose_name="是否为葡萄提供的H5页面")

    def pt_h5__text__(self):
        return "是" if self.pt_h5 and int(self.pt_h5) == 1 else "否"

    def get_check_title(self):
        return "dest_title"

    class Meta:
        managed = False
        db_table = 'cms_actions'
        ordering = ['-id']


class CmsImageInfo(CmsBaseModel):
    image_name = models.CharField(verbose_name="图片名称", unique=True, max_length=200)
    image_category = models.CharField(verbose_name="图片分类", max_length=200)
    image_sec_category = models.CharField(verbose_name="图片二级分类", max_length=200)
    image_url = models.CharField(verbose_name="图片URL", max_length=200)
    mark = models.CharField(verbose_name="备注", max_length=500)
    deal_time = models.DateTimeField(verbose_name="上传时间", blank=True, null=True)

    def save(self, *args, **kwargs):
        self.deal_time = timezone.now()
        return super(CmsImageInfo, self).save(*args, **kwargs)

    def get_check_title(self):
        return "image_name"

    class Meta:
        db_table = 'cms_image_info'
        ordering = ['-deal_time']  # 按上传时间逆序


class CmsGoods(CmsBaseModel):
    goods_id = models.IntegerField(verbose_name="商品ID")
    title = models.CharField(verbose_name="标题", max_length=256)
    title_style = models.CharField(verbose_name="标题颜色", max_length=256, default='#000000')
    name = models.CharField(verbose_name="商品名称", max_length=256)
    name_style = models.CharField(verbose_name="商品名称颜色", max_length=256, default='#000000')
    desc = models.CharField(verbose_name="描述", max_length=2048, blank=True, null=True)
    desc_style = models.CharField(verbose_name="描述颜色", max_length=256, blank=True, null=True)
    search_keyword = models.CharField(verbose_name="搜索关键词", max_length=1024, blank=True, null=True)
    small_icon_url = models.CharField(verbose_name="小图标", max_length=1024)
    icon_url = models.CharField(verbose_name="大图标", max_length=1024)
    location = models.IntegerField(verbose_name="排序", default=0)
    action_id = models.IntegerField(verbose_name="动作")
    dot_info = models.CharField(verbose_name="打点信息", max_length=2048, blank=True, null=True)
    strategy = models.IntegerField(verbose_name="", blank=True, null=True, default=0)
    valid_time = models.CharField(verbose_name="有效时间", max_length=256, blank=True, null=True, default='* * * * *')
    city = models.CharField(verbose_name="城市", max_length=256, blank=True, null=True, default="*")
    memo = models.CharField(verbose_name="备注", max_length=256, blank=True, null=True)
    scene_id = models.IntegerField(verbose_name="场景", default=0)
    parent_id = models.IntegerField(verbose_name="", default=-1)
    open_cp_id = models.IntegerField(verbose_name="")
    open_service_id = models.IntegerField(verbose_name="")
    source_id = models.CharField(verbose_name="", max_length=256, blank=True, null=True)
    action_json = models.TextField(blank=True, null=True)
    fav_price = models.DecimalField(verbose_name="商品现价", max_digits=10, decimal_places=2, blank=True, null=True,
                                    default='0.00')
    fav_price_style = models.CharField(verbose_name="商品现价颜色", max_length=256, blank=True, null=True, default='#000000')
    price = models.DecimalField(verbose_name="商品原价", max_digits=10, decimal_places=2, blank=True, null=True,
                                default='0.00')
    num = models.IntegerField(verbose_name="商品数量", blank=True, null=True, default=0)
    sold = models.IntegerField(verbose_name="已售数量", blank=True, null=True, default=-1)
    latitude = models.FloatField(verbose_name="", blank=True, null=True, default=0)
    longitude = models.FloatField(verbose_name="", blank=True, null=True, default=0)
    mobile = models.CharField(verbose_name="", max_length=2048, blank=True, null=True, editable=False)
    fav_price_desc = models.CharField(verbose_name="商品现价描述", max_length=256, blank=True, null=True)
    fav_price_desc_style = models.CharField(verbose_name="商品现价描述颜色", max_length=256)
    from_op = models.IntegerField(verbose_name="是否来自开放平台", default=0)
    category = models.IntegerField(verbose_name="分类", blank=True, null=True)
    second_category = models.IntegerField(verbose_name="二级分类", blank=True, null=True)
    new_category = models.IntegerField(verbose_name="新分类", blank=True, null=True)
    new_second_category = models.IntegerField(verbose_name="新二级分类", blank=True, null=True)
    cp_name = models.CharField(verbose_name="商家名称", max_length=64, blank=True, null=True)
    mark = models.CharField(verbose_name="运营标签", max_length=256, blank=True, null=True)
    is_support_cart = models.IntegerField(verbose_name='是否支持购物车', blank=True, null=True)
    min_version = models.CharField(verbose_name='支持最小版本', max_length=1000, blank=True)
    max_version = models.CharField(verbose_name='支持最大版本', max_length=1000, blank=True)
    # 推荐列表标签,V4.1添加 haole
    recommend_icon = models.CharField(verbose_name='列表标签', max_length=1000, blank=True)
    # 推荐理由标签,V4.2添加haole
    recommend_reason = models.CharField(verbose_name='葡萄推荐理由', max_length=1000, blank=True)
    # 商品排序
    sort = models.CharField(verbose_name='商品分类排序', max_length=100, blank=True, default=0)
    # 商品支持城市区域
    citysJson = models.TextField(verbose_name='商品支持城市区域', blank=True)
    # 商品支持的配送范围
    serviceRangeJson = models.TextField(verbose_name='商品支持的配送范围', blank=True)
    # 运营标签1
    tag1 = models.CharField(verbose_name='运营标签1', max_length=1000, blank=True)
    # 运营标签1样式
    tag1_style = models.CharField(verbose_name='运营标签1样式', max_length=256, blank=True, default="#3eaffb")
    # 运营标签2
    tag2 = models.CharField(verbose_name='运营标签2', max_length=1000, blank=True)
    # 运营标签2样式
    tag2_style = models.CharField(verbose_name='运营标签2样式', max_length=256, blank=True, default="#46c578")
    # 运营标签3
    tag3 = models.CharField(verbose_name='运营标签3', max_length=1000, blank=True)
    # 运营标签3样式
    tag3_style = models.CharField(verbose_name='运营标签3样式', max_length=256, blank=True, default="#ffa800")
    # 推荐商品
    recommend_goodsId = models.IntegerField(verbose_name='推荐商品ID', default=0)
    # 推荐商品描述
    recommend_goods_reason = models.CharField(verbose_name='推荐商品理由', max_length=1000, blank=True)

    price_unit = models.CharField(max_length=100, blank=True, null=True)
    card_type = models.IntegerField(u"商品类型", default=0)
    service_times = models.IntegerField(u"次卡服务次数", blank=True, null=True)
    card_minutes = models.IntegerField(u"小时卡分钟数", blank=True, null=True)
    serviceRangeGraph = models.TextField(verbose_name='服务范围添加封闭区域', blank=True, null=True)
    card_icon = models.CharField(u"卡片内容流图片",max_length=255, blank=True, null=True)
    sale_status = models.IntegerField(u"可销售字段", blank=True, null=True)
    is_select_count = models.IntegerField(u"是否支持选择数量", blank=True, null=True)
    min_buy_count = models.IntegerField(u"最低限购", blank=True, null=True)
    max_buy_count = models.IntegerField(u"最高限购", blank=True, null=True)
    c_time = models.BigIntegerField(u"创建时间", blank=True, null=True)

    card_support_length = models.IntegerField(verbose_name=u'套餐卡支持的服务时长', blank=True)
    # 新增葡萄新版本推荐理由1 V4.5 添加
    new_recommend_1 = models.CharField(verbose_name=u'葡萄推荐理由1',max_length=255,blank=True)
    # 新增葡萄新版本推荐理由2 V4.5 添加
    new_recommend_2 = models.CharField(verbose_name=u'葡萄推荐理由2',max_length=255,blank=True)
    # 新增葡萄新版本推荐理由3 V4.5 添加
    new_recommend_3 = models.CharField(verbose_name=u'葡萄推荐理由3',max_length=255,blank=True)
    # 新增商品服务时长字段 V4.5 添加
    service_length = models.IntegerField(u'服务时长', blank=True, null=True)



    def category__text__(self):
        if self.category:
            return CmsNaviCategory.objects.get(id=self.category).name
        else:
            return ""

    def second_category__text__(self):
        if self.category:
            return CmsNaviCategory.objects.get(id=self.second_category).name
        else:
            return ""

    def from_op__text__(self):
        return "是" if self.from_op and int(self.from_op) == 1 else "否"

    def city__text__(self):
        return get_city_str(self.city)

    def valid_time__text__(self):
        return get_valid_time(self.valid_time)

    def scene_id__text__(self):
        return get_scene_name(self.scene_id)

    def get_check_title(self):
        return "title"

    class Meta:
        managed = False
        db_table = 'cms_goods'
        ordering = ['-id']


class CmsAdbeans(CmsBaseModel):
    img_url = models.CharField(verbose_name="图片", max_length=256)
    start = models.IntegerField(verbose_name="起始时间")
    end = models.IntegerField(verbose_name="结束时间")
    location = models.IntegerField(verbose_name="排序")
    action_id = models.IntegerField(verbose_name="动作")
    strategy = models.IntegerField(verbose_name="", blank=True, null=True, default=0)
    valid_time = models.CharField(verbose_name="有效时间", max_length=256, blank=True, null=True)
    city = models.TextField(verbose_name="城市", blank=True, null=True)
    open_cp_id = models.IntegerField(verbose_name="", default=0)
    open_service_id = models.IntegerField(verbose_name="", default=0)
    open_goods_id = models.IntegerField(verbose_name="", default=0)
    open_type = models.IntegerField(verbose_name="类别")
    action_json = models.TextField(blank=True, null=True)
    name = models.CharField(verbose_name="广告名称", max_length=200)
    phone_type = models.CharField(verbose_name="机型", max_length=200, blank=True, null=True)

    def start__text__(self):
        return timestamp2str_space(self.start)

    def end__text__(self):
        return timestamp2str_space(self.end)

    def city__text__(self):
        return get_city_str(self.city)

    def valid_time__text__(self):
        return get_valid_time(self.valid_time)

    def get_check_title(self):
        return "name"

    class Meta:
        managed = False
        db_table = 'cms_adbeans'
        ordering = ['location']  # 按排序来排序

    def __str__(self):
        return self.name

    def open_type__text__(self):
        return get_2array_value(open_type, self.open_type)


class CmsAds(CmsBaseModel):
    location = models.IntegerField(verbose_name="排序")
    size = models.IntegerField(verbose_name="篇幅")
    type = models.IntegerField(verbose_name="类型")
    scene_id = models.IntegerField(verbose_name="场景")

    def size__text__(self):
        return get_2array_value(ad_size, self.size)

    def type__text__(self):
        return get_2array_value(ad_type, self.type)

    def scene_id__text__(self):
        return get_scene_name(self.scene_id)

    class Meta:
        managed = False
        db_table = 'cms_ads'
        ordering = ['scene_id', 'location']  # 先按场景再按排序来排序


class CmsAdsBeans(CmsBaseModel):
    ad = models.ForeignKey(CmsAds)  # ad_id = models.IntegerField()
    bean = models.ForeignKey(CmsAdbeans)  # bean_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'cms_ads_beans'
        unique_together = (('ad', 'bean'),)  # unique_together = (('ad_id', 'bean_id'),)


class CmsViewAd(CmsBaseModel):
    ad = models.ForeignKey(CmsAds)  # ad_id = models.IntegerField()
    channel = models.ForeignKey(CmsChannels)  # channel_id = models.IntegerField()
    status = models.IntegerField(blank=True, null=True, default=0)

    class Meta:
        managed = False
        db_table = 'cms_view_ad'
        unique_together = (('ad', 'channel'),)  # unique_together = (('ad_id', 'channel_id'),)


class CmsViewService(CmsBaseModel):
    service_id = models.IntegerField(verbose_name="服务/商品/分类名称")  # service = models.ForeignKey(CmsServices)
    open_type = models.IntegerField()
    channel = models.ForeignKey(CmsChannels)  # channel_id = models.IntegerField()
    status = models.IntegerField(blank=True, null=True, default=0)

    def service_id__text__(self):
        if self.open_type == 0:
            return CmsServices.objects.get(id=self.service_id).name
        elif self.open_type == 1:
            return CmsGoods.objects.get(id=self.service_id).title
        else:
            return CmsNaviCategory.objects.get(id=self.service_id).name

    def get_check_title(self):
        return "service_id"

    class Meta:
        managed = False
        db_table = 'cms_view_service'
        unique_together = (('service_id', 'channel'),)  # unique_together = (('service_id', 'channel_id'),)


class CmsCategoryItem(CmsBaseModel):
    """二级分类"""
    name = models.CharField(verbose_name="二级分类标题", max_length=256, blank=True, null=True)
    name_color = models.CharField(verbose_name="标题颜色", max_length=256)
    sort = models.IntegerField(verbose_name="排序")
    service = models.ForeignKey(CmsServices)  # service_id = models.IntegerField()
    category_id = models.IntegerField(verbose_name="分类id")
    scene_id = models.IntegerField(verbose_name="场景")

    def scene_id__text__(self):
        return get_scene_name(self.scene_id)

    def get_check_title(self):
        return "name"

    class Meta:
        managed = False
        db_table = 'cms_category_item'


"""
#服务入口确认
{
  "service_info":[{
  "service_name":"",//服务名称
  "service_icon":"",//服务icon
  "target_activity":"",//服务对应activity
  "url":"",//如果为H5页面则为url地址，如果不是则为空
  "from_browser": true/false,//是否通过浏览器启动
  "parameter":""//参数
  },...]
	"webSite": "www.sf-express.com?_f=putaovip",    #官方主页
	"weibo": "http://weibo.com/sfsuyun",    #微博主页
	"name": "顺丰速运", #名称
	"photoUrl": "http://resource.putao.so/lenovo/putao_a0501.png",  #待确认，跟icon字段的关系
	"search_info": [{
		"search_key": "顺丰速运",   #搜索关键词
		"search_category": "生活服务",  #搜索分类
		"search_show": "查看附近顺丰速运"   #查看附近
	}],
	"dataSource": "葡萄", #写死的
	"numbers": [{
		"number": "4008111111", #电话号码
		"number_description": "顺丰速运"    #电话描述
	}]
}
"""


class CmsCategoryItembean(CmsBaseModel):
    """商家"""
    item_id = models.CharField(verbose_name="ID", max_length=256)
    name = models.CharField(verbose_name="商家名称", max_length=256)
    icon = models.CharField(verbose_name="头像", max_length=256)
    sort = models.IntegerField(verbose_name="搜索词")
    target_activity = models.CharField(max_length=1024, blank=True, null=True)
    target_params = models.TextField(blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    remind_code = models.IntegerField()
    key_tag = models.CharField(max_length=256, blank=True, null=True)
    search_sort = models.IntegerField(verbose_name="搜索分类")
    description = models.CharField(verbose_name="描述", max_length=1024, blank=True, null=True)
    dot_info = models.TextField(verbose_name="打点信息", blank=True, null=True)
    strategy = models.IntegerField(verbose_name="", default=0)
    city = models.TextField(verbose_name="城市")
    valid_time = models.CharField(verbose_name="有效时间", max_length=256)
    parent_id = models.IntegerField(verbose_name="", blank=True, null=True, default=-1)

    def city__text__(self):
        return get_city_str(self.city)

    def valid_time__text__(self):
        return get_valid_time(self.valid_time)

    def get_check_title(self):
        return "name"

    class Meta:
        managed = False
        db_table = 'cms_category_itembean'
        ordering = ['-id']  # 按排序来排序


class CmsCategoryitemItembean(CmsBaseModel):
    """二级分类-商家 映射表"""
    category_item = models.ForeignKey(CmsCategoryItem)  # category_item_id = models.IntegerField()
    item_bean = models.ForeignKey(CmsCategoryItembean)  # item_bean_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'cms_categoryitem_itembean'


class CmsViewCategoryitem(CmsBaseModel):
    category_item = models.ForeignKey(CmsCategoryItem)  # category_item_id = models.IntegerField()
    channel = models.ForeignKey(CmsChannels)  # channel_id = models.IntegerField()
    status = models.IntegerField(default=0)

    class Meta:
        managed = False
        db_table = 'cms_view_categoryitem'


"""
    所有的分类: cms_navi_category
    左边导航类别表：cms_navicategories-----------category_id(cms_navi_category)
    导航与渠道关系表：cms_view_navi--------------navicat_id(cms_navicategories)------渠道
    导航与分类关系表：cms_navicates_category-----cate_id(cms_navicategories)---------category_id(cms_navi_category)
    导航与服务关系表：cms_navicates_services-----cate_id(cms_navicategories)
    导航与商品关系表：cms_navicates_goods--------cate_id(cms_navicategories)
"""


class CmsNaviCategory(CmsBaseModel):
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

    def city__text__(self):
        return get_city_str(self.city)

    def valid_time__text__(self):
        return get_valid_time(self.valid_time)

    def scene_id__text__(self):
        return get_scene_name(self.scene_id)

    def show_style__text__(self):
        return get_show_style(self.show_style)

    def get_check_title(self):
        return "name"

    class Meta:
        managed = True
        db_table = 'cms_navi_category'
        ordering = ["-id"]


class CmsNavicategories(CmsBaseModel):
    """左边导航类别表"""
    category = models.ForeignKey(CmsNaviCategory)  # category_id = models.IntegerField()
    name_style = models.CharField(verbose_name="颜色", max_length=256)
    location = models.IntegerField(verbose_name="排序")
    scene_id = models.IntegerField(verbose_name="场景")
    dot_info = models.CharField(verbose_name="打点信息", max_length=2048, blank=True,
                                null=True)  # dot_info = models.CharField(max_length=2048)

    def scene_id__text__(self):
        return get_scene_name(self.scene_id)

    class Meta:
        managed = False
        db_table = 'cms_navicategories'


class CmsNavicatesCategory(CmsBaseModel):
    """导航与分类关系表"""
    cate = models.ForeignKey(CmsNavicategories)  # cate_id = models.IntegerField()
    category = models.ForeignKey(CmsNaviCategory)  # category_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'cms_navicates_category'


class CmsNavicatesGoods(CmsBaseModel):
    """导航与商品关系表"""
    cate = models.ForeignKey(CmsNavicategories)  # cate_id = models.IntegerField()
    goods = models.ForeignKey(CmsGoods)  # goods_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'cms_navicates_goods'
        unique_together = (('cate', 'goods'),)  # unique_together = (('cate_id', 'goods_id'),)


class CmsNavicatesServices(CmsBaseModel):
    """导航与服务关系表"""
    cate = models.ForeignKey(CmsNavicategories)  # cate_id = models.IntegerField()
    service = models.ForeignKey(CmsServices)  # service_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'cms_navicates_services'
        unique_together = (('cate', 'service'),)  # unique_together = (('cate_id', 'service_id'),)


class CmsViewNavi(CmsBaseModel):
    navicat = models.ForeignKey(CmsNavicategories)  # navicat_id = models.IntegerField()
    channel = models.ForeignKey(CmsChannels)  # channel_id = models.IntegerField()
    status = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cms_view_navi'
        unique_together = (('navicat', 'channel'),)  # unique_together = (('navicat_id', 'channel_id'),)


class CmsOpconfig(CmsBaseModel):
    """运营配置表"""
    key = models.CharField(max_length=128)
    value = models.CharField(max_length=1024)

    def key__text__(self):
        print(self.key, OP_CONFIG.get_key_text(self.key))
        return OP_CONFIG.get_key_text(self.key)

    def value__text__(self):
        return OP_CONFIG.get_value_text(self.key, self.value)

    def get_check_title(self):
        return "key"

    class Meta:
        managed = False
        db_table = 'cms_opconfig'


class CmsViewOpconfig(CmsBaseModel):
    """运营配置和渠道关联表"""
    opconfig = models.ForeignKey(CmsOpconfig)  # opconfig_id = models.IntegerField()
    channel = models.ForeignKey(CmsChannels)  # channel_id = models.IntegerField()
    status = models.IntegerField(blank=True, null=True, default=0)

    class Meta:
        managed = False
        db_table = 'cms_view_opconfig'
        unique_together = (('opconfig', 'channel'),)


class CmsSpecialTopic(CmsBaseModel):
    title = models.CharField(verbose_name="专题标题", max_length=256)
    title_color = models.CharField(verbose_name="标题颜色", max_length=256)
    subtitle = models.CharField(verbose_name="副标题", max_length=256)
    subtitle_color = models.CharField(verbose_name="副标题颜色", max_length=256)
    image_url = models.CharField(verbose_name="图片", max_length=2048)
    action_id = models.IntegerField(verbose_name="动作")
    strategy = models.IntegerField(verbose_name="", default=0)
    valid_time = models.CharField(verbose_name="有效时间", max_length=256)
    city = models.TextField(verbose_name="城市")
    scene_id = models.IntegerField(verbose_name="场景")
    open_cp_id = models.IntegerField(verbose_name="")
    open_service_id = models.IntegerField(verbose_name="")
    open_goods_id = models.IntegerField(verbose_name="")
    open_type = models.IntegerField(verbose_name="类别")
    create_time = models.DateTimeField(verbose_name="", blank=True, null=True)
    update_time = models.DateTimeField(verbose_name="")

    def open_type__text__(self):
        return get_2array_value(open_type, self.open_type)

    def city__text__(self):
        return get_city_str(self.city)

    def valid_time__text__(self):
        return get_valid_time(self.valid_time)

    def scene_id__text__(self):
        return get_scene_name(self.scene_id)

    def get_check_title(self):
        return "title"

    def save(self, *args, **kwargs):
        if not self.id:
            self.create_time = timezone.now()
        self.update_time = timezone.now()
        return super(CmsSpecialTopic, self).save(*args, **kwargs)

    class Meta:
        managed = False
        db_table = 'cms_special_topic'
        ordering = ["-id"]


class CmsViewHomepageTopic(CmsBaseModel):
    """首页专题"""
    topic = models.ForeignKey(CmsSpecialTopic)  # topic_id = models.IntegerField()
    channel = models.ForeignKey(CmsChannels)  # channel_id = models.IntegerField()
    status = models.IntegerField(default=0)

    class Meta:
        managed = False
        db_table = 'cms_view_homepage_topic'


class CmsViewFindTopic(CmsBaseModel):
    """发现页专题"""
    topic_id = models.IntegerField(verbose_name="")
    is_top = models.IntegerField(verbose_name="是否置顶", blank=True, null=True, default=0)
    channel_id = models.IntegerField(verbose_name="")  # channel = models.ForeignKey(CmsChannels)
    status = models.IntegerField(verbose_name="", default=0)
    update_time = models.DateTimeField(verbose_name="")
    create_time = models.DateTimeField(verbose_name="", blank=True, null=True)
    is_deleted = models.IntegerField(verbose_name="是否删除", default=0)
    delete_time = models.DateTimeField(verbose_name="", blank=True, null=True)
    mark_info = models.CharField(max_length=200, blank=True, null=True)

    def is_top__text__(self):
        return "是" if self.is_top else "否"

    def is_deleted__text__(self):
        return "是" if self.is_top else "否"

    def save(self, *args, **kwargs):
        if self.id:
            self.update_time = timezone.now()
        return super(CmsViewFindTopic, self).save(*args, **kwargs)

    class Meta:
        managed = False
        db_table = 'cms_view_find_topic'


class CmsStreamcontent(CmsBaseModel):
    """内容流组表"""
    type = models.IntegerField(verbose_name="类别")
    location = models.IntegerField(verbose_name="排序")
    scene_id = models.IntegerField(verbose_name="场景")

    def type__text__(self):
        return get_2array_value(streams_type, self.type)

    def scene_id__text__(self):
        return get_scene_name(self.scene_id)

    class Meta:
        managed = False
        db_table = 'cms_streamcontent'


class CmsStreamcontentbeans(CmsBaseModel):
    """内容流表"""
    location = models.IntegerField(verbose_name="排序")
    img_url = models.CharField(verbose_name="图标", max_length=256)
    title = models.CharField(verbose_name="内容流标题", max_length=256)
    title_style = models.CharField(verbose_name="标题颜色", max_length=256)
    descibe = models.CharField(verbose_name="描述", max_length=2048)
    descibe_style = models.CharField(verbose_name="描述颜色", max_length=256)
    name = models.CharField(verbose_name="商品名称", max_length=256, blank=True, null=True)
    name_style = models.CharField(verbose_name="商品名称颜色", max_length=256)
    price = models.FloatField(verbose_name="商品现价")
    price_style = models.CharField(verbose_name="商品现价颜色", max_length=256, blank=True, null=True)
    price_desc = models.CharField(verbose_name="商品现价描述", max_length=256, blank=True, null=True)
    price_desc_style = models.CharField(verbose_name="商品现价描述颜色", max_length=256)
    orig_price = models.FloatField(verbose_name="商品原价")
    sold = models.IntegerField(verbose_name="已售数量", blank=True, null=True)
    latitude = models.FloatField(verbose_name="")
    longitude = models.FloatField(verbose_name="")
    action_id = models.IntegerField(verbose_name="动作")
    params = models.CharField(verbose_name="附加参数", max_length=2048)
    strategy = models.IntegerField(verbose_name="", blank=True, null=True, default=0)
    valid_time = models.CharField(verbose_name="有效时间", max_length=256, blank=True, null=True)
    city = models.TextField(verbose_name="城市", blank=True, null=True)
    open_cp_id = models.IntegerField(verbose_name="", default=0)
    open_service_id = models.IntegerField(verbose_name="", default=0)
    open_goods_id = models.IntegerField(verbose_name="", default=0)
    open_type = models.IntegerField(verbose_name="类别")
    action_json = models.TextField(blank=True, null=True)
    mark = models.CharField(verbose_name="运营标签", max_length=256, blank=True, null=True)

    def open_type__text__(self):
        return get_2array_value(open_type, self.open_type)

    def city__text__(self):
        return get_city_str(self.city)

    def valid_time__text__(self):
        return get_valid_time(self.valid_time)

    def get_check_title(self):
        return "title"

    class Meta:
        managed = False
        db_table = 'cms_streamcontentbeans'


class CmsStreamcontentsBeans(CmsBaseModel):
    """内容流组表和内容流关系表"""
    streamcontent = models.ForeignKey(CmsStreamcontent)  # streamcontent_id = models.IntegerField()
    bean = models.ForeignKey(CmsStreamcontentbeans)  # bean_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'cms_streamcontents_beans'
        unique_together = (('streamcontent', 'bean'),)  # unique_together = (('streamcontent_id', 'bean_id'),)


class CmsStreamcontentsGoods(CmsBaseModel):
    """内容流组表和商品关系表"""
    streamcontent = models.ForeignKey(CmsStreamcontent)  # streamcontent_id = models.IntegerField()
    goods = models.ForeignKey(CmsGoods)  # goods_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'cms_streamcontents_goods'


class CmsViewStream(CmsBaseModel):
    """内容流组表和渠道关联表"""
    streamcontent = models.ForeignKey(CmsStreamcontent)  # streamcontent_id = models.IntegerField()
    channel = models.ForeignKey(CmsChannels)  # channel_id = models.IntegerField()
    status = models.IntegerField(blank=True, null=True, default=0)

    class Meta:
        managed = False
        db_table = 'cms_view_stream'
        unique_together = (('streamcontent', 'channel'),)  # unique_together = (('streamcontent_id', 'channel_id'),)


class CmsCoupon(CmsBaseModel):
    """内容库 优惠券表"""
    coupon_id = models.IntegerField(verbose_name="优惠券ID")
    name = models.CharField(verbose_name="优惠券名称", max_length=256)
    url = models.CharField(verbose_name="图片", max_length=256)
    height = models.SmallIntegerField(verbose_name="高度")
    location = models.IntegerField(verbose_name="排序")
    start = models.IntegerField(verbose_name="起始时间")
    end = models.IntegerField(verbose_name="结束时间")
    strategy = models.IntegerField(verbose_name="", blank=True, null=True, default=0)
    valid_time = models.CharField(verbose_name="有效时间", max_length=256, blank=True, null=True)
    city = models.TextField(verbose_name="城市", blank=True, null=True)
    scene_id = models.IntegerField(verbose_name="场景")
    open_cp_id = models.IntegerField(verbose_name="", default=0)
    open_service_id = models.IntegerField(verbose_name="", default=0)
    open_goods_id = models.CharField(verbose_name="", max_length=255, default=0)
    open_coupon_id = models.IntegerField(verbose_name="", default=0)
    parent_id = models.IntegerField(verbose_name="", default=-1)
    mobile = models.CharField(verbose_name="", max_length=256, blank=True, null=True)

    def start__text__(self):
        return timestamp2str_space(self.start)

    def end__text__(self):
        return timestamp2str_space(self.end)

    def city__text__(self):
        return get_city_str(self.city)

    def valid_time__text__(self):
        return get_valid_time(self.valid_time)

    def scene_id__text__(self):
        return get_scene_name(self.scene_id)

    def get_check_title(self):
        return "name"

    class Meta:
        managed = False
        db_table = 'cms_coupon'
        ordering = ['-id']


class CmsLikes(CmsBaseModel):
    """配置库 猜你喜欢表"""
    title = models.CharField(verbose_name="猜你喜欢标题", max_length=256)
    desc = models.CharField(verbose_name="描述", max_length=2048)
    title_style = models.CharField(verbose_name="标题颜色", max_length=256, blank=True, null=True)
    desc_style = models.CharField(verbose_name="描述颜色", max_length=256, blank=True, null=True)
    scene_id = models.IntegerField(verbose_name="场景")

    def scene_id__text__(self):
        return get_scene_name(self.scene_id)

    def get_check_title(self):
        return "title"

    class Meta:
        managed = False
        db_table = 'cms_likes'


class CmsViewLike(CmsBaseModel):
    """猜你喜欢和渠道关联表"""
    like = models.ForeignKey(CmsLikes)
    channel = models.ForeignKey(CmsChannels)
    status = models.IntegerField(blank=True, null=True, default=0)

    class Meta:
        managed = False
        db_table = 'cms_view_like'
        unique_together = (('like', 'channel'),)


class CmsLikesGoods(CmsBaseModel):
    like = models.ForeignKey(CmsLikes)
    goods = models.ForeignKey(CmsGoods)

    class Meta:
        managed = False
        db_table = 'cms_likes_goods'
        unique_together = (('like', 'goods'),)


class CmsLikesServices(CmsBaseModel):
    like = models.ForeignKey(CmsLikes)
    service = models.ForeignKey(CmsServices)

    class Meta:
        managed = False
        db_table = 'cms_likes_services'
        unique_together = (('like', 'service'),)


class CmsActivities(CmsBaseModel):
    """活动表"""
    url = models.CharField(max_length=256)
    height = models.SmallIntegerField(verbose_name="高度")
    location = models.IntegerField(verbose_name="排序")
    start = models.IntegerField(verbose_name="起始时间")
    end = models.IntegerField(verbose_name="结束时间")
    strategy = models.IntegerField(verbose_name="", blank=True, null=True, default=0)
    valid_time = models.CharField(verbose_name="有效时间", max_length=256, blank=True, null=True)
    city = models.TextField(verbose_name="城市", blank=True, null=True)
    scene_id = models.IntegerField(verbose_name="场景")
    open_cp_id = models.IntegerField(verbose_name="", default=0)
    open_service_id = models.IntegerField(verbose_name="", default=0)
    open_goods_id = models.IntegerField(verbose_name="", default=0)
    open_type = models.IntegerField(verbose_name="类别")

    def start__text__(self):
        return timestamp2str_space(self.start)

    def end__text__(self):
        return timestamp2str_space(self.end)

    def city__text__(self):
        return get_city_str(self.city)

    def valid_time__text__(self):
        return get_valid_time(self.valid_time)

    def scene_id__text__(self):
        return get_scene_name(self.scene_id)

    def open_type__text__(self):
        return get_2array_value(open_type, self.open_type)

    class Meta:
        managed = False
        db_table = 'cms_activities'


class CmsViewActivity(CmsBaseModel):
    """活动和渠道关联表"""
    activity = models.ForeignKey(CmsActivities)
    channel = models.ForeignKey(CmsChannels)
    status = models.IntegerField(blank=True, null=True, default=0)

    class Meta:
        managed = False
        db_table = 'cms_view_activity'


class CmsViewCoupon(CmsBaseModel):
    coupon = models.ForeignKey(CmsCoupon)  # coupon_id = models.IntegerField()
    channel = models.ForeignKey(CmsChannels)  # channel_id = models.IntegerField()
    status = models.IntegerField(blank=True, null=True, default=0)

    class Meta:
        managed = False
        db_table = 'cms_view_coupon'


class CmsChoicenessCategory(CmsBaseModel):
    """精品分类表"""

    category = models.ForeignKey(CmsNaviCategory)
    img_url = models.CharField(verbose_name="图片", max_length=255, blank=True, null=True)
    city = models.TextField(verbose_name="城市", blank=True, null=True)
    strategy = models.IntegerField(verbose_name="", blank=True, null=True, default=0)
    status = models.IntegerField(verbose_name="", default=0)
    valid_time = models.CharField(verbose_name="有效时间", max_length=45, blank=True, null=True)
    img_url_d = models.CharField(verbose_name="按下时图片", max_length=255, blank=True, null=True)
    background_color = models.CharField(verbose_name="背景颜色", max_length=45, blank=True, null=True)
    location = models.IntegerField(verbose_name="排序", blank=True, null=True)

    def city__text__(self):
        return get_city_str(self.city)

    def valid_time__text__(self):
        return get_valid_time(self.valid_time)

    class Meta:
        managed = False
        db_table = 'cms_choiceness_category'


class CmsViewChoicenessCategory(CmsBaseModel):
    """精品分类表和渠道关联表"""
    choiceness_category = models.ForeignKey(CmsChoicenessCategory)  # choiceness_category_id = models.IntegerField()
    channel = models.ForeignKey(CmsChannels)  # channel_id = models.IntegerField()
    status = models.IntegerField(blank=True, null=True, default=0)

    class Meta:
        managed = False
        db_table = 'cms_view_choiceness_category'
        unique_together = (('choiceness_category', 'channel'),)


class CmsChannelChannel(CmsBaseModel):
    """渠道关联表"""
    channel_id1 = models.IntegerField(verbose_name="源渠道")
    channel_id2 = models.IntegerField(verbose_name="目标渠道")
    config_items = models.CharField(verbose_name="项", max_length=128, blank=True, null=True)
    op_type = models.IntegerField(verbose_name="类型", blank=True, null=True, default=0)

    def channel_id1__text__(self):
        c, v, t = getCVT(self.channel_id1)
        text = get_nav_text(str(t))
        return "应用为%s，版本为%s，渠道为%s" % (text, v, c)

    def channel_id2__text__(self):
        c, v, t = getCVT(self.channel_id2)
        text = get_nav_text(str(t))
        return "应用为%s，版本为%s，渠道为%s" % (text, v, c)

    def config_items__text__(self):
        if not self.config_items:
            return "全部"

        def __(arr, v):
            for item in arr:
                if v == item[1]:
                    return item[0]
            return ""

        arr = self.config_items.split(",")
        result = []
        for a in arr:
            result.append(__(item_modules, a))
        return " | ".join(result)

    def op_type__text__(self):
        arr = [[1, "复制"], [0, "关联"]]
        return get_2array_value(arr, self.op_type)

    class Meta:
        managed = False
        db_table = 'cms_channel_channel'
        unique_together = (('channel_id1', 'channel_id2'),)


class CmsCheck(CmsBaseModel):
    channel_id = models.IntegerField(default=0)  # 0代表内容库
    module = models.CharField(max_length=100, blank=True, null=True)
    submit_person = models.CharField(max_length=100, blank=True, null=True)
    submit_date = models.DateTimeField(blank=True, null=True)
    check_person = models.CharField(max_length=100, blank=True, null=True)
    check_date = models.DateTimeField(blank=True, null=True)
    table_name = models.CharField(max_length=256)
    data_id = models.IntegerField()
    op_type = models.IntegerField(blank=True, null=True)
    status = models.IntegerField(blank=True, null=True, default=1)
    is_show = models.IntegerField(blank=True, null=True, default=1)
    remark = models.CharField(max_length=1024, blank=True, null=True)  # 删除，title, name。若remark为空，则显示所有信息
    alter_person = models.CharField(max_length=100, blank=True, null=True)
    alter_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cms_check'


class CmsCheckHistory(CmsBaseModel):
    status = models.CharField(max_length=45)
    check_person = models.CharField(max_length=100)
    check_date = models.CharField(max_length=45)
    type = models.CharField(max_length=1024)
    version = models.CharField(max_length=1024)
    channel_no = models.CharField(max_length=1024)
    module = models.CharField(max_length=45)
    submit_person = models.CharField(max_length=100)
    submit_date = models.CharField(max_length=45)
    content = models.TextField()

    class Meta:
        managed = False
        db_table = 'cms_check_history'
        ordering = ['-check_date']


class CmsScreenads(CmsBaseModel):
    name = models.CharField(verbose_name="开屏广告名称", max_length=200, blank=True, null=True)
    img_url = models.CharField(verbose_name="图片", max_length=256)
    start = models.IntegerField(verbose_name="起始时间")
    end = models.IntegerField(verbose_name="结束时间")
    location = models.IntegerField(verbose_name="排序", default=-1)
    action_id = models.IntegerField(verbose_name="动作")
    strategy = models.IntegerField(verbose_name="", blank=True, null=True, default=0)
    valid_time = models.CharField(verbose_name="有效时间", max_length=256, blank=True, null=True)
    city = models.TextField(verbose_name="城市", blank=True, null=True)
    open_cp_id = models.IntegerField(verbose_name="", default=0)
    open_service_id = models.IntegerField(verbose_name="", default=0)
    open_goods_id = models.IntegerField(verbose_name="", default=0)
    open_type = models.IntegerField(verbose_name="类别", default=0)
    action_json = models.TextField(blank=True, null=True)
    phone_type = models.CharField(verbose_name="机型", max_length=200, blank=True, null=True)
    show_times = models.IntegerField(verbose_name="展示次数", blank=True, null=True)  # 展示次数，1，仅展示一次，100，每次进入展示
    show_hold = models.IntegerField(verbose_name="展示时长", blank=True, null=True)  # 展示时长 精确到秒

    def show_times__text__(self):
        return get_2array_value(screen_ad_times, self.show_times)

    def start__text__(self):
        return timestamp2str_space(self.start)

    def end__text__(self):
        return timestamp2str_space(self.end)

    def city__text__(self):
        return get_city_str(self.city)

    def valid_time__text__(self):
        return get_valid_time(self.valid_time)

    def open_type__text__(self):
        return get_2array_value(open_type, self.open_type)

    def show_hold__text__(self):
        return "不限" if self.show_hold == -1 else self.show_hold

    def get_check_title(self):
        return "name"

    class Meta:
        managed = False
        db_table = 'cms_screenads'


class CmsViewScreenads(CmsBaseModel):
    screenad = models.ForeignKey(CmsScreenads)  # screenad_id = models.IntegerField()
    channel = models.ForeignKey(CmsChannels)  # channel_id = models.IntegerField()
    status = models.IntegerField(blank=True, null=True, default=0)

    class Meta:
        managed = False
        db_table = 'cms_view_screenads'
        unique_together = (('screenad', 'channel'),)  # unique_together = (('screenad_id', 'channel_id'),)


class CmsNativeActivity(CmsBaseModel):
    title = models.CharField(verbose_name="Native活动标题", max_length=256)
    title_color = models.CharField(verbose_name="标题颜色", max_length=256)
    subtitle = models.CharField(verbose_name="副标题", max_length=256)
    image_url = models.CharField(verbose_name="图片", max_length=256)
    start_time = models.IntegerField(verbose_name="开始时间")
    end_time = models.IntegerField(verbose_name="结束时间")
    sort = models.IntegerField(verbose_name="排序")
    action_id = models.IntegerField(verbose_name="动作")
    strategy = models.IntegerField(verbose_name="", blank=True, null=True, default=0)
    valid_time = models.CharField(verbose_name="有效时间", max_length=256)
    city = models.TextField(verbose_name="城市")
    scene_id = models.IntegerField(verbose_name="场景")
    open_cp_id = models.IntegerField(verbose_name="", default=0)
    open_service_id = models.IntegerField(verbose_name="", default=0)
    open_goods_id = models.IntegerField(verbose_name="", default=0)
    open_type = models.IntegerField(verbose_name="类别")
    action_json = models.TextField(blank=True, null=True)
    open_time = models.IntegerField(verbose_name="活动倒计时开始时间", blank=True, null=True)
    close_time = models.IntegerField(verbose_name="活动倒计时结束时间", blank=True, null=True)

    def start_time__text__(self):
        return timestamp2str_space(self.start_time)

    def end_time__text__(self):
        return timestamp2str_space(self.end_time)

    def open_time__text__(self):
        return timestamp2str_space(self.open_time)

    def close_time__text__(self):
        return timestamp2str_space(self.close_time)

    def city__text__(self):
        return get_city_str(self.city)

    def valid_time__text__(self):
        return get_valid_time(self.valid_time)

    def scene_id__text__(self):
        return get_scene_name(self.scene_id)

    def open_type__text__(self):
        return get_2array_value(open_type, self.open_type)

    def get_check_title(self):
        return "title"

    class Meta:
        managed = False
        db_table = 'cms_native_activity'


class CmsViewNativeActivity(CmsBaseModel):
    nactivity = models.ForeignKey(CmsNativeActivity)  # nactivity_id = models.IntegerField()
    channel = models.ForeignKey(CmsChannels)  # channel_id = models.IntegerField()
    status = models.IntegerField(default=0)

    class Meta:
        managed = False
        db_table = 'cms_view_native_activity'


class CmsChannelJpush(CmsBaseModel):
    """
    极光推送表
    """
    channel_no = models.CharField(max_length=256, blank=True, null=True)
    channel_name = models.CharField(max_length=256, blank=True, null=True)
    app_key = models.CharField(max_length=500, blank=True, null=True)
    master_secret = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cms_channel_jpush'


class CmsOpenVersion(CmsBaseModel):
    name = models.CharField(max_length=64)

    class Meta:
        managed = False
        db_table = 'cms_open_version'


class CmsOpenChannel(CmsBaseModel):
    name = models.CharField(max_length=64)
    app_version = models.ForeignKey(CmsOpenVersion)  # app_version_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'cms_open_channel'


class CmsOpenService(CmsBaseModel):
    action = models.ForeignKey(CmsActions)  # action_id = models.IntegerField()
    show_name = models.CharField(max_length=256, blank=True, null=True)
    icon = models.CharField(max_length=256)
    city = models.CharField(max_length=256)
    distribute = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'cms_open_service'


class CmsViewOpenService(CmsBaseModel):
    channel = models.ForeignKey(CmsOpenChannel)  # channel_id = models.IntegerField()
    service = models.ForeignKey(CmsOpenService)  # service_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'cms_view_open_service'


class CmsViewPush(CmsBaseModel):
    channel_id = models.IntegerField()
    city = models.CharField(max_length=20, blank=True, null=True)
    data_version = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cms_view_push'
        unique_together = (('channel_id', 'city'),)


class CmsCpinfo(CmsBaseModel):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=256)
    icon = models.CharField(max_length=256)

    class Meta:
        managed = False
        db_table = 'cms_cpinfo'


# ====================v3.7======================
class CmsCPCategory(models.Model):
    """品牌分类"""
    name = models.CharField(verbose_name="分类名", max_length=256)
    location = models.IntegerField(verbose_name="排序")

    class Meta:
        managed = False
        db_table = 'cms_cp_category'
        ordering = ["id"]


class CmsCP(models.Model):
    """品牌"""
    name = models.CharField(verbose_name="品牌名", max_length=256)
    name_style = models.CharField(verbose_name="名称颜色", max_length=256, blank=True, null=True, default='#000000')
    icon = models.CharField(verbose_name="图片", max_length=256)
    adver_icon = models.CharField(verbose_name="宣传图", max_length=256)
    desc = models.CharField(verbose_name="描述", max_length=256, blank=True, null=True)
    desc_style = models.CharField(verbose_name="描述颜色", max_length=256, blank=True, null=True, default='#000000')
    action_id = models.IntegerField(verbose_name="动作", blank=True, null=True)
    action_json = models.TextField(blank=True, null=True)
    search_keyword = models.TextField(verbose_name="搜索关键词", blank=True, null=True)
    service_time = models.CharField(verbose_name="服务时间", max_length=256, blank=True, null=True)
    shop_type = models.CharField(verbose_name="商家类型", max_length=256, blank=True, null=True)  # 旗舰店
    company_name = models.CharField(verbose_name="企业名称", max_length=256, blank=True, null=True)
    certified_company = models.IntegerField(verbose_name="是否认证企业")
    location2 = models.IntegerField(verbose_name="品牌页排序", default=1)
    sort = models.IntegerField(verbose_name='品牌列表排序', blank=True, default=0)
    # V4.1添加
    tag_in_list = models.CharField(verbose_name='CP列表标签', max_length=1000, blank=True)
    # V4.3添加 ,90% 则数据库存90
    feedback = models.CharField(verbose_name='好评率', max_length=256, null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'cms_cp'
        ordering = ["-id"]


class CmsCpdisplay(models.Model):
    location1 = models.IntegerField(verbose_name="首页排序", blank=True, default=0)
    mark = models.CharField(verbose_name="运营标签", max_length=256, blank=True, null=True)
    text = models.CharField(verbose_name="运营文案", max_length=256, blank=True, null=True)
    meta = models.ForeignKey(CmsCP)
    op_desc = models.CharField(verbose_name="运营描述", max_length=256, blank=True, null=True)
    parent_id = models.IntegerField(default=1)

    class Meta:
        managed = False
        db_table = 'cms_cpdisplay'
        ordering = ["location1"]


class CmsViewCP(models.Model):
    """品牌和品牌分类的关联表"""
    cp_category = models.ForeignKey(CmsCPCategory)
    cp = models.ForeignKey(CmsCP)

    class Meta:
        managed = False
        db_table = 'cms_view_cp'


class CmsHomeCP(models.Model):
    """品牌渠道关联"""
    channel = models.ForeignKey(CmsChannels)
    cp = models.ForeignKey(CmsCpdisplay)

    class Meta:
        managed = False
        db_table = 'cms_home_cp'


class CmsStreamCp(models.Model):
    """内容流组表和品牌的关系表"""
    stream = models.ForeignKey(CmsStreamcontent)
    cp = models.ForeignKey(CmsCpdisplay)

    class Meta:
        managed = False
        db_table = 'cms_stream_cp'


class CmsActivityV37(models.Model):
    """活动表"""
    name = models.CharField(verbose_name="活动名称", max_length=256)
    action_id = models.IntegerField(verbose_name="动作")
    action_json = models.TextField(blank=True, null=True)
    img = models.CharField(verbose_name="图片", max_length=256)
    # 该字段作用到同个CP下有多个活动时的排序
    priority = models.IntegerField(verbose_name="优先级")
    cp = models.ManyToManyField(CmsCP, verbose_name="品牌", through='CmsActivityCP', through_fields=('activity', 'cp'))
    goods = models.ManyToManyField(CmsGoods, verbose_name="商品", through='CmsActivityGoods',
                                   through_fields=('activity', 'goods'))
    valid_time = models.CharField(verbose_name="有效时间", max_length=256)
    city = models.TextField(verbose_name="城市")

    class Meta:
        managed = False
        db_table = 'cms_activity_v37'
        ordering = ['-id']


class CmsViewActivity37(models.Model):
    """渠道和活动的关联表"""
    channel = models.ForeignKey(CmsChannels)
    activity = models.ForeignKey(CmsActivityV37)

    class Meta:
        managed = False
        db_table = 'cms_view_activity37'


class CmsActivityCP(models.Model):
    """活动和品牌的关联表"""
    activity = models.ForeignKey(CmsActivityV37)
    cp = models.ForeignKey(CmsCP)

    class Meta:
        managed = False
        db_table = 'cms_activity_cp'


class CmsActivityGoods(models.Model):
    """活动和商品的关联表"""
    activity = models.ForeignKey(CmsActivityV37)
    goods = models.ForeignKey(CmsGoods)

    class Meta:
        managed = False
        db_table = 'cms_activity_goods'


class CmsCategoryGroup(models.Model):
    """分类组表"""
    name = models.CharField(verbose_name="名称", max_length=256)
    location = models.IntegerField(verbose_name="排序")
    memo = models.CharField(verbose_name="备注", max_length=256, blank=True, null=True)
    valid_time = models.CharField(verbose_name="有效时间", max_length=256)
    city = models.TextField(verbose_name="城市")

    class Meta:
        managed = False
        db_table = 'cms_category_group'


class CmsViewGroupCategory(models.Model):
    """分类组和分类的关联表"""
    group = models.ForeignKey(CmsCategoryGroup)
    category = models.ForeignKey(CmsNaviCategory)

    class Meta:
        managed = False
        db_table = 'cms_view_group_category'


class CmsViewChannelGroup(models.Model):
    """渠道和分类组关联表"""
    channel = models.ForeignKey(CmsChannels)
    group = models.ForeignKey(CmsCategoryGroup)

    class Meta:
        managed = False
        db_table = 'cms_view_channel_group'


class CmsShareCoupon(models.Model):
    """
    is_dialog:1 弹，0不弹
    """
    product_type = models.IntegerField()
    dialog_title = models.CharField(max_length=256)
    dialog_content = models.CharField(max_length=256)
    dialog_img = models.CharField(max_length=256, blank=True, null=True)
    button_name = models.CharField(max_length=256)
    action_type = models.IntegerField()
    share_imgurl = models.CharField(max_length=256, blank=True, null=True)
    share_title = models.CharField(max_length=256, blank=True, null=True)
    share_content = models.CharField(max_length=256, blank=True, null=True)
    share_url = models.CharField(max_length=256, blank=True, null=True)
    action_id = models.IntegerField(blank=True, null=True)
    action_json = models.CharField(max_length=256, blank=True, null=True)
    times_limit = models.IntegerField(blank=True, null=True)
    start_time = models.IntegerField(blank=True, null=True)
    end_time = models.IntegerField(blank=True, null=True)
    city = models.CharField(max_length=256)
    show_style = models.IntegerField()
    icon = models.CharField(max_length=256, blank=True, null=True)
    details_url = models.CharField(max_length=256, blank=True, null=True)
    activity_id = models.CharField(max_length=200, blank=True, null=True)
    is_dialog = models.IntegerField(blank=True, null=True)
    # V4.5
    sns_url = models.CharField(u"社交平台分享图片", max_length=255, blank=True, null=True)


    class Meta:
        managed = False
        db_table = 'cms_share_coupon'


class CmsViewShareCoupon(models.Model):
    channel = models.ForeignKey(CmsChannels)  # channel_id = models.IntegerField()
    share_coupon = models.ForeignKey(CmsShareCoupon)  # share_coupon_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'cms_view_share_coupon'


# 秒杀活动基础配置
class CmsSecKill(models.Model):
    title = models.CharField(max_length=1000, verbose_name='标题')
    desc = models.CharField(max_length=1000, verbose_name='描述')
    image_bcg = models.CharField(max_length=2000, verbose_name='秒杀活动图片')
    price_desc = models.CharField(max_length=1000, verbose_name='秒杀价')
    price_sub_desc = models.CharField(max_length=1000, blank=True, verbose_name='原价')
    image_mark = models.CharField(max_length=1000, blank=True, verbose_name='运营标签')
    show_start_time = models.DateTimeField(verbose_name='活动展示开始时间')
    show_end_time = models.DateTimeField(verbose_name='活动展示结束时间')
    action_id = models.IntegerField(verbose_name='动作ID')
    share_title = models.CharField(max_length=1000, verbose_name='分享标题')
    share_desc = models.CharField(max_length=2000, verbose_name='分享描述')
    share_url = models.CharField(max_length=1000, verbose_name='分享链接')
    share_thumbnail = models.CharField(max_length=1000, verbose_name='分享缩略图')
    activity_id = models.IntegerField(verbose_name='营销活动ID')
    goods_id = models.IntegerField(verbose_name='商品ID')
    city = models.CharField(max_length=2000, verbose_name='活动城市')
    tips = models.CharField(max_length=1000, blank=True, verbose_name='更新提醒')
    seckill_remark_url = models.CharField(max_length=1000, blank=True, verbose_name='秒杀说明')

    class Meta:
        managed = False
        db_table = 'cms_seckill'


class CmsSecKillView(models.Model):
    channel_id = models.IntegerField(verbose_name='渠道ID')
    seckill_id = models.IntegerField(verbose_name='秒杀配置ID')
    status = models.IntegerField(verbose_name='状态')

    class Meta:
        managed = False
        db_table = 'cms_seckill_view'


class CmsSecKillViewTemp(models.Model):
    channel = models.ForeignKey(CmsChannels)
    seckill = models.ForeignKey(CmsSecKill)
    status = models.IntegerField(verbose_name='状态')

    class Meta:
        managed = False
        db_table = 'cms_seckill_view'


class ViewCmsSecKillView(models.Model):
    channel_id = models.IntegerField(verbose_name='渠道ID')
    seckill_id = models.IntegerField(verbose_name='秒杀配置ID')
    title = models.CharField(max_length=1000, verbose_name='标题')
    desc = models.CharField(max_length=2000, verbose_name='描述')
    image_bcg = models.CharField(max_length=2000, verbose_name='图片')
    price_desc = models.CharField(max_length=1000, verbose_name='秒杀价格')
    price_sub_desc = models.CharField(max_length=1000, verbose_name='原价')
    image_mark = models.CharField(max_length=1000, verbose_name='运营标签')
    show_start_time = models.DateTimeField(verbose_name='活动展示开始时间')
    show_end_time = models.DateTimeField(verbose_name='活动展示结束时间')
    city = models.CharField(max_length=2000, verbose_name='城市')

    class Meta:
        managed = False
        db_table = 'view_cms_seckills'


class OpGoodsActivity(models.Model):
    activityId = models.IntegerField(verbose_name='营销活动ID')
    activityPrice = models.IntegerField(verbose_name='营销价格')
    price = models.IntegerField(verbose_name='价格')
    applyUser = models.CharField(max_length=100)
    commentCount = models.IntegerField(verbose_name='评论数')
    cpid = models.IntegerField(verbose_name='CP ID')
    goodsId = models.IntegerField(verbose_name='商品ID')
    gorder = models.IntegerField(verbose_name='gorder')
    orderCount = models.IntegerField(verbose_name='销售数量')
    promotionMsg = models.CharField(max_length=256, verbose_name='活动描述')
    promotionType = models.IntegerField(verbose_name='类型')
    activityBeginDate = models.DateTimeField(verbose_name='活动开始时间')
    activityEndDate = models.DateTimeField(verbose_name='活动结束时间')
    activityCity = models.TextField(verbose_name='活动支持城市')
    rawstring = models.TextField(verbose_name='备注')
    updateTime = models.DateTimeField(verbose_name='更新时间')
    is_seckill = models.IntegerField(verbose_name='是否秒杀')
    capacity = models.IntegerField(verbose_name='活动供货量')

    class Meta:
        managed = False
        db_table = 'op_goods_activity_act'


class OpGoodsActivityView(models.Model):
    name = models.CharField(max_length=200, verbose_name='商品名')
    cp_name = models.CharField(max_length=200, verbose_name='CP名字')
    activityId = models.IntegerField(verbose_name='营销活动ID')
    activityPrice = models.IntegerField(verbose_name='营销价格')
    price = models.IntegerField(verbose_name='价格')
    applyUser = models.CharField(max_length=100)
    commentCount = models.IntegerField(verbose_name='评论数')
    cpid = models.IntegerField(verbose_name='CP ID')
    goodsId = models.IntegerField(verbose_name='商品ID')
    gorder = models.IntegerField(verbose_name='gorder')
    orderCount = models.IntegerField(verbose_name='销售数量')
    promotionMsg = models.CharField(max_length=256, verbose_name='活动描述')
    promotionType = models.IntegerField(verbose_name='类型')
    activityBeginDate = models.DateTimeField(verbose_name='活动开始时间')
    activityEndDate = models.DateTimeField(verbose_name='活动结束时间')
    activityCity = models.TextField(verbose_name='活动支持城市')
    rawstring = models.TextField(verbose_name='备注')
    updateTime = models.DateTimeField(verbose_name='更新时间')
    is_seckill = models.IntegerField(verbose_name='是否秒杀')
    capacity = models.IntegerField(verbose_name='活动供货量')

    class Meta:
        managed = False
        db_table = 'op_goods_activity_view'


# 常见问题
class CmsProblem(models.Model):
    problem = models.CharField(verbose_name='问题', max_length=1000)
    answer = models.CharField(verbose_name='答案', max_length=4000)
    sort = models.IntegerField(verbose_name='排序')

    class Meta:
        managed = False
        db_table = 'cms_problem'


class CmsQuickOrder(models.Model):
    cms_quick_name = models.CharField(verbose_name="快捷入口名", max_length=255)
    cms_quick_desc = models.CharField(verbose_name="快捷入口名", max_length=255)
    image_url = models.CharField(verbose_name="快捷入口名", max_length=255)
    background_style = models.CharField(verbose_name="底色", max_length=256)
    order_style = models.CharField(verbose_name="分类名底色", max_length=256)
    create_date = models.IntegerField(verbose_name="创建时间戳")
    create_uid = models.IntegerField(verbose_name="创建用户ID")
    is_h5 = models.IntegerField(verbose_name=u"是否为H5流程")
    h5_url = models.CharField(verbose_name=u"URL地址", max_length=255)
    is_new = models.IntegerField(verbose_name=u"是否新版本", default=1)

    class Meta:
        managed = False
        db_table = 'cms_quick_order'


class CmsQuickOrderCategory(models.Model):
    quick_order_id = models.IntegerField(verbose_name="快捷入口ID")
    category_id = models.IntegerField(verbose_name="二级分类ID")
    create_date = models.IntegerField(verbose_name="创建时间戳")
    create_uid = models.IntegerField(verbose_name="创建用户ID")

    class Meta:
        managed = False
        db_table = 'cms_quick_order_category'


class CmsQuickOrderGoods(models.Model):
    quick_order_id = models.IntegerField(verbose_name="快捷入口ID")
    goods_id = models.IntegerField(verbose_name="商品(服务)ID")
    operation_desc = models.CharField(verbose_name='运营描述', max_length=255)
    sort = models.IntegerField(verbose_name='优先级')
    create_date = models.IntegerField(verbose_name="创建时间戳")
    create_uid = models.IntegerField(verbose_name="创建用户ID")

    class Meta:
        managed = False
        db_table = 'cms_quick_order_goods'


class CmsCategoryIndex(models.Model):
    category_id = models.IntegerField(verbose_name="二级分类ID")
    city = models.TextField(verbose_name="城市")
    is_need_all_service = models.IntegerField(verbose_name="是否需要全部服务接口")
    create_date = models.IntegerField(verbose_name="创建时间戳")
    create_uid = models.IntegerField(verbose_name="创建用户ID")

    class Meta:
        managed = False
        db_table = 'cms_category_index'


class CmsCategoryIndexQuickOrder(models.Model):
    quick_order_id = models.IntegerField(verbose_name="快捷入口ID")
    category_index_id = models.IntegerField(verbose_name="分类首页ID")
    create_date = models.IntegerField(verbose_name="创建时间戳")
    create_uid = models.IntegerField(verbose_name="创建用户ID")
    sort = models.IntegerField(verbose_name='优先级')

    class Meta:
        managed = False
        db_table = 'cms_category_index_quick_order'


class CmsCategoryIndexAds(models.Model):
    category_index_id = models.IntegerField(verbose_name="分类首页ID")
    create_date = models.IntegerField(verbose_name="创建时间戳")
    create_uid = models.IntegerField(verbose_name="创建用户ID")
    adbean_id = models.IntegerField(verbose_name="广告组ID")
    sort = models.IntegerField(verbose_name='优先级')

    class Meta:
        managed = False
        db_table = 'cms_category_index_ads'


class CmsCategoryIndexRecommendedGoods(models.Model):
    category_index_id = models.IntegerField(verbose_name="分类首页ID")
    sort = models.IntegerField(verbose_name='排序')
    goods_id = models.IntegerField(verbose_name="服务ID")
    start_date = models.IntegerField(verbose_name="开始时间戳")
    end_date = models.IntegerField(verbose_name="结束时间戳")
    create_date = models.IntegerField(verbose_name="创建时间戳")
    create_uid = models.IntegerField(verbose_name="创建用户ID")

    class Meta:
        managed = False
        db_table = "cms_category_index_recommended_goods"


class AuthToken(models.Model):
    id = models.IntegerField(primary_key=True)
    user_id = models.CharField(max_length=100, unique=True)
    token = models.CharField(max_length=100)

    class Meta:
        db_table = u'auth_token'