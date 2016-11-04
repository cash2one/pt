# coding: utf-8


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
def vip_redeem_codes(request, template_name):
    vip_info = get_vip_info()
    secondary_categorys = get_vip_secondary_category()
    third_categorys = get_vip_third_category()
    payload = {'cardId': vip_pub.CARD_ID, 'start': 0, 'size': 30}
    r = requests.get(vip_pub.VIP_EXCHANGE_LIST, params=payload)
    vip_return_data = r.json()
    table_coulumns = vip_return_data['data']
    return report_render(request,template_name, {
        "table_columns": table_coulumns,
        "vip_info": vip_info,
        "secondary_categorys": secondary_categorys,
        "third_categorys": third_categorys,
    }, context_instance=RequestContext(request))


def update_order_info(orders):
    result = []
    for order in orders:
        result.append([
            str(order.id),
            str('已上架'),
            str(order.prod_name),
            str(order.prod_price),
            str(order.prod_content),
            str('aa'),
            str('编辑'),
        ])
    return result


@login_required
@permission_required(u'man.%s' % ReportConst.SHELVES_MANAGEMENT_VIP, raise_exception=True)
def vip_redeem_codes_ajax(request):
    per_page = request.POST.get("per_page")
    cur_page = request.POST.get("cur_page")
    start_page = int(per_page) * (int(cur_page) - 1)
    payload = {'cardId': vip_pub.CARD_ID, 'start': start_page, 'size': per_page}
    r = requests.get(vip_pub.VIP_EXCHANGE_LIST, params=payload)
    vip_return_data = r.json()
    table_columns = vip_return_data['data']

    # 列表展示信息
    payload = {'cardId': vip_pub.CARD_ID, 'size': 9999999}
    r = requests.get(vip_pub.VIP_EXCHANGE_LIST, params=payload)
    vip_r_data = r.json()
    num_pages = vip_r_data['data'].__len__()
    num = int(ceil(float(num_pages) / int(per_page)))
    return HttpResponse(json.dumps([table_columns, num]))


@login_required
@permission_required(u'man.%s' % ReportConst.SHELVES_MANAGEMENT_VIP, raise_exception=True)
def vip_redeem_codes_csv(request):
    g_data = []
    if request.method == 'GET':
        cardGoodsId = request.GET.get("cardGoodsId")
        filename = 'card_%s_redeem_codes.txt' % cardGoodsId
        redeem_code_url = get_get_redeem_code_url()
        para = {'cardGoodsId': cardGoodsId, 'start': 0, 'size': 5000}
        r = requests.get(redeem_code_url, params=para)
        r_data = r.json()
    else:
        # a=request.POST.copy()
        r_data = json.loads(request.POST.get('data'))
        filename = 'card_redeem_codes.txt'

    csv_data = [["cardSeqNo",
                 "cardPwd",
                 "status",
                 "exchangeTime",
                 "creteTime"]]

    for obj in r_data['data']:
        if obj:
            g_data.append([
                str(obj['cardSeqNo']),
                str(obj['cardPwd']),
                str(obj['status']),
                str(obj['exchangeTime']),
                str(obj['creteTime']),
            ])
    csv_data.extend(g_data)
    return get_csv_response(filename, csv_data)
