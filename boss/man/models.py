# coding: utf-8

"""
    修改django本身的权限管理
"""

from django.db import models


class AuthGroup(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=80, unique=True)

    class Meta:
        db_table = u'auth_group'


class DjangoContentType(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    app_label = models.CharField(max_length=100, unique=True)
    model = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = u'django_content_type'


class AuthPermission(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)  # 视图控制，英文；应用控制，应用id
    content_type_id = models.IntegerField()  # 两种类型，视图控制199，应用控制为200
    codename = models.CharField(max_length=100, unique=True)  # 如果content_type是视图控制，中文
    module_id = models.IntegerField(blank=True,null=True)  # modules分类名

    class Meta:
        db_table = u'auth_permission'


class AuthGroupPermissions(models.Model):
    id = models.IntegerField(primary_key=True)
    group = models.ForeignKey(AuthGroup)
    permission = models.ForeignKey(AuthPermission)

    class Meta:
        db_table = u'auth_group_permissions'


class AuthUser(models.Model):
    # id = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=30, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=75)
    password = models.CharField(max_length=128)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    is_superuser = models.IntegerField()
    last_login = models.DateTimeField()
    date_joined = models.DateTimeField()

    class Meta:
        db_table = u'auth_user'


class AuthUserGroups(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(AuthUser)
    group = models.ForeignKey(AuthGroup)

    class Meta:
        db_table = u'auth_user_groups'


class ModuleGroup(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=80, unique=True)

    class Meta:
        db_table = u'module_group'


class AuthUserUserPermissions(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(AuthUser)
    permission = models.ForeignKey(AuthPermission)

    class Meta:
        db_table = u'auth_user_user_permissions'


class AuthToken(models.Model):
    id = models.IntegerField(primary_key=True)
    user_id = models.CharField(max_length=100, unique=True)
    token = models.CharField(max_length=100)

    class Meta:
        db_table = u'auth_token'

