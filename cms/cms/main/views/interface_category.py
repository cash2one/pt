# coding: utf-8

# from .main_pub import *
# from main.forms import *
import requests
import logging

import time
from django.views.decorators.csrf import csrf_exempt

from cms.settings import CMS_CHECK_ON, INSTALL_TYPE
from common.const import CmsModule, CheckOpType
from main.models import CmsNaviCategory, CmsCheck, CmsGoods, CmsChannels, CmsViewService, CmsNavicategories, \
    CmsNavicatesGoods, CmsNavicatesCategory, CmsStreamcontent, CmsLikes, CmsStreamcontentsGoods
import json
from django.http import HttpResponse
from pttools.ptdecorators import require_iplimit

log = logging.getLogger('django')


def get_default_channel(app_version):
    database = "default"
    if CMS_CHECK_ON:
        database = "online"
    default_channels = CmsChannels.objects.using(database).filter(app_version__app_version=app_version, order=1)
    if default_channels:
        return default_channels[0].id
    return None


def category_is_old(app_id, version):
    try:
        tmp_ver = [int(a) for a in version.split(".")]
        if (int(app_id) == 30 and tmp_ver >= [2, 5, 0]) or (int(app_id) == 10 and tmp_ver >= [3, 7, 0]):
            return False
    except:
        pass
    return True


def get_channel_goods(channel_id, old):
    database = "default"
    if CMS_CHECK_ON:
        database = "online"
    goods = set()
    second_categories_ids = []
    # 1.常用服务下的商品
    services = CmsViewService.objects.using(database).filter(open_type=1, channel__id=channel_id).values_list(
        'service_id', flat=True)
    for service in services:
        goods.add(CmsGoods.objects.get(id=service).id)
    view_second_categories = CmsViewService.objects.filter(open_type=4, channel__id=channel_id).values_list(
        'service_id', flat=True)
    second_categories_ids.extend(view_second_categories)
    # 2.分类页服务下的商品
    groups = CmsNavicategories.objects.using(database).filter(cmsviewnavi__channel_id=channel_id)
    for group in groups:
        navi_goods = CmsNavicatesGoods.objects.using(database).filter(cate=group)
        for navi_good in navi_goods:
            try:
                goods.add(navi_good.goods.id)
            except:
                continue
        # 分类
        navi_categories = CmsNavicatesCategory.objects.using(database).filter(cate=group)
        for navi_category in navi_categories:
            category = navi_category.category
            second_categories_ids.append(category.id)
    if old:
        temp = CmsGoods.objects.using(database).filter(second_category__in=second_categories_ids).values_list('id',
                                                                                                              flat=True)
    else:
        temp = CmsGoods.objects.using(database).filter(new_second_category__in=second_categories_ids).values_list('id',
                                                                                                                  flat=True)
    goods.update(temp)
    # 3.内容流下的商品
    groups = CmsStreamcontent.objects.using(database).filter(cmsviewstream__channel__id=channel_id)
    for group in groups:
        temp = CmsGoods.objects.using(database).filter(cmsstreamcontentsgoods__streamcontent=group).values_list("id",
                                                                                                                flat=True)
        goods.update(temp)
    # 4.猜你喜欢下的商品
    groups = CmsLikes.objects.using(database).filter(cmsviewlike__channel__id=channel_id)
    for group in groups:
        temp = CmsGoods.objects.using(database).filter(cmslikesgoods__like=group).values_list("id", flat=True)
        goods.update(temp)
    return goods


def count_first_category(request):
    """获取商品“所属服务”下和商品有相同“一级分类”的商品数量"""
    database = "default"
    if CMS_CHECK_ON:
        database = "online"
    try:
        app_id = request.GET.get("app_id")
        version = request.GET.get("version")
        channel_no = request.GET.get("channel")
        goodsId = request.GET.get("goodsId")

        old = category_is_old(app_id, version)

        # 获取渠道
        channel_id = CmsChannels.objects.using(database).get(channel_no=channel_no, app_version__app_version=version).id
        #         goods = get_channel_goods(channel_id, old)
        #         if not goods:
        #             default_channel_id = get_default_channel(version)
        #             if default_channel_id:
        #                 goods = get_channel_goods(default_channel_id, old)
        cms_goods = CmsGoods.objects.using(database).filter(goods_id=goodsId).last()
        cp_name = cms_goods.cp_name
        if cp_name:
            code = 0
            msg = "SUCCESS"
            if old:
                data = CmsGoods.objects.using(database).filter(category=cms_goods.category, cp_name=cp_name).values(
                    "goods_id").distinct().count()
            else:
                data = CmsGoods.objects.using(database).filter(new_category=cms_goods.new_category,
                                                               cp_name=cp_name).values("goods_id").distinct().count()
        else:
            data = 0
            code = -1
            msg = "category is null"
    except Exception as e:
        data = 0
        code = -2
        msg = str(e)
    ret = {
        "code": code,
        "msg": msg,
        "data": data
    }
    log.error(json.dumps(ret))
    return HttpResponse(json.dumps(ret))


