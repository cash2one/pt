# coding: utf-8

"""
    存放report views中的一些共有的方法
"""
import time
from django.contrib.auth.decorators import permission_required, login_required
from django.core.exceptions import PermissionDenied
import json, functools
from django.shortcuts import render_to_response
from django.db import connections
from django.views.decorators.csrf import csrf_exempt

from report.models import *
from man.models import *
from django.contrib import auth
from common.views import *
from django.db import connection, transaction

from report.views.report_pub import PtHttpResponse


def report_render(request, template, context={}):
    """
    增加权限控制
    :param request:
    :param template:
    :param context:
    :return:
    """
    objs = AuthUserUserPermissions.objects.filter(user=request.user)
    for obj in objs:
        if obj.permission.content_type_id == PermissionType.MODULE:
            context[obj.permission.name] = True
    return render_to_response(template, context)


def add_report_var(f):
    @functools.wraps(f)
    def _(*args, **kwargs):
        result = f(*args, **kwargs)
        # 查找所有的应用
        objs = AuthUserUserPermissions.objects.filter(user=args[0].user)
        items = []
        for obj in objs:
            if obj.permission.content_type_id == PermissionType.APP:
                items.append("['%s', '%s']" % (obj.permission.name, obj.permission.codename))
        apps_str = "[%s]" % ",".join(items)
        vars = {
            "user": auth.get_user(args[0]).username,
            # "lasturl": args[0].path,
            "lasturl": args[0].get_full_path(),
            "apps": apps_str
        }
        for key in vars:
            result.content = result.content.replace("{_tongji_begin_%s_end_}" % key, vars[key])
        return result

    return _


class ReportConst:
    PHONE_FEE = "充话费"
    FLOW = "充流量"
    MOVIE = "电影票"
    QB = "游戏充值"
    TRAIN = "火车票"
    HOTEL = "酒店"
    WEC = "水电煤"

    # 设定订单管理模块权限名称
    ORDER_MANAGEMENT_RECHARGE = "充值业务订单查询"
    ORDER_MANAGEMENT_MOVIE = "电影业务订单查询"
    ORDER_MANAGEMENT_DAOJIA = "到家业务订单查询"
    ORDER_MANAGEMENT_VIP = "VIP卡业务订单查询"


FULL_ORDER_STATUS = [
    [0, "订单取消"],
    [5, "退款中"],
    [6, "退款成功"],
    [9, "待支付"],
    [10, "订单关闭"],
    [11, "订单受理中"],
    [12, "订单确认"],
    [13, "服务人员出发"],
    [14, "服务中"],
    [15, "已服务"],
    [16, "退款失败"],
    [17, "预约成功"],
    [18, "预约失败"],
    [19, "订单取消中"],
    [20, "订单取消成功"],
    [22, "服务方取消订单"],
    [25, "订单服务完成"],
    [-1, "未知状态"]
]

TEST_STATUS = [
    [0, "测试订单"],
    [1, "非测试订单"]
]

# 到家订单列表（key,列名，是否默认显示）
DAOJIA_TABLE_COLUMNS = [
    [0, "ID", 1],
    [1, "分类", 1],
    [2, "订单号", 1],
    [3, "CP订单号", 0],
    [4, "商品名称", 1],
    [5, "CP", 1],
    [6, "CP电话", 0],
    [7, "支付类型", 0],
    [8, "服务开始时间", 1],
    [9, "服务时长", 0],
    [10, "服务预约城市", 1],
    [11, "服务预约地址", 0],
    [12, "消费者", 1],
    [13, "消费者电话", 1],
    [14, "下单人电话", 1],
    [15, "数量", 1],
    [16, "价格（元）", 1],
    [17, "VIP价格（元）", 1],
    [18, "用户备注", 0],
    [19, "订单金额（元）", 1],
    [20, "创建时间", 1],
    [21, "更新时间", 0],
    [22, "状态", 1],
    [23, "促销活动信息", 0],
    [24, "超时接单状态", 0],
    [25, "上门确认状态", 0],
    [26, "服务回访状态", 0],
    [27, "超时接单评论", 0],
    [28, "上门确认评论", 0],
    [29, "服务回访评论", 0],
    [30, "服务人员名称", 0],
    [31, "服务人员联系方式", 0],
    [32, "交易流水号", 0],
    [33, "订单渠道", 1],
    [34, "CP取消原因", 1],
    [35, "优惠券金额", 1],
    [36, "用户实付金额", 1],
    [37, "补差价", 1],
    [38, "u_id", 0],
]

