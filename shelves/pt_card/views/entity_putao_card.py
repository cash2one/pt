# coding: utf-8
import json
from decimal import Decimal

import requests
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render_to_response
from math import ceil

from common.views import add_common_var, get_csv_response
from common.views import report_render
from phone_fee.models import CpPhoneFeeProduct, PtDaojiaOrderGuarantee
from pt_card.models import PtCard, PtEntityCard
from pt_card.views.pt_card_pub import PtConst, Paginator, HttpResponse, get_ptcard_info
from wallet.views import vip_pub
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.hashers import make_password
from django.template import RequestContext
from django.db import connection, transaction, connections
import time


def get_entity_putao_card_list(request):
    """
    实体卡列表
    :param request:
    :return:
    """
    try:
        data = {}
        per_page = int(request.GET.get("per_page", 30))
        cur_page = int(request.GET.get("cur_page", 1))
        objs = _get_entity_obj()
        p = Paginator(objs, per_page)
        num_pags = p.num_pages
        if cur_page > num_pags:
            return {'code': '-1', 'msg': '页数太大'}
        r_data = p.page(cur_page)
        r_list = []
        for obj in r_data:
            if obj[4] == 0 :
                service_len = u'不限'
            else:
                service_len = str(obj[4]) + '分钟' if obj[4] < 60 else str(
                    round(obj[4] / 60.0, 2)) + '小时'
            r_list.append(dict(
                id=obj[0],
                icon=obj[1],
                name=obj[2],
                usable_times=obj[3],
                service_length=service_len,
                instruction=obj[5],
                expire_dates=obj[6],
                valid_dates=obj[7].strftime("%Y-%m-%d %H:%M:%S") + '至' + obj[8].strftime("%Y-%m-%d %H:%M:%S") if obj[7] and
                                                                                                                 obj[
                                                                                                                     8] else '无限制',
                exchange_amount=obj[9],
                eid=obj[10]
            ))
        data['data'] = r_list
        data['page'] = num_pags
        data['code'] = '0'
        return data
    except Exception as e:
        return {'code': '-1', 'msg': e.message}


def _get_entity_obj():
    """
    获取实体卡obj
    :return:
    """
    cur = connections['pt_card'].cursor()
    sql = """
        SELECT c.id,c.icon,c.name,c.usable_times,c.service_length,
        c.instruction,c.expire_dates,e.expire_date_begin,
        e.expire_date_end,e.exchange_amount,e.id
        FROM pt_vip.pt_entity_card as e left join pt_vip.pt_card as c on e.card_id = c.id order by e.id desc;
          """
    cur.execute(sql)
    row = cur.fetchall()
    return row


def create_entity_putao_card(request):
    """
    实体卡商品创建
    :param request:
    :return:
    """
    data = {}
    try:
        request_data = json.loads(request.body) if request.body else ''
        if request_data:
            id = request_data.get('pt_id', '')
            starttime = request_data.get('starttime', None)
            endtime = request_data.get('endtime', None)
            exchange_amount = request_data.get('exchange_amount', '')
            redeem_code_url = PtConst.ADDPTCARD
            if starttime and starttime is not None:
                para = {'cardId': id,'exchangeAmount':exchange_amount,'expireDateBegin':starttime,'expireDateEnd':endtime}
            else:
                para = {'cardId': id, 'exchangeAmount': exchange_amount}
            r = requests.get(redeem_code_url, params=para)
            re = r.json()
            if re['code'] != "0":
                return {"msg": re["msg"], "code": '-1'}
            if id :
                id_a = []
                id_a .append(id)
            else:
                id_a = []
            param = get_ptcard_info(id_a, re['data'], '', 1)
            ptgoodsurl = PtConst.ADDPTGOODS
            r = requests.post(ptgoodsurl, data=param)
            re = r.json()
            if re['code'] != 0:
                return {"msg": 'remote' + re["msg"], "code": '-1'}
            return {"msg": u"添加成功", "code": '0'}
        data = {"msg": u"缺少参数", "code": '-1'}
    except Exception as err:
        data = {"msg": err.message, "code": '-1'}

    return data


def get_one_putao(obj):
    """
    获取单个实体卡商品
    :param request:
    :return:
    """
    pass


