# -*- coding: utf-8 -*-
# Author:songroger
# Jun.23.2016
from __future__ import unicode_literals
from __future__ import division
import json
import time

import requests

from .models import CouponResource, CouponAllot, CouponCodeMain, \
    ShareActivity, CouponResourceScope, InviteAward, CouponAllotRecord
from django.db.models import Q
from django.core.paginator import Paginator
from pttools.ptapps import code_gen
from main.models import CmsNaviCategory
from django.db import connection, connections, transaction, IntegrityError
from .click_action import click_action_url
import traceback
import logging
from datetime import datetime, timedelta

log = logging.getLogger("main.app")


def get_coupon_list(page, limit, scope, kwd):
    data = {}
    data['coupons'] = []
    coupons = CouponResource.objects.using('activity').all().order_by('-id')
    if scope:
        coupons = coupons.filter(scope=scope)
    if kwd:
        coupons = coupons.filter(
            id__contains=kwd) | coupons.filter(name__contains=kwd)
    p = Paginator(coupons, limit)
    if page > p.num_pages:
        return data
    cps = p.page(page)
    cids = [c.id for c in cps]
    count_dict = _get_count_dict(cids)

    data['coupons'] = [
        dict(id=c.id,
             name=c.name,
             scope=c.scope,
             biz_type=c.biz_type,
             reason=c.reason,
             amount=c.amount if c.biz_type == 1 else c.amount / 100,
             start_time=c.start_time.strftime(
                 "%Y/%m/%d %H:%M") if c.start_time else '',
             end_time=c.end_time.strftime(
                 "%Y/%m/%d %H:%M") if c.end_time else '',
             min_consume=c.min_consume if not c.min_consume else c.min_consume / 100,
             # coupon_count=_get_coupon_count(c.id),
             # used_count=_get_used_coupon_count(c.id)
             coupon_count=int(count_dict.get("coupon_count").get(
                 c.id)) if count_dict.get("coupon_count").get(c.id) else 0,
             used_count=int(count_dict.get("used_count").get(
                 c.id) if count_dict.get("used_count").get(c.id) else 0)
             ) for c in cps]

    data["total"] = p.count
    data['page'] = page
    data["totalpage"] = p.num_pages
    data["hasNext"] = cps.has_next()
    return data


def _get_count_dict(cids):
    data = {}
    data["coupon_count"] = {}
    data["used_count"] = {}
    # c_sql = """
    # SELECT cid, COUNT(cid)
    # FROM coupon_allot
    # WHERE cid IN ("279","278") AND STATUS=0
    # GROUP BY cid;
    # """
    sql = """
    SELECT cid
      ,SUM(CASE WHEN STATUS = 0 or 1 THEN 1 ELSE 0 END) AS TOTAL_COUNT
      ,SUM(CASE WHEN STATUS = 1 THEN 1 ELSE 0 END) AS STATUS_1_COUNT
    FROM coupon_allot
    WHERE cid IN (%s)
    GROUP BY cid;
    """
    cur = connections['activity'].cursor()
    sql_exe = sql % ",".join(map(str, cids))
    cur.execute(sql_exe)
    row = cur.fetchall()
    for r in row:
        data["coupon_count"].update({r[0]: r[1]})
        data["used_count"].update({r[0]: r[2]})

    return data


def _get_coupon_count(cid):
    count = CouponAllot.objects.using('activity').filter(cid=cid).count()
    return count


def _get_used_coupon_count(cid):
    count = CouponAllot.objects.using(
        'activity').filter(cid=cid, status=1).count()
    return count


def delete_coupon(cid):
    try:
        coupon = CouponResource.objects.using('activity').get(id=cid)
        coupon.delete()
        data = {"msg": u"删除成功", "code": 0}
    except CouponResource.DoesNotExist:
        data = {"msg": u"优惠券不存在", "code": 1}

    return data


def get_coupon(cid):
    data = {}
    try:
        coupon = CouponResource.objects.using("activity").get(id=cid)
        crs = CouponResourceScope.objects.using("activity").filter(cid=cid)
        data["data"] = {"id": coupon.id,
                        "name": coupon.name,
                        "start_time": coupon.start_time.strftime(
                            "%Y-%m-%d %H:%M") if coupon.start_time else '',
                        "end_time": coupon.end_time.strftime(
                            "%Y-%m-%d %H:%M") if coupon.end_time else '',
                        "scope": coupon.scope,
                        "remark": coupon.remark,
                        "amount": coupon.amount if coupon.biz_type == 1 else coupon.amount / 100,
                        "min_consume": coupon.min_consume if not coupon.min_consume else coupon.min_consume / 100,
                        "consume_remark": coupon.consume_remark,
                        "is_mutex": coupon.is_mutex,
                        "cost_type": coupon.cost_type,
                        "cp_cost": coupon.cp_cost,
                        "putao_cost": coupon.putao_cost,
                        "biz_type": coupon.biz_type,
                        "effect_type": coupon.effect_type,
                        "effect_days": coupon.effect_days,
                        "all_scope": [dict(cps=cr.cps,
                                           cps_x=cr.cps_x,
                                           goods_cat=cr.goods_cat,
                                           goods_cat_x=cr.goods_cat_x,
                                           gids=cr.gids,
                                           gids_x=cr.gids_x)
                                      for cr in crs],
                        "click_action": coupon.click_action,
                        "reason": coupon.reason
                        }
        data["code"] = 0
    except CouponResource.DoesNotExist:
        data = {"msg": u"优惠券不存在", "code": 1}

    return data


