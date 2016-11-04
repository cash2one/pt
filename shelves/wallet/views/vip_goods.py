# coding: utf-8
from decimal import Decimal

from django.shortcuts import render_to_response
from math import ceil

from phone_fee.models import CpPhoneFeeProduct, PtDaojiaOrderGuarantee
from wallet.views import vip_pub
from wallet.views.vip_pub import *
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.hashers import make_password
from django.template import RequestContext
from django.db import connection, transaction
import time
import requests


@login_required
@permission_required(u'man.%s' % ReportConst.SHELVES_MANAGEMENT_VIP, raise_exception=True)
@add_common_var
def vip_goods(request, template_name):
    vip_info = get_vip_info()
    secondary_categorys = get_vip_secondary_category()
    third_categorys = get_vip_third_category()
    cp_names = get_pf_cp()
    carriers = get_pf_carrier()
    pf_management_table_columns = get_pf_management_table_columns()
    provinces = get_pf_province()

    return report_render(request,template_name, {
        "provinces": provinces,
        "cp_names": cp_names,
        "carriers": carriers,
        "table_columns": pf_management_table_columns,
        "vip_info": vip_info,
        "secondary_categorys": secondary_categorys,
        "third_categorys": third_categorys,
    }, context_instance=RequestContext(request))


def update_order_info(orders):
    result = []
    for order in orders:
        result.append([
            str(''),
            str('已上架'),
            str(order.id),
            str(order.prod_name),
            str(order.prod_price),
            str(order.prod_content),
            str('aa'),
            str('编辑'),
        ])
    return result


def show_selected_columns(result, selected_columns):
    pf_management_table_columns = get_pf_management_table_columns()
    show_columns = []
    show_result = []
    row = []
    for col in selected_columns:
        for d_col in pf_management_table_columns:
            if col == d_col[1]:
                show_columns.append(d_col[0])
    for obj in result:
        for s_col in show_columns:
            row.append(obj[s_col])
        show_result.append(row)
        row = []
    return show_result


@login_required
@permission_required(u'man.%s' % ReportConst.SHELVES_MANAGEMENT_VIP, raise_exception=True)
def vip_goods_ajax(request):
    per_page = request.POST.get("per_page")
    cur_page = request.POST.get("cur_page")
    start_page = int(per_page) * (int(cur_page) - 1)
    payload = {'cardId': vip_pub.CARD_ID, 'start': start_page, 'size': per_page}
    r = requests.get(vip_pub.VIP_RECHARGE_LIST, params=payload)
    vip_return_data = r.json()
    table_columns = vip_return_data['data']

    # 列表展示信息
    payload = {'cardId': vip_pub.CARD_ID, 'size': 9999999}
    r = requests.get(vip_pub.VIP_RECHARGE_LIST, params=payload)
    vip_r_data = r.json()
    num_pages = vip_r_data['data'].__len__()
    num = int(ceil(float(num_pages) / int(per_page)))
    return HttpResponse(json.dumps([table_columns, num]))


@login_required
@permission_required(u'man.%s' % ReportConst.SHELVES_MANAGEMENT_VIP, raise_exception=True)
def vip_goods_csv(request):
    filename = '话费商品列表.csv'
    csv_data = [[" ",
                 "排序",
                 "状态",
                 "供应商",
                 "省份",
                 "运营商",
                 "面值",
                 "售价",
                 "进货价",
                 "提示语",
                 "操作"]]
    # csv_data.extend(g_data)
    return get_csv_response(filename, csv_data)


@login_required
@permission_required(u'man.%s' % ReportConst.SHELVES_MANAGEMENT_VIP, raise_exception=True)
def batch_edit_guarantee_order_info(request):
    edit_order_list = request.POST.get("edit_order_list")
    g_special_filter = request.POST.get("g_special_filter")
    check_status = request.POST.get("check_status")
    msg = 'no data update!'

    if edit_order_list and g_special_filter:
        cursor = connections['main'].cursor()
        sql = "UPDATE pt_biz_db.pt_daojia_order_guarantee SET check_status = " + str(
            check_status) + " WHERE g_type = " + str(g_special_filter) + "  AND order_no IN ( " + str(
            edit_order_list) + " );"
        cursor.execute(sql)
        transaction.commit(using='main')
        msg = 'order update successfully!'

    return HttpResponse(json.dumps(msg))