# 充值业务订单列表（key,列名，是否默认显示）
RECHARGE_TABLE_COLUMNS = [
    [0, "ID", 1],
    [1, "订单号", 1],
    [2, "业务类型", 1],
    [3, "面值", 1],
    [4, "充值电话", 1],
    [5, "下单人电话", 1],
    [6, "商品名称", 0],
    [7, "CP名称", 1],
    [8, "数量", 0],
    [9, "支付价格", 1],
    [10, "用户唯一标实（PT_UID）", 1],
    [11, "优惠券ID", 1],
    [12, "优惠券面值", 1],
    [13, "订单创建时间", 1],
    [14, "支付类型", 1],
    [15, "订单状态", 1],
    [16, "应用渠道", 0],
    [17, "支付渠道", 0],
    [18, "应用ID", 0],
    [19, "应用版本", 0],
    [20, "交易流水号", 0],
]

# VIP业务订单列表（key,列名，是否默认显示）
VIP_TABLE_COLUMNS = [
    [0, "ID", 1],
    [1, "订单号", 1],
    [2, "商品名称", 1],
    [3, "用户手机号", 1],
    [4, "订单金额", 1],
    [5, "实付金额", 1],
    [6, "订单状态", 1],
    [7, "应用ID", 1],
    [8, "版本号", 1],
    [9, "渠道号", 1],
    [10, "用户ID", 1],
    [11, "创建时间", 1],
    [12, "促销活动信息", 1],
]

# 电影业务订单列表（key,列名，是否默认显示）
MOVIE_TABLE_COLUMNS = [
    [0, "ID", 1],
    [1, "葡萄订单号", 1],
    [2, "CP订单号", 1],
    [3, "影院名称", 1],
    [4, "影片名称", 1],
    [5, "放映时间", 1],
    [6, "影厅", 0],
    [7, "座位信息", 1],
    [8, "取票码", 1],
    [9, "取票单号", 1],
    [10, "取票验证吗", 1],
    [11, "价格", 1],
    [12, "购票电话", 1],
    [13, "注册电话", 1],
    [14, "商品名称", 0],
    [15, "CP名称", 1],
    [16, "数量", 0],
    [17, "支付价格", 1],
    [18, "用户唯一标实（PT_UID）", 1],
    [19, "优惠券ID", 0],
    [20, "优惠券面值", 1],
    [21, "订单创建时间", 1],
    [22, "支付类型", 1],
    [23, "订单状态", 1],
    [24, "应用渠道", 0],
    [25, "支付渠道", 0],
    [26, "应用ID", 0],
    [27, "应用版本", 0],
    [28, "交易流水号", 0],
]

ALL_ORDER_STATUS = [0, 5, 6, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 22]

# 自营业务订单状态
NORMAL_ORDER_STATUS = [
    [0, "订单取消"],
    [1, "订单待支付"],
    [3, "订单处理中"],
    [4, "支付成功"],
    [5, "退款中"],
    [6, "退款成功"],
    [7, "订单关闭"],
]

# 优惠券列表
COUPONS_TABLE_COLUMNS = [
    [0, "PTUID", 1],
    [1, "用户手机号", 1],
    [2, "优惠券ID", 1],
    [3, "优惠券名称", 1],
    [4, "面额", 1],
    [5, "使用限制", 1],
    [6, "使用说明", 1],
    [7, "参与活动", 1],
    [8, "优惠券领取时间", 1],
    [9, "优惠券截止日期", 1],
    [10, "优惠券使用时间", 1],
    [11, "订单号", 1],
    [12, "优惠券使用商品名称", 1],
]


