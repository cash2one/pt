# -*- coding: utf-8 -*-
# Author:songroger
# Jun.22.2016
from __future__ import unicode_literals
from .models import CouponCodeSub
from pttools.pthttp import PtHttpResponse, get_csv_response
from django.views.decorators.http import require_http_methods, require_safe
from django.contrib.auth.decorators import login_required
from .utils import get_coupon_list, delete_coupon, get_coupon,\
    add_coupon, up_coupon, get_cps_list, get_goods_list, get_coupons,\
    create_coupons, get_coupon_created_list, allot_coupon_to, \
    get_codes_list, get_invite_gift_list, updown_share, \
    get_invite, add_invite, up_invite, get_category_list, down_share, \
    get_share_activity_list, get_coupons_valid, get_vip_list


@require_safe
@login_required
def coupon_list(request):
    """
    获取优惠券列表
    """
    page = int(request.GET.get('page', 1))
    limit = int(request.GET.get('limit', 10))
    scope = request.GET.get('scope', None)
    kwd = request.GET.get('wd', None)
    data = get_coupon_list(page, limit, scope, kwd)
    return PtHttpResponse(data)


@require_http_methods(['GET', 'POST', 'PUT', 'DELETE'])
@login_required
def coupon(request):
    data = {}
    if request.method == "GET":
        cid = request.GET.get('id', None)
        if cid:
            data = get_coupon(cid)
            return PtHttpResponse(data)
    elif request.method == "POST":
        data = add_coupon(request)
        return PtHttpResponse(data)
    elif request.method == "PUT":
        cid = request.GET.get('id', None)
        if cid:
            data = up_coupon(request, cid)
            return PtHttpResponse(data)
    elif request.method == "DELETE":
        cid = request.GET.get('id', None)
        if cid:
            data = delete_coupon(cid)
            return PtHttpResponse(data)
    return PtHttpResponse(data)


# @require_safe
@login_required
def cps_list(request):
    """
    获取服务商列表
    """
    data = get_cps_list(request)
    return PtHttpResponse(data)


@require_http_methods(['POST'])
@login_required
def goods_list(request):
    """
    获取商品列表
    """
    data = get_goods_list(request)
    return PtHttpResponse(data)


@require_safe
@login_required
def coupons_list(request):
    """
    获取coupons列表
    @return 优惠券ID，name列表
    """
    data = get_coupons_valid()
    return PtHttpResponse(data)


@require_safe
@login_required
def coupons_list_valid(request):
    """
    获取有效coupons列表
    @return 优惠券ID，name列表
    """
    data = get_coupons_valid()
    return PtHttpResponse(data)


@require_http_methods(['POST'])
@login_required
def create_codes(request):
    """
    生成券码
    @return
    """
    data = create_coupons(request)
    return PtHttpResponse(data)


@require_safe
@login_required
def coupon_created_list(request):
    """
    优惠券发放情况列表
    """
    page = int(request.GET.get('page', 1))
    limit = int(request.GET.get('limit', 10))

    data = get_coupon_created_list(page, limit)
    return PtHttpResponse(data)


@require_safe
@login_required
def invite_gift_list(request):
    """
    邀请有礼情况列表
    """

    page = int(request.GET.get('page', 1))
    limit = int(request.GET.get('limit', 10))
    # da = [{'gids':[1,2,3],'gids_x':[11,'2'],'cps':'','cps_x':[1],'goods_cat':["328","332"],'goods_cat_x':''},{}]
    # data = click_action_url(da)
    data = get_invite_gift_list(page, limit)
    return PtHttpResponse(data)


@require_http_methods(['PUT'])
@login_required
def invite_gift_updown(request):
    """
    邀请有礼上架
    :param request:
    :return:
    """
    data = {}
    id = request.GET.get('id', None)
    if id:
        data = updown_share(request, id)
        return PtHttpResponse(data)
    return PtHttpResponse(data)


@require_http_methods(['PUT'])
@login_required
def invite_gift_down(request):
    """
    邀请有礼下架
    :param request:
    :return:
    """
    data = {}
    id = request.GET.get('id', None)
    if id:
        data = down_share(request, id)
        return PtHttpResponse(data)
    return PtHttpResponse(data)

@login_required
def vip_list(request):
    """
    返回vip商品
    :param request:
    :return:
    """
    data = get_vip_list()
    return PtHttpResponse(data)

@require_http_methods(['GET', 'POST', 'PUT', 'DELETE'])
@login_required
def invite_gift(request):
    """
    邀请有礼的增删改查
    :param request:
    :return:
    """
    data = {}
    if request.method == 'GET':
        sid = request.GET.get('id', None)
        if sid:
            data = get_invite(request, sid)
    elif request.method == 'POST':
        data = add_invite(request)
    elif request.method == 'PUT':
        sid = request.GET.get('id', None)
        if sid:
            data = up_invite(request, sid)
    elif request.method == 'DELETE':
        pass
    return PtHttpResponse(data)


@require_http_methods(['POST'])
@login_required
def allot_coupon(request):
    """
    发放指定券
    @return
    """
    data = allot_coupon_to(request)
    return PtHttpResponse(data)


@require_safe
@login_required
def download_codes(request):
    """
    下载券码
    @return
    """
    code_main_id = request.GET.get('cid', None)
    if code_main_id:
        filename = 'No.%s_codes.txt' % code_main_id
        data = CouponCodeSub.objects.using("activity").filter(
            main_id=code_main_id).only("exchange_code")
        codes = [[d.exchange_code] for d in data]
        return get_csv_response(filename, codes)
    else:
        return PtHttpResponse({"code": 1, "msg": u"无参数"})


@require_safe
@login_required
def codes_list(request):
    """
    券码批次列表
    @return
    """
    data = get_codes_list(request)
    return PtHttpResponse(data)


@require_safe
@login_required
def category_list(request):
    """
    分类列表
    @return
    """
    data = get_category_list(request)
    return PtHttpResponse(data)


@require_safe
@login_required
def share_activity_list(request):
    """
    活动名称列表
    @return
    """
    data = get_share_activity_list(request)
    return PtHttpResponse(data)
