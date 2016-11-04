#coding: utf-8

"""
    存放report views中的一些共有的方法
"""

from django.contrib.auth.decorators import permission_required, login_required
from django.core.exceptions import PermissionDenied
import json, functools
from django.shortcuts import render_to_response
from django.db import connections
from report.models import *
from man.models import *
from django.contrib import auth
from common.views import *
from django.db import connection,transaction

def PtHttpResponse(data, dump=True, status=200):
    return HttpResponse(
        json.dumps(data) if dump else data,
        content_type="application/json",
        status=status,
    )


def report_render(request, template, context = None):
    """
    增加权限控制
    :param request:
    :param template:
    :param context:
    :return:
    """
    context = context if context is not None else {}
    objs = AuthUserUserPermissions.objects.filter(user=request.user)
    for obj in objs:
        if obj.permission.content_type_id == PermissionType.MODULE:
            context[obj.permission.name] = True
    return render_to_response(template, context)


def add_report_var(f):
    @functools.wraps(f)
    def _(*args, **kwargs):
        result = f(*args, **kwargs)
        #查找所有的应用
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
    DAOJIA = "商品全托管"
    VIP = 'VIP卡'

    COUPON = "用券情况"
    CP = "订单多CP报表"
    FAILED_ORDERS = "失败订单报表"
    ORDER_REPORTS = "订单日报表"
    ORDER_SUM = "订单汇总报表"
    TRADE = "营销费用报表"
    SERVICE = "业务情况"
    FULL_HOSTING = "全托管业务"
    GOODS = "商品统计"

    # auth control constant for business analysis module
    BA_TRANSACTION_ANALYSIS_GENERAL = "交易分析交易概况"
    BA_TRANSACTION_ANALYSIS_REAL_TIME = "交易分析实时统计"
    BA_TRANSACTION_ANALYSIS_SELF_PRODUCT = "交易分析自营业务分析"
    BA_TRANSACTION_ANALYSIS_DAOJIA_PRODUCT = "交易分析到家业务分析"
    BA_TRANSACTION_ANALYSIS_ACTIVITY = "交易分析活动分析"
    BA_TRANSACTION_ANALYSIS_USER = "交易分析用户分析"
    BA_TRANSACTION_ANALYSIS_DJ_SERVICE_QUALITY = "交易分析到家服务质量"
    BA_PRODUCT_ANALYSIS_REAL_TIME_REPORT = "订单实时报表"
    BA_PRODUCT_ANALYSIS_MOVIE_REPORT = "电影汇总报表"
    REPORT_DITUI_MANAGE = "地推人员管理"
    ORDER_COUPONS_QUERY = "订单优惠券查询"
    INVITE_BUSINESS_ANALY = "邀请有礼"


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

DAOJIA_TABLE_COLUMNS = [
    [0, "ID",1],
    [1, "订单号",1],
    [2, "CP订单号",0],
    [3, "商品名称",1],
    [4, "gid",1],
    [5, "分类",1],
    [6, "CP",1],
    [7, "CP电话",0],
    [8, "支付类型",0],
    [9, "服务开始时间",1],
    [10, "服务时长",0],
    [11, "服务预约城市",1],
    [12, "服务预约地址",0],
    [13, "消费者",1],
    [14, "消费者电话",0],
    [15, "下单人电话",1],
    [16, "数量",0],
    [17, "价格（元）",1],
    [18, "用户备注",0],
    [19, "订单金额（元）",0],
    [20, "创建时间",1],
    [21, "更新时间",0],
    [22, "状态",1],
    [23, "取消方",1],
    [24, "促销活动信息",0],
    [25, "服务人员名称",0],
    [26, "服务人员联系方式",0],
    [27, "渠道",1],
    [28, "首单/复购",1],
    [29, "地推小区",0],
    [30, "地推负责人",0],
    [31, "地推时间",0],
    [32, "活动渠道",1],
    [33, "用户支付金额金额",1],
    [34, "结算金额",1],
    [35, "优惠券实耗",1],
    [36, "活动营销费用",1],
    [37, "优惠券葡萄承担费用",1],
    [38, "优惠券CP承担费用",1],
]

ALL_ORDER_STATUS = [0, 5, 6, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18 ,19, 20, 22]

ORDER_STATES = [
    ['3', "处理中"],
    ['4',"交易成功"],
    ['5',"退款中"],
    ['6',"退款成功"],
]

INVITE_TABLE = [
    [0, "PTUID", 1],
    [1, "用户手机号", 1],
    [2, "邀请注册成功人数", 1],
    [3, "首单下单成功人数", 1],
    [4, "首单服务完成人数", 1],
    [5, "获券总额", 1],
    [6, "修改时间", 1],
    [7, "操作", 1],
]

