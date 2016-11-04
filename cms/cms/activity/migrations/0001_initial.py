# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-23 11:14
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='\u540d\u79f0')),
                ('remark', models.CharField(blank=True, max_length=255, null=True, verbose_name='\u63cf\u8ff0')),
                ('start_time', models.DateTimeField(blank=True, default=datetime.datetime.now, verbose_name='\u5f00\u59cb\u65f6\u95f4')),
                ('end_time', models.DateTimeField(blank=True, default=datetime.datetime.now, verbose_name='\u7ed3\u675f\u65f6\u95f4')),
                ('type', models.IntegerField(verbose_name='\u7c7b\u578b')),
                ('c_time', models.DateTimeField(blank=True, null=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('m_time', models.DateTimeField(blank=True, null=True, verbose_name='\u4fee\u6539\u65f6\u95f4')),
                ('c_user', models.CharField(blank=True, max_length=50, null=True, verbose_name='\u521b\u5efa\u4eba')),
                ('m_user', models.CharField(blank=True, max_length=50, null=True, verbose_name='\u4fee\u6539\u4eba')),
                ('provider', models.CharField(blank=True, max_length=100, null=True, verbose_name='\u6d3b\u52a8\u63d0\u4f9b\u65b9')),
            ],
            options={
                'db_table': 'activity',
            },
        ),
        migrations.CreateModel(
            name='ActivityGiftRule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gift_name', models.CharField(blank=True, max_length=50, null=True, verbose_name='\u793c\u54c1\u540d\u79f0')),
                ('is_entity', models.IntegerField(blank=True, null=True, verbose_name='\u662f\u5426\u5b9e\u7269\u793c\u54c1')),
                ('entity_id', models.BigIntegerField(blank=True, null=True, verbose_name='\u5b9e\u7269\u793c\u54c1id')),
                ('is_need_consume', models.IntegerField(blank=True, null=True, verbose_name='\u662f\u5426\u6d88\u8d39')),
                ('consume_type', models.IntegerField(blank=True, null=True, verbose_name='\u6d88\u8d39\u7c7b\u578b')),
                ('min_consume', models.IntegerField(blank=True, null=True, verbose_name='\u6d88\u8d39\u4e0b\u9650')),
                ('max_consume', models.IntegerField(blank=True, null=True, verbose_name='\u6d88\u8d39\u4e0a\u9650')),
                ('start_time', models.DateTimeField(blank=True, null=True, verbose_name='\u793c\u54c1\u91ca\u653e\u65f6\u95f4')),
                ('is_combine_pkg', models.IntegerField(blank=True, null=True, verbose_name='\u662f\u5426\u7ec4\u5408\u793c\u54c1')),
                ('lottery_rule', models.CharField(blank=True, max_length=255, null=True, verbose_name='\u7ec4\u5408\u793c\u54c1id\u548c\u6bd4\u7387')),
                ('gift_description', models.CharField(blank=True, max_length=255, null=True, verbose_name='\u793c\u54c1\u63cf\u8ff0')),
                ('daily_amount_limit', models.IntegerField(blank=True, null=True, verbose_name='\u793c\u54c1\u5355\u65e5\u53d1\u653e\u4e0a\u7ebf')),
                ('max_amount', models.IntegerField(blank=True, null=True, verbose_name='\u793c\u54c1\u4e0a\u9650')),
                ('ratio', models.IntegerField(blank=True, null=True, verbose_name='\u767e\u5206\u6bd4')),
                ('activity_id', models.BigIntegerField(blank=True, null=True, verbose_name='\u6d3b\u52a8id')),
                ('extends_col', models.TextField(blank=True, null=True, verbose_name='\u6269\u5c55json\u4e32')),
            ],
            options={
                'db_table': 'activity_gift_rule',
            },
        ),
        migrations.CreateModel(
            name='ActivityJoinRule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activity_id', models.BigIntegerField(verbose_name='\u89c4\u5219\u5173\u8054\u7684\u6d3b\u52a8id')),
                ('is_need_login', models.IntegerField(verbose_name='\u6d3b\u52a8\u662f\u5426\u9700\u8981\u767b\u5f55')),
                ('default_times', models.IntegerField(verbose_name='\u9ed8\u8ba4\u53c2\u4e0e\u6b21\u6570')),
                ('daily_times', models.IntegerField(verbose_name='\u5355\u65e5\u53c2\u4e0e\u6b21\u6570\u9650\u5236')),
                ('personal_times', models.IntegerField(verbose_name='\u5355\u4eba\u53c2\u6570\u6b21\u6570\u9650\u5236')),
                ('total_num', models.IntegerField(verbose_name='\u6d3b\u52a8\u53c2\u4e0e\u603b\u540d\u989d\u9650\u5236')),
                ('is_need_consume', models.IntegerField(verbose_name='\u662f\u5426\u9700\u8981\u6d88\u8d39')),
                ('consume_type', models.IntegerField(verbose_name='\u6d88\u8d39\u7684\u4ea7\u54c1\u7684\u7c7b\u578b')),
                ('min_consume', models.IntegerField(verbose_name='\u6700\u4f4e\u6d88\u8d39\u989d')),
                ('gifts', models.CharField(blank=True, max_length=255, null=True, verbose_name='\u793c\u54c1\u4e32')),
                ('extends_col', models.TextField(blank=True, null=True, verbose_name='\u9884\u7559\u6269\u5c55json\u4e32')),
            ],
            options={
                'db_table': 'activity_join_rule',
            },
        ),
        migrations.CreateModel(
            name='ActivityLotteryRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activity_id', models.BigIntegerField(verbose_name='\u6d3b\u52a8id')),
                ('resource_id', models.BigIntegerField(verbose_name='\u8d44\u6e90id')),
                ('resource_type', models.IntegerField(verbose_name='\u83b7\u5f97\u7684\u8d44\u6e90\u7c7b\u578b')),
                ('c_time', models.DateTimeField(blank=True, null=True, verbose_name='\u83b7\u53d6\u65f6\u95f4')),
                ('uid', models.CharField(max_length=50, verbose_name='\u4e2d\u5956\u7684\u7528\u6237')),
                ('mobile', models.CharField(blank=True, max_length=11, null=True, verbose_name='\u624b\u673a\u53f7')),
                ('remark', models.CharField(max_length=100, verbose_name='\u4e2d\u5956\u63cf\u8ff0')),
            ],
            options={
                'db_table': 'activity_lottery_record',
            },
        ),
        migrations.CreateModel(
            name='CouponAllot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cid', models.BigIntegerField(verbose_name='\u5238id')),
                ('uid', models.CharField(max_length=50, verbose_name='\u7528\u6237id')),
                ('allot_time', models.DateTimeField(auto_now_add=True, verbose_name='\u9886\u53d6\u65f6\u95f4')),
                ('status', models.IntegerField(default=0, verbose_name='\u4f7f\u7528\u72b6\u6001')),
                ('consume_time', models.DateTimeField(blank=True, null=True, verbose_name='\u4f7f\u7528\u65f6\u95f4')),
                ('m_time', models.DateTimeField(auto_now_add=True, null=True, verbose_name='\u4fee\u6539\u65f6\u95f4')),
                ('activity_id', models.BigIntegerField(blank=True, null=True, verbose_name='\u6d3b\u52a8id')),
                ('exchange_code_id', models.BigIntegerField(blank=True, null=True, verbose_name='\u5151\u6362\u7801id')),
                ('name', models.CharField(blank=True, max_length=50, null=True, verbose_name='\u5238\u5c55\u793a\u540d\u79f0')),
                ('reason', models.CharField(blank=True, max_length=255, null=True, verbose_name='\u53d1\u5238\u7406\u7531')),
                ('start_time', models.DateTimeField(blank=True, null=True, verbose_name='\u6709\u6548\u5f00\u59cb\u65f6\u95f4')),
                ('end_time', models.DateTimeField(blank=True, null=True, verbose_name='\u6709\u6548\u7ed3\u675f\u65f6\u95f4')),
                ('is_del', models.IntegerField(blank=True, default=0, null=True, verbose_name='\u662f\u5426\u5220\u9664')),
                ('c_user', models.CharField(blank=True, max_length=50, null=True, verbose_name='\u521b\u5efa\u4eba')),
                ('channel', models.CharField(blank=True, max_length=50, null=True, verbose_name='\u9886\u5238\u6e20\u9053')),
                ('mobile', models.CharField(blank=True, max_length=11, null=True, verbose_name='\u7528\u6237\u7535\u8bdd')),
            ],
            options={
                'db_table': 'coupon_allot',
            },
        ),
        migrations.CreateModel(
            name='CouponCodeMain',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cids', models.TextField(verbose_name='\u53ef\u5151\u6362\u5238ids')),
                ('amount', models.IntegerField(verbose_name='\u6570\u91cf')),
                ('is_muti', models.IntegerField(blank=True, null=True, verbose_name='\u662f\u5426\u4f7f\u7528\u76f8\u540c\u5151\u6362\u7801')),
                ('start_time', models.DateTimeField(auto_now_add=True, null=True, verbose_name='\u5151\u6362\u6709\u6548\u671f\u5f00\u59cb\u65f6\u95f4')),
                ('end_time', models.DateTimeField(blank=True, null=True, verbose_name='\u5151\u6362\u6709\u6548\u671f\u7ed3\u675f\u65f6\u95f4')),
                ('c_time', models.DateTimeField(auto_now_add=True, null=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('m_time', models.DateTimeField(auto_now=True, null=True, verbose_name='\u4fee\u6539\u65f6\u95f4')),
                ('c_user', models.CharField(blank=True, max_length=50, null=True, verbose_name='\u521b\u5efa\u4eba')),
                ('m_user', models.CharField(blank=True, max_length=50, null=True, verbose_name='\u4fee\u6539\u4eba')),
                ('user_max_count', models.IntegerField(blank=True, default=0, null=True, verbose_name='\u5355\u4e2a\u7528\u6237\u5151\u6362\u6b21\u6570\u4e0a\u9650')),
            ],
            options={
                'db_table': 'coupon_code_main',
            },
        ),
        migrations.CreateModel(
            name='CouponCodeSub',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('main_id', models.BigIntegerField(verbose_name='\u5151\u6362\u7801\u4e3b\u4f53id')),
                ('exchange_code', models.CharField(max_length=20, verbose_name='\u5151\u6362\u7801')),
                ('status', models.IntegerField(blank=True, default=0, null=True, verbose_name='\u662f\u5426\u5151\u6362\u8fc7')),
                ('uid', models.CharField(blank=True, max_length=50, null=True, verbose_name='\u5151\u6362\u7684\u7528\u6237\u7684id')),
                ('c_time', models.DateTimeField(auto_now_add=True, null=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('m_time', models.DateTimeField(auto_now=True, null=True, verbose_name='\u4fee\u6539\u65f6\u95f4')),
            ],
            options={
                'db_table': 'coupon_code_sub',
            },
        ),
        migrations.CreateModel(
            name='CouponResource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='\u540d\u79f0')),
                ('remark', models.CharField(blank=True, max_length=255, null=True, verbose_name='\u63cf\u8ff0')),
                ('amount', models.IntegerField(blank=True, null=True, verbose_name='\u5238\u9762\u6570\u503c')),
                ('biz_type', models.IntegerField(blank=True, null=True, verbose_name='\u5238\u7c7b\u578b')),
                ('effect_type', models.IntegerField(blank=True, null=True, verbose_name='\u751f\u6548\u7c7b\u578b')),
                ('start_time', models.DateTimeField(blank=True, null=True, verbose_name='\u5f00\u59cb\u6709\u6548\u65f6\u95f4')),
                ('end_time', models.DateTimeField(blank=True, null=True, verbose_name='\u7ed3\u675f\u6709\u6548\u65f6\u95f4')),
                ('effect_days', models.IntegerField(blank=True, null=True, verbose_name='\u6709\u6548\u5929\u6570')),
                ('min_consume', models.IntegerField(blank=True, null=True, verbose_name='\u6700\u4f4e\u6d88\u8d39')),
                ('consume_remark', models.CharField(blank=True, max_length=255, null=True, verbose_name='\u6700\u4f4e\u6d88\u8d39\u8bf4\u660e')),
                ('cost_type', models.IntegerField(blank=True, null=True, verbose_name='\u6210\u672c\u7c7b\u578b')),
                ('cp_cost', models.IntegerField(blank=True, null=True, verbose_name='cp\u6210\u672c\u91d1\u989d')),
                ('putao_cost', models.IntegerField(blank=True, null=True, verbose_name='\u8461\u8404\u6210\u672c\u91d1\u989d')),
                ('c_time', models.DateTimeField(auto_now_add=True, null=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('m_time', models.DateTimeField(auto_now=True, null=True, verbose_name='\u4fee\u6539\u65f6\u95f4')),
                ('c_user', models.CharField(blank=True, max_length=50, null=True, verbose_name='\u521b\u5efa\u4eba')),
                ('m_user', models.CharField(blank=True, max_length=50, null=True, verbose_name='\u4fee\u6539\u4eba')),
                ('is_mutex', models.IntegerField(blank=True, null=True, verbose_name='\u662f\u5426\u4e92\u65a5')),
                ('scope', models.CharField(blank=True, max_length=50, null=True, verbose_name='\u4f7f\u7528\u8303\u56f4')),
                ('gids', models.TextField(blank=True, null=True, verbose_name='\u8001\u7248\u4f18\u60e0\u5238\u5546\u54c1\u5217\u8868')),
                ('click_action', models.CharField(blank=True, max_length=255, null=True, verbose_name='app\u5bfc\u822a\u8fde\u63a5')),
                ('icon', models.CharField(blank=True, default='http://img.putao.so/open/putao_icon_quick_daojiafuwu.png', max_length=255, null=True, verbose_name='\u5238\u56fe\u6807')),
            ],
            options={
                'db_table': 'coupon_resource',
            },
        ),
        migrations.CreateModel(
            name='CouponResourceScope',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cid', models.IntegerField(verbose_name='\u5238ID')),
                ('goods_cat', models.TextField(blank=True, null=True, verbose_name='\u652f\u6301\u7684\u4ea7\u54c1\u5206\u7c7b')),
                ('goods_cat_x', models.TextField(blank=True, null=True, verbose_name='\u4e0d\u652f\u6301\u7684\u4ea7\u54c1\u5206\u7c7b')),
                ('gids', models.TextField(blank=True, null=True, verbose_name='\u652f\u6301\u5546\u54c1\u7684id')),
                ('gids_x', models.TextField(blank=True, null=True, verbose_name='\u4e0d\u652f\u6301\u5546\u54c1id')),
                ('cps', models.TextField(blank=True, null=True, verbose_name='\u652f\u6301\u7684cp')),
                ('cps_x', models.TextField(blank=True, null=True, verbose_name='\u4e0d\u652f\u6301\u7684cp')),
            ],
            options={
                'db_table': 'coupon_resource_scope',
            },
        ),
        migrations.CreateModel(
            name='EntityAllot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.CharField(max_length=50, verbose_name='\u7528\u6237id')),
                ('eid', models.BigIntegerField(verbose_name='\u5b9e\u4f53\u5956\u54c1id')),
                ('allot_time', models.DateTimeField(verbose_name='\u83b7\u53d6\u65f6\u95f4')),
                ('status', models.IntegerField(verbose_name='\u72b6\u6001')),
                ('m_time', models.DateTimeField(blank=True, null=True, verbose_name='\u4fee\u6539\u65f6\u95f4')),
                ('activity_id', models.BigIntegerField(blank=True, null=True, verbose_name='\u6d3b\u52a8id')),
                ('c_user', models.CharField(blank=True, max_length=50, null=True, verbose_name='\u521b\u5efa\u4eba')),
            ],
            options={
                'db_table': 'entity_allot',
            },
        ),
        migrations.CreateModel(
            name='EntityReceiverAddr',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('en_alt_id', models.CharField(max_length=50, verbose_name='\u4e2d\u5956\u8bb0\u5f55id')),
                ('addr', models.CharField(max_length=255, verbose_name='\u6536\u8d27\u5730\u5740')),
                ('c_time', models.DateTimeField(blank=True, null=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('m_time', models.DateTimeField(blank=True, null=True, verbose_name='\u4fee\u6539\u65f6\u95f4')),
                ('mobile', models.CharField(blank=True, max_length=11, null=True, verbose_name='\u6536\u8d27\u4eba\u624b\u673a\u53f7')),
                ('receiver', models.CharField(blank=True, max_length=50, null=True, verbose_name='\u6536\u8d27\u4eba\u5730\u5740')),
            ],
            options={
                'db_table': 'entity_receiver_addr',
            },
        ),
        migrations.CreateModel(
            name='EntityResource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='\u5b9e\u7269\u8d44\u6e90\u540d\u79f0')),
                ('remark', models.CharField(blank=True, max_length=255, null=True, verbose_name='\u5b9e\u7269\u8d44\u6e90\u63cf\u8ff0')),
                ('amount', models.IntegerField(verbose_name='\u6570\u91cf')),
                ('url', models.CharField(blank=True, max_length=255, null=True, verbose_name='\u9886\u53d6\u5730\u5740')),
                ('c_time', models.DateTimeField(blank=True, null=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('m_time', models.DateTimeField(blank=True, null=True, verbose_name='\u4fee\u6539\u65f6\u95f4')),
                ('c_user', models.CharField(blank=True, max_length=50, null=True, verbose_name='\u521b\u5efa\u4eba')),
                ('m_user', models.CharField(blank=True, max_length=50, null=True, verbose_name='\u4fee\u6539\u4eba')),
                ('cost_type', models.IntegerField(verbose_name='\u6210\u672c\u7c7b\u578b')),
                ('cp_cost', models.IntegerField(blank=True, null=True, verbose_name='cp\u6210\u672c')),
                ('putao_cost', models.IntegerField(blank=True, null=True, verbose_name='\u8461\u8404\u6210\u672c')),
            ],
            options={
                'db_table': 'entity_resource',
            },
        ),
        migrations.CreateModel(
            name='InviteAward',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('share_activity_id', models.BigIntegerField()),
                ('number', models.IntegerField()),
                ('cids', models.CharField(blank=True, max_length=255, null=True)),
                ('vip_charge', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'invite_award',
            },
        ),
        migrations.CreateModel(
            name='ShareActivity',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50, verbose_name='\u6d3b\u52a8\u540d\u79f0')),
                ('description', models.CharField(blank=True, max_length=255, null=True, verbose_name='\u6d3b\u52a8\u8bf4\u660e')),
                ('cids', models.TextField(verbose_name='\u6d3b\u52a8\u53d1\u653e\u7684\u5238\u7684json\u5f62\u5f0f')),
                ('before_vip_charge', models.BigIntegerField(blank=True, null=True)),
                ('after_vip_charge', models.BigIntegerField(blank=True, null=True)),
                ('activity_rule', models.TextField(blank=True, null=True, verbose_name='\u6d3b\u52a8\u89c4\u5219')),
                ('coupon_count', models.IntegerField(verbose_name='\u6d3b\u52a8\u5206\u4eab\u7684\u5355\u4e2a\u94fe\u63a5\u53c2\u4e0e\u6b21\u6570\u4e0a\u9650')),
                ('start_time', models.DateTimeField(blank=True, null=True, verbose_name='\u6d3b\u52a8\u5f00\u59cb\u65f6\u95f4')),
                ('end_time', models.DateTimeField(blank=True, null=True, verbose_name='\u6d3b\u52a8\u7ed3\u675f\u65f6\u95f4')),
                ('c_time', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('is_use', models.SmallIntegerField(blank=True, null=True, verbose_name='\u662f\u5426\u4e0a\u67b6')),
                ('daily_pick_limit', models.IntegerField(blank=True, null=True, verbose_name='\u5355\u4eba\u5355\u65e5\u53c2\u4e0e\u6d3b\u52a8\u6b21\u6570\u9650\u5236')),
                ('link_valid_days', models.IntegerField(blank=True, null=True, verbose_name='\u5206\u4eab\u94fe\u63a5\u6709\u6548\u671f\uff0c\u5982\u679c\u4e3a0\u5219\u4e0e\u6d3b\u52a8\u65f6\u95f4\u4e00\u81f4')),
                ('share_coupons', models.TextField(verbose_name='\u56de\u9988\u7ed9\u5206\u4eab\u4eba\u7684\u5238json')),
                ('inviter_vip_charge', models.BigIntegerField(blank=True, null=True)),
                ('share_count', models.IntegerField(blank=True, null=True, verbose_name='\u5206\u4eab\u94fe\u63a5\u88ab\u70b9\u51fb\u591a\u5c11\u6b21\u624d\u7ed9\u5206\u4eab\u4eba\u53d1\u5238')),
                ('is_share_award', models.SmallIntegerField(blank=True, null=True, verbose_name='\u662f\u5426\u542f\u7528\u7ed9\u5206\u4eab\u4eba\u8fd4\u5238\uff0c1 \u662f\uff0c0\u5426')),
                ('share_type', models.SmallIntegerField(blank=True, null=True, verbose_name='\u5224\u65ad\u662f\u5426\u9080\u8bf7\u6709\u793c\u7684\u7c7b\u578b,1\u8868\u793a\u9080\u8bf7\u6709\u793c')),
                ('guide_word', models.CharField(max_length=100, verbose_name='\u5f15\u5bfc\u9875')),
            ],
            options={
                'db_table': 'share_activity',
            },
        ),
    ]
