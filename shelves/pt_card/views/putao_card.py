# coding: utf-8
import json
from decimal import Decimal

import requests
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render_to_response
from math import ceil

from common.views import add_common_var
from common.views import report_render
from phone_fee.models import CpPhoneFeeProduct, PtDaojiaOrderGuarantee
from pt_card.click_action import click_action_url, filter_gids
from pt_card.models import PtCard, PtCardScope, PtCardGoods, PtEntityCard
from pt_card.views.pt_card_pub import PtConst, Paginator, HttpResponse, get_ptcard_info, update_goods_id
from wallet.views import vip_pub
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.hashers import make_password
from django.template import RequestContext
from django.db import connection, transaction
import time


def get_putao_card_list(request):
    """
    葡萄卡列表
    :param request:
    :return:
    """
    try:
        data = {}
        per_page = int(request.GET.get("per_page", 30))
        cur_page = int(request.GET.get("cur_page", 1))
        start_site = (cur_page - 1) * per_page
        end_site = start_site + per_page
        r_data = PtCard.objects.all()[start_site:end_site]
        all_page = int(ceil(PtCard.objects.count() / float(per_page)))
        if cur_page > all_page or cur_page <= 0:
            return {'code': '-1', 'msg': '页数太大或太小'}
        r_list = []
        for obj in r_data:
            if obj.service_length == 0:
                service_len = u'不限'
            else:
                service_len = str(obj.service_length) + '分钟' if obj.service_length < 60 else str(
                    round(obj.service_length / 60.0, 2)) + '小时'
            r_list.append(dict(
                id=obj.id,
                icon=obj.icon,
                remark=obj.remark if obj.remark else '',
                name=obj.name,
                retail_price=round(obj.retail_price / 100.0, 2),
                usable_times=obj.usable_times,
                service_length=service_len,
                instruction=obj.instruction,
                expire_dates=obj.expire_dates if obj.expire_dates else '不限',
            ))
        data['data'] = r_list
        data['page'] = all_page
        data['code'] = '0'
        return data
    except Exception as e:
        return {'code': '-1', 'msg': e.message}


def create_putao_card(request):
    """
    葡萄卡商品创建
    :param request:
    :return:
    """
    data = {}
    try:
        request_data = json.loads(request.body) if request.body else ''
        if request_data:
            icon = request_data.get('putaoDitu', '')
            icon_inactive = request_data.get('icon_inactive', '')
            name = request_data.get('puName', '')
            remark = request_data.get('remark', '')
            retail_price = request_data.get('retail_price', '')
            usable_times = request_data.get('serviceCount', '')
            service_length = request_data.get('serviceTime', '')
            timeType = request_data.get('timeType', '')
            cancel_minutes = float(str(request_data.get('timeLimit', '')))
            instruction = request_data.get('description', '')
            expire_dates = request_data.get('validity', '')
            # is_app_sale = 1 if request_data.get('is_sale') else 0
            all_scope = request_data.get('all_scope')
            service_length = None if len(service_length) == 0  else float(str(service_length))
            if service_length is not None:
                service_length = int(round(service_length * 60)) if timeType == 'hour' else int(round(service_length))
            else:
                service_length = 0
            if all_scope is None:
                return {"msg": u"无服务范围", "code": '0'}
            pt = PtCard.objects.create(
                name=name,
                icon=icon,
                icon_inactive=icon_inactive,
                remark=remark,
                retail_price=int(round(float(str(retail_price)) * 100)),  # 单位分
                usable_times=int(usable_times),
                service_length=service_length,
                cancel_minutes=int(round(cancel_minutes * 60)),
                instruction=instruction,
                expire_dates=expire_dates if expire_dates else 365,
                is_app_sale=0,
            )
            try:
                click_url, gids = click_action_url(all_scope, pt.id)
                pt.click_action = click_url
                pt.save()
            except Exception as err:
                return {'msg': 'action:' + err.message, 'code': '-1'}
            for i in all_scope:
                str_gid, str_sku = filter_gids(i['gids'], 1)
                str_gid_x, str_sku_x = filter_gids(i['gids_x'], 1)
                PtCardScope.objects.create(
                    card_id=pt.id,
                    positive_second_category_id=i['goods_cat'],
                    reverse_second_category_id=i['goods_cat_x'],
                    positive_category_id=i['sanji'],
                    reverse_category_id=i['sanji_x'],
                    positive_cpid=i['cps'],
                    reverse_cpid=i['cps_x'],
                    positive_gid=str_gid,
                    reverse_gid=str_gid_x,
                    positive_skuid=str_sku,
                    reverse_skuid=str_sku_x,
                )
            return {"msg": u"添加成功", "code": '0'}
        data = {"msg": u"缺少参数", "code": '-1'}
    except Exception as err:
        data = {"msg": err.message, "code": '-1'}

    return data


