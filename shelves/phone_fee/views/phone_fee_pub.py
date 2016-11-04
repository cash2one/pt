# coding: utf-8

"""
    存放report views中的一些共有的方法
"""
from __future__ import unicode_literals

import json
from datetime import datetime
from django.core.exceptions import PermissionDenied
import functools
from django.db import connections

from common.conf import get_http_url
from common.models import VwPtTongjiFilter, PtCpInfo, TongjiPayProduct, VwPtAppVersionFilter, VwPtAppChannelNoFilter, \
    TongjiSysApp
from common.views import PermissionType
from main.models import AuthUserUserPermissions
from django.contrib import auth
from django.db import transaction

from phone_fee.models import CpPhoneFeeProduct, PtPhoneFeeProduct, PtPhonefeeCpRelation


def add_report_var(f):
    @functools.wraps(f)
    def _(*args, **kwargs):
        result = f(*args, **kwargs)
        # 查找所有的应用
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
    PHONE_FEE = u"充话费"
    FLOW = u"充流量"
    MOVIE = u"电影票"
    QB = u"游戏充值"
    TRAIN = u"火车票"
    HOTEL = u"酒店"
    WEC = u"水电煤"

    # 设定订单管理模块权限名称
    SHELVES_MANAGEMENT_PHONE_FEE = u"话费商品管理"
    SHELVES_MANAGEMENT_PHONE_FLOW = u"流量商品管理"
    SHELVES_MANAGEMENT_VIP = u"VIP卡商品管理"


FULL_ORDER_STATUS = [
    [0, u"订单取消"],
    [5, u"退款中"],
    [6, u"退款成功"],
    [9, u"待支付"],
    [10, u"订单关闭"],
    [11, u"订单受理中"],
    [12, u"订单确认"],
    [13, u"服务人员出发"],
    [14, u"服务中"],
    [15, u"服务完成"],
    [16, u"退款失败"],
    [17, u"预约成功"],
    [18, u"预约失败"],
    [19, u"订单取消中"],
    [20, u"订单取消成功"],
    [22, u"服务方取消订单"],
    [-1, u"未知状态"]
]

TEST_STATUS = [
    [0, u"测试订单"],
    [1, u"非测试订单"]
]

# 话费商品管理列表（key,列名，是否默认显示）
PF_MANAGEMENT_TABLE_COLUMNS = [
    [0, " ", 1],
    [1, u"排序", 1],
    [2, u"状态", 1],
    [3, u"供应商", 1],
    [4, u"省份", 1],
    [5, u"运营商", 1],
    [6, u"面值", 1],
    [7, u"售价", 1],
    [8, u"进货价", 1],
    [9, u"提示语", 1],
    [10, u"操作", 1],
]

ALL_ORDER_STATUS = [0, 5, 6, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 22]


def get_full_order_status():
    return FULL_ORDER_STATUS


def get_test_status():
    return TEST_STATUS


def get_pf_management_table_columns():
    return PF_MANAGEMENT_TABLE_COLUMNS


def get_full_cp_names():
    cp_names = []
    cursor = connections['main'].cursor()
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
    cursor.execute(sql)
    transaction.commit(using='main')
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

def get_app_name(app_id):
    if app_id:
        try:
            app_name = TongjiSysApp.objects.get(app_id=app_id).app_name
        except:
            app_name = u"未知app"
        return app_name
    else:
        return u"全部应用"


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