INVITE_TABLE_B = [
    [0, "PTUID", 1],
    [1, "被邀请人手机号", 1],
    [2, "获券/注册时间", 1],
    [3, "首单下单成功时间", 1],
    [4, "首单服务完成时间", 1],
    [5, "获券总额", 1],
    [6, "邀请人手机号", 1],
]

INVITE_TABLE_DETAIL = [
    [0, "PTUID", 1],
    [1, "邀请人获券", 1],
    [2, "被邀请人获券面值", 1],
    [3, "被邀人获券时间", 1],
    [4, "被邀人手机号", 1],
    [5, "被邀人获券", 1],
    [6, "被邀人获券时间", 1],
]

VIP_TABLE_COLUMNS = [
    [0, "日期", 1],
    [1, "扫码ID", 1],
    [2, "扫码渠道", 1],
    [3, "VIP卡类型", 1],
    [4, "本期实收款", 1],
    [5, "本期充值人数", 1],
    [6, "扫描赠送额度", 1],
    [7, "扫码用户数", 1],
    [8, "本期消耗", 1],
    [9, "本期实付", 1],
    [10, "用户下单数", 1],
    [11, "子订单", 1],
]

ENTITY_CARD_COLUMNS = [
    [0, "实体卡批次", 1],
    [1, "卡片名称", 1],
    [2, "卡片备注", 1],
    [3, "卡片次数", 1],
    [4, "卡片售价", 1],
    [5, "有效期", 1],
    [6, "生成时间", 1],
    [7, "生成数量", 1],
    [8, "激活数量", 1],
    [9, "订单创建次数", 1],
    [10, "服务完成次数", 1],
    [11, "操作", 1],
]

vip_card_types = \
    [
        [0,"recharege","充值卡"],
        [1,"exchange","次卡"],
    ]

def get_order_states():
    return ORDER_STATES

def get_invite_table():
    return INVITE_TABLE

def get_invite_table_b():
    return INVITE_TABLE_B

def get_invite_detail():
    return INVITE_TABLE_DETAIL

def get_full_order_status():
    return FULL_ORDER_STATUS

def get_test_status():
    return TEST_STATUS

def get_daojia_table_columns():
    return DAOJIA_TABLE_COLUMNS

def get_vip_table_columns():
    return VIP_TABLE_COLUMNS

def get_entity_card_columns():
    return ENTITY_CARD_COLUMNS

def get_vip_card_types():
    return vip_card_types

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
    #print(sql)
    cursor.execute(sql)
    transaction.commit_unless_managed(using='report')
    for obj in cursor:
        cp_name = [str(obj[0]),str(obj[1])]
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
        #有NULL的版本，但咱不显示
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
        #有NULL的渠道，但咱不显示
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
        ReportConst.DAOJIA,
        ReportConst.QB,
        ReportConst.VIP
    ]
    products = []
    for name in names:
        products.append([TongjiPayProduct.objects.get(name=name).type, name])
    return products


def report_check_app(request, app):
    if app is None or app =='':
        return
    objs = AuthUserUserPermissions.objects.filter(user=request.user)
    per = []
    if not app:
        app = ""
    for obj in objs:
        if obj.permission.content_type_id == PermissionType.APP:
            per.append(obj.permission.name)
    if app not in per:
        raise PermissionDenied


def get_time_diff(start,end, format):
    start = datetime.datetime.strptime(start, format)
    end = datetime.datetime.strptime(end, format)
    return (end-start).days+1

def get_citys():
    citys = []
    cursor = connections['order'].cursor()
    sql = """SELECT DISTINCT city FROM pt_biz_db.pt_daojia_order;"""
    cursor.execute(sql)
    transaction.commit_unless_managed(using='report')
    for obj in cursor:
        if obj[0] == '' or str(obj[0]) == '1':
            continue
        if obj[0][-1:] == u'市':
            channel = [str(obj[0][0:-1]), str(obj[0][0:-1])]
        else:
            channel = [str(obj[0]), str(obj[0])]
        if channel not in citys:
            citys.append(channel)
        else:
            pass
    return citys

def get_activity_channels():
    activity_channels = []
    cursor = connections['report'].cursor()
    sql = """
        SELECT DISTINCT activity_channel
        FROM tongji_daojia_order_detail;
    """
    # print(sql)
    cursor.execute(sql)
    transaction.commit_unless_managed(using='report')
    for obj in cursor:
        channel = [str(obj[0]),str(obj[0])]
        activity_channels.append(channel)
    return activity_channels