def format_sku(str_id, type):
    """
    type=0  str id 前面加s
    type=1  str id 前面加g
    :param str_id:
    :return:
    """
    lt_id = str_id.split(',') if str_id else []
    if type == 0:
        return ','.join(map(lambda x: 's' + x, lt_id)) if lt_id else ''
    else:
        return ','.join(map(lambda x: 'g' + x, lt_id)) if lt_id else ''


def get_one_putao(obj):
    """
    获取单个葡萄卡商品
    :param request:
    :return:
    """
    data = {}
    ptcardscope = PtCardScope.objects.filter(card_id=obj.id)
    all_scope = []
    for i in ptcardscope:
        gids = format_sku(i.positive_gid, 1) if i.positive_gid is not None else ''
        gids_x = format_sku(i.reverse_gid, 1) if i.reverse_gid is not None else ''
        sku = format_sku(i.positive_skuid, 0) if i.positive_skuid is not None else ''
        sku_x = format_sku(i.reverse_skuid, 0) if i.reverse_skuid is not None else ''
        gid_format = gids + ',' + sku if gids or sku else gids + sku
        gid_x_format = gids_x + ',' + sku_x if gids_x or sku_x else gids_x + sku_x
        all_scope.append(
            dict(
                goods_cat=i.positive_second_category_id if i.positive_second_category_id is not None else '',
                goods_cat_x=i.reverse_second_category_id if i.reverse_second_category_id is not None else '',
                sanji=i.positive_category_id if i.positive_category_id is not None else '',
                sanji_x=i.reverse_category_id if i.reverse_category_id is not None else '',
                cps=i.positive_cpid if i.positive_cpid is not None else '',
                cps_x=i.reverse_cpid if i.reverse_cpid is not None else '',
                gids=gid_format,
                gids_x=gid_x_format,
            )
        )

    if obj.service_length < 60:
        timeType = 'minute'
        service_length = obj.service_length
    else:
        timeType = 'hour'
        service_length = round(obj.service_length / 60.0, 2)
    data['data'] = dict(
        putaoDitu=obj.icon,
        icon_inactive=obj.icon_inactive,
        puName=obj.name,
        remark=obj.remark,
        retail_price=round(obj.retail_price / 100.0, 2),
        serviceCount=obj.usable_times,
        serviceTime=service_length if service_length != 0 else '',
        timeType=timeType,
        timeLimit=round(obj.cancel_minutes / 60.0, 2),
        description=obj.instruction,
        validity=obj.expire_dates if obj.expire_dates else 365,
        # is_sale=True if obj.is_app_sale == 1 else False,
        all_scope=all_scope,

    )
    data['code'] = '0'
    return data