def get_normal_order_status():
    return NORMAL_ORDER_STATUS


def get_full_order_status():
    return FULL_ORDER_STATUS


def get_test_status():
    return TEST_STATUS


def get_daojia_table_columns():
    return DAOJIA_TABLE_COLUMNS


def get_recharge_table_columns():
    return RECHARGE_TABLE_COLUMNS


def get_vip_table_columns():
    return VIP_TABLE_COLUMNS


def get_movie_table_columns():
    return MOVIE_TABLE_COLUMNS


def get_coupons_table_columns():
    return COUPONS_TABLE_COLUMNS


def get_full_cp_names():
    cp_names = []
    cursor = connections['order'].cursor()
    sql = """
            SELECT d1.provider
                  ,d1.appId
            FROM (
                  SELECT IFNULL(p1.provider, p1.appId) AS provider
                        ,p1.appId
                        ,MAX(p1.create_time) AS create_time
                  FROM pt_daojia_order p1
                  GROUP BY p1.provider
                          ,p1.appId
                  ) d1
            WHERE create_time = (
                  SELECT MAX(create_time)
                  FROM (
                         SELECT IFNULL(p2.provider, p2.appId) AS provider
                               ,p2.appId
                               ,MAX(p2.create_time) AS create_time
                         FROM pt_daojia_order p2
                         GROUP BY p2.provider
                                 ,p2.appId
                  ) d2
                  WHERE d1.appId = d2.appId
                  )
            GROUP BY d1.appId;
    """
    # print(sql)
    cursor.execute(sql)
    transaction.commit_unless_managed(using='report')
    for obj in cursor:
        cp_name = [str(obj[0]), str(obj[1])]
        cp_names.append(cp_name)
    return cp_names


def get_report_filters(filter_name):
    try:
        return VwPtTongjiFilter.objects.get(filter_name=filter_name).filter_content.split(",")
    except:
        return []


def get_cp_info(product_type):
    objs = PtCpInfo.objects.filter(product_type=product_type)
    return [[obj.id, obj.remark] for obj in objs]


def get_product_type(name):
    return TongjiPayProduct.objects.get(name=name).type


def get_app_versions(app_id):
    """
    获取app对应的所有版本
    :param app_id: 应用ID
    :return:
    """
    if not app_id:
        return []
    app_versions = set()
    objs = VwPtAppVersionFilter.objects.filter(app_id=app_id)
    for obj in objs:
        # 有NULL的版本，但咱不显示
        if obj.app_version:
            app_versions.add(obj.app_version)
    ret = list(app_versions)
    ret.sort(reverse=True)
    return ret


def get_app_channels(app_id):
    """
    获取app对应的所有渠道
    :param app_id: 应用ID
    :return:
    """
    if not app_id:
        return []
    app_channels = set()
    objs = VwPtAppChannelNoFilter.objects.filter(app_id=app_id)
    for obj in objs:
        # 有NULL的渠道，但咱不显示
        if obj.channel_no:
            app_channels.add(obj.channel_no)
    ret = list(app_channels)
    ret.sort()
    return ret


# @login_required
# def change_app_ajax(request):
#     """
#     根据对应的app，更新对应的渠道和版本
#     :param request:
#     :return:
#     """
#     app = request.POST.get("app")
#     vers = get_app_versions(app)
#     channels = get_app_channels(app)
#     return HttpResponse(json.dumps([vers, channels]))


