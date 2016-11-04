# coding: utf-8

"""
    存放 views中的一些共有的方法
"""
from __future__ import unicode_literals
from django.contrib.auth.decorators import permission_required, login_required
from django.core.exceptions import PermissionDenied
import json
import functools
from django.shortcuts import render_to_response
from django.db import connections
from main.models import *
from phone_fee.models import *
from django.contrib import auth
from common.views import *
from common.models import *
from django.db import connection, transaction
import requests
import sys

from pt_card.models import CmsImageInfo, PtCard, PtCardScope
from pt_shelves.settings import MY_HOST
from wallet.views.vip_pub import get_vip_third_category

try:
    reload(sys)
    sys.setdefaultencoding('utf8')
except:
    pass


class PtConst:
    PT_CARD = '葡萄卡管理'
    host = MY_HOST
    # 实体卡
    ADDPTCARD = 'http://api.%sputao.so/svip/ptcard/entity_card/add' % (host)
    UPDATEPTCARD = 'http://api.%sputao.so/svip/ptcard/entity_card/update' % (host)
    CREATECODES = 'http://api.%sputao.so/svip/ptcard/entity_card/query' % (host)

    # 葡萄卡商品
    ADDPTGOODS = 'http://api.%sputao.so/sopen/shop/card/shelves/add' % (host)
    # ADDPTGOODS = 'http://192.168.1.238:8080/pt_open/shop/card/shelves/add'
    UPDATEPTGOODS = 'http://api.%sputao.so/sopen/shop/card/shelves/update' % (host)
    # UPDATEPTGOODS = 'http://192.168.1.238:8080/pt_open/shop/card/shelves/update'
    DELETEPTGOODS = ''


def add_report_var(f):
    @functools.wraps(f)
    def _(*args, **kwargs):
        result = f(*args, **kwargs)
        # 查找所有的应用
        objs = AuthUserUserPermissions.objects.filter(user=args[0].user.id)
        items = []
        for obj in objs:
            if obj.permission.content_type_id == PermissionType.APP:
                items.append("['%s', '%s']" %
                             (obj.permission.name, obj.permission.codename))
        apps_str = "[%s]" % ",".join(items)
        vars = {
            "user": auth.get_user(args[0]).username,
            # "lasturl": args[0].path,
            "lasturl": args[0].get_full_path(),
            "apps": apps_str
        }
        for key in vars:
            result.content = result.content.replace(
                "{_tongji_begin_%s_end_}" % key, vars[key])
        return result
    return _



def get_gid_by_skuid_other(g_id,type):
    """
    用sku_id获取商品id,返回格式gid-sid
    0表示商品id
    1表示规格id
    :param id:
    :return:
    """
    if not g_id:
        return ''
    cursor = connections['cms_db'].cursor()
    if type == 0 :
        sql = """
        SELECT concat(CAST(goods_id AS CHAR),'-',CAST(sku_id AS CHAR)) FROM cms_sku where goods_id in (%s) ;"""
    else:
        sql = """
        SELECT concat(CAST(goods_id AS CHAR),'-',CAST(sku_id AS CHAR)) FROM cms_sku where sku_id in (%s);"""
    sqls = sql % (','.join(map(str,g_id.split(','))))
    cursor.execute(sqls)
    row =  cursor.fetchall()
    if row:
        r_d = [r[0] for r in row]
        return ','.join(r_d) if r_d else ''
    return ''


def get_ptcard_name(lt):
    """
    从葡萄卡id获取名字
    :param lt: 逗号分开的id,[1,2,3]
    :return:
    """
    try:
        data = PtCard.objects.filter(id__in=lt).values('name')
        if data:
            return [i['name'] for i in data]
        else:
            return []
    except Exception as e:
        return []