def add_coupon(request):
    """
    添加优惠券
    """
    data = {}
    c_user = request.user.username
    json_string = request.body.decode('utf-8')
    try:
        request_data = json.loads(json_string)
        if request_data:
            scope = request_data.get('scope', None)
            name = request_data.get('name', None)
            remark = request_data.get('remark', None)
            amount = request_data.get('amount', None)
            min_consume = request_data.get('min_consume', None)
            consume_remark = request_data.get('consume_remark', None)
            start_time = request_data.get('start_time', None)
            end_time = request_data.get('end_time', None)
            is_mutex = request_data.get('is_mutex', None)
            cost_type = request_data.get('cost_type', None)
            cp_cost = request_data.get('cp_cost', None)
            putao_cost = request_data.get('putao_cost', None)
            all_scope = request_data.get('all_scope', [])
            biz_type = request_data.get('biz_type', None)
            effect_type = request_data.get('effect_type', 0)
            effect_days = request_data.get('effect_days', None)
            reason = request_data.get('reason', None)
            click_action, goods_ids = click_action_url(all_scope)
            gids = ','.join(map(lambda x: str(x), goods_ids))

            if biz_type == "0":
                amount = round(float(amount) * 100)

            _create_coupon(name, scope, remark, amount, biz_type, min_consume,
                           consume_remark, start_time, end_time, is_mutex,
                           cost_type, cp_cost, putao_cost, c_user, all_scope,
                           gids, effect_type, effect_days, reason, click_action)

            return {"msg": u"添加成功", "code": 0}
        data = {"msg": u"缺少参数", "code": 1}
    except:
        data = {"msg": u"添加失败", "code": 1}

    return data


def _create_coupon(name, scope, remark, amount, biz_type, min_consume,
                   consume_remark, start_time, end_time, is_mutex,
                   cost_type, cp_cost, putao_cost, c_user, all_scope,
                   gids, effect_type, effect_days, reason, click_action=None):
    """
    创建优惠券及优惠券适用范围
    """
    cr = CouponResource.objects.using('activity'). \
        create(name=name,
               scope=scope,
               remark=remark,
               amount=float(amount) if amount else None,
               biz_type=int(biz_type),
               min_consume=round(float(min_consume) *
                                 100) if min_consume else None,
               consume_remark=consume_remark,
               start_time=start_time if start_time else None,
               end_time=end_time if end_time else None,
               is_mutex=int(is_mutex) if is_mutex else None,
               cost_type=int(cost_type) if cost_type else None,
               cp_cost=float(cp_cost) if cp_cost else None,
               putao_cost=float(putao_cost) if putao_cost else None,
               c_user=c_user,
               gids=gids,
               effect_type=int(effect_type),
               effect_days=int(effect_days) if effect_days else None,
               click_action=click_action,
               reason=reason
               )
    for a in all_scope:
        _create_coupon_scope(cr.id,
                             a.get('cps', None),
                             a.get('cps_x', None),
                             a.get('goods_cat', None),
                             a.get('goods_cat_x', None),
                             a.get('gids', None),
                             a.get('gids_x', None)
                             )


def _create_coupon_scope(cid, cps, cps_x, goods_cat,
                         goods_cat_x, gids, gids_x):
    """
    创建优惠券适用范围
    """
    CouponResourceScope.objects.using("activity"). \
        create(cid=cid,
               cps=cps,
               cps_x=cps_x,
               goods_cat=goods_cat,
               goods_cat_x=goods_cat_x,
               gids=gids,
               gids_x=gids_x
               )


