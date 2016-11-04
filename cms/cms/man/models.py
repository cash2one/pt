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
    last_login = models.DateTimeField(blank=True, null=True,auto_now=True)
    is_superuser = models.IntegerField(default=0)
    username = models.CharField(unique=True, max_length=30)
    first_name = models.CharField(max_length=30, default="")
    last_name = models.CharField(max_length=30, default="")
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField(default=1)
    date_joined = models.DateTimeField(auto_now_add=True)

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

class AuthToken(models.Model):
    id = models.IntegerField(primary_key=True)
    user_id = models.CharField(max_length=100, unique=True)
    token = models.CharField(max_length=100)

    class Meta:
        db_table = u'auth_token'