def update_putao(pk, request):
    """
    更改单个葡萄卡商品
    :param request:
    :return:
    """
    data = {}
    try:
        ptcard = PtCard.objects.filter(id=pk)
        request_data = json.loads(request.body) if request.body else ''
        if request_data:
            icon = request_data.get('putaoDitu', '')
            icon_inactive = request_data.get('icon_inactive', '')
            name = request_data.get('puName', '')
            remark = request_data.get('remark', '')
            # retail_price = request_data.get('retail_price', '')
            # usable_times = request_data.get('serviceCount', '')
            service_length = request_data.get('serviceTime', '')
            timeType = request_data.get('timeType', '')
            cancel_minutes = float(str(request_data.get('timeLimit', '')))
            instruction = request_data.get('description', '')
            expire_dates = request_data.get('validity', '')
            # is_app_sale = 1 if request_data.get('is_sale') else 0
            all_scope = request_data.get('all_scope')
            service_length = None if len(service_length) == 0  else float(str(service_length))
            if service_length is not None:
                service_length = int(round(service_length * 60)) if timeType == 'hour' else int(round(service_length))
            else:
                service_length = 0
            if all_scope is None:
                return {"msg": u"无服务范围", "code": '0'}
            ptcard.update(
                name=name,
                icon=icon,
                icon_inactive=icon_inactive,
                remark=remark,
                service_length=service_length,
                cancel_minutes=cancel_minutes * 60,
                instruction=instruction,
                expire_dates=expire_dates if expire_dates else 365,
                # is_app_sale=is_app_sale,
            )
            try:
                ptcard_get = PtCard.objects.get(id=pk)
                click_url, gids = click_action_url(all_scope, pk)
                ptcard_get.click_action = click_url
                ptcard_get.save()
            except Exception as err:
                return {'msg': 'action:' + err.message, 'code': '-1'}
            PtCardScope.objects.filter(card_id=pk).delete()
            for i in all_scope:
                str_gid, str_sku = filter_gids(i['gids'], 1)
                str_gid_x, str_sku_x = filter_gids(i['gids_x'], 1)
                PtCardScope.objects.filter(card_id=pk).create(
                    card_id=pk,
                    positive_second_category_id=i['goods_cat'],
                    reverse_second_category_id=i['goods_cat_x'],
                    positive_category_id=i['sanji'],
                    reverse_category_id=i['sanji_x'],
                    positive_cpid=i['cps'],
                    reverse_cpid=i['cps_x'],
                    positive_gid=str_gid,
                    reverse_gid=str_gid_x,
                    positive_skuid=str_sku,
                    reverse_skuid=str_sku_x,
                )
            # 同步商品
            pt_goods = update_goods_id(pk)
            for i in pt_goods:
                if not i:
                    continue
                param = get_ptcard_info([pk], i[0], i[1], 0)
                ptgoodsurl = PtConst.UPDATEPTGOODS
                r = requests.post(ptgoodsurl, data=param)
                re = r.json()
                if re['code'] != 0:
                    return {"msg": '同步商品失败:' + re["msg"], "code": '-1'}
            # 同步实体卡
            pt_ent = PtEntityCard.objects.filter(card_id=pk)
            for e in pt_ent:
                param = get_ptcard_info([pk], e.id, '', 1)
                ptgoodsurl = PtConst.UPDATEPTGOODS
                r = requests.post(ptgoodsurl, data=param)
                re = r.json()
                if re['code'] != 0:
                    return {"msg": '同步实体卡失败' + re["msg"], "code": '-1'}
            return {"msg": u"添加成功", "code": '0'}
        data = {"msg": u"缺少参数", "code": '-1'}
    except Exception as err:
        data = {"msg": err.message, "code": '-1'}

    return data


@login_required
@permission_required(u'man.%s' % PtConst.PT_CARD, raise_exception=True)
@add_common_var
def putao_card_info(request, template_name):
    return report_render(request, template_name, {
    }, context_instance=RequestContext(request))


@login_required
@permission_required(u'man.%s' % PtConst.PT_CARD, raise_exception=True)
@add_common_var
def putao_card_edit(request, template_name):
    return report_render(request, template_name,
                         {},
                         context_instance=RequestContext(request))


@login_required
@permission_required(u'man.%s' % PtConst.PT_CARD, raise_exception=True)
def putao_card_goods(request):
    """
    葡萄卡的列表显示和卡的增加
    :param request:
    :return:
    """
    data = {'code': '-1', 'msg': 'GET or POST 方法'}
    if request.method == 'GET':
        data = get_putao_card_list(request)
    elif request.method == 'POST':
        data = create_putao_card(request)
    return JsonResponse(data)


@login_required
@permission_required(u'man.%s' % PtConst.PT_CARD, raise_exception=True)
def putao_card_goods_detail(request):
    """
    get 单个信息
    post 更改信息
    delete 葡萄卡的删除
    :param request:
    :return:
    """
    data = {'code': '-1', 'msg': 'GET or PUT 方法'}
    try:
        pk = request.GET.get('pk', request.POST.get('pk'))
        did = PtCard.objects.get(id=pk)
    except:
        data = {'msg': u'没有这个值', 'code': '1'}
    else:
        if request.method == 'GET':
            data = get_one_putao(did)
        elif request.method == 'PUT':
            data = update_putao(pk, request)
        elif request.method == 'DELETE':
            pass
    return JsonResponse(data)
