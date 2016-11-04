#coding: utf-8

"""
    进行某些特殊操作，发布的时候，须注释掉
"""

from django.http import HttpResponse
from report.models import TongjiSysApp
from django.contrib.auth.hashers import make_password
from common.views import *
from man.models import *


def create_permission(request):
    """
    #模块查看权限
    #应用查看权限
    INSERT INTO `pt_op_total`.`django_content_type`
    (`id`,
    `name`,
    `app_label`,
    `model`)
    VALUES
    (199,
    "module",
    "man",
    "report1"),
    (200,
    "app",
    "man",
    "report2");
    """
    # content_types = [
    #     [PermissionType.MODULE, "module", "man", "report1"], #业务模块查看权限
    #     [PermissionType.APP, "app", "man", "report2"], #业务应用查看权限
    #     [PermissionType.USER_ON, "user_on", "man", "user1"],    #用户模块查看权限
    #     [PermissionType.STAFF_ON, "staff_on", "man", "staff1"]    #账号管理
    # ]
    # for c in content_types:
    #     a = DjangoContentType(id=c[0], name=c[1], app_label=c[2], model=c[3])
    #     a.save()

    # #业务应用权限
    # objs = TongjiSysApp.objects.all()
    # for obj in objs:
    #     a = AuthPermission(name=obj.app_id, content_type_id=PermissionType.APP, codename=obj.app_name)
    #     a.save()
    # a = AuthPermission(name="", content_type_id=PermissionType.APP, codename="全部应用")
    # a.save()
    #业务模块权限
    objs = [
        # ["order_reports", "订单日报表"],
        ["order_sum", "订单汇总报表"],
        # ["cp", "订单多CP报表"],
        # ["failed_orders", "失败订单报表"],
        # ["trade", "营销费用报表"],
        # ["phone_fee", "充话费"],
        # ["flow", "充流量"],
        # ["qb", "游戏充值"],
        # ["movie", "电影票"],
        # ["service", "业务情况"],
        # ["coupon", "用券情况"],
        # ["full_hosting", "全托管业务"],
        # ["goods", "商品统计"]
    ]
    for obj in objs:
        a = AuthPermission(name=obj[0], content_type_id=PermissionType.MODULE, codename=obj[1])
        a.save()
    # #用户模块开关
    # a = AuthPermission(name="user_on", content_type_id=PermissionType.USER_ON, codename="用户模块开关")
    # a.save()
    # #账号管理开关
    # a = AuthPermission(name="staff_on", content_type_id=PermissionType.STAFF_ON, codename="账号管理开关")
    # a.save()
    return HttpResponse("ok")


def reset_pwd(request):
    """
    密码重置
    :param request:
    :return:
    """
    user = AuthUser.objects.get(id=1)
    user.password = make_password("1")
    user.save()
    return HttpResponse("ok")