# 上下架
def updown_shelves(app, goods, done, is_updown,start_time='',end_time='',updown_status=-1):
    if goods[5].find('.') != -1:
        goods[5] = goods[5][0:goods[5].find('.')]
    # 查看
    if done == '-1':
        pt_data = []
        for i in app:
            goods_clone = goods[:]
            try:
                pt_p_f_data = PtPhoneFeeProduct.objects.filter(prod_name=goods[3] + goods[4], prod_content=goods[5],
                                                               app_id=i).values_list('id', 'prod_price', 'status',
                                                                                     'purchase_price')
                pt_p_f_data = list(pt_p_f_data[0])
                pt_p_f_data.append(i)
                pt_cp_re = PtPhonefeeCpRelation.objects.filter(pt_prod_id=pt_p_f_data[0]).values_list('cp_prod_id',
                                                                                                      'cp_name')

                pt_cp_re = list(pt_cp_re[0])
                if pt_p_f_data[1] != goods[6] or pt_cp_re[1] != goods[2]:
                    pt_data.append(pt_p_f_data + pt_cp_re)
                else:
                    pt_data.append([])
                app_names = get_app_name(i)
                goods_clone.append(app_names)
                pt_data.append(goods_clone)

            except Exception as error:
                pt_data.append([])
                app_names = get_app_name(i)
                goods_clone.append(app_names)
                pt_data.append(goods_clone)

        return pt_data
    # 修改
    else:
        # 　print goods, app, done, is_updown
        cp_prod_id = CpPhoneFeeProduct.objects.get(id=goods[0]).prod_id

        for i in app:
            try:
                pt_p_fee_pro = PtPhoneFeeProduct.objects.get(prod_name=goods[3] + goods[4], prod_content=goods[5],
                                                             app_id=i)
                pt_p_fee_pro.prod_price = goods[6]
                pt_p_fee_pro.purchase_price = goods[7]
                pt_p_fee_pro.status = is_updown
                pt_p_fee_pro.message = goods[8]
                pt_p_fee_pro.is_special = 0
                pt_p_fee_pro.start_time = start_time
                pt_p_fee_pro.end_time = end_time
                pt_p_fee_pro.updown_status = updown_status
                pt_p_f_r=PtPhonefeeCpRelation.objects.filter(pt_prod_id=pt_p_fee_pro.id)
                if pt_p_f_r:
                    pt_p_f_r.update(cp_prod_id=cp_prod_id,cp_name = goods[2])
                else:
                    PtPf=PtPhonefeeCpRelation(pt_prod_id=pt_p_fee_pro.id,cp_prod_id=cp_prod_id,cp_name=goods[2])
                    PtPf.save()
                pt_p_fee_pro.save()
            except:
                pt_p_fee_pro = PtPhoneFeeProduct(prod_name=goods[3] + goods[4], prod_content=goods[5], app_id=i,
                                                 status=is_updown, prod_price=goods[6], message=goods[8],
                                                 purchase_price=goods[7], is_special=0,start_time = start_time,
                                                 end_time = end_time,updown_status = updown_status)
                pt_p_fee_pro.save()
                pt_p_fee_pro_id = PtPhoneFeeProduct.objects.get(prod_name=goods[3] + goods[4], prod_content=goods[5],
                                                                app_id=i, status=is_updown, prod_price=goods[6],
                                                                message=goods[8]).id
                # print pt_p_fee_pro_id, cp_prod_id, goods[2]
                pt_cp_re = PtPhonefeeCpRelation(pt_prod_id=pt_p_fee_pro_id, cp_prod_id=cp_prod_id, cp_name=goods[2])
                pt_cp_re.save()

        return []

def updown_shelves_app(app, goods, is_updown,str_time,end_time,updown_status):
    try:
        PtPhoneFeeProduct.objects.filter(id=goods[0],app_id=app).update(status=is_updown, start_time=str_time,
                                                                        end_time=end_time, updown_status=updown_status,m_time=datetime.now())
    except Exception as error:
        return {'err': error.message}
    return []

def get_max_prod_id():
    cursor = connections['phone_fee'].cursor()
    sql = """
              SELECT MAX(CONVERT(prod_id,SIGNED)) FROM cp_phone_fee_product ;
          """
    cursor.execute(sql)
    transaction.commit(using='phone_fee')
    max_prod_id = cursor.fetchone()[0]
    return max_prod_id


def edit_notify(data, msg, app_id):
    err = []
    if app_id == '-1':
        try:
            cp_fee_p = CpPhoneFeeProduct.objects.get(id=data[0])
            pt_cp_re = PtPhonefeeCpRelation.objects.filter(cp_prod_id=cp_fee_p.prod_id).values_list('pt_prod_id',
                                                                                                    )

        except Exception as error:
            return {'err': error.message}
        else:
            cp_fee_p.default_message = msg
            cp_fee_p.save()
            # print pt_cp_re,data[0]
            PtPhoneFeeProduct.objects.filter(id__in=pt_cp_re).update(message=msg)
    else:
        try:
            PtPhoneFeeProduct.objects.filter(id=data[0], app_id=app_id).update(message=msg)
        except Exception as error:
            return {'err': error.message}
    return err


def edit_sale_price(data, argv, not_cover,app_id):
    err = []
    if app_id == '-1':
        try:
            cp_fee_p = CpPhoneFeeProduct.objects.get(id=data[0])

            pt_cp_re = PtPhonefeeCpRelation.objects.filter(cp_prod_id=cp_fee_p.prod_id).values_list('pt_prod_id',
                                                                                                    )
        except Exception as error:
            return err.append(error.message)
        else:
            if argv == '0':
                data_list = PtPhoneFeeProduct.objects.filter(id__in=pt_cp_re, is_special=1).values_list('id',
                                                                                                        'prod_name',
                                                                                                        'prod_content',
                                                                                                        'prod_price',
                                                                                                        'app_id')
                lists = []
                for i in data_list:
                    app_names = get_app_name(i[4])
                    i = list(i)
                    i[4] = app_names
                    i.append(data[10])
                    lists.append(i)
                return lists
            else:
                cp_fee_p.putao_price = data[10]
                cp_fee_p.save()
                try:
                    PtPhoneFeeProduct.objects.filter(id__in=pt_cp_re).exclude(id__in=not_cover).update(
                            prod_price=data[10],
                            is_special=0)
                except Exception as error:
                    return err.append(error.message)
    else:
        try:
            PtPhoneFeeProduct.objects.filter(id=data[0]).update(
                prod_price=data[10],
                is_special=1)
        except Exception as error:
            return err.append(error.message)
    return err