def get_service_quality_data(start_date, end_date, app, ver, channel, operator, province, face, cp, product_name):
    """
    获取服务质量数据
    :param start_date: 开始日期
    :param end_date: 结束日期
    :param app: 应用id
    :param ver: 版本
    :param channel: 渠道
    :param operator: 运营商   游戏充值（游戏名称）
    :param province: 省份
    :param face: 面值
    :param cp: 供应商
    :param product_name: 产品名称，充话费、充流量等
    :return:
    """

    if not start_date:
        start_date = None
    if not end_date:
        end_date = None
    if not app:
        app = None
    if not ver:
        ver = None
    if not channel:
        channel = None
    if not operator:
        operator = None
    if not province:
        province = None
    if not face:
        face = None
    if not cp:
        cp = None
    product_type = get_product_type(product_name)
    cursor = connections['report'].cursor()
    cursor.execute("call `SP_T_RP_D_SERVICE_QUALITY`(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                   [start_date, end_date, product_type, cp, face, province, operator, ver, channel, app])
    objs = cursor.fetchall()
    data = []
    for obj in objs:
        data.append([
            str(obj[0]),
            int(obj[1]),
            int(obj[2]),
            int(obj[3]),
            '%0.2f%%' % float(obj[4] * 100),
            int(obj[5]),
            '%0.2f%%' % float(obj[6] * 100),
            int(obj[7]),
            '%0.2f%%' % float(obj[8] * 100),
            int(obj[9]),
            '%0.2f%%' % float(obj[10] * 100),
            int(obj[11]),
            '%0.2f%%' % float(obj[12] * 100),
            int(obj[13]),
            '%0.2f%%' % float(obj[14] * 100)
        ])
    if not data:
        data.append([Const.NONE] * 15)
    else:
        data.sort(key=lambda o: o[0], reverse=True)
    return data


def get_app_name(app_id):
    if app_id:
        return TongjiSysApp.objects.get(app_id=app_id).app_name
    else:
        return "全部应用"


def get_order_types():
    names = [
        ReportConst.PHONE_FEE,
        ReportConst.FLOW,
        ReportConst.MOVIE,
        ReportConst.TRAIN,
        ReportConst.HOTEL,
        ReportConst.WEC,
        ReportConst.QB
    ]
    products = []
    for name in names:
        products.append([TongjiPayProduct.objects.get(name=name).type, name])
    return products


def report_check_app(request, app):
    objs = AuthUserUserPermissions.objects.filter(user=request.user)
    per = []
    if not app:
        app = ""
    for obj in objs:
        if obj.permission.content_type_id == PermissionType.APP:
            per.append(obj.permission.name)
    if app not in per:
        raise PermissionDenied


def get_time_diff(start, end, format):
    start = datetime.datetime.strptime(start, format)
    end = datetime.datetime.strptime(end, format)
    return (end - start).days + 1


def get_daojia_goods_category():
    cms_cursor = connections['cms'].cursor()
    cms_cursor.execute("""SELECT g.appId
                            ,CASE WHEN c.`name` IS NULL
                                  THEN '未获取分类信息'
                                  ELSE c.`name`
		                      END AS category_name
                            ,g.cp_name
                            ,1 AS cp_count
                            ,g.cp_goods_count
                            ,g.citys
                            ,g.avg_good_price
                      FROM(
                             SELECT cms_goods.new_category as category_id
                                    ,MAX(cms_goods.cp_name) as cp_name
                                    ,cms_goods.open_service_id as appId
                                    ,MAX(cms_goods.city) as citys
                                    ,ROUND(AVG(cms_goods.price),2) as avg_good_price
                                    ,COUNT(DISTINCT cms_goods.goods_id) as cp_goods_count
                             FROM pt_cms_db.cms_goods
                             WHERE cms_goods.new_category IS NOT NULL
                               AND cms_goods.goods_id > 0
                             GROUP BY cms_goods.open_service_id

                             UNION ALL

							 SELECT cms_goods.new_category as category_id
                                    ,MAX(cms_goods.cp_name) as cp_name
                                    ,cms_goods.open_service_id as appId
                                    ,MAX(cms_goods.city) as citys
                                    ,ROUND(AVG(cms_goods.price),2) as avg_good_price
                                    ,COUNT(DISTINCT cms_goods.goods_id) as cp_goods_count
                             FROM pt_cms_db.cms_goods
                             GROUP BY cms_goods.open_service_id
							 HAVING SUM(IFNULL(new_category,0))=0
                      ) g
                      LEFT JOIN pt_cms_db.cms_navi_category AS c
                             ON g.category_id = c.id""")
    goods = cms_cursor.fetchall()
    category_info = {}
    for obj in goods:
        category_info[str(obj[0])] = str(obj[1])
    return category_info


