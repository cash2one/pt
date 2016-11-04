# -*- coding: utf-8 -*-
# Author:wrd
# Jun.23.2016
from __future__ import unicode_literals

from django.db import connections, connection

from pt_card.models import PGoodsInfo
from pt_card.views.pt_card_pub import get_erji_id, get_category_list, get_category_list_local, get_all_sanji_local


def make_url_service(gids):
    """
    生成对应json url,具体商品页
    :param gids: 对应商品id list
    :return: json url
    """
    gids = int(gids) if gids else ''
    action_p = '{"key": "so.contacts.hub.services.open.ui.GoodsDetailActivity","params": {"expend_params": "{\\\"goodsId\\\":%s}"}}' % (
        gids)
    return action_p


def make_url_tab(tab):
    """
    首页分类页
    :param tab: 0:分类页 , 1:分类品牌也
    :return: json url
    """
    tab = int(tab) if tab else 0
    action_p = '{"key": "so.contacts.hub.YellowPageMainActivity","params": {"expend_params": "{\\\"page_index\\\": 1, \\\"tab\\\": %s}"}}' % (
        tab)
    return action_p

def make_url_card(cardID):
    """
    跳转所支持的二级分类list
    :param
    :return: json url
    """
    action_p = '{"key": "so.contacts.hub.services.putaocard.PutaoCardSecondCategoryActivity","params": {"expend_params": "{\\\"pt_card_id\\\": %s}"}}' % (
        cardID)
    return action_p


def make_url_cp(gids):
    """
    生成对应json url  具体cp页
    :param gids: 对应商品id list
    :return: json url
    """
    gids = int(gids) if gids else ''
    action_p = '{"key": "so.contacts.hub.services.open.ui.CpDetailActivity","params":{"expend_params":  "{\\\"cp_id\\\": %s}"}}' % (
        gids)
    return action_p


def make_url_goodslist(cate_id, tag_id=0,cardID=None):
    """
    生成对应json url   商品列表页
    :param cate_id: 二级分类id
    :param tag_id: 三级分类id
    :return: json url
    """
    show_title = get_erji(cate_id)
    if tag_id:
        show_title = get_sanji(tag_id)
    cate_id = int(cate_id) if cate_id else 0
    tag_id = int(tag_id) if tag_id else 0
    action_p = '{"key": "so.contacts.hub.services.open.ui.GoodsListActivity","params": {"id": %s,"action_id": 285,"show_title":"%s","expend_params": "{\\\"title\\\":\\\"%s\\\",\\\"pt_card_id\\\":%s,\\\"category_id\\\": %s, \\\"tag_id\\\": %s}"}}' % (
            cate_id, show_title, show_title,cardID, cate_id, tag_id)
    return action_p


def get_goods_list_action(cps, cps_x):
    """
    通过cp或cps_x查询所有服务
    :param cps: 正选
    :param cps_x: 反选
    :return: 所有服务list
    """
    if cps_x:
        goods = PGoodsInfo.objects.using('open').exclude(
            appid__in=cps_x).only("pid")
        data = [good.pid for good in goods]
    elif cps:
        goods = PGoodsInfo.objects.using('open').filter(
            appid__in=cps).only("pid")
        data = [good.pid for good in goods]
    else:
        data = []
    return data

def get_goods_lists(goods_cat,goods_cat_x):
    """
    如果只选了二级分类
    :param goods_cat:
    :param goods_cat_x:
    :return:
    """
    cursor = connections['cms_db'].cursor()
    if goods_cat_x:
        goods_cat_x = ','.join(goods_cat_x)
        sql = "SELECT goods_id FROM view_cms_goods_formal " \
              "WHERE new_category not in (%s) ;" %(goods_cat_x)
        cursor.execute(sql)
    elif goods_cat:
        goods_cat = ','.join(goods_cat)
        sql = "SELECT goods_id FROM view_cms_goods_formal " \
              "WHERE new_category in (%s) ;" %(goods_cat)
        cursor.execute(sql)
    else :
        return []
    cur = cursor.fetchall()
    if cur:
        lists = [r[0] for r in cur]
    else :
        lists = []
    return lists

def get_goods_lists_sanji(sanji,sanji_x):
    """
    如果只选了三级分类
    :param goods_cat:
    :param goods_cat_x:
    :return:
    """
    cursor = connections['cms_db'].cursor()
    if sanji_x:
        goods_cat_x = ','.join(sanji_x)
        sql = "SELECT group_concat(goods_id) FROM view_cms_goods_formal " \
              "WHERE new_second_category not in (%s) ;" %(goods_cat_x)
        cursor.execute(sql)
    elif sanji:
        goods_cat = ','.join(sanji)
        sql = "SELECT group_concat(goods_id) FROM view_cms_goods_formal " \
              "WHERE new_second_category in (%s) ;" %(goods_cat)
        cursor.execute(sql)
    else :
        return []
    cur = cursor.fetchall()[0][0]
    if cur is not None:
        lists = cur.split(',')
        lists = map(lambda x:int(x),lists)
    else :
        lists = []
    return lists