def up_coupon(request, cid):
    data = {}
    m_user = request.user.username
    json_string = request.body.decode('utf-8')
    try:
        request_data = json.loads(json_string)
        if request_data:
            coupon = CouponResource.objects.using('activity').filter(id=cid)

            scope = request_data.get('scope', coupon[0].scope)
            name = request_data.get('name', coupon[0].name)
            remark = request_data.get('remark', coupon[0].remark)
            amount = request_data.get('amount')
            min_consume = request_data.get('min_consume')
            consume_remark = request_data.get(
                'consume_remark', coupon[0].consume_remark)
            start_time = request_data.get('start_time', coupon[0].start_time)
            end_time = request_data.get('end_time', coupon[0].end_time)
            is_mutex = request_data.get('is_mutex', coupon[0].is_mutex)
            cost_type = request_data.get('cost_type', coupon[0].cost_type)
            cp_cost = request_data.get('cp_cost', coupon[0].cp_cost)
            putao_cost = request_data.get('putao_cost', coupon[0].putao_cost)
            all_scope = request_data.get('all_scope', [])
            biz_type = request_data.get('biz_type', coupon[0].biz_type)
            effect_type = request_data.get(
                'effect_type', coupon[0].effect_type)
            effect_days = request_data.get(
                'effect_days', coupon[0].effect_days)
            reason = request_data.get('reason', coupon[0].reason)
            click_action, goods_ids = click_action_url(all_scope)
            gids = ','.join(map(lambda x: str(x), goods_ids))

            if biz_type == "0":
                amount = round(float(amount) * 100)

            coupon.update(name=name,
                          scope=scope,
                          remark=remark,
                          amount=float(amount) if amount else None,
                          biz_type=biz_type,
                          min_consume=round(
                              float(min_consume) * 100) if min_consume else None,
                          consume_remark=consume_remark,
                          start_time=start_time,
                          end_time=end_time,
                          is_mutex=int(is_mutex) if is_mutex else None,
                          cost_type=int(cost_type) if cost_type else None,
                          cp_cost=float(cp_cost) if cp_cost else None,
                          putao_cost=float(putao_cost) if putao_cost else None,
                          m_user=m_user,
                          gids=gids,
                          effect_type=int(
                              effect_type) if effect_type else None,
                          effect_days=int(
                              effect_days) if effect_days else None,
                          click_action=click_action,
                          reason=reason
                          )

            CouponResourceScope.objects.using(
                'activity').filter(cid=cid).delete()
            for a in all_scope:
                _create_coupon_scope(cid,
                                     a.get('cps', None),
                                     a.get('cps_x', None),
                                     a.get('goods_cat', None),
                                     a.get('goods_cat_x', None),
                                     a.get('gids', None),
                                     a.get('gids_x', None)
                                     )

            return {"msg": u"修改成功", "code": 0}
        data = {"msg": u"无改动", "code": 1}
    except:
        data = {"msg": u"修改失败", "code": 1}

    return data


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
                     WHERE cms_goods.new_category
                     IN %s)
                AS a
                GROUP BY a.id,a.name;
            '''
            cur = connection.cursor()
            cur.execute(sql % cids)
            row = cur.fetchall()
            data = [dict(id=r[0], name=r[1]) for r in row]
    except:
        data = {"msg": u"未获取到参数", "code": 1}
    return data


def get_goods_list(request):
    """
    获取商品列表
    """
    json_string = request.body.decode('utf-8')
    try:
        request_data = json.loads(json_string)
        if request_data:
            cids = request_data.get('cids', "''")
            cat_ids = request_data.get('cat_ids', "''")

            sql = '''
                SELECT goods_id, name
                FROM view_cms_goods_formal
                where new_category IN (%s)
                and open_service_id IN (%s);
            '''

            cur = connection.cursor()
            sql_exe = sql % (",".join(map(str, cat_ids)),
                             ",".join(map(str, cids)))
            cur.execute(sql_exe)
            row = cur.fetchall()
            # goods = PGoodsInfo.objects.using('open').filter(
            #     appid__in=cids).only("pid", "name")
            data = [dict(cid=r[0], name=r[1]) for r in row]
            return data
    except:
        data = {"msg": u"未获取到参数", "code": 1}
    return data


def get_coupons():
    """
    获取coupons列表filter(end_time__gte=datetime.now())
    """
    cps = CouponResource.objects.using(
        'activity').all().only("id", "name").order_by("-id")
    data = [dict(cid=cp.id, name=cp.name) for cp in cps]
    return data


def get_coupons_valid():
    """
    获取coupons列表
    """
    cps = CouponResource.objects.using('activity').filter(
        Q(end_time__gte=datetime.now()) | Q(effect_type=1)).only("id", "name").order_by("-id")
    data = [dict(cid=cp.id, name=cp.name) for cp in cps]
    return data


def create_coupons(request):
    """
    生成对应优惠券的券码
    """
    data = {}
    c_user = request.user.username
    json_string = request.body.decode('utf-8')
    try:
        request_data = json.loads(json_string)
        if request_data:
            cids = request_data.get('cps', None)
            end_time = request_data.get('end_time', None)
            amount = request_data.get('amount', 0)
            is_muti = request_data.get('is_muti', None)

            if int(amount) > 20000:
                return {"msg": u"一次最多生成2万张", "code": 1}
            if int(amount) < 1:
                return {"msg": u"生成数量至少为1", "code": 1}

            coupon_code = CouponCodeMain.objects.using('activity'). \
                create(cids=cids,
                       amount=amount,
                       end_time=end_time,
                       is_muti=is_muti,
                       c_user=c_user,
                       )
            _code_generate(coupon_code.id, int(amount), is_muti)

            return {"msg": u"生成券码成功", "code": 0}
        data = {"msg": u"缺少参数", "code": 1}
    except:
        data = {"msg": u"生成失败", "code": 1}

    return data


def _code_generate(cid, amount, is_muti):
    cur = connections['activity'].cursor()

    if is_muti == 0:
        code = code_gen()
        code_str = [(cid, code, 0) for a in range(amount)]
        value_list = str(tuple(code_str))[1:-1].rstrip(",")
        code_sql = r'insert into `' + 'coupon_code_sub' + \
            '`(`main_id`,`exchange_code`,`status`) values ' + \
            value_list + ';'
        cur.execute(code_sql)
    elif is_muti == 1:
        code_str = [(cid, code_gen(), 0) for a in range(amount)]
        value_list = str(tuple(code_str))[1:-1].rstrip(",")
        code_sql = r'insert into `' + 'coupon_code_sub' + \
            '`(`main_id`,`exchange_code`,`status`) values ' + \
            value_list + ';'
        cur.execute(code_sql)
    else:
        cur.close()


def get_coupon_created_list(page, limit):
    data = {}
    data['coupons'] = []
    coupons = CouponAllotRecord.objects.using('activity').order_by('-id')
    # coupons = _get_allot_coupons_list()

    p = Paginator(coupons, limit)
    if page > p.num_pages:
        return data
    cps = p.page(page)

    # data['coupons'] = [
    #     dict(count=c[2],
    #          name=c[1],
    #          reason=c[0],
    #          operator=c[4],
    #          start_time=c[3].strftime('%Y-%m-%d %H:%M:%S'),
    #          user_count=c[5],
    #          ) for c in cps]
    data['coupons'] = [
        dict(name=c.cnames,
             count=c.count,
             user_count=c.ucount,
             reason=c.reason,
             start_time=c.allot_time.strftime('%Y-%m-%d %H:%M:%S'),
             operator=c.c_user,
             ) for c in cps]

    data["total"] = p.count
    data['page'] = page
    data["totalpage"] = p.num_pages
    data["hasNext"] = cps.has_next()
    return data


def _get_allot_coupons_list():
    cur = connections['activity'].cursor()
    sql = '''
        SELECT a.reason
               ,GROUP_CONCAT(DISTINCT r.name) AS coupons_name
               ,COUNT(a.id) AS allot_count
               ,MIN(a.allot_time) AS allot_time
               ,MAX(a.c_user) AS c_user
               ,COUNT(DISTINCT a.uid) AS user_count
        FROM coupon_allot AS a
        LEFT JOIN coupon_resource r
          ON a.cid = r.id
        WHERE a.reason IS NOT NULL
        GROUP BY a.reason
        ORDER BY allot_time DESC
    '''
    cur.execute(sql)
    row = cur.fetchall()
    return row


def allot_coupon_to(request):
    """
    发放指定券给用户
    @parameter：is_phone: 0 用户ID，1 用户手机
    """
    data = {}
    c_user = request.user.username
    json_string = request.body.decode('utf-8')
    try:
        request_data = json.loads(json_string)
        if request_data:
            reason = request_data.get('reason', '')

            uids = request_data.get('uids', [])
            cids = request_data.get('cids', [])
            pids = request_data.get('pids', [])
            is_phone = int(request_data.get('is_p', "2"))
            names = _get_coupons_name(cids)
            cnames = []
            vcids = []  # 有效发券ID
            vto_uids = []  # 有效到券人
            count = 0  # 有效发券总数

            to_uids_filter = {0: lambda uids, pids, c: _allot_filter(_filter_uid_by_uids(uids), c),
                              1: lambda uids, pids, c: _allot_filter(_get_uid_by_phone(pids), c),
                              2: lambda uids, pids, c: []}

            try:
                with transaction.atomic():
                    for c in cids:
                        start_time, end_time = _get_coupon_time(c)
                        # to_uids = _allot_filter(uids, c)
                        to_uids = to_uids_filter.get(is_phone)(uids, pids, c)
                        name = names.get(c, None)
                        if to_uids:
                            vcids.append(c)
                            cnames.append(name)
                            ca_objects = [CouponAllot(cid=c,
                                                      uid=u,
                                                      name=name,
                                                      reason=reason,
                                                      start_time=start_time,
                                                      end_time=end_time,
                                                      c_user=c_user) for u in to_uids]
                            CouponAllot.objects.using(
                                "activity").bulk_create(ca_objects)
                            vto_uids.extend(to_uids)
                            count += len(to_uids)
                    if cnames and count:
                        ucount = len(set(vto_uids))
                        CouponAllotRecord.objects.using(
                            'activity').create(cids=','.join(map(str, vcids)),
                                               cnames=','.join(map(str, cnames)),
                                               count=count,
                                               ucount=ucount,
                                               reason=reason,
                                               c_user=c_user)

                return {"msg": u"发放成功", "code": 0}
            except IntegrityError:
                return {"msg": u"部分所选券数据错误", "code": 1}
        else:
            data = {"msg": u"缺少参数", "code": 1}
    except:
        data = {"msg": u"发放失败", "code": 1}

    return data


def _get_coupons_name(cids):
    cur = connections['activity'].cursor()
    sql = '''
        SELECT id, name
        FROM coupon_resource
        WHERE id in (%s);
    '''
    sql_exe = sql % ",".join(map(str, cids))
    cur.execute(sql_exe)
    row = cur.fetchall()
    data = {}
    for r in row:
        data.update({r[0]: r[1]})
    return data


def _filter_uid_by_uids(uids):
    cur = connections['user'].cursor()
    sql = """
        SELECT u_id FROM p_relate_user
        WHERE u_id IN (%s);
        """
    sql_exe = sql % ('"' + '","'.join(map(str, uids)) + '"')
    cur.execute(sql_exe)
    row = cur.fetchall()
    return [r[0] for r in row]


def _get_uid_by_phone(pids):
    cur = connections['user'].cursor()
    sql = """
        SELECT u_id FROM p_relate_user
        WHERE acc_source = 1
        AND acc_type = 1
        AND isUnbinding = 0
        AND name IN (%s);
        """
    sql_exe = sql % ('"' + '","'.join(map(str, pids)) + '"')
    cur.execute(sql_exe)
    row = cur.fetchall()
    return [r[0] for r in row]


def _allot_filter(uids, cid):
    cur = connections['activity'].cursor()
    sql = """
        SELECT uid
        FROM coupon_allot
        WHERE cid =%s AND uid IN (%s);
        """
    sql_exe = sql % (cid, '"' + '","'.join(map(str, uids)) + '"')
    cur.execute(sql_exe)
    row = cur.fetchall()
    nuid = [r[0] for r in row]

    return list(set(uids).difference(set(nuid)))


def _allot_coupon(sql_str):
    cur = connections['activity'].cursor()
    value_list = str(tuple(sql_str))[1:-1].rstrip(",")
    sql_exe = u'insert into `' + 'coupon_allot' + \
        '`(`cid`,`uid`,`allot_time`,`status`,`reason`,`name`,`start_time`,`end_time`,`c_user`) values '\
        + value_list + ';'
    cur.execute(sql_exe)
    cur.close()


def _get_coupon_time(cid):
    get_time_dict = {"0": lambda cr: {"start_time": cr.start_time,
                                      "end_time": cr.end_time},
                     "1": lambda cr: {"start_time": datetime.now(),
                                      "end_time": datetime.now() +
                                      timedelta(days=int(cr.effect_days))}}
    cr = CouponResource.objects.using("activity").get(id=cid)
    try:
        start_time = get_time_dict.get(str(cr.effect_type))(cr)["start_time"]
        end_time = get_time_dict.get(str(cr.effect_type))(cr)["end_time"]
    except:
        return "", ""
    return start_time, end_time


def get_codes_list(request):
    """
    获取券码批次列表
    """
    data = []
    code_sub = _get_code_sub_id()
    ccm = CouponCodeMain.objects.using(
        'activity').filter(id__in=code_sub).only("id", "cids", "c_time"). \
        order_by("-c_time")

    for c in ccm:
        # name = [cr.name for cr in CouponResource.objects.using(
        #     'activity').filter(id__in=c.cids.split(","))]
        # if name:
        data.append(dict(id=c.id, name=c.cids,
                         c_time=c.c_time.strftime("%Y/%m/%d %H:%M")))
    return data


def _get_code_sub_id():
    sql = """
    SELECT DISTINCT main_id FROM coupon_code_sub ORDER BY main_id;
    """
    cur = connections['activity'].cursor()
    cur.execute(sql)
    row = cur.fetchall()
    return [r[0] for r in row]


def get_category_list(request):
    """
    获取分类列表
    """
    cnc = CmsNaviCategory.objects.filter(
        parent_id=0, fatherid=0, type__gt=0).only("id", "name").order_by("-id")
    return [dict(id=c.id, name=c.name) for c in cnc]


def json_get_cpname(data):
    # cid_data = '[' + data + ']'
    res = True
    cid_list = []
    try:
        cid_data = data
        cid_data = json.loads(cid_data)
        for j in cid_data:
            try:
                cid_list.append(int(j['cid']))
            except:
                res = False
    except:
        res = False
    # cid_list = [int(j['cid']) for j in cid_data]
    return [x.name for x in
            CouponResource.objects.using('activity').filter(id__in=cid_list)]


def json_get_cpname_aa(data):

    try:
        cid_data = list(data)
        for i in cid_data:
            if i['cids'] is not None:
                i['cids'] = [int(x) for x in i['cids'].split(',')]
                cids_list = [x.name for x in CouponResource.objects.using(
                    'activity').filter(id__in=i['cids'])]
                i['cids'] = cids_list
                i['vip_charge'] = ''
            else:
                i['cids'] = ''
                i['vip_charge'] = get_vip_name(i['vip_charge'])

    except:
        cid_data = []
    return cid_data


def json_get_cpname_a(data):
    # cid_data = '[' + data + ']'
    cid_list = []
    res = True
    try:
        cid_data = data
        cid_data = json.loads(cid_data)
        for j in cid_data['after']:
            try:
                cid_list.append(int(j['cid']))
            except:
                res = False
    except:
        res = False
    # cid_list = [int(j['cid']) for j in cid_data]
    return [x.name for x in
            CouponResource.objects.using('activity').filter(id__in=cid_list)]


def json_get_cpname_b(data):
    # cid_data = '[' + data + ']'
    cid_list = []
    res = True
    try:
        cid_data = data
        cid_data = json.loads(cid_data)
        for j in cid_data['before']:
            try:
                cid_list.append(int(j['cid']))
            except:
                res = False
    except:
        res = False
    # cid_list = [int(j['cid']) for j in cid_data]
    return [x.name for x in
            CouponResource.objects.using('activity').filter(id__in=cid_list)]


def get_invite_gift_list(page, limit):
    """
    分享有礼列表展示
    :param page: 当前页数
    :param limit:每页显示
    :return:
    """
    data = {}
    data['sharegift'] = []
    Shares = ShareActivity.objects.using(
        'activity').filter(share_type=1).order_by('-is_use', '-c_time', 'id')
    p = Paginator(Shares, limit)
    total_page = p.num_pages
    if page > total_page:
        return data
    cps = p.page(page)
    sharedata = []
    for c in cps:
        try:
            award = InviteAward.objects.using("activity").filter(
                share_activity_id=c.id).values('number', 'cids','vip_charge')

        except:
            award = []
        sharedata.append(dict(id=c.id,
                              name=c.name,
                              description=c.description,
                              cids_a=json_get_cpname_a(c.cids),
                              cids_b=json_get_cpname_b(c.cids),
                              v_cids_b=get_vip_name(str(c.before_vip_charge)) if c.before_vip_charge is not None else '',
                              v_cids_a=get_vip_name(str(c.after_vip_charge)) if c.after_vip_charge is not None else '',
                              start_time=c.start_time.strftime(
                                  "%Y/%m/%d %H:%M:%S") if c.start_time else '',
                              end_time=c.end_time.strftime(
                                  "%Y/%m/%d %H:%M:%S") if c.end_time else '',
                              is_user=c.is_use,
                              # daily_pick_limit=c.daily_pick_limit,
                              # link_valid_days=c.link_valid_days,
                              share_coupons=json_get_cpname(c.share_coupons),
                              v_share_coupons= get_vip_name(str(c.inviter_vip_charge)) if c.inviter_vip_charge is not None else '',
                              ye=c.guide_word,
                              award=json_get_cpname_aa(award),
                              ))
    data['sharegift'] = sharedata
    data["total"] = p.count
    data['page'] = page
    data["totalpage"] = total_page
    data["hasNext"] = cps.has_next()
    return data


def updown_share(request, id):
    """
    分享有礼上架
    :param request:
    :param id: 活动id
    :return:
    """
    data = {}
    sid = ShareActivity.objects.using('activity').filter(id=id)
    if sid:
        try:
            ShareActivity.objects.using(
                'activity').exclude(id=id).update(is_use=0)
            sid.update(is_use=1)
            data = {u"msg": u"上架成功", "code": 0}
        except:
            data = {u"msg": u"上架失败", "code": 1}
    else:
        data = {u"msg": u"无此id", "code": 1}
    return data


def down_share(request, id):
    """
    分享有礼下架
    :param request:
    :param id: 活动id
    :return:
    """
    data = {}
    sid = ShareActivity.objects.using('activity').filter(id=id)
    if sid:
        try:
            sid.update(is_use=0)
            data = {u"msg": u"下架成功", "code": 0}
        except:
            data = {u"msg": u"下架失败", "code": 1}
    else:
        data = {u"msg": u"无此id", "code": 1}
    return data


def json_get_cp(data):
    # cid_data = '[' + data + ']'
    if not data or data is None:
        return ''
    cid_data = json.loads(data)
    # c_id = []
    # for j in cid_data:
    #     c_id.append(j['cid'])
    return [j['cid']  if j else ''  for j in cid_data]


def cid_json_get_a(data):
    cid_data = json.loads(data)
    return [j['cid'] if j else '' for j in cid_data['after']]


def cid_json_get_b(data):
    cid_data = json.loads(data)
    return [j['cid']  if j else '' for j in cid_data['before']]


def get_time_chuo(str_time):
    return time.mktime(time.strptime(str_time, "%Y-%m-%d %H:%M:%S"))


def get_vip_list():
    """
    获取vip列表
    :return:
    """
    payload = {'cardId': 3, 'size': 9999999}
    r = requests.get('http://api.test.putao.so/svip/card/goods/listRecharge', params=payload)
    vip_r_data = r.json()['data']
    if not vip_r_data:
        return []
    data = []
    for vip in vip_r_data:
        if vip['usefulTime']:
            st_time = get_time_chuo(vip['usefulTime'].split('至')[0])
            en_time = get_time_chuo(vip['usefulTime'].split('至')[1])
            if time.time() >=st_time and time.time() <= en_time:
                data.append(dict(vid=vip['cardGoodsId'], vname=vip['goodsName']))
    return data


def get_vip_name(id):
    data = get_vip_list()
    try:
        for i in data:
            if i['vid'] == int(id) :
                return i['vname']
        return ''
    except:
        return ''


def get_invite(request, id):
    """
    通过id获取邀请有礼信息
    :param request:
    :param id:
    :return:
    """

    data = {}
    try:
        shares = ShareActivity.objects.using("activity").get(id=id)
        award = InviteAward.objects.using("activity").filter(
            share_activity_id=id).values('number', 'cids','vip_charge')
        award = list(award)
        data["data"] = {
            "id": shares.id,
            "name": shares.name,
            "description": shares.description,
            "cids_a": cid_json_get_a(shares.cids),
            "cids_b": cid_json_get_b(shares.cids),
            "v_cids_b": [str(shares.before_vip_charge)] if shares.before_vip_charge is not None else '',
            "v_cids_a": [str(shares.after_vip_charge)] if shares.after_vip_charge is not None else '',
            "start_time": shares.start_time.strftime(
                "%Y-%m-%d %H:%M") if shares.start_time else '',
            "end_time": shares.end_time.strftime(
                "%Y-%m-%d %H:%M") if shares.end_time else '',
            "is_user": shares.is_use,
            "share_coupons": json_get_cp(shares.share_coupons),
            "v_share_coupons": [str(shares.inviter_vip_charge)] if shares.inviter_vip_charge is not None else '',
            "ye": shares.guide_word,
            'award': award,
        }
        data["code"] = 0
    except Exception as e:
        data = {"msg": u"不存在", "code": 1}

    return data


def add_invite(request):
    """
    添加邀请有礼活动
    :param request:
    :return:
    """
    data = {}
    json_string = request.body.decode('utf-8')
    try:
        request_data = json.loads(json_string)
        if request_data:
            name = request_data.get('name', '')
            description = request_data.get('description', '')
            cids = request_data.get('cps', '')
            v_cids = request_data.get('v_cps', '')
            start_time = request_data.get('start_time', '')
            end_time = request_data.get('end_time', '')
            share_coupons_a = request_data.get('cps_a', [])
            share_coupons_b = request_data.get('cps_b', '')
            v_share_coupons_a = request_data.get('v_cps_a', '')
            v_share_coupons_b = request_data.get('v_cps_b', '')
            is_share_award = request_data.get('is_share_award', 1)
            nums = request_data.get('nums', [])
            number = request_data.get('number', []) if type(request_data.get(
                'number', [])) == list else [request_data.get('number', [])]
            guide_word = request_data.get('ye', '')
            if cids:
                if not isinstance(cids, list):
                    cids = [cids]
                cid_data = [dict({"cid": str(i), "percent": "100%",
                                  "useTime": time.strftime('%Y-%m-%d', time.localtime(time.time()))}) for i in
                            cids]
                cids = json.dumps(cid_data)
            elif v_cids and cids:
                return {"msg": u"邀请人获券只能选其一", "code": 1}
            elif v_share_coupons_a and len(share_coupons_a) != 0:
                return {"msg": u"被邀请人完成可领券只能选其一", "code": 1}
            elif v_share_coupons_b and len(share_coupons_b) != 0:
                return {"msg": u"邀请人可获券只能选其一", "code": 1}
            if share_coupons_b or share_coupons_a:
                if not isinstance(share_coupons_a, list):
                    a= []
                    if share_coupons_a:
                        a.append(str(share_coupons_a))
                    share_coupons_a = a
                if not isinstance(share_coupons_b, list):
                    a = []
                    if share_coupons_b :
                        a.append(str(share_coupons_b))
                    share_coupons_b = a
                share_data = {}
                if len(share_coupons_b) > 0:
                    share_data['before'] = [{"cid": str(i), "percent": "100%",
                                             "useTime": time.strftime('%Y-%m-%d', time.localtime(time.time()))} for i in
                                            share_coupons_b]
                else:
                    share_data['before'] = []
                if len(share_coupons_a)>0:
                    share_data['after'] = [{"cid": str(i), "percent": "100%",
                                            "useTime": time.strftime('%Y-%m-%d', time.localtime(time.time()))} for i in
                                           share_coupons_a]
                else:
                    share_data['after'] = []
                share_coupons = json.dumps(share_data)
            else:
                share_data = {}
                share_data['after'] = []
                share_data['before'] = []
                share_coupons = json.dumps(share_data)
            share = ShareActivity.objects.using('activity'). \
                create(name=name,
                       description=description,
                       cids=share_coupons,  # 被邀请人
                       before_vip_charge = int(v_share_coupons_b) if v_share_coupons_b else None,
                       after_vip_charge = int(v_share_coupons_a) if v_share_coupons_a else None,
                       start_time=start_time,
                       end_time=end_time,
                       is_use=0,
                       share_coupons=cids,  # 邀请人
                       inviter_vip_charge=int(v_cids) if v_cids else None,  # 邀请人
                       is_share_award=is_share_award,
                       guide_word=guide_word,
                       share_type=1,
                       )
            if number:
                for x, y in enumerate(number):
                    if nums[x]['st'] == 'nums':
                        InviteAward.objects.using('activity').create(
                            share_activity_id=share.id, number=y, cids=','.join(nums[x]['id']))
                    else:
                        InviteAward.objects.using('activity').create(
                            share_activity_id=share.id, number=y, vip_charge=int(nums[x]['id'][0]))
            return {"msg": u"添加成功", "code": 0}
        data = {"msg": u"缺少参数", "code": 1}
    except Exception as err:
        data = {"msg": u"添加失败", "code": 1}

    return data


def up_invite(request, id):
    """
    更新邀请有礼
    :param request:
    :param id:
    :return:
    """
    data = {}
    json_string = request.body.decode('utf-8')
    try:
        request_data = json.loads(json_string)
        share = ShareActivity.objects.using('activity').filter(id=id)

        if request_data and share:
            name = request_data.get('name', '')
            description = request_data.get('description', '')
            # cids = request_data.get('cps', '')
            # activity_rule = request_data.get('activity_rule', '')
            # coupon_count = request_data.get('coupon_count', '')
            start_time = request_data.get('start_time', '')
            end_time = request_data.get('end_time', '')
            # daily_pick_limit = request_data.get('daily_pick_limit', '')
            # link_valid_days = request_data.get('link_valid_days', 0)
            # share_coupons_a = request_data.get('cps_a', '')
            # share_coupons_b = request_data.get('cps_b', '')
            # share_count = request_data.get('share_count', '')
            is_share_award = request_data.get('is_share_award', 1)
            guide_word = request_data.get('ye', '')
            # if cids:
            #     if not isinstance(cids, list):
            #         cids = [cids]
            #     cid_data = [dict({"cid": str(i), "percent": "100%",
            #                       "useTime": time.strftime('%Y-%m-%d', time.localtime(time.time()))}) for i in
            #                 cids]
            #     cids = json.dumps(cid_data)
            # if share_coupons_a and share_coupons_b:
            #     if not isinstance(share_coupons_a, list):
            #         share_coupons_a = [share_coupons_a]
            #     if not isinstance(share_coupons_b, list):
            #         share_coupons_b = [share_coupons_b]
            #     share_data = {}
            #     share_data['before'] = [{"cid": str(i), "percent": "100%",
            #                              "useTime": time.strftime('%Y-%m-%d', time.localtime(time.time()))} for i in
            #                             share_coupons_b]
            #     share_data['after'] = [{"cid": str(i), "percent": "100%",
            #                             "useTime": time.strftime('%Y-%m-%d', time.localtime(time.time()))} for i in
            #                            share_coupons_a]
            #     share_coupons = json.dumps(share_data)
            share.using('activity').update(
                    # name=name,
                    # description=description,
                    # cids=share_coupons,  # 被邀请人
                    # activity_rule=activity_rule,
                    # coupon_count=int(coupon_count),
                    start_time=start_time,
                    end_time=end_time,
                    # is_use=0,
                    # daily_pick_limit=int(daily_pick_limit),
                    # link_valid_days=int(link_valid_days),
                    # share_coupons=cids,  # 邀请人
                    # share_count=int(share_count),
                    # is_share_award=is_share_award,
                    guide_word=guide_word,
                    share_type=1,
                )

            return {"msg": u"添加成功", "code": 0}
        data = {"msg": u"缺少参数", "code": 1}
    except Exception as err:
        data = {"msg": u"添加失败", "code": 1}

    return data


def get_share_activity_list(request):
    sql = """
    SELECT id, name
    FROM share_activity ORDER BY id;
    """
    cur = connections['activity'].cursor()
    cur.execute(sql)
    row = cur.fetchall()
    return [dict(id=r[0], name=r[1]) for r in row]
