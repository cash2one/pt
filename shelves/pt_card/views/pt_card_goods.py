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
from pt_card.models import PtCard, PtEntityCard, PtCardGoods
from pt_card.views.pt_card_pub import PtConst, Paginator, HttpResponse, get_ptcard_name, get_ptcard_info
from wallet.views import vip_pub
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.hashers import make_password
from django.template import RequestContext
from django.db import connection, transaction, connections
import time


def get_pt_card_goods_list(request):
    """
    葡萄卡商品列表
    :param request:
    :return:
    """
    try:
        data = {}
        per_page = int(request.GET.get("per_page", 30))
        cur_page = int(request.GET.get("cur_page", 1))
        start_site = (cur_page - 1) * per_page
        end_site = start_site + per_page
        r_data = PtCardGoods.objects.all()[start_site:end_site]
        all_page = int(ceil(PtCardGoods.objects.count() / float(per_page)))
        if cur_page > all_page or cur_page <= 0:
            return {'code': '-1', 'msg': '页数太大或太小'}
        #r_data = [['123','这是真的商品名称',['2小时5次保洁卡','2小时5次保洁卡'],[10,11]]]
        r_list = []
        for obj in r_data:
            ids = obj.pt_cids.split(',')
            pt_names = get_ptcard_name(ids)
            r_list.append(dict(
                gid=obj.id,
                g_name=obj.goods_name,
                pt_name=pt_names,
                pt_id=ids,
            ))
        data['data'] = r_list
        data['page'] = all_page
        data['code'] = '0'
        return data
    except Exception as e:
        return {'code': '-1', 'msg': e.message}




def create_pt_card_goods(request):
    """
    葡萄卡商品商品创建
    :param request:
    :return:
    """
    data = {}
    try:
        request_data = json.loads(request.body) if request.body else ''
        if request_data:
            goods_name = request_data.get('goods_name', '')
            pt_id = request_data.get('pt_id', '')
            pt_cids = ','.join(pt_id)
            pt_goods = PtCardGoods.objects.create(
                goods_name=goods_name,
                pt_cids=pt_cids
            )
            param = get_ptcard_info(pt_id,pt_goods.id,goods_name,0)
            ptgoodsurl = PtConst.ADDPTGOODS
            r = requests.post(ptgoodsurl, data=param)
            re = r.json()
            if re['code'] != 0:
                pt_goods.delete()
                return {"msg": 'remote'+re["msg"], "code": '-1'}
            return {"msg": u"添加成功", "code": '0'}
        data = {"msg": u"缺少参数", "code": '-1'}
    except Exception as err:
        pt_goods.delete()
        data = {"msg": err.message, "code": '-1'}

    return data


def get_one_putao(obj):
    """
    获取单个葡萄卡商品商品
    :param request:
    :return:
    """
    pass


def update_putao(pk, request):
    """
    更改单个葡萄卡商品商品
    :param request:
    :return:
    """
    data = {}
    try:
        request_data = json.loads(request.body) if request.body else ''
        if request_data:
            goods_name = request_data.get('goods_name', '')
            pt_id = request_data.get('pt_id', '')
            g_id = request_data.get('g_id', '')
            pt_cids = ','.join(pt_id)
            param = get_ptcard_info(pt_id, g_id, goods_name,0)
            ptgoodsurl = PtConst.UPDATEPTGOODS
            r = requests.post(ptgoodsurl, data=param)
            re = r.json()
            if re['code'] != 0:
                return {"msg": 'remote'+re["msg"], "code": '-1'}
            PtCardGoods.objects.filter(id=g_id).update(
                goods_name=goods_name,
                pt_cids=pt_cids
            )
            return {"msg": u"添加成功", "code": '0'}
        data = {"msg": u"缺少参数", "code": '-1'}
    except Exception as err:
        data = {"msg": err.message, "code": '-1'}

    return data


@login_required
@permission_required(u'man.%s' % PtConst.PT_CARD, raise_exception=True)
@add_common_var
def pt_card_goods_index(request, template_name):
    objs = PtCard.objects.all()
    ptlist = [[i.id, i.name] for i in objs]
    return report_render(request, template_name, {'ptlist': ptlist,
                                                  }, context_instance=RequestContext(request))


@login_required
@permission_required(u'man.%s' % PtConst.PT_CARD, raise_exception=True)
def pt_card_goods_info(request):
    """
    葡萄卡商品的列表显示和卡的增加
    :param request:
    :return:
    """
    data = {'code': '-1', 'msg': 'GET or POST 方法'}
    if request.method == 'GET':
        data = get_pt_card_goods_list(request)
    elif request.method == 'POST':
        data = create_pt_card_goods(request)
    return JsonResponse(data)


@login_required
@permission_required(u'man.%s' % PtConst.PT_CARD, raise_exception=True)
def pt_card_goods_info_detail(request):
    """
    get 单个信息
    post 更改信息
    delete 葡萄卡商品的删除
    :param request:
    :return:
    """
    data = {'code': '-1', 'msg': 'GET or PUT or DELETE方法'}
    try:
        pk = request.GET.get('pk', request.POST.get('pk'))
        #did = PtEntityCard.objects.get(id=pk)
    except:
        data = {'msg': u'没有这个值', 'code': '1'}
    else:
        if request.method == 'GET':
            pass
            #data = get_one_putao(did)
        elif request.method == 'PUT':
            data = update_putao(pk, request)
        elif request.method == 'DELETE':
            #did.delete()
            data = {'msg': u'delete ok', 'code': '0'}
    return JsonResponse(data)