def get_ptcard_info(lt_id,gid,goods_name,cardType):
    """
    返回葡萄卡所有的信息
    :param lt_id:['1','2']
    :param gid:商品id
    :return:
    """
    r_data = {}
    cards = []
    gid_name = ''
    for i in lt_id:
        ptcardscope = PtCardScope.objects.filter(card_id=i)
        ptcard = PtCard.objects.get(id=i)
        all_scope = []
        for i in ptcardscope:
            c_ids = i.positive_second_category_id if i.positive_second_category_id is not None else ''
            c_ids_x = i.reverse_second_category_id if i.reverse_second_category_id is not None else ''
            s_ids = i.positive_category_id if i.positive_category_id is not None else ''
            s_ids_x = i.reverse_category_id if i.reverse_category_id is not None else ''
            cp_id = i.positive_cpid if i.positive_cpid is not None else ''
            cp_id_x = i.reverse_cpid if i.reverse_cpid is not None else ''
            g_id = i.positive_gid if i.positive_gid is not None else ''
            g_id_x = i.reverse_gid if i.reverse_gid is not None else ''
            sku_id = i.positive_skuid if i.positive_skuid is not None else ''
            sku_id_x = i.reverse_skuid if i.reverse_skuid is not None else ''
            g_format_id = get_gid_by_skuid_other(g_id,0)
            g_format_x_id = get_gid_by_skuid_other(g_id_x,0)
            s_format_id = get_gid_by_skuid_other(sku_id,1)
            s_format_x_id = get_gid_by_skuid_other(sku_id_x,1)
            format_id = g_format_id + ',' + s_format_id if g_format_id and s_format_id else g_format_id + s_format_id
            format_x_id = g_format_x_id + ',' + s_format_x_id if g_format_x_id and s_format_x_id else g_format_x_id + s_format_x_id
            all_scope.append(
                dict(
                    categoryIds= c_ids if c_ids else c_ids_x,
                    categoryReverse= 0 if c_ids else 1,
                    thirdCategoryIds=s_ids if s_ids else s_ids_x,
                    thirdCategoryReverse=0 if s_ids else 1,
                    cpIds=cp_id if cp_id else cp_id_x,
                    cpReverse=0 if cp_id else 1,
                    goodsSkuIds=format_id if format_id  else format_x_id,
                    goodsReverse=0 if format_id else 1,
                )
            )
        cards.append(
            dict(
                ptCardApplyRangeList=all_scope,
                cardName=ptcard.name,
                picture=ptcard.icon,
                price=ptcard.retail_price,
                ptCardEffectiveDays=ptcard.expire_dates,
                ptShelvesCardId=ptcard.id,
                remarks=ptcard.remark,
                serviceCount=ptcard.usable_times,
                serviceLength=ptcard.service_length,
                subOrderCancelTimeLimit=ptcard.cancel_minutes,
                useDesc=ptcard.instruction,
                serviceLengthUnit=0,
            )
        )
        gid_name = ptcard.name
    r_data['cardsJson'] = json.dumps(cards)
    r_data['goodsName'] = goods_name if goods_name else gid_name
    r_data['goodsShelvesId'] = gid
    r_data['cardType'] = cardType
    return r_data