def filter_gds_cp(data):
    """
    通过服务商品id查找对应的二级分类,三级分类
    :param data: 商品id list
    :return: [(商品id,..),(二级分类去重),(三级分类去重)]
    """
    data_str = ','.join(map(lambda x: str(x), data))
    cursor = connections['cms_db'].cursor()
    sql = "SELECT distinct goods_id,new_category,new_second_category " \
          "FROM view_cms_goods_formal " \
          "where goods_id in (%s) ;" %(data_str)
    cursor.execute(sql)
    cds = cursor.fetchall()
    gs_list = []
    cp_list = []
    cat_list = []
    for i in cds:
        if i[1] and i[2]:
            gs_list.append(i[0])
            cp_list.append(i[1])
            cat_list.append(i[2])
    return [gs_list, list(set(cp_list)), list(set(cat_list))]



def get_erji(id):
    """
    二级id获取名字
    :param id:
    :return:
    """
    cursor = connections['cms_db'].cursor()
    sql = "SELECT name FROM cms_navi_category  WHERE parent_id = 0 AND fatherId = 0 AND type > 0 and id =%s;"
    cursor.execute(sql, [id])
    r_data = cursor.fetchone()
    return r_data[0] if r_data is not None else ''


def get_sanji(id):
    """
    三级id获取名字
    :param id:
    :return:
    """
    cursor = connections['cms_db'].cursor()
    sql = "SELECT c1.NAME FROM cms_navi_category c1 LEFT JOIN cms_navi_category c2 ON c1.fatherId = c2.id " \
          "WHERE c1.fatherId IN (SELECT id FROM cms_navi_category " \
          "WHERE parent_id = 0 AND fatherId = 0 AND type > 0) and c1.id = %s ORDER BY c1.fatherId;"
    cursor.execute(sql, [id])
    r_data = cursor.fetchone()
    return r_data[0] if r_data is not None else ''

def get_gid_by_skuid(id):
    """
    用sku_id获取商品id
    :param id:
    :return:
    """
    if not id :
        return []
    cursor = connections['cms_db'].cursor()
    sql = """
    SELECT distinct goods_id FROM cms_sku where sku_id in (%s);"""
    sqls = sql % (','.join(map(str,id.split(','))))
    cursor.execute(sqls)
    row =  cursor.fetchall()
    if row:
        return [r[0] for r in row]
    return []

def filter_gids(gids_sku,type):
    """去掉前面的s和g
    type=0 把商品和规格合并到gids里面
    type=1 区分商品和规格 返回以逗号隔开的字符串
    :param gids_sku:
    :return:
    """
    gid = []
    sku = []
    if not gids_sku:
        return '',''
    for i in gids_sku.split(','):
        if i[0:1] == 's':
            sku.append(i[1:])
        elif i[0:1] == 'g':
            gid.append(i[1:])
    str_gid = ','.join(list(set(gid)))
    str_sku = ','.join(list(set(sku)))
    if type == 1 :
        return str_gid if str_gid else None,str_sku if str_sku else None
    else:
        return list(set(get_gid_by_skuid(str_sku) + gid))



def decode_dict(cli_data):
    gids = []
    gids_x = []
    cps = []
    cps_x = []
    goods_cat = []
    goods_cat_x = []
    sanji = []
    sanji_x = []
    for i in cli_data:
        if not i:
            continue
        if i.get('gids'):
            gids.append(filter_gids(i.get('gids'),0))
        else:
            gids.append([])
        if i.get('gids_x'):
            gids_x.append(filter_gids(i.get('gids_x'),0))
        else:
            gids_x.append([])
        if i.get('cps'):
            cps.append(i.get('cps').split(','))
        else:
            cps.append([])
        if i.get('cps_x'):
            cps_x.append(i.get('cps_x').split(','))
        else:
            cps_x.append([])
        if i.get('goods_cat'):
            goods_cat.append(i.get('goods_cat').split(','))
        else:
            goods_cat.append([])
        if i.get('goods_cat_x'):
            goods_cat_x.append(i.get('goods_cat_x').split(','))
        else:
            goods_cat_x.append([])
        if i.get('sanji'):
            sanji.append(i.get('sanji').split(','))
        else:
            sanji.append([])
        if i.get('sanji_x'):
            sanji_x.append(i.get('sanji_x').split(','))
        else:
            sanji_x.append([])
    gids = reduce(lambda x, y: list(set(x + y)), gids)
    gids_x = reduce(lambda x, y: list(set(x + y)), gids_x)
    cps = reduce(lambda x, y: list(set(x + y)), cps)
    cps_x = reduce(lambda x, y: list(set(x + y)), cps_x)
    goods_cat = reduce(lambda x, y: list(set(x + y)), goods_cat)
    goods_cat_x = reduce(lambda x, y: list(set(x + y)), goods_cat_x)
    sanji = reduce(lambda x, y: list(set(x + y)), sanji)
    sanji_x = reduce(lambda x, y: list(set(x + y)), sanji_x)
    return map(lambda x: int(x), gids), map(lambda x: int(x), gids_x), \
           map(lambda x: int(x), cps), \
           map(lambda x: int(x), cps_x), \
           map(lambda x: int(x),
               goods_cat), map(lambda x: int(x), goods_cat_x),map(lambda x: int(x), sanji),map(lambda x: int(x), sanji_x)