def update_putao(pk, request):
    """
    更改单个实体卡商品
    :param request:
    :return:
    """
    data = {}
    try:
        request_data = json.loads(request.body) if request.body else ''
        if request_data:
            id = request_data.get('pt_id', '')
            gid = request_data.get('g_id', [])
            if gid:
                gida = []
                gida.append(gid)
            else:
                gida = []
            starttime = request_data.get('starttime', None)
            endtime = request_data.get('endtime', None)
            redeem_code_url = PtConst.UPDATEPTCARD
            if starttime and starttime is not None:
                para = {'id': id,  'expireDateBegin': starttime,
                        'expireDateEnd': endtime}
            else:
                para = {'id': id}
            r = requests.get(redeem_code_url, params=para)
            re = r.json()
            if re['ret_code'] != '0':
                return {"msg": re["msg"], "code": '-1'}
            param = get_ptcard_info(gida, id, '', 1)
            ptgoodsurl = PtConst.UPDATEPTGOODS
            r = requests.post(ptgoodsurl, data=param)
            re = r.json()
            if re['code'] != 0:
                return {"msg": 'remote' + re["msg"], "code": '-1'}
            return {"msg": u"添加成功", "code": '0'}
        data = {"msg": u"缺少参数", "code": '-1'}
    except Exception as err:
        data = {"msg": err.message, "code": '-1'}

    return data



def get_codes_list():
    """
    获取所有codes,倒序
    :return:
    """
    data = [dict(
        c_time='2016/08/23 12:13',
        id='2',
        name='20132',
    ) for i in range(2)]
    return data


@login_required
@permission_required(u'man.%s' % PtConst.PT_CARD, raise_exception=True)
@add_common_var
def entity_putao_card_info(request, template_name):
    objs = PtCard.objects.all()
    ptlist = [[i.id, i.name] for i in objs]
    return report_render(request, template_name, {'ptlist': ptlist,
                                                  }, context_instance=RequestContext(request))


@login_required
@permission_required(u'man.%s' % PtConst.PT_CARD, raise_exception=True)
def entity_putao_card_goods(request):
    """
    实体卡的列表显示和卡的增加
    :param request:
    :return:
    """
    data = {'code': '-1', 'msg': 'GET or POST 方法'}
    if request.method == 'GET':
        data = get_entity_putao_card_list(request)
    elif request.method == 'POST':
        data = create_entity_putao_card(request)
    return JsonResponse(data)


@login_required
@permission_required(u'man.%s' % PtConst.PT_CARD, raise_exception=True)
def entity_putao_card_goods_detail(request):
    """
    get 单个信息
    post 更改信息
    delete 实体卡的删除
    :param request:
    :return:
    """
    data = {'code': '-1', 'msg': 'GET or PUT or DELETE方法'}
    try:
        pk = request.GET.get('pk', request.POST.get('pk'))
        did = PtEntityCard.objects.get(id=pk)
    except:
        data = {'msg': u'没有这个值', 'code': '1'}
    else:
        if request.method == 'GET':
            data = get_one_putao(did)
        elif request.method == 'PUT':
            data = update_putao(pk, request)
        elif request.method == 'DELETE':

            # did.delete()
            data = {'msg': u'delete ok', 'code': '0'}
    return JsonResponse(data)


@login_required
@permission_required(u'man.%s' % PtConst.PT_CARD, raise_exception=True)
def entity_codes_list(request):
    """
    get 获取实体卡列表,这个功能废除
    :param request:
    :return:
    """
    data = {'code': '-1', 'msg': 'GET 方法'}
    if request.method == 'GET':
        data = get_codes_list()
    return HttpResponse(json.dumps(data), content_type="application/json")


@login_required
@permission_required(u'man.%s' % PtConst.PT_CARD, raise_exception=True)
def entity_codes_down(request):
    """
    下载券码
    @return
    """
    code_main_id = request.GET.get('id', '')
    if code_main_id:
        g_data = []
        filename = 'No.%s_codes.txt' % code_main_id
        redeem_code_url = PtConst.CREATECODES
        para = {'id': code_main_id}
        r = requests.get(redeem_code_url, params=para)
        r_data = r.json()

        csv_data = [["cardSeqNo",
                     "cardPwd",
                     "qrCode",
                     "status",
                     "exchangeTime",
                     "creteTime"]]

        for obj in r_data['data']:
            if obj:
                g_data.append([
                    str(obj['cardSeqNo']),
                    str(obj['cardPwd']),
                    str(obj['qrCode']),
                    str(obj['status']),
                    str(obj['exchangeTime']),
                    str(obj['creteTime']),
                ])
        csv_data.extend(g_data)
        return get_csv_response(filename, csv_data)
    return JsonResponse({'code':'-1','msg':'无参数'})
