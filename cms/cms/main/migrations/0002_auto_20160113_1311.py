# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CmsCpdisplay',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('location1', models.IntegerField(verbose_name='首页排序')),
                ('location2', models.IntegerField(verbose_name='品牌页排序')),
                ('mark', models.CharField(blank=True, null=True, verbose_name='运营标签', max_length=256)),
                ('op_desc', models.CharField(blank=True, null=True, verbose_name='运营描述', max_length=256)),
            ],
            options={
                'db_table': 'cms_cpdisplay',
                'managed': False,
            },
        ),
        migrations.AlterModelOptions(
            name='cmscpcategory',
            options={'ordering': ['id'], 'managed': False},
        ),
    ]
