# coding: utf-8

"""
    存放finance views中的一些共用的方法
"""
import time
from django.contrib.auth.decorators import permission_required, login_required
from django.core.exceptions import PermissionDenied
import json, functools
from django.shortcuts import render_to_response
from django.db import connections
from django.views.decorators.csrf import csrf_exempt

from common.views import PermissionType, Const
from finance.models import VwPtTongjiFilter, PtCpInfo, TongjiSysApp, TongjiPayProduct, VwPtAppVersionFilter, \
    VwPtAppChannelNoFilter, VmPtCpBillsFilter, VmPtCpPaysFilter, CpSettlement
from man.models import *
from django.contrib import auth
from common.views import *
from django.db import connection, transaction
from man.models import AuthUserUserPermissions


class FinanceConst:
    FINANCE_SUM = "收支汇总"
    DAILY_SUM = "运营汇总"
    EXCEPT_ORDER_SUM = "异常订单汇总"

    # 权限管理，页面
    FINANCE_ZF_PAYMENT_CHANNEL_REPORT = "支付渠道数据汇总表"
    FINANCE_ZF_PRODUCT_REPORT = "支付数据分业务汇总表"
    FINANCE_ZF_DAOJIA_REPORT = "全托管支付数据分渠道汇总表"

    FINANCE_OPERATION_OPERATION_SUMMARY = "运营数据汇总报表"
    FINANCE_OPERATION_DAOJIA_OPERATION_SUMMARY = "全托管运营数据报表"
    FINANCE_OPERATION_DAOJIA_OPERATION_COST_SUMMARY = "全托管营销费用报表"
    FINANCE_OPERATION_VIP_OPERATION_SUMMARY = "VIP卡运营数据报表"

    FINANCE_DETAIL_ABNORMAL_ORDER_SUMMARY = "异常订单汇总表"
    FINANCE_DETAIL_NO_OV_ORDER_DETAIL = "无压单对账"
    FINANCE_DETAIL_OV_ORDER_DETAIL = "有压单对账"
    FINANCE_DETAIL_DAOJIA_COUPON ="到家优惠券明细"
    FINANCE_DETAIL_NR_ORDER_DETAIL = "非匹配订单对账"
    FINANCE_DETAIL_OVERTIME_SELF_ORDER_DETAIL = "自营业务跨时段订单明细"
    FINANCE_DETAIL_OVERTIME_DAOJIA_ORDER_DETAIL = "到家业务跨时段订单明细"

    FINANCE_EVENT_UPLOAD_CP_BILL = "上传对账单(cp)"
    FINANCE_EVENT_UPLOAD_CP_PAY = "上传对账单(pay)"
    FINANCE_EVENT_DOWNLOAD_CP_STATMENT = "下载结算单"


def PtHttpResponse(data, dump=True, status=200):
    return HttpResponse(
        json.dumps(data) if dump else data,
        content_type="application/json",
        status=status,
    )

def report_render(request, template, context=None):
    context = context if context is not None else {}
    objs = AuthUserUserPermissions.objects.filter(user=request.user)
    for obj in objs:
        # print(obj.permission.content_type_id, obj.permission.name)
        if obj.permission.content_type_id == PermissionType.MODULE:
            context[obj.permission.name] = True

    return render_to_response(template, context)


VIP_FINANCE_TABLE_COLUMNS = [
    [0, "用户ID", 1],
    [1, "VIP卡ID", 1],
    [2, "VIP卡类型", 1],
    [3, "本期实收款", 1],
    [4, "本期额度", 1],
    [5, "本期消耗", 1],
    [6, "剩余额度", 1],
    [7, "本期实付", 1],
    [8, "子订单", 1],
]
VIP_ORDER_TABLE_COLUMNS = [
    [0, "用户ID", 1],
    [1, "VIP卡ID", 1],
    [2, "订单号", 1],
    [3, "服务商", 1],
    [4, "商品名称", 1],
    [5, "应付款", 1],
    [6, "应收款", 1],
    [7, "实收款", 1],
    [8, "实退款", 1],
    [9, "实付款", 1],
    [10, "优惠券", 1],
    [11, "批价策略", 1],
]


def get_vip_finance_table_columns():
    return VIP_FINANCE_TABLE_COLUMNS


def get_vip_order_table_columns():
    return VIP_ORDER_TABLE_COLUMNS