def count_second_category(request):
    """获取和商品有相同“二级分类”的商品数量"""
    database = "default"
    if CMS_CHECK_ON:
        database = "online"
    try:
        app_id = request.GET.get("app_id")
        version = request.GET.get("version")
        channel_no = request.GET.get("channel")
        goodsId = request.GET.get("goodsId")

        old = category_is_old(app_id, version)

        # 获取渠道
        channel_id = CmsChannels.objects.using(database).get(channel_no=channel_no, app_version__app_version=version).id
        #         goods = get_channel_goods(channel_id, old)
        #         if not goods:
        #             default_channel_id = get_default_channel(version)
        #             if default_channel_id:
        #                 goods = get_channel_goods(default_channel_id, old)
        if old:
            second_category = CmsGoods.objects.using(database).filter(goods_id=goodsId).last().second_category
        else:
            second_category = CmsGoods.objects.using(database).filter(goods_id=goodsId).last().new_second_category
        if second_category:
            code = 0
            msg = "SUCCESS"
            if old:
                data = CmsGoods.objects.using(database).filter(second_category=second_category).values(
                    "goods_id").distinct().count()
            else:
                data = CmsGoods.objects.using(database).filter(new_second_category=second_category).values(
                    "goods_id").distinct().count()
        else:
            data = 0
            code = -1
            msg = "second category is null"
    except Exception as e:
        data = 0
        code = -2
        msg = str(e)
    ret = {
        "code": code,
        "msg": msg,
        "data": data
    }
    log.error(json.dumps(ret))
    return HttpResponse(json.dumps(ret))


def get_category_info(request):
    """获取商品 “分类”信息"""
    database = "default"
    if CMS_CHECK_ON:
        database = "online"
    try:
        app_id = request.GET.get("app_id")
        version = request.GET.get("version")
        channel_no = request.GET.get("channel")
        goodsId = request.GET.get("goodsId")

        # 获取渠道
        goods = CmsGoods.objects.using(database).filter(goods_id=goodsId).last()
        code = 0
        msg = "SUCCESS"

        if category_is_old(app_id, version):
            category = goods.category
            second_category = goods.second_category
        else:
            category = goods.new_category
            second_category = goods.new_second_category

        data = {
            "categoryId": category,
            "categoryName": CmsNaviCategory.objects.using(database).get(id=category).name,
            "secondCategoryId": second_category,
            "secondCategoryName": CmsNaviCategory.objects.using(database).get(id=second_category).name
        }
    except Exception as e:
        code = -2
        msg = str(e)
        data = {}
    ret = {
        "code": code,
        "msg": msg,
        "data": data
    }
    return HttpResponse(json.dumps(ret))


# 接收商品信息接口（开放平台）
@require_iplimit("default")
@csrf_exempt
def synch_goods(request):
    result = {}
    database = "default"
    result['ret_code'] = -1
    if request.method == "GET":
        return HttpResponse(0)
    if request.method == "DELETE":
        goods_id = request.GET.get("goodsId")
        goods = CmsGoods.objects.using(database).filter(goods_id=goods_id)
        ids = [good[0] for good in goods.values_list("id")]
        viewservices = CmsViewService.objects.using(database).filter(service_id__in=ids, open_type=1)
        if CMS_CHECK_ON:
            for viewservice in viewservices:
                CmsCheck(module=CmsModule.MAIN_GOODS,
                         table_name='CmsViewService',
                         data_id=viewservice.id,
                         op_type=CheckOpType.NEW,
                         is_show=0,
                         alter_person=request.user.username,
                         alter_date=time.strftime("%Y-%m-%d %X", time.localtime())).save()
        goods.delete()
        if CMS_CHECK_ON:
            for i, id in enumerate(ids):
                is_show = 1 if i == 0 else 0
                CmsCheck(module=CmsModule.MAIN_GOODS,
                         table_name='CmsGoods',
                         data_id=id,
                         op_type=CheckOpType.DELETE,
                         is_show=is_show,
                         alter_person=request.user.username,
                         alter_date=time.strftime("%Y-%m-%d %X", time.localtime())).save()
    if request.method == "PUT" or request.method == "POST":
        reservedProperties = ['id', 'location']
        data = getJsonData(request)
        goods_id = data['goods_id']
        goods = CmsGoods.objects.using(database).filter(goods_id=goods_id)
        if goods:
            ids = [good[0] for good in goods.values_list("id")]
            if CMS_CHECK_ON:
                for i, id in enumerate(ids):
                    is_show = 1 if i == 0 else 0
                    CmsCheck(module=CmsModule.MAIN_GOODS,
                             table_name='CmsGoods',
                             data_id=id,
                             op_type=CheckOpType.EDIT,
                             is_show=is_show,
                             alter_person=request.user.username,
                             alter_date=time.strftime("%Y-%m-%d %X", time.localtime())).save()
            streamgoods = CmsStreamcontentsGoods.objects.using(database).filter(goods__in=goods)
            for good_stream in streamgoods:
                new_data = {}
                for key in data.keys():
                    if key in reservedProperties:
                        continue
                    new_data[key] = data[key]
                try:
                    CmsGoods.objects.using(database).filter(id=good_stream.goods_id).update(**new_data)
                except Exception as ex:
                    log.error("new data:", new_data)
                    log.error(requests)
                    log.exception(ex)

                del ids[ids.index(good_stream.goods_id)]
            for id in ids:
                CmsGoods.objects.using(database).filter(id=id).update(**data)
        else:
            data['title'] = data['name']
            objgoods = CmsGoods(**data)
            objgoods.save(using=database)
            if CMS_CHECK_ON:
                CmsCheck(module=CmsModule.MAIN_GOODS,
                         table_name='CmsGoods',
                         data_id=objgoods.id,
                         op_type=CheckOpType.NEW,
                         alter_person=request.user.username,
                         alter_date=time.strftime("%Y-%m-%d %X", time.localtime())).save()
    result['ret_code'] = 0
    return HttpResponse(json.dumps(result))


