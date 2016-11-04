#coding: utf-8

"""
    存放report views中的一些共有的方法
"""
from __future__ import unicode_literals
from django.contrib.auth.decorators import permission_required, login_required
from django.core.exceptions import PermissionDenied
import json, functools
from django.shortcuts import render_to_response
from django.db import connections
from main.models import *
from phone_fee.models import *
from django.contrib import auth
from common.views import *
from common.models import *
from django.db import connection,transaction
import requests
import sys

from pt_shelves.settings import MY_HOST,CARD_ID

try:
    reload(sys)
    sys.setdefaultencoding('utf8')
except:
    pass


def add_report_var(f):
    @functools.wraps(f)
    def _(*args, **kwargs):
        result = f(*args, **kwargs)
        #查找所有的应用
        objs = AuthUserUserPermissions.objects.filter(user=args[0].user.id)
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

    #设定订单管理模块权限名称
    SHELVES_MANAGEMENT_PHONE_FEE = u"话费商品管理"
    SHELVES_MANAGEMENT_PHONE_FLOW = u"流量商品管理"
    SHELVES_MANAGEMENT_VIP = u"VIP卡商品管理"

"""
vip卡接口信息
:card_id
:vip_info_url
:edit_vip_info_url
"""
card_id = CARD_ID
host = MY_HOST
VIP_INFO_URL = "http://api.%sputao.so/svip/card/view?cardId=%s" % (host,card_id)
EDIT_VIP_INFO_URL = "http://api.%sputao.so/svip/card/update" % (host)
EDIT_TOP_URL = "http://api.%sputao.so/svip/card/goods/setTop" % (host)
EDIT_VENDIBILITY_URL = "http://api.%sputao.so/svip/card/goods/setVendibility" % (host)
GET_REDEEM_CODE_URL = "http://api.%sputao.so/svip/card/goods/exchange/listCodes" % (host)

VIP_RECHARGE_LIST = 'http://api.%sputao.so/svip/card/goods/listRecharge' % (host)
VIP_RECHARGE_ADD = 'http://api.%sputao.so/svip/card/goods/add' % (host)
VIP_RECHARGE_UPDATE = 'http://api.%sputao.so/svip/card/goods/update' % (host)

VIP_EXCHANGE_LIST = 'http://api.%sputao.so/svip/card/goods/listExchange' % (host)


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
    [15, "服务完成"],
    [16, "退款失败"],
    [17, "预约成功"],
    [18, "预约失败"],
    [19, "订单取消中"],
    [20, "订单取消成功"],
    [22, "服务方取消订单"],
    [-1, "未知状态"]
]

TEST_STATUS = [
    [0, "测试订单"],
    [1, "非测试订单"]
]

# 话费商品管理列表（key,列名，是否默认显示）
PF_MANAGEMENT_TABLE_COLUMNS = [
    [0, " ", 1],
    [1, "序号", 1],
    [2, "状态", 1],
    [3, "充值卡编号", 1],
    [4, "商品名称", 1],
    [5, "售价", 1],
    [6, "面值", 1],
    [7, "有效期", 1],
    [8, "操作", 1]
]

ALL_ORDER_STATUS = [0, 5, 6, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18 ,19, 20, 22]


def get_card_id():
    return CARD_ID


def get_edit_top_url():
    return EDIT_TOP_URL


def get_edit_vendibility_url():
    return EDIT_VENDIBILITY_URL


def get_get_redeem_code_url():
    return GET_REDEEM_CODE_URL


def get_pf_management_table_columns():
    return PF_MANAGEMENT_TABLE_COLUMNS


# 获取VIP卡信息
def get_vip_info():
    vip_info = []
    vip_info_req = requests.get(VIP_INFO_URL)
    vip_info_text = vip_info_req.json()
    vip_info.append([
        vip_info_text['data']['scopeDto']['categoryIds'].split(","),
        vip_info_text['data']['baseInfoDto']['userProtocolUrl'],
        vip_info_text['data']['baseInfoDto']['title'],
        vip_info_text['data']['baseInfoDto']['descsSimple'],
        vip_info_text['data']['baseInfoDto']['creatorId'],
        vip_info_text['data']['baseInfoDto']['descs'],
    ])
    if vip_info:
        return vip_info
    else:
        return 0