def click_action_url(cli_data,cardID):
    """
    跳转规则url,生成
    形如 [{'gids':'1,2,3','gids_x':'11','cps':'','cps_x':'1',
    'goods_cat':[328,332],'goods_cat_x':''},{}]
    :param cli_data: [dict,dict]
    :return: json url,正选商品列表
    """
    urls = ''
    if not cli_data:
        urls = make_url_tab(0)
        return urls,[]
    goods_list = []
    gid_lists = []
    for i in cli_data:
        if not i:
            continue
        if i.get('cps') or i.get('cps_x'):
            cps = i.get('cps').split(',') if i.get('cps') else []
            cps_x = i.get('cps_x').split(',') if i.get('cps_x') else []
            goods_list.append(get_goods_list_action(cps, cps_x))
            continue
        elif i.get('sanji') or i.get('sanji_x'):
            sanji = i.get('sanji').split(',') if i.get('sanji') else ''
            sanji_x = i.get('sanji_x').split(',') if i.get('sanji_x') else ''
            goods_list.append(get_goods_lists_sanji(sanji, sanji_x))
            continue
        elif i.get('goods_cat') or i.get('goods_cat_x'):
            goods_cat = i.get('goods_cat').split(',') if i.get('goods_cat') else ''
            goods_cat_x = i.get('goods_cat_x').split(',') if i.get('goods_cat_x') else ''
            goods_list.append(get_goods_lists(goods_cat, goods_cat_x))
            continue
    gids, gids_x, cps, cps_x, goods_cat, goods_cat_x,sanji,sanji_x = decode_dict(cli_data)
    if len(goods_list) > 1:
        goods_list = reduce(lambda x, y: list(set(x + y)), goods_list)
    else:
        try:
            goods_list = goods_list[0]
        except :
            goods_list = []
    if gids or len(gids_x) != 0:
        if len(gids_x) != 0:
            # 正选gids
            gid_list = filter(lambda x: x not in gids_x, goods_list)
            if len(gid_list) == 0:
                # 如果只反选了商品会出现这样的情况,所以返回以下url
                urls = make_url_card(cardID)
                return urls,[]
            gid_lists = gid_list
            cds = filter_gds_cp(gid_list)
        else:
            gid_list = gids
            gid_lists = gid_list
            cds = filter_gds_cp(gid_list)
        if len(gid_list) >= 2:
            if len(cds[2]) == 1:
                urls = make_url_goodslist(cds[1][0], tag_id=cds[2][0],cardID=cardID)
            elif len(cds[1]) == 1 and len(cds[2]) != 1:
                urls = make_url_goodslist(cds[1][0],cardID=cardID)
            else:
                urls = make_url_card(cardID)
        else:
            urls = make_url_service(gid_lists[0])
    elif len(cps_x) != 0 :
        gid_lists = goods_list
        if len(cps_x) != 0:
            urls = make_url_tab(1)
        else:
            urls = make_url_tab(1)
    elif cps:
        gid_lists = goods_list
        if len(cps) == 1:
            urls = make_url_cp(cps[0])
        else:
            urls = make_url_tab(1)
    elif len(sanji_x) != 0:
        gid_lists = goods_list
        all_sanji = get_all_sanji_local()
        filter_sanji = filter(lambda x: x not in sanji_x, all_sanji)
        if len(filter_sanji) == 1:
            urls = make_url_goodslist(get_erji_id(filter_sanji[0]), filter_sanji[0], cardID=cardID)
        else:
            erji_list = get_erji_id(-1,filter_sanji)
            if len(erji_list) == 1:
                urls = make_url_goodslist(erji_list[0], cardID=cardID)
            else:
                urls = make_url_card(cardID)
    elif sanji:
        gid_lists = goods_list
        if len(sanji) == 1:
            urls = make_url_goodslist(get_erji_id(sanji[0]),sanji[0],cardID=cardID)
        else:
            erji_list = get_erji_id(-1, sanji)
            if len(erji_list) == 1:
                urls = make_url_goodslist(erji_list[0], cardID=cardID)
            else:
                urls = make_url_card(cardID)
    elif len(goods_cat_x) != 0:
        gid_lists = goods_list
        all_erji = get_category_list_local()
        filter_erji = filter(lambda x: x not in goods_cat_x, all_erji)
        if len(filter_erji) == 1:
            urls = make_url_goodslist(filter_erji[0], cardID=cardID)
        else:
            urls = make_url_card(cardID)
    elif goods_cat:
        gid_lists = goods_list
        if len(goods_cat) == 1:
            urls = make_url_goodslist(goods_cat[0],cardID=cardID)
        else:
            urls = make_url_card(cardID)
    else:
        urls = make_url_tab(0)
    return urls, gid_lists