def getJsonData(request):
    data = {}
    request_data = json.loads(request.POST.get("data"))
    city = "*"
    citylst = request_data.get("city")
    if citylst:
        city = ",".join(citylst)
    data["goods_id"] = request_data.get("id")
    data["name"] = request_data.get("name")
    data["search_keyword"] = ",".join(request_data.get("tag"))
    data["small_icon_url"] = request_data.get("icon96")
    data["icon_url"] = request_data.get("icon144")
    data["open_cp_id"] = request_data.get("cpid")
    data["cp_name"] = request_data.get("cpname")
    data["open_service_id"] = request_data.get("appid")
    data["city"] = city
    data["desc"] = request_data.get("desc")
    data["fav_price"] = request_data.get("fav_price")
    data["source_id"] = request_data.get("source_id")
    data["num"] = request_data.get("num")
    data["price"] = request_data.get("price")
    data["location"] = request_data.get("location") if request_data.get("location") else 0
    data['citysJson'] = request_data.get("citysJson")
    data['serviceRangeJson'] = request_data.get('serviceRangeJson')
    action_json = {}
    data["action_id"] = -1
    if not request_data.get("trade_url"):
        action_json['click_type'] = 1
        action_json['dest_activity'] = 'so.contacts.hub.services.open.ui.GoodsDetailActivity'
    else:
        action_json['click_type'] = 2
        action_json['dest_activity'] = 'so.contacts.hub.ui.yellowpage.YellowPageDetailActivity'
        action_json['dest_url'] = request_data.get('trade_url')
    cpInfo = {}
    cpInfo['provider'] = "来自" + request_data.get("appname")
    cpInfo['entry_url'] = request_data.get('entry_url')
    action_json['cp_info'] = json.dumps(cpInfo)
    action_json['dest_title'] = data['name']
    actionParams = {}
    actionParams['goodsId'] = data['goods_id']
    actionParams['serviceId'] = data['open_service_id']
    action_json['action_params'] = json.dumps(actionParams)
    action_json['pt_h5'] = '0'
    data['action_json'] = json.dumps(action_json)
    data['mobile'] = request_data.get("mobile")
    # 商品同步接口中同步是否支持购物车字段,0为不支持，1为支持
    data['is_support_cart'] = request_data.get("is_support_cart")
    if data['mobile']:
        data['name'] = data['name'] + "(测试)"
    if not data['cp_name']:
        data['cp_name'] = request_data.get("appname")
    data['fav_price_desc'] = request_data.get("price_unit")
    data['from_op'] = 1
    return data


# 同步搜索接口 ['category', 'second_category', 'new_second_category', 'new_category']
def sync_search(goods_id, data):
    cate_fields = ['category', 'second_category', 'new_category', 'new_second_category', 'min_version', 'max_version',
                   'recommend_icon', 'recommend_reason', 'sort', 'mark', 'operation_tag', 'tag1', 'tag1_style', 'tag2',
                   'tag2_style', 'tag3', 'tag3_style',
                   'recommend_goodsId', 'recommend_goods_reason', 'op_tag', 'search_keyword']
    if INSTALL_TYPE == 3:
        url = 'http://search1.putao.so/putao3/goods'
    else:
        # url = 'http://api.copy.putao.so/ssearch/putao3/goods'
        url = 'http://api.test.putao.so/ssearch/putao3/goods'
    send_data = {"id": goods_id}
    for cate_field in cate_fields:
        if cate_field in data.keys():
            if cate_field in ['category', 'second_category', 'new_category', 'new_second_category']:
                category = CmsNaviCategory.objects.get(id=data[cate_field])
                send_data.update({cate_field: category.id, cate_field + "_name": category.name})
            send_data.update({cate_field: data[cate_field]})
        else:
            send_data.update({cate_field: "", cate_field + "_name": ""})
    try:
        data = {"data": json.dumps(send_data)}
        r = requests.post(url, data=data)
        log.info(r.status_code)
        log.info(r.content)
        log.info(data)
        content = json.loads(str(r.content, encoding='utf-8'))
        log.info(content['msg'])
    except Exception:
        pass