@login_required
@permission_required(u'man.%s' % ReportConst.SHELVES_MANAGEMENT_VIP, raise_exception=True)
def normal_edit_recharge_info(request):
    data = request.POST.copy()
    data['v_sale_price'] = int(Decimal(data['v_sale_price']) * 100)
    data['v_prod_content'] = int(Decimal(data['v_prod_content']) * 100)
    data['v_vendibility'] = request.POST.get('v_vendibility', 0)
    data['v_display'] = request.POST.get('v_display', 0)
    data['v_isRecommend'] = request.POST.get('v_isRecommend', 0)
    data['v_cdkey_num'] = request.POST.get('v_cdkey_num', 0)
    data['v_center_tips'] = request.POST.get('v_center_tips', '')
    data['v_operTags'] = request.POST.get('v_operTags', '')

    if data['edit'] == '0':
        payload = {'cardId': vip_pub.CARD_ID, 'goodsName': data['v_goods_name'], 'goodsType': data['goodsType'],
                   'operTags': data['v_operTags'],
                   'operDesc': data['v_description'], 'salePrice': data['v_sale_price'],
                   'realValue': data['v_prod_content'], 'startTime': data['v_start_time'],
                   'endTime': data['v_end_time'], 'displayUserCenter': data['v_display'],
                   'userCenterTips': data['v_center_tips'], 'exchangeAmount': data['v_cdkey_num'],
                   'vendibility': data['v_vendibility'],'isRecommend':data['v_isRecommend']}
        r = requests.post(vip_pub.VIP_RECHARGE_ADD, data=payload)
    else:
        payload = {'cardGoodsId': data['v_card_g_id'], 'goodsName': data['v_goods_name'],
                   'goodsType': data['goodsType'],
                   'operTags': data['v_operTags'],
                   'operDesc': data['v_description'], 'salePrice': data['v_sale_price'],
                   'realValue': data['v_prod_content'], 'startTime': data['v_start_time'],
                   'endTime': data['v_end_time'], 'displayUserCenter': data['v_display'],
                   'userCenterTips': data['v_center_tips'], 'exchangeAmount': data['v_cdkey_num'],
                   'vendibility': data['v_vendibility'],'isRecommend':data['v_isRecommend']}
        r = requests.post(vip_pub.VIP_RECHARGE_UPDATE, data=payload)

    # r = requests.post('http://api.test.putao.so/svip/card/goods/add', data=payload)

    return HttpResponse(r.text)


# 编辑置顶
@login_required
@permission_required(u'man.%s' % ReportConst.SHELVES_MANAGEMENT_VIP, raise_exception=True)
def edit_top(request):
    cardGoodsId = request.POST.get("cardGoodsId")
    setTop = request.POST.get("setTop")
    edit_top_url = get_edit_top_url()
    para = {
        'cardGoodsId': cardGoodsId,
        'isTop': setTop,
    }
    r = requests.post(edit_top_url, data=para)
    r_txt = r.json()
    msg = 'order update successfully!'

    return HttpResponse(json.dumps(msg))


# 编辑商品上下架
@login_required
@permission_required(u'man.%s' % ReportConst.SHELVES_MANAGEMENT_VIP, raise_exception=True)
def edit_vendibility(request):
    cardGoodsId = request.POST.get("cardGoodsId")
    setVendibility = request.POST.get("setVendibility")
    edit_vendibility_url = get_edit_vendibility_url()
    para = {
        'cardGoodsIds': cardGoodsId,
        'vendibility': setVendibility,
    }
    r = requests.post(edit_vendibility_url, data=para)
    r_txt = r.json()
    msg = 'order update successfully!'

    return HttpResponse(json.dumps(msg))
