# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AuthGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=80, unique=True)),
            ],
            options={
                'managed': False,
                'db_table': 'auth_group',
            },
        ),
        migrations.CreateModel(
            name='AuthGroupPermissions',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
            ],
            options={
                'managed': False,
                'db_table': 'auth_group_permissions',
            },
        ),
        migrations.CreateModel(
            name='AuthPermission',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('codename', models.CharField(max_length=100)),
            ],
            options={
                'managed': False,
                'db_table': 'auth_permission',
            },
        ),
        migrations.CreateModel(
            name='AuthUser',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('password', models.CharField(max_length=128)),
                ('last_login', models.DateTimeField(blank=True, null=True)),
                ('is_superuser', models.IntegerField(default=0)),
                ('username', models.CharField(max_length=30, unique=True)),
                ('first_name', models.CharField(max_length=30, default='')),
                ('last_name', models.CharField(max_length=30, default='')),
                ('email', models.CharField(max_length=254)),
                ('is_staff', models.IntegerField()),
                ('is_active', models.IntegerField(default=1)),
                ('date_joined', models.DateTimeField()),
            ],
            options={
                'managed': False,
                'db_table': 'auth_user',
            },
        ),
        migrations.CreateModel(
            name='AuthUserGroups',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
            ],
            options={
                'managed': False,
                'db_table': 'auth_user_groups',
            },
        ),
        migrations.CreateModel(
            name='AuthUserUserPermissions',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
            ],
            options={
                'managed': False,
                'db_table': 'auth_user_user_permissions',
            },
        ),
        migrations.CreateModel(
            name='CmsActions',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('type', models.IntegerField(verbose_name='类型')),
                ('dest_activity', models.CharField(max_length=256, blank=True, null=True)),
                ('dest_url', models.CharField(max_length=256, blank=True, null=True)),
                ('dest_title', models.CharField(verbose_name='动作标题', max_length=256, blank=True, null=True)),
                ('cp_info', models.CharField(verbose_name='商家信息', max_length=2048, blank=True, null=True)),
                ('action_params', models.CharField(max_length=2048, blank=True, null=True)),
                ('memo', models.CharField(verbose_name='备注', max_length=256, blank=True, null=True)),
                ('pt_h5', models.IntegerField(verbose_name='是否为葡萄提供的H5页面')),
            ],
            options={
                'ordering': ['-id'],
                'managed': False,
                'db_table': 'cms_actions',
            },
        ),
        migrations.CreateModel(
            name='CmsActivities',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('url', models.CharField(max_length=256)),
                ('height', models.SmallIntegerField(verbose_name='高度')),
                ('location', models.IntegerField(verbose_name='排序')),
                ('start', models.IntegerField(verbose_name='起始时间')),
                ('end', models.IntegerField(verbose_name='结束时间')),
                ('strategy', models.IntegerField(verbose_name='', default=0, blank=True, null=True)),
                ('valid_time', models.CharField(verbose_name='有效时间', max_length=256, blank=True, null=True)),
                ('city', models.TextField(verbose_name='城市', blank=True, null=True)),
                ('scene_id', models.IntegerField(verbose_name='场景')),
                ('open_cp_id', models.IntegerField(verbose_name='', default=0)),
                ('open_service_id', models.IntegerField(verbose_name='', default=0)),
                ('open_goods_id', models.IntegerField(verbose_name='', default=0)),
                ('open_type', models.IntegerField(verbose_name='类别')),
            ],
            options={
                'managed': False,
                'db_table': 'cms_activities',
            },
        ),
        migrations.CreateModel(
            name='CmsActivityCP',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
            ],
            options={
                'managed': False,
                'db_table': 'cms_activity_cp',
            },
        ),
        migrations.CreateModel(
            name='CmsActivityGoods',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
            ],
            options={
                'managed': False,
                'db_table': 'cms_activity_goods',
            },
        ),
        migrations.CreateModel(
            name='CmsActivityV37',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('name', models.CharField(verbose_name='活动名称', max_length=256)),
                ('action_id', models.IntegerField(verbose_name='动作')),
                ('icon', models.CharField(verbose_name='图片', max_length=256)),
                ('priority', models.IntegerField(verbose_name='优先级')),
                ('valid_time', models.CharField(verbose_name='有效时间', max_length=256)),
                ('city', models.TextField(verbose_name='城市')),
                ('parent_id', models.IntegerField(verbose_name='原始活动ID', default=0)),
            ],
            options={
                'managed': False,
                'db_table': 'cms_activity_v37',
            },
        ),
        migrations.CreateModel(
            name='CmsAdbeans',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('img_url', models.CharField(verbose_name='图片', max_length=256)),
                ('start', models.IntegerField(verbose_name='起始时间')),
                ('end', models.IntegerField(verbose_name='结束时间')),
                ('location', models.IntegerField(verbose_name='排序')),
                ('action_id', models.IntegerField(verbose_name='动作')),
                ('strategy', models.IntegerField(verbose_name='', default=0, blank=True, null=True)),
                ('valid_time', models.CharField(verbose_name='有效时间', max_length=256, blank=True, null=True)),
                ('city', models.TextField(verbose_name='城市', blank=True, null=True)),
                ('open_cp_id', models.IntegerField(verbose_name='', default=0)),
                ('open_service_id', models.IntegerField(verbose_name='', default=0)),
                ('open_goods_id', models.IntegerField(verbose_name='', default=0)),
                ('open_type', models.IntegerField(verbose_name='类别')),
                ('action_json', models.TextField(blank=True, null=True)),
                ('name', models.CharField(verbose_name='广告名称', max_length=200)),
                ('phone_type', models.CharField(verbose_name='机型', max_length=200, blank=True, null=True)),
            ],
            options={
                'ordering': ['location'],
                'managed': False,
                'db_table': 'cms_adbeans',
            },
        ),
        migrations.CreateModel(
            name='CmsAds',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('location', models.IntegerField(verbose_name='排序')),
                ('size', models.IntegerField(verbose_name='篇幅')),
                ('type', models.IntegerField(verbose_name='类型')),
                ('scene_id', models.IntegerField(verbose_name='场景')),
            ],
            options={
                'ordering': ['scene_id', 'location'],
                'managed': False,
                'db_table': 'cms_ads',
            },
        ),
        migrations.CreateModel(
            name='CmsAdsBeans',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
            ],
            options={
                'managed': False,
                'db_table': 'cms_ads_beans',
            },
        ),
        migrations.CreateModel(
            name='CmsCategoryGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('name', models.CharField(verbose_name='名称', max_length=256)),
                ('location', models.IntegerField(verbose_name='排序')),
                ('memo', models.CharField(verbose_name='备注', max_length=256, blank=True, null=True)),
                ('valid_time', models.CharField(verbose_name='有效时间', max_length=256)),
                ('city', models.TextField(verbose_name='城市')),
            ],
            options={
                'managed': False,
                'db_table': 'cms_category_group',
            },
        ),
        migrations.CreateModel(
            name='CmsCategoryItem',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('name', models.CharField(verbose_name='二级分类标题', max_length=256, blank=True, null=True)),
                ('name_color', models.CharField(verbose_name='标题颜色', max_length=256)),
                ('sort', models.IntegerField(verbose_name='排序')),
                ('category_id', models.IntegerField(verbose_name='分类id')),
                ('scene_id', models.IntegerField(verbose_name='场景')),
            ],
            options={
                'managed': False,
                'db_table': 'cms_category_item',
            },
        ),
        migrations.CreateModel(
            name='CmsCategoryItembean',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('item_id', models.CharField(verbose_name='ID', max_length=256)),
                ('name', models.CharField(verbose_name='商家名称', max_length=256)),
                ('icon', models.CharField(verbose_name='头像', max_length=256)),
                ('sort', models.IntegerField(verbose_name='搜索词')),
                ('target_activity', models.CharField(max_length=1024, blank=True, null=True)),
                ('target_params', models.TextField(blank=True, null=True)),
                ('content', models.TextField(blank=True, null=True)),
                ('remind_code', models.IntegerField()),
                ('key_tag', models.CharField(max_length=256, blank=True, null=True)),
                ('search_sort', models.IntegerField(verbose_name='搜索分类')),
                ('description', models.CharField(verbose_name='描述', max_length=1024, blank=True, null=True)),
                ('dot_info', models.TextField(verbose_name='打点信息', blank=True, null=True)),
                ('strategy', models.IntegerField(verbose_name='', default=0)),
                ('city', models.TextField(verbose_name='城市')),
                ('valid_time', models.CharField(verbose_name='有效时间', max_length=256)),
                ('parent_id', models.IntegerField(verbose_name='', default=-1, blank=True, null=True)),
            ],
            options={
                'ordering': ['-id'],
                'managed': False,
                'db_table': 'cms_category_itembean',
            },
        ),
        migrations.CreateModel(
            name='CmsCategoryitemItembean',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
            ],
            options={
                'managed': False,
                'db_table': 'cms_categoryitem_itembean',
            },
        ),
        migrations.CreateModel(
            name='CmsChannelChannel',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('channel_id1', models.IntegerField(verbose_name='源渠道')),
                ('channel_id2', models.IntegerField(verbose_name='目标渠道')),
                ('config_items', models.CharField(verbose_name='项', max_length=128, blank=True, null=True)),
                ('op_type', models.IntegerField(verbose_name='类型', default=0, blank=True, null=True)),
            ],
            options={
                'managed': False,
                'db_table': 'cms_channel_channel',
            },
        ),
        migrations.CreateModel(
            name='CmsChannelJpush',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('channel_no', models.CharField(max_length=256, blank=True, null=True)),
                ('channel_name', models.CharField(max_length=256, blank=True, null=True)),
                ('app_key', models.CharField(max_length=500, blank=True, null=True)),
                ('master_secret', models.CharField(max_length=500, blank=True, null=True)),
            ],
            options={
                'managed': False,
                'db_table': 'cms_channel_jpush',
            },
        ),
        migrations.CreateModel(
            name='CmsChannels',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('channel_no', models.CharField(verbose_name='渠道号', max_length=256)),
                ('order', models.IntegerField(verbose_name='是否默认')),
                ('user_id', models.CharField(verbose_name='', max_length=256)),
            ],
            options={
                'ordering': ['channel_no'],
                'managed': False,
                'db_table': 'cms_channels',
            },
        ),
        migrations.CreateModel(
            name='CmsChannelsAppVersion',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('app_version', models.CharField(verbose_name='版本名称', max_length=64)),
                ('type_id', models.IntegerField(verbose_name='应用名称')),
            ],
            options={
                'ordering': ['-app_version'],
                'managed': False,
                'db_table': 'cms_channels_app_version',
            },
        ),
        migrations.CreateModel(
            name='CmsChannelsType',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('name', models.CharField(verbose_name='应用名称', max_length=256, blank=True, null=True)),
            ],
            options={
                'managed': False,
                'db_table': 'cms_channels_type',
            },
        ),
        migrations.CreateModel(
            name='CmsCheck',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('channel_id', models.IntegerField(default=0)),
                ('module', models.CharField(max_length=100, blank=True, null=True)),
                ('submit_person', models.CharField(max_length=100, blank=True, null=True)),
                ('submit_date', models.DateTimeField(blank=True, null=True)),
                ('check_person', models.CharField(max_length=100, blank=True, null=True)),
                ('check_date', models.DateTimeField(blank=True, null=True)),
                ('table_name', models.CharField(max_length=256)),
                ('data_id', models.IntegerField()),
                ('op_type', models.IntegerField(blank=True, null=True)),
                ('status', models.IntegerField(default=1, blank=True, null=True)),
                ('is_show', models.IntegerField(default=1, blank=True, null=True)),
                ('remark', models.CharField(max_length=1024, blank=True, null=True)),
                ('alter_person', models.CharField(max_length=100, blank=True, null=True)),
                ('alter_date', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'managed': False,
                'db_table': 'cms_check',
            },
        ),
        migrations.CreateModel(
            name='CmsCheckHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('status', models.CharField(max_length=45)),
                ('check_person', models.CharField(max_length=100)),
                ('check_date', models.CharField(max_length=45)),
                ('type', models.CharField(max_length=1024)),
                ('version', models.CharField(max_length=1024)),
                ('channel_no', models.CharField(max_length=1024)),
                ('module', models.CharField(max_length=45)),
                ('submit_person', models.CharField(max_length=100)),
                ('submit_date', models.CharField(max_length=45)),
                ('content', models.TextField()),
            ],
            options={
                'ordering': ['-check_date'],
                'managed': False,
                'db_table': 'cms_check_history',
            },
        ),
        migrations.CreateModel(
            name='CmsChoicenessCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('img_url', models.CharField(verbose_name='图片', max_length=255, blank=True, null=True)),
                ('city', models.TextField(verbose_name='城市', blank=True, null=True)),
                ('strategy', models.IntegerField(verbose_name='', default=0, blank=True, null=True)),
                ('status', models.IntegerField(verbose_name='', default=0)),
                ('valid_time', models.CharField(verbose_name='有效时间', max_length=45, blank=True, null=True)),
                ('img_url_d', models.CharField(verbose_name='按下时图片', max_length=255, blank=True, null=True)),
                ('background_color', models.CharField(verbose_name='背景颜色', max_length=45, blank=True, null=True)),
                ('location', models.IntegerField(verbose_name='排序', blank=True, null=True)),
            ],
            options={
                'managed': False,
                'db_table': 'cms_choiceness_category',
            },
        ),
        migrations.CreateModel(
            name='CmsCoupon',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('coupon_id', models.IntegerField(verbose_name='优惠券ID')),
                ('name', models.CharField(verbose_name='优惠券名称', max_length=256)),
                ('url', models.CharField(verbose_name='图片', max_length=256)),
                ('height', models.SmallIntegerField(verbose_name='高度')),
                ('location', models.IntegerField(verbose_name='排序')),
                ('start', models.IntegerField(verbose_name='起始时间')),
                ('end', models.IntegerField(verbose_name='结束时间')),
                ('strategy', models.IntegerField(verbose_name='', default=0, blank=True, null=True)),
                ('valid_time', models.CharField(verbose_name='有效时间', max_length=256, blank=True, null=True)),
                ('city', models.TextField(verbose_name='城市', blank=True, null=True)),
                ('scene_id', models.IntegerField(verbose_name='场景')),
                ('open_cp_id', models.IntegerField(verbose_name='', default=0)),
                ('open_service_id', models.IntegerField(verbose_name='', default=0)),
                ('open_goods_id', models.CharField(verbose_name='', max_length=255, default=0)),
                ('open_coupon_id', models.IntegerField(verbose_name='', default=0)),
                ('parent_id', models.IntegerField(verbose_name='', default=-1)),
                ('mobile', models.CharField(verbose_name='', max_length=256, blank=True, null=True)),
            ],
            options={
                'ordering': ['-id'],
                'managed': False,
                'db_table': 'cms_coupon',
            },
        ),
        migrations.CreateModel(
            name='CmsCP',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('name', models.CharField(verbose_name='品牌名', max_length=256)),
                ('name_style', models.CharField(verbose_name='名称颜色', max_length=256)),
                ('icon', models.CharField(verbose_name='图片', max_length=256)),
                ('adver_icon', models.CharField(verbose_name='宣传图', max_length=256)),
                ('location1', models.IntegerField(verbose_name='首页排序')),
                ('location2', models.IntegerField(verbose_name='品牌页排序')),
                ('mark', models.CharField(verbose_name='运营标签', max_length=256, blank=True, null=True)),
                ('desc', models.CharField(verbose_name='描述', max_length=256, blank=True, null=True)),
                ('desc_style', models.CharField(verbose_name='描述颜色', max_length=256, blank=True, null=True)),
                ('action_id', models.IntegerField(verbose_name='动作')),
                ('action_json', models.TextField(blank=True, null=True)),
                ('search_keyword', models.TextField(verbose_name='搜索关键词', blank=True, null=True)),
                ('service_time', models.IntegerField(verbose_name='服务时间')),
                ('flagship', models.IntegerField(verbose_name='是否旗舰店')),
                ('company_name', models.CharField(verbose_name='企业名称', max_length=256)),
                ('certified_company', models.IntegerField(verbose_name='是否认证企业')),
                ('valid_time', models.CharField(verbose_name='有效时间', max_length=256)),
                ('city', models.TextField(verbose_name='城市')),
            ],
            options={
                'ordering': ['-id'],
                'managed': False,
                'db_table': 'cms_cp',
            },
        ),
        migrations.CreateModel(
            name='CmsCPCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('name', models.CharField(verbose_name='分类名', max_length=256)),
                ('location', models.IntegerField(verbose_name='排序')),
            ],
            options={
                'ordering': ['-id'],
                'managed': False,
                'db_table': 'cms_cp_category',
            },
        ),
        migrations.CreateModel(
            name='CmsCpinfo',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=256, blank=True, null=True)),
                ('icon', models.CharField(max_length=256)),
            ],
            options={
                'managed': False,
                'db_table': 'cms_cpinfo',
            },
        ),
        migrations.CreateModel(
            name='CmsGoods',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('goods_id', models.IntegerField(verbose_name='商品ID')),
                ('title', models.CharField(verbose_name='标题', max_length=256)),
                ('title_style', models.CharField(verbose_name='标题颜色', max_length=256, default='#000000')),
                ('name', models.CharField(verbose_name='商品名称', max_length=256)),
                ('name_style', models.CharField(verbose_name='商品名称颜色', max_length=256, default='#000000')),
                ('desc', models.CharField(verbose_name='描述', max_length=2048, blank=True, null=True)),
                ('desc_style', models.CharField(verbose_name='描述颜色', max_length=256, blank=True, null=True)),
                ('search_keyword', models.CharField(verbose_name='搜索关键词', max_length=1024)),
                ('small_icon_url', models.CharField(verbose_name='小图标', max_length=1024)),
                ('icon_url', models.CharField(verbose_name='大图标', max_length=1024)),
                ('location', models.IntegerField(verbose_name='排序', default=0)),
                ('action_id', models.IntegerField(verbose_name='动作')),
                ('dot_info', models.CharField(verbose_name='打点信息', max_length=2048, blank=True, null=True)),
                ('strategy', models.IntegerField(verbose_name='', default=0, blank=True, null=True)),
                ('valid_time', models.CharField(verbose_name='有效时间', max_length=256, default='* * * * *', blank=True, null=True)),
                ('city', models.CharField(verbose_name='城市', max_length=256, default='*', blank=True, null=True)),
                ('memo', models.CharField(verbose_name='备注', max_length=256, blank=True, null=True)),
                ('scene_id', models.IntegerField(verbose_name='场景', default=0)),
                ('parent_id', models.IntegerField(verbose_name='', default=-1)),
                ('open_cp_id', models.IntegerField(verbose_name='')),
                ('open_service_id', models.IntegerField(verbose_name='')),
                ('source_id', models.CharField(verbose_name='', max_length=256, blank=True, null=True)),
                ('action_json', models.TextField(blank=True, null=True)),
                ('fav_price', models.DecimalField(verbose_name='商品现价', max_digits=10, blank=True, null=True, decimal_places=2, default='0.00')),
                ('fav_price_style', models.CharField(verbose_name='商品现价颜色', max_length=256, default='#000000', blank=True, null=True)),
                ('price', models.DecimalField(verbose_name='商品原价', max_digits=10, blank=True, null=True, decimal_places=2, default='0.00')),
                ('num', models.IntegerField(verbose_name='商品数量', default=0, blank=True, null=True)),
                ('sold', models.IntegerField(verbose_name='已售数量', default=-1, blank=True, null=True)),
                ('latitude', models.FloatField(verbose_name='', default=0, blank=True, null=True)),
                ('longitude', models.FloatField(verbose_name='', default=0, blank=True, null=True)),
                ('mobile', models.CharField(verbose_name='', max_length=2048, blank=True, editable=False, null=True)),
                ('fav_price_desc', models.CharField(verbose_name='商品现价描述', max_length=256, blank=True, null=True)),
                ('fav_price_desc_style', models.CharField(verbose_name='商品现价描述颜色', max_length=256)),
                ('from_op', models.IntegerField(verbose_name='是否来自开放平台', default=0)),
                ('category', models.IntegerField(verbose_name='分类', blank=True, null=True)),
                ('second_category', models.IntegerField(verbose_name='二级分类', blank=True, null=True)),
                ('cp_name', models.CharField(verbose_name='商家名称', max_length=64, blank=True, null=True)),
            ],
            options={
                'ordering': ['-id'],
                'managed': False,
                'db_table': 'cms_goods',
            },
        ),
        migrations.CreateModel(
            name='CmsHomeCP',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
            ],
            options={
                'managed': False,
                'db_table': 'cms_home_cp',
            },
        ),
        migrations.CreateModel(
            name='CmsLikes',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('title', models.CharField(verbose_name='猜你喜欢标题', max_length=256)),
                ('desc', models.CharField(verbose_name='描述', max_length=2048)),
                ('title_style', models.CharField(verbose_name='标题颜色', max_length=256, blank=True, null=True)),
                ('desc_style', models.CharField(verbose_name='描述颜色', max_length=256, blank=True, null=True)),
                ('scene_id', models.IntegerField(verbose_name='场景')),
            ],
            options={
                'managed': False,
                'db_table': 'cms_likes',
            },
        ),
        migrations.CreateModel(
            name='CmsLikesGoods',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
            ],
            options={
                'managed': False,
                'db_table': 'cms_likes_goods',
            },
        ),
        migrations.CreateModel(
            name='CmsLikesServices',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
            ],
            options={
                'managed': False,
                'db_table': 'cms_likes_services',
            },
        ),
        migrations.CreateModel(
            name='CmsNativeActivity',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('title', models.CharField(verbose_name='Native活动标题', max_length=256)),
                ('title_color', models.CharField(verbose_name='标题颜色', max_length=256)),
                ('subtitle', models.CharField(verbose_name='副标题', max_length=256)),
                ('image_url', models.CharField(verbose_name='图片', max_length=256)),
                ('start_time', models.IntegerField(verbose_name='开始时间')),
                ('end_time', models.IntegerField(verbose_name='结束时间')),
                ('sort', models.IntegerField(verbose_name='排序')),
                ('action_id', models.IntegerField(verbose_name='动作')),
                ('strategy', models.IntegerField(verbose_name='', default=0, blank=True, null=True)),
                ('valid_time', models.CharField(verbose_name='有效时间', max_length=256)),
                ('city', models.TextField(verbose_name='城市')),
                ('scene_id', models.IntegerField(verbose_name='场景')),
                ('open_cp_id', models.IntegerField(verbose_name='', default=0)),
                ('open_service_id', models.IntegerField(verbose_name='', default=0)),
                ('open_goods_id', models.IntegerField(verbose_name='', default=0)),
                ('open_type', models.IntegerField(verbose_name='类别')),
                ('action_json', models.TextField(blank=True, null=True)),
                ('open_time', models.IntegerField(verbose_name='活动倒计时开始时间', blank=True, null=True)),
                ('close_time', models.IntegerField(verbose_name='活动倒计时结束时间', blank=True, null=True)),
            ],
            options={
                'managed': False,
                'db_table': 'cms_native_activity',
            },
        ),
        migrations.CreateModel(
            name='CmsNavicategories',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('name_style', models.CharField(verbose_name='颜色', max_length=256)),
                ('location', models.IntegerField(verbose_name='排序')),
                ('scene_id', models.IntegerField(verbose_name='场景')),
                ('dot_info', models.CharField(verbose_name='打点信息', max_length=2048, blank=True, null=True)),
            ],
            options={
                'managed': False,
                'db_table': 'cms_navicategories',
            },
        ),
        migrations.CreateModel(
            name='CmsNavicatesCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
            ],
            options={
                'managed': False,
                'db_table': 'cms_navicates_category',
            },
        ),
        migrations.CreateModel(
            name='CmsNavicatesGoods',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
            ],
            options={
                'managed': False,
                'db_table': 'cms_navicates_goods',
            },
        ),
        migrations.CreateModel(
            name='CmsNavicatesServices',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
            ],
            options={
                'managed': False,
                'db_table': 'cms_navicates_services',
            },
        ),
        migrations.CreateModel(
            name='CmsOpconfig',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('key', models.CharField(max_length=128)),
                ('value', models.CharField(max_length=1024)),
            ],
            options={
                'managed': False,
                'db_table': 'cms_opconfig',
            },
        ),
        migrations.CreateModel(
            name='CmsOpenChannel',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=64)),
            ],
            options={
                'managed': False,
                'db_table': 'cms_open_channel',
            },
        ),
        migrations.CreateModel(
            name='CmsOpenService',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('show_name', models.CharField(max_length=256, blank=True, null=True)),
                ('icon', models.CharField(max_length=256)),
                ('city', models.CharField(max_length=256)),
                ('distribute', models.IntegerField()),
            ],
            options={
                'managed': False,
                'db_table': 'cms_open_service',
            },
        ),
        migrations.CreateModel(
            name='CmsOpenVersion',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=64)),
            ],
            options={
                'managed': False,
                'db_table': 'cms_open_version',
            },
        ),
        migrations.CreateModel(
            name='CmsScreenads',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('name', models.CharField(verbose_name='开屏广告名称', max_length=200, blank=True, null=True)),
                ('img_url', models.CharField(verbose_name='图片', max_length=256)),
                ('start', models.IntegerField(verbose_name='起始时间')),
                ('end', models.IntegerField(verbose_name='结束时间')),
                ('location', models.IntegerField(verbose_name='排序', default=-1)),
                ('action_id', models.IntegerField(verbose_name='动作')),
                ('strategy', models.IntegerField(verbose_name='', default=0, blank=True, null=True)),
                ('valid_time', models.CharField(verbose_name='有效时间', max_length=256, blank=True, null=True)),
                ('city', models.TextField(verbose_name='城市', blank=True, null=True)),
                ('open_cp_id', models.IntegerField(verbose_name='', default=0)),
                ('open_service_id', models.IntegerField(verbose_name='', default=0)),
                ('open_goods_id', models.IntegerField(verbose_name='', default=0)),
                ('open_type', models.IntegerField(verbose_name='类别', default=0)),
                ('action_json', models.TextField(blank=True, null=True)),
                ('phone_type', models.CharField(verbose_name='机型', max_length=200, blank=True, null=True)),
                ('show_times', models.IntegerField(verbose_name='展示次数', blank=True, null=True)),
                ('show_hold', models.IntegerField(verbose_name='展示时长', blank=True, null=True)),
            ],
            options={
                'managed': False,
                'db_table': 'cms_screenads',
            },
        ),
        migrations.CreateModel(
            name='CmsServices',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('srv_id', models.IntegerField()),
                ('name', models.CharField(verbose_name='服务名称', max_length=256)),
                ('name_style', models.CharField(verbose_name='名称颜色', max_length=256)),
                ('desc', models.CharField(verbose_name='描述', max_length=2048, blank=True, null=True)),
                ('desc_style', models.CharField(verbose_name='描述颜色', max_length=256, blank=True, null=True)),
                ('search_keyword', models.CharField(verbose_name='搜索关键词', max_length=1024)),
                ('small_icon_url', models.CharField(verbose_name='小图标', max_length=1024)),
                ('icon_url', models.CharField(verbose_name='大图标', max_length=1024)),
                ('location', models.IntegerField(verbose_name='排序')),
                ('action_id', models.IntegerField(verbose_name='动作')),
                ('dot_info', models.CharField(verbose_name='打点信息', max_length=2048, blank=True, null=True)),
                ('strategy', models.IntegerField(verbose_name='', default=0, blank=True, null=True)),
                ('valid_time', models.CharField(verbose_name='有效时间', max_length=256, blank=True, null=True)),
                ('city', models.TextField(verbose_name='城市', blank=True, null=True)),
                ('memo', models.CharField(verbose_name='备注', max_length=256, blank=True, null=True)),
                ('type', models.IntegerField(verbose_name='', blank=True, null=True)),
                ('scene_id', models.IntegerField(verbose_name='场景')),
                ('parent_id', models.IntegerField(verbose_name='')),
                ('open_cp_id', models.IntegerField(verbose_name='')),
                ('open_service_id', models.IntegerField(verbose_name='')),
                ('open_goods_id', models.IntegerField(verbose_name='')),
                ('source_id', models.CharField(verbose_name='', max_length=256, blank=True, null=True)),
                ('action_json', models.TextField(blank=True, null=True)),
                ('mobile', models.CharField(verbose_name='', max_length=256, blank=True, null=True)),
            ],
            options={
                'ordering': ['scene_id', 'location'],
                'managed': False,
                'db_table': 'cms_services',
            },
        ),
        migrations.CreateModel(
            name='CmsSpecialTopic',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('title', models.CharField(verbose_name='专题标题', max_length=256)),
                ('title_color', models.CharField(verbose_name='标题颜色', max_length=256)),
                ('subtitle', models.CharField(verbose_name='副标题', max_length=256)),
                ('subtitle_color', models.CharField(verbose_name='副标题颜色', max_length=256)),
                ('image_url', models.CharField(verbose_name='图片', max_length=2048)),
                ('action_id', models.IntegerField(verbose_name='动作')),
                ('strategy', models.IntegerField(verbose_name='', default=0)),
                ('valid_time', models.CharField(verbose_name='有效时间', max_length=256)),
                ('city', models.TextField(verbose_name='城市')),
                ('scene_id', models.IntegerField(verbose_name='场景')),
                ('open_cp_id', models.IntegerField(verbose_name='')),
                ('open_service_id', models.IntegerField(verbose_name='')),
                ('open_goods_id', models.IntegerField(verbose_name='')),
                ('open_type', models.IntegerField(verbose_name='类别')),
                ('create_time', models.DateTimeField(verbose_name='', blank=True, null=True)),
                ('update_time', models.DateTimeField(verbose_name='')),
            ],
            options={
                'ordering': ['-id'],
                'managed': False,
                'db_table': 'cms_special_topic',
            },
        ),
        migrations.CreateModel(
            name='CmsStreamcontent',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('type', models.IntegerField(verbose_name='类别')),
                ('location', models.IntegerField(verbose_name='排序')),
                ('scene_id', models.IntegerField(verbose_name='场景')),
            ],
            options={
                'managed': False,
                'db_table': 'cms_streamcontent',
            },
        ),
        migrations.CreateModel(
            name='CmsStreamcontentbeans',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('location', models.IntegerField(verbose_name='排序')),
                ('img_url', models.CharField(verbose_name='图标', max_length=256)),
                ('title', models.CharField(verbose_name='内容流标题', max_length=256)),
                ('title_style', models.CharField(verbose_name='标题颜色', max_length=256)),
                ('descibe', models.CharField(verbose_name='描述', max_length=2048)),
                ('descibe_style', models.CharField(verbose_name='描述颜色', max_length=256)),
                ('name', models.CharField(verbose_name='商品名称', max_length=256, blank=True, null=True)),
                ('name_style', models.CharField(verbose_name='商品名称颜色', max_length=256)),
                ('price', models.FloatField(verbose_name='商品现价')),
                ('price_style', models.CharField(verbose_name='商品现价颜色', max_length=256, blank=True, null=True)),
                ('price_desc', models.CharField(verbose_name='商品现价描述', max_length=256, blank=True, null=True)),
                ('price_desc_style', models.CharField(verbose_name='商品现价描述颜色', max_length=256)),
                ('orig_price', models.FloatField(verbose_name='商品原价')),
                ('sold', models.IntegerField(verbose_name='已售数量', blank=True, null=True)),
                ('latitude', models.FloatField(verbose_name='')),
                ('longitude', models.FloatField(verbose_name='')),
                ('action_id', models.IntegerField(verbose_name='动作')),
                ('params', models.CharField(verbose_name='附加参数', max_length=2048)),
                ('strategy', models.IntegerField(verbose_name='', default=0, blank=True, null=True)),
                ('valid_time', models.CharField(verbose_name='有效时间', max_length=256, blank=True, null=True)),
                ('city', models.TextField(verbose_name='城市', blank=True, null=True)),
                ('open_cp_id', models.IntegerField(verbose_name='', default=0)),
                ('open_service_id', models.IntegerField(verbose_name='', default=0)),
                ('open_goods_id', models.IntegerField(verbose_name='', default=0)),
                ('open_type', models.IntegerField(verbose_name='类别')),
                ('action_json', models.TextField(blank=True, null=True)),
            ],
            options={
                'managed': False,
                'db_table': 'cms_streamcontentbeans',
            },
        ),
        migrations.CreateModel(
            name='CmsStreamcontentsBeans',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
            ],
            options={
                'managed': False,
                'db_table': 'cms_streamcontents_beans',
            },
        ),
        migrations.CreateModel(
            name='CmsStreamcontentsGoods',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
            ],
            options={
                'managed': False,
                'db_table': 'cms_streamcontents_goods',
            },
        ),
        migrations.CreateModel(
            name='CmsStreamCp',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
            ],
            options={
                'managed': False,
                'db_table': 'cms_stream_cp',
            },
        ),
        migrations.CreateModel(
            name='CmsViewActivity',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('status', models.IntegerField(default=0, blank=True, null=True)),
            ],
            options={
                'managed': False,
                'db_table': 'cms_view_activity',
            },
        ),
        migrations.CreateModel(
            name='CmsViewActivity37',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
            ],
            options={
                'managed': False,
                'db_table': 'cms_view_activity37',
            },
        ),
        migrations.CreateModel(
            name='CmsViewAd',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('status', models.IntegerField(default=0, blank=True, null=True)),
            ],
            options={
                'managed': False,
                'db_table': 'cms_view_ad',
            },
        ),
        migrations.CreateModel(
            name='CmsViewCategoryitem',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('status', models.IntegerField(default=0)),
            ],
            options={
                'managed': False,
                'db_table': 'cms_view_categoryitem',
            },
        ),
        migrations.CreateModel(
            name='CmsViewChannelGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
            ],
            options={
                'managed': False,
                'db_table': 'cms_view_channel_group',
            },
        ),
        migrations.CreateModel(
            name='CmsViewChoicenessCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('status', models.IntegerField(default=0, blank=True, null=True)),
            ],
            options={
                'managed': False,
                'db_table': 'cms_view_choiceness_category',
            },
        ),
        migrations.CreateModel(
            name='CmsViewCoupon',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('status', models.IntegerField(default=0, blank=True, null=True)),
            ],
            options={
                'managed': False,
                'db_table': 'cms_view_coupon',
            },
        ),
        migrations.CreateModel(
            name='CmsViewCP',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
            ],
            options={
                'managed': False,
                'db_table': 'cms_view_cp',
            },
        ),
        migrations.CreateModel(
            name='CmsViewFindTopic',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('topic_id', models.IntegerField(verbose_name='')),
                ('is_top', models.IntegerField(verbose_name='是否置顶', default=0, blank=True, null=True)),
                ('channel_id', models.IntegerField(verbose_name='')),
                ('status', models.IntegerField(verbose_name='', default=0)),
                ('update_time', models.DateTimeField(verbose_name='')),
                ('create_time', models.DateTimeField(verbose_name='', blank=True, null=True)),
                ('is_deleted', models.IntegerField(verbose_name='是否删除', default=0)),
                ('delete_time', models.DateTimeField(verbose_name='', blank=True, null=True)),
                ('mark_info', models.CharField(max_length=200, blank=True, null=True)),
            ],
            options={
                'managed': False,
                'db_table': 'cms_view_find_topic',
            },
        ),
        migrations.CreateModel(
            name='CmsViewGroupCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
            ],
            options={
                'managed': False,
                'db_table': 'cms_view_group_category',
            },
        ),
        migrations.CreateModel(
            name='CmsViewHomepageTopic',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('status', models.IntegerField(default=0)),
            ],
            options={
                'managed': False,
                'db_table': 'cms_view_homepage_topic',
            },
        ),
        migrations.CreateModel(
            name='CmsViewLike',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('status', models.IntegerField(default=0, blank=True, null=True)),
            ],
            options={
                'managed': False,
                'db_table': 'cms_view_like',
            },
        ),
        migrations.CreateModel(
            name='CmsViewNativeActivity',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('status', models.IntegerField(default=0)),
            ],
            options={
                'managed': False,
                'db_table': 'cms_view_native_activity',
            },
        ),
        migrations.CreateModel(
            name='CmsViewNavi',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('status', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'managed': False,
                'db_table': 'cms_view_navi',
            },
        ),
        migrations.CreateModel(
            name='CmsViewOpconfig',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('status', models.IntegerField(default=0, blank=True, null=True)),
            ],
            options={
                'managed': False,
                'db_table': 'cms_view_opconfig',
            },
        ),
        migrations.CreateModel(
            name='CmsViewOpenService',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
            ],
            options={
                'managed': False,
                'db_table': 'cms_view_open_service',
            },
        ),
        migrations.CreateModel(
            name='CmsViewPush',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('channel_id', models.IntegerField()),
                ('city', models.CharField(max_length=20, blank=True, null=True)),
                ('data_version', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'managed': False,
                'db_table': 'cms_view_push',
            },
        ),
        migrations.CreateModel(
            name='CmsViewScreenads',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('status', models.IntegerField(default=0, blank=True, null=True)),
            ],
            options={
                'managed': False,
                'db_table': 'cms_view_screenads',
            },
        ),
        migrations.CreateModel(
            name='CmsViewService',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('service_id', models.IntegerField(verbose_name='服务/商品/分类名称')),
                ('open_type', models.IntegerField()),
                ('status', models.IntegerField(default=0, blank=True, null=True)),
            ],
            options={
                'managed': False,
                'db_table': 'cms_view_service',
            },
        ),
        migrations.CreateModel(
            name='CmsViewStream',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('status', models.IntegerField(default=0, blank=True, null=True)),
            ],
            options={
                'managed': False,
                'db_table': 'cms_view_stream',
            },
        ),
        migrations.CreateModel(
            name='DjangoContentType',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('app_label', models.CharField(max_length=100)),
                ('model', models.CharField(max_length=100)),
            ],
            options={
                'managed': False,
                'db_table': 'django_content_type',
            },
        ),
        migrations.CreateModel(
            name='PtYellowCitylist',
            fields=[
                ('city_name', models.CharField(max_length=30, blank=True, null=True)),
                ('city_py', models.CharField(max_length=255, blank=True, null=True)),
                ('self_id', models.SmallIntegerField(serialize=False, primary_key=True)),
                ('parent_id', models.SmallIntegerField(blank=True, null=True)),
                ('city_type', models.IntegerField(blank=True, null=True)),
                ('district_code', models.CharField(max_length=10, blank=True, null=True)),
                ('city_hot', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'managed': False,
                'db_table': 'pt_yellow_citylist',
            },
        ),
        migrations.CreateModel(
            name='CmsImageInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('image_name', models.CharField(verbose_name='图片名称', max_length=200, unique=True)),
                ('image_category', models.CharField(verbose_name='图片分类', max_length=200)),
                ('image_sec_category', models.CharField(verbose_name='图片二级分类', max_length=200)),
                ('image_url', models.CharField(verbose_name='图片URL', max_length=200)),
                ('mark', models.CharField(verbose_name='备注', max_length=500)),
                ('deal_time', models.DateTimeField(verbose_name='上传时间', blank=True, null=True)),
            ],
            options={
                'ordering': ['-deal_time'],
                'db_table': 'cms_image_info',
            },
        ),
        migrations.CreateModel(
            name='CmsNaviCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('name', models.CharField(verbose_name='分类名称', max_length=255)),
                ('name_style', models.CharField(verbose_name='名称颜色', max_length=256)),
                ('fatherid', models.IntegerField(verbose_name='', db_column='fatherId')),
                ('search_keyword', models.TextField(verbose_name='搜索关键词', blank=True, null=True)),
                ('used_by_op', models.IntegerField(verbose_name='是否为开放平台使用', default=1)),
                ('desc', models.CharField(verbose_name='描述', max_length=256, blank=True, null=True)),
                ('desc_style', models.CharField(verbose_name='描述颜色', max_length=256)),
                ('small_icon_url', models.CharField(verbose_name='小图标', max_length=1024, blank=True, null=True)),
                ('icon_url', models.CharField(verbose_name='大图标', max_length=1024, blank=True, null=True)),
                ('location', models.IntegerField(verbose_name='排序')),
                ('action_id', models.IntegerField(verbose_name='动作')),
                ('dot_info', models.CharField(verbose_name='打点信息', max_length=2048, blank=True, null=True)),
                ('strategy', models.IntegerField(verbose_name='', default=0, blank=True, null=True)),
                ('valid_time', models.CharField(verbose_name='有效时间', max_length=256)),
                ('city', models.TextField(verbose_name='城市')),
                ('memo', models.CharField(verbose_name='备注', max_length=256, blank=True, null=True)),
                ('scene_id', models.IntegerField(verbose_name='场景')),
                ('parent_id', models.IntegerField(verbose_name='')),
                ('show_style', models.IntegerField(verbose_name='展现形式')),
                ('location2', models.IntegerField(verbose_name='首页排序')),
            ],
            options={
                'ordering': ['-id'],
                'managed': True,
                'db_table': 'cms_navi_category',
            },
        ),
        migrations.CreateModel(
            name='CmsScene',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=128)),
            ],
            options={
                'db_table': 'cms_scene',
            },
        ),
        migrations.CreateModel(
            name='PtCityCityGroups',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('city', models.ForeignKey(to='main.PtYellowCitylist')),
            ],
            options={
                'db_table': 'pt_city_city_groups',
            },
        ),
        migrations.CreateModel(
            name='PtCityGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('name', models.CharField(verbose_name='城市分组名称', max_length=80, unique=True)),
                ('remark', models.CharField(verbose_name='备注', max_length=256, blank=True, null=True)),
            ],
            options={
                'ordering': ['-id'],
                'db_table': 'pt_city_group',
            },
        ),
        migrations.AddField(
            model_name='ptcitycitygroups',
            name='group',
            field=models.ForeignKey(to='main.PtCityGroup'),
        ),
        migrations.AlterUniqueTogether(
            name='ptcitycitygroups',
            unique_together=set([('city', 'group')]),
        ),
    ]