def add_report_var(f):
    @functools.wraps(f)
    def _(*args, **kwargs):
        result = f(*args, **kwargs)
        objs = AuthUserUserPermissions.objects.filter(user=args[0].user)
        items = []
        for obj in objs:
            if obj.permission.content_type_id == PermissionType.APP:
                items.append("['%s', '%s']" % (obj.permission.name, obj.permission.codename))

        apps_str = "[%s]" % ",".join(items)
        vars = {
            "user": auth.get_user(args[0]).username,
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

    COUPON = "用券情况"
    CP = "订单多CP报表"
    FAILED_ORDERS = "失败订单报表"
    ORDER_REPORTS = "订单总报表"
    TRADE = "营销费用报表"
    SERVICE = "业务情况"
    FULL_HOSTING = "商品全托管"


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


def get_user_apps(user):
    objs = AuthUserUserPermissions.objects.filter(user=user)
    apps = ""
    for obj in objs:
        # print(obj.permission.content_type_id, PermissionType.APP)
        if obj.permission.codename == "全部应用":
            return None
        if obj.permission.content_type_id == PermissionType.APP:
            if apps:
                apps = "%s|^%s$" % (apps, obj.permission.name)
            else:
                apps = "^%s$" % obj.permission.name
    return apps


def get_user_zfs(user):
    objs = AuthUserUserPermissions.objects.filter(user=user)
    zfs = ""
    for obj in objs:
        # print(obj.permission.content_type_id, PermissionType.APP)
        if obj.permission.codename == "全部支付账户":
            return None
        if obj.permission.content_type_id == PermissionType.ZF:
            if zfs:
                zfs = "%s|^%s$" % (zfs, obj.permission.name)
            else:
                zfs = "^%s$" % obj.permission.name
    if not zfs:
        print("not have zf permission")
        raise PermissionDenied
    return zfs


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
    cursor.execute("call `SP_T_RP_D_ACCOUNT_CHECKING`(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
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
        ReportConst.QB,
        ReportConst.FULL_HOSTING,
    ]
    print(names)
    products = []
    for name in names:
        products.append([TongjiPayProduct.objects.get(name=name).type, name])
    return products


order_states = \
    [
        ['3', "处理中订单"],
        ['4', "交易成功订单"],
        ['5', "交易失败，未退款"],
        ['6', "交易失败，退款成功"],
    ]

finance_result_type = \
    [
        [0, "正常"],
        [1, "异常"],
    ]

payment_types = \
    [
        [1, "支付宝"],
        [2, "微信"],
        [4, "华为"],
        [99, "其他"],
    ]

movie_cp_types = \
    [
        [2, "格瓦拉"],
        [3, "中影"],
        [5, "卖座"],
        [115, "微电影"],
        [116, "抠电影"],
    ]


def get_order_states():
    return order_states


def get_finance_result_type():
    return finance_result_type


def get_cp_types():
    objs = VmPtCpBillsFilter.objects.all()
    cp_infos = []
    for obj in objs:
        single_info = [obj.cp_id, obj.remark, obj.product_type]
        cp_infos.append(single_info)
    return cp_infos


def get_pay_types():
    objs = VmPtCpPaysFilter.objects.all()
    cp_infos = []
    for obj in objs:
        single_info = [obj.cp_id, obj.remark, obj.product_type]
        cp_infos.append(single_info)
    return cp_infos


def get_payment_types():
    return payment_types


def report_check_app(request, app):
    objs = AuthUserUserPermissions.objects.filter(user=request.user)
    per = []

    for obj in objs:
        # print(obj.permission.content_type_id, PermissionType.APP)
        if obj.permission.content_type_id == PermissionType.APP:
            per.append(obj.permission.name)
    if (app and (app not in per)) or ((not app) and len(per) < 1):
        print("report failed")
        raise PermissionDenied


def get_full_cp_names():
    cp_names = []
    cursor = connections['order'].cursor()
    sql = "select distinct concat(IFNULL(provider,'未匹配CP'),'-',appId), appId from pt_daojia_order order by 1 DESC;"
    # print(sql)
    cursor.execute(sql)
    transaction.commit_unless_managed(using='report')
    for obj in cursor:
        cp_name = [str(obj[0]), int(obj[1])]
        cp_names.append(cp_name)
    return cp_names

def get_cp_name(id):
    cursor = connections['order'].cursor()
    sql = "select distinct IFNULL(provider,'未匹配CP') from pt_daojia_order where appId = "+str(id)+";"
    # print(sql)
    cursor.execute(sql)
    cur = cursor.fetchone()
    cp_name = str(cur[0]) if cur is not None else u'未匹配CP'
    return cp_name


vip_card_types = \
    [
        [0,"recharege","充值卡"],
        [1,"exchange","次卡"],
    ]


def get_vip_card_types():
    return vip_card_types


def is_valid_date(str):
    """
    判断是否是一个有效的日期字符串
    :param str:
    :return:
    """
    try:
        time.strptime(str, "%Y-%m-%d")
        return True
    except:
        return False


def check_get(start_date, end_date, cpid, page_no, page_size):
    try:
        if not is_valid_date(start_date):
            return {"msg": "请输入正确的开始时间如2016-05-05", "code": -1}
        if not is_valid_date(end_date):
            return {"msg": "请输入正确的结束时间如2016-05-06", "code": -1}
        try:
            page_no = int(page_no)
        except:
            return {"msg": "请输入正确的page_no", "code": -1}
        if int(page_no < 0):
            return {"msg": "请输入大于等于0的page_no", "code": -1}
        try:
            page_size = int(page_size)
        except:
            return {"msg": "请输入正确的page_size", "code": -1}
        if int(page_size) < 1:
            return {"msg": "请输入大于0的page_size", "code": -1}
        return {"code": 0}
    except Exception as e:
        return {"msg": e.message, "code": -1}



@csrf_exempt
def order_settlement_amount(request):
    """
    GET,POST方法获取订单结算金额接口
    :param start_time:起始时间（包含）
    :param end_time:终止时间（包含）
    :param cpid:商家id（可不传，不传则查询全部商家. 如果多个，则用逗号分隔）
    :param page_no:第几个
    :param page_size:每页几行数据,默认显示20条
    :return:
    """
    if request.method == 'GET' or request.method == 'POST':
        data = {}
        try:
            if request.method == 'GET':
                start_date = request.GET.get("start_time")
                end_date = request.GET.get("end_time")
                cpid = request.GET.get("cpid", -1)
                page_no = request.GET.get("page_no", 0)
                page_size = request.GET.get("page_size", 20)
            else:
                start_date = request.POST.get("start_time")
                end_date = request.POST.get("end_time")
                cpid = request.POST.get("cpid", -1)
                page_no = request.POST.get("page_no", 0)
                page_size = request.POST.get("page_size", 20)
            c_check = check_get(start_date, end_date, cpid, page_no, page_size)
            from django.db.models import Sum
            if c_check['code'] == -1:
                return PtHttpResponse({"code": -1, "msg": c_check["msg"]})
            end_date_d = datetime.datetime.strptime(end_date, "%Y-%m-%d") + datetime.timedelta(days=1)
            if cpid == -1 or cpid == '':
                order_amount = CpSettlement.objects.using('default').filter(settlement_time__gte=start_date,
                                                                            settlement_time__lte=end_date_d).order_by(
                    'cp_id')
                total_amount = order_amount.aggregate(Sum('settlement_price'))
            else:
                try:
                    cps = cpid.split(',')
                except:
                    return PtHttpResponse({"code": -1, "msg": "cpid请以逗号分隔"})
                order_amount = CpSettlement.objects.using('default').filter(settlement_time__gte=start_date,
                                                                            cp_id__in=cps,
                                                                            settlement_time__lte=end_date_d).order_by(
                    'cp_id')
                total_amount = order_amount.aggregate(Sum('settlement_price'))
            data['data'] = [dict(
                order_no=obj.order_no,
                settle_price=obj.settlement_price,
                cpid=obj.cp_id
            ) for obj in order_amount[int(page_no):(int(page_size)+int(page_no))]]
            data['code'] = 0
            data['msg'] = "success"
            data['total_count'] = len(order_amount)
            data['total_amount'] = 0 if total_amount['settlement_price__sum'] is None else total_amount['settlement_price__sum']
            return PtHttpResponse(data)
        except Exception as err:
            data['msg'] = err.message
            data['code'] = -1
            return PtHttpResponse(data)
    else:
        return PtHttpResponse({"code": -1, "msg": "请使用GET或者POST方法请求"})