def get_table_paginator(objs, per_page, cur_page):
    """
    获取分页
    :param objs: list
    :param per_page: 每页个数
    :param cur_page: 当前页码
    :return: 当前页数据和总得页数
    """
    paginator = Paginator(objs, per_page)
    try:
        result = paginator.page(cur_page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        result = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        result = paginator.page(paginator.num_pages)
    return result, paginator.num_pages


@login_required
def search_image(request):
    per_page = request.GET.get("per_page", 36)
    cur_page = request.GET.get("cur_page", 1)
    key = request.GET.get("key")
    image_category = request.GET.get('image_category')
    search_datas = CmsImageInfo.objects.using('cms_db').filter(image_category=image_category, image_name__contains=key).values_list(
        'image_name', 'image_category', 'image_url', 'id')
    result, num_pages = get_table_paginator(search_datas, per_page, cur_page)
    if search_datas:
        # return HttpResponse(json.dumps([list(result), num_pages]))
        c = json.dumps([list(result), num_pages])
    else:
        c = json.dumps([[], num_pages])
    return HttpResponse(c)


@login_required
def get_category_list(request):
    """
    获取二级分类列表
    """
    from pt_card.models import CmsNaviCategory
    cnc = CmsNaviCategory.objects.using('cms_db').filter(
        parent_id=0, fatherid=0, type__gt=0).only("id", "name").order_by("-id")
    return HttpResponse(json.dumps([dict(id=c.id, name=c.name) for c in cnc]), content_type="application/json")


@login_required
def get_sanji_list(request):
    """
    从二级筛三级
    """
    json_string = request.body.decode('utf-8')
    try:
        request_data = json.loads(json_string)
        if request_data:
            cids = request_data.get('cat_ids', "('')")
            sql = '''
                    SELECT c1.id,c1.NAME FROM cms_navi_category c1 LEFT JOIN cms_navi_category c2 ON c1.fatherId = c2.id WHERE c1.fatherId IN (SELECT id FROM cms_navi_category
          WHERE parent_id = 0 AND fatherId = 0 AND type > 0 and id in %s)  ORDER BY c1.fatherId;
                '''
            cur = connections['cms_db'].cursor()
            cur.execute(sql % cids)
            row = cur.fetchall()
            data = [dict(id=r[0], name=r[1]) for r in row]
    except:
        data = {"msg": u"未获取到参数", "code": 1}
    return HttpResponse(json.dumps(data), content_type="application/json")


@login_required
def get_all_sanji(request):
    """
    获取所有三级分类列表
    :param request:
    :return:
    """
    sql = '''SELECT c1.id,c1.NAME FROM cms_navi_category c1 LEFT JOIN cms_navi_category c2 ON c1.fatherId = c2.id WHERE c1.fatherId IN (SELECT id FROM cms_navi_category
          WHERE parent_id = 0 AND fatherId = 0 AND type > 0)  ORDER BY c1.fatherId;
                '''
    cur = connections['cms_db'].cursor()
    cur.execute(sql)
    row = cur.fetchall()
    data = [dict(id=r[0], name=r[1]) for r in row]
    return HttpResponse(json.dumps(data), content_type="application/json")


@login_required
def get_all_cps(request):
    """
    获取所有cps
    :param request:
    :return:
    """
    sql = '''SELECT a.id,a.name
                FROM
                    (SELECT cms_cp.*
                     FROM
                        view_cms_goods_formal
                        AS cms_goods
                     LEFT JOIN cms_cp
                     ON cms_goods.cp_name=cms_cp.name
                     WHERE  card_type = 0
                          AND pay_way = 0
                          AND is_post_paied_goods = 0)
                  AS a
                GROUP BY a.id,a.name;
                '''
    cur = connections['cms_db'].cursor()
    cur.execute(sql)
    row = cur.fetchall()
    data = [dict(id=r[0], name=r[1]) for r in row]
    return HttpResponse(json.dumps(data), content_type="application/json")


@login_required
def get_cps_list(request):
    """
    获取服务商列表
    """
    # cps = PAppInfo.objects.using('open').all().only("pid", "name")
    json_string = request.body.decode('utf-8')
    try:
        request_data = json.loads(json_string)
        if request_data:
            cids = request_data.get('cat_ids', "('')")
            sql = '''
                SELECT a.id,a.name
                FROM
                    (SELECT cms_cp.*
                     FROM
                        view_cms_goods_formal
                        AS cms_goods
                     LEFT JOIN cms_cp
                     ON cms_goods.cp_name=cms_cp.name
                     WHERE cms_goods.new_second_category
                     IN %s AND card_type = 0
                AND pay_way = 0
                AND is_post_paied_goods = 0)
                AS a
                GROUP BY a.id,a.name;
            '''
            cur = connections['cms_db'].cursor()
            cur.execute(sql % cids)
            row = cur.fetchall()
            data = [dict(id=r[0], name=r[1]) for r in row]
    except:
        data = {"msg": u"未获取到参数", "code": 1}
    return HttpResponse(json.dumps(data), content_type="application/json")

# @login_required
def get_goods_san_cp(request):
    """
    根据三级和cp获取商品列表
    """
    json_string = request.body.decode('utf-8')
    try:
        request_data = json.loads(json_string)
        if request_data:
            cids = request_data.get('cids', "''")
            sids = request_data.get('sids', "''") if request_data.get('sids', "''") else "''"
            time_type = request_data.get('type', "")
            time_value = int(request_data.get(
                'time')) * 60 if time_type == "hour" and request_data.get('time') else request_data.get('time')

            sql = '''
                SELECT DISTINCT a.goods_id AS gid
                       ,a.name
                       ,IFNULL(s.sku_name,"") AS sku_name
                       ,IFNULL(s.sku_id,0) AS sku_id
                       ,a.open_service_id
                       ,a.city
                       ,s.service_length
                       ,a.cp_name
                FROM view_cms_goods_formal a
                LEFT JOIN cms_sku s
                ON s.goods_id=a.goods_id
                WHERE card_type = 0
                AND pay_way = 0
                AND is_post_paied_goods = 0
                AND (open_service_id IN (%s) and new_second_category in (%s) )
            '''
            if time_value and time_value != '0':
                sql += "AND s.service_length = %s" % time_value

            cur = connections['cms_db'].cursor()
            sql_exe = sql % (",".join(map(str, cids)),
                             ",".join(map(str, sids)))
            cur.execute(sql_exe)
            row = cur.fetchall()
            data = [dict(gid=("s" + str(r[3])) if r[3] else ("g" + str(r[0])),
                         name=("-".join([r[1], str(r[2]), r[7], ','.join(r[5].split(',')[0:3])]))
                         if r[3] else ("-".join([r[1], str(r[2] if r[2] != r[1] else ''), r[7], ','.join(r[5].split(',')[0:3])]))) for r in row]
            return HttpResponse(json.dumps(data), content_type="application/json")
    except Exception as e:
        data = {"msg": e.message, "code": 1}
    return HttpResponse(json.dumps(data), content_type="application/json")

# @login_required
def get_goods_list(request):
    """
    根据cp获取商品列表
    """
    json_string = request.body.decode('utf-8')
    try:
        request_data = json.loads(json_string)
        if request_data:
            cids = request_data.get('cids', "''")
            sids = request_data.get('sids', "''") if request_data.get('sids', "''") else "''"
            eids = request_data.get('eids', "''")
            time_type = request_data.get('type', "")
            time_value = int(request_data.get(
                'time')) * 60 if time_type == "hour" and request_data.get('time') else request_data.get('time')

            sql = '''
                SELECT DISTINCT a.goods_id AS gid
                       ,a.name
                       ,IFNULL(s.sku_name,"") AS sku_name
                       ,IFNULL(s.sku_id,0) AS sku_id
                       ,a.open_service_id
                       ,a.city
                       ,s.service_length
                       ,a.cp_name
                FROM view_cms_goods_formal a
                LEFT JOIN cms_sku s
                ON s.goods_id=a.goods_id
                WHERE card_type = 0
                AND pay_way = 0
                AND is_post_paied_goods = 0
                AND (open_service_id IN (%s) or new_second_category in (%s) or new_category in (%s))
            '''
            if time_value and time_value != '0':
                sql += "AND s.service_length = %s" % time_value

            cur = connections['cms_db'].cursor()
            sql_exe = sql % (",".join(map(str, cids)),
                             ",".join(map(str, sids)),
                             ",".join(map(str, eids)))
            cur.execute(sql_exe)
            row = cur.fetchall()
            data = [dict(gid=("s" + str(r[3])) if r[3] else ("g" + str(r[0])),
                         name=("-".join([r[1], str(r[2]), r[7], ','.join(r[5].split(',')[0:3])]))
                         if r[3] else ("-".join([r[1], str(r[2] if r[2] != r[1] else ''), r[7], ','.join(r[5].split(',')[0:3])]))) for r in row]
            return HttpResponse(json.dumps(data), content_type="application/json")
    except Exception as e:
        data = {"msg": e.message, "code": 1}
    return HttpResponse(json.dumps(data), content_type="application/json")


@login_required
def get_serch_goods(request):
    """
    根据名字获取商品id
    """
    json_string = request.body.decode('utf-8')
    try:
        request_data = json.loads(json_string)
        if request_data:
            wrd = request_data.get('kwrd', "")
            time_type = request_data.get('type', "")
            time = request_data.get('time')
            time_value = int(time) * 60 if time_type == "hour" and time else time

            sql = '''
                SELECT DISTINCT a.goods_id AS gid
                       ,a.name
                       ,IFNULL(s.sku_name,"") AS sku_name
                       ,IFNULL(s.sku_id,0) AS sku_id
                       ,a.open_service_id
                       ,a.city
                       ,s.service_length
                       ,a.cp_name
                FROM view_cms_goods_formal a
                LEFT JOIN cms_sku s
                ON s.goods_id=a.goods_id
                WHERE card_type = 0
                AND pay_way = 0
                AND is_post_paied_goods = 0
                AND name Like  %s
            '''
            if time_value and time_value != '0':
                sql += "AND s.service_length = %s" % time_value
            q_word = '%' + wrd + '%'

            cur = connections['cms_db'].cursor()
            cur.execute(sql, q_word)
            row = cur.fetchall()
            data = [dict(gid=("s" + str(r[3])) if r[3] else ("g" + str(r[0])),
                         name=("-".join([r[1], str(r[2]), r[7], ','.join(r[5].split(',')[0:3])]))
                         if r[3] else ("-".join([r[1], str(r[2] if r[2] != r[1] else ''), r[7], ','.join(r[5].split(',')[0:3])]))) for r in row]
            return HttpResponse(json.dumps(data), content_type="application/json")
    except Exception as e:
        data = {"msg": e.message, "code": 1}
    return HttpResponse(json.dumps(data), content_type="application/json")


def get_erji_id(id,lt_id=None):
    """
    三级id获取二级id
    :param id:
    :return:
    """
    if lt_id == None:
        sql = '''SELECT c2.id FROM cms_navi_category c1 LEFT JOIN cms_navi_category c2 ON c1.fatherId = c2.id WHERE c1.fatherId IN (SELECT id FROM cms_navi_category
              WHERE parent_id = 0 AND fatherId = 0 AND type > 0) and c1.id=%s ORDER BY c1.fatherId;'''
        cur = connections['cms_db'].cursor()
        cur.execute(sql,[id])
        r_data = cur.fetchone()
        data = r_data[0] if r_data is not None else ''
    else:
        sql = '''SELECT distinct c2.id FROM cms_navi_category c1 LEFT JOIN cms_navi_category c2 ON c1.fatherId = c2.id WHERE c1.fatherId IN (SELECT id FROM cms_navi_category
                      WHERE parent_id = 0 AND fatherId = 0 AND type > 0) and c1.id in (%s) ORDER BY c1.fatherId;'''
        sqls = sql % (','.join(map(str,lt_id)))
        cur = connections['cms_db'].cursor()
        cur.execute(sqls)
        r_data = cur.fetchall()
        data = [r[0] for r in r_data] if r_data[0][0] is not None and r_data else []
    return data

def get_category_list_local():
    """
    本地获取二级分类列表
    """
    from pt_card.models import CmsNaviCategory
    cnc = CmsNaviCategory.objects.using('cms_db').filter(
        parent_id=0, fatherid=0, type__gt=0).only("id", "name").order_by("-id")
    return [c.id for c in cnc]

def get_all_sanji_local():
    """
    本地获取所有三级分类列表
    :param request:
    :return:
    """
    sql = '''SELECT c1.id,c1.NAME FROM cms_navi_category c1 LEFT JOIN cms_navi_category c2 ON c1.fatherId = c2.id WHERE c1.fatherId IN (SELECT id FROM cms_navi_category
          WHERE parent_id = 0 AND fatherId = 0 AND type > 0)  ORDER BY c1.fatherId;
                '''
    cur = connections['cms_db'].cursor()
    cur.execute(sql)
    row = cur.fetchall()
    data = [r[0] for r in row]
    return data

def get_all_goods(request):
    """
    获取所有商品
    """
    json_string = request.body.decode('utf-8')
    try:
        request_data = json.loads(json_string)
        if request_data:
            cids = request_data.get('cids', "''")
            sids = request_data.get('sids', "''") if request_data.get('sids', "''") else "''"
            eids = request_data.get('eids', "''")
            time_type = request_data.get('type', "")
            time_value = int(request_data.get(
                'time')) * 60 if time_type == "hour" and request_data.get('time') else request_data.get('time')

            sql = '''
                SELECT DISTINCT a.goods_id AS gid
                       ,a.name
                       ,IFNULL(s.sku_name,"") AS sku_name
                       ,IFNULL(s.sku_id,0) AS sku_id
                       ,a.open_service_id
                       ,a.city
                       ,s.service_length
                       ,a.cp_name
                FROM view_cms_goods_formal a
                LEFT JOIN cms_sku s
                ON s.goods_id=a.goods_id
                WHERE card_type = 0
                AND pay_way = 0
                AND is_post_paied_goods = 0
            '''
            if time_value and time_value != '0':
                sql += "AND s.service_length = %s" % time_value

            cur = connections['cms_db'].cursor()
            sql_exe = sql
            cur.execute(sql_exe)
            row = cur.fetchall()
            data = [dict(gid=("s" + str(r[3])) if r[3] else ("g" + str(r[0])),
                         name=("-".join([r[1], str(r[2]), r[7], ','.join(r[5].split(',')[0:3])]))
                         if r[3] else ("-".join([r[1], str(r[2] if r[2] != r[1] else ''), r[7], ','.join(r[5].split(',')[0:3])]))) for r in row]
            return HttpResponse(json.dumps(data), content_type="application/json")
    except Exception as e:
        data = {"msg": e.message, "code": 1}
    return HttpResponse(json.dumps(data), content_type="application/json")


def update_goods_id(gid):
    """
    更新葡萄卡商品管理的卡信息
    :return:
    """
    cursor = connections['pt_card'].cursor()
    sql = "SELECT * FROM pt_vip.pt_card_goods where pt_cids like '%,"+gid+",%' or pt_cids like '%,"+gid+"' or pt_cids like '"+gid+",%' or pt_cids = '"+gid+"'"
    cursor.execute(sql)
    cur = cursor.fetchall()
    if cur:
        lists = cur
    else :
        lists = []
    return lists