# 获取VIP卡信息
def get_vip_info_ajax(request):
    vip_info = []
    vip_info_req = requests.get(VIP_INFO_URL)
    vip_info_text = vip_info_req.json()
    vip_info.append([
        vip_info_text['data']['scopeDto']['categoryIds'].split(","),
        vip_info_text['data']['baseInfoDto']['userProtocolUrl'],
        vip_info_text['data']['baseInfoDto']['title'],
        vip_info_text['data']['baseInfoDto']['descsSimple'],
        vip_info_text['data']['baseInfoDto']['creatorId'],
        vip_info_text['data']['baseInfoDto']['descs'],
    ])
    return HttpResponse(json.dumps([vip_info]))

# 更新VIP卡信息
def edit_vip_card(request):
    title = request.POST.get("title")
    userProtocolUrl = request.POST.get("userProtocolUrl")
    descsSimple = request.POST.get("descsSimple")
    descs = request.POST.get("descs")
    categoryIds = request.POST.get("categoryIds")
    para_vip_info = {
        'cardId':CARD_ID,
        'baseInfoDto.title':title,
        'baseInfoDto.userProtocolUrl':userProtocolUrl,
        'baseInfoDto.descsSimple':descsSimple,
        'baseInfoDto.descs':descs,
        'scopeDto.categoryIds':categoryIds,
    }
    r = requests.post(EDIT_VIP_INFO_URL, data=para_vip_info)
    r_txt = r.json()

    msg = 'order update successfully!'

    return HttpResponse(json.dumps(msg))


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

def get_app_name(app_id):
    if app_id:
        return TongjiSysApp.objects.get(app_id=app_id).app_name
    else:
        return "全部应用"


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


def get_time_diff(start,end, format):
    start = datetime.datetime.strptime(start, format)
    end = datetime.datetime.strptime(end, format)
    return (end-start).days+1


def get_pf_province():
    try:
        provinces = []
        objs = CpPhoneFeeProduct.objects.values('prod_province_id').distinct()
        for obj in objs:
            provinces.append(obj["prod_province_id"])
        return provinces
    except:
        return []


def get_pf_cp():
    try:
        cp_names = []
        objs = CpPhoneFeeProduct.objects.values('cp_name').distinct()
        for obj in objs:
            cp_names.append(obj["cp_name"])
        return cp_names
    except:
        return []


def get_pf_carrier():
    try:
        carriers = []
        objs = CpPhoneFeeProduct.objects.values('prod_isptype').distinct()
        for obj in objs:
            carriers.append(obj["prod_isptype"])
        return carriers
    except:
        return []


def get_vip_secondary_category():
    secondary_categorys = []
    cursor = connections['cms_db'].cursor()
    sql = """
            SELECT *
            FROM cms_navi_category
            WHERE parent_id = 0
                AND fatherId = 0
                AND type > 0;
    """
    cursor.execute(sql)
    transaction.commit(using='cms_db')
    for obj in cursor:
        category = [str(obj[0]),str(obj[1])]
        secondary_categorys.append(category)
    return secondary_categorys


def get_vip_third_category():
    third_categorys = []
    cursor = connections['cms_db'].cursor()
    sql = """
            SELECT c1.id
                ,c1.fatherId
                ,CONCAT (
                    c2.NAME
                    ,'-'
                    ,c1.NAME
                    )
            FROM cms_navi_category c1
            LEFT JOIN cms_navi_category c2 ON c1.fatherId = c2.id
            WHERE c1.fatherId IN (
                    SELECT id
                    FROM cms_navi_category
                    WHERE parent_id = 0
                        AND fatherId = 0
                        AND type > 0
                    )
            ORDER BY c1.fatherId;
    """
    cursor.execute(sql)
    transaction.commit(using='cms_db')
    for obj in cursor:
        category = [str(obj[0]), str(obj[1]), str(obj[2])]
        third_categorys.append(category)
    return third_categorys

