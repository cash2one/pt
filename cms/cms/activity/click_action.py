# -*- coding: utf-8 -*-
# Author:wrd
# Jun.23.2016
from __future__ import unicode_literals

from django.db import connections, connection

from pt_open.models import PGoodsInfo


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
    else:
        goods = PGoodsInfo.objects.using('open').filter(
            appid__in=cps).only("pid")
        data = [good.pid for good in goods]

    return data


def filter_gds_cp(data):
    """
    通过服务商品id查找对应的二级分类,三级分类
    :param data: 商品id list
    :return: [(商品id,..),(二级分类去重),(三级分类去重)]
    """
    data_str = ','.join(map(lambda x: str(x), data))
    cursor = connections['default'].cursor()
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
    分类导航,cp导航
    :param tab: 0,分类导航,1,cp导航
    :return: json url
    """
    tab = int(tab) if tab else 0
    action_p = '{"key": "so.contacts.hub.YellowPageMainActivity","params": {"expend_params": "{\\\"page_index\\\": 1, \\\"tab\\\": %s}"}}' % (
        tab)
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


def make_url_goodslist(cate_id, tag_id=0):
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
    action_p = '{"key": "so.contacts.hub.services.open.ui.GoodsListActivity","params": {"id": %s,"action_id": 285,"show_title":"%s","expend_params": "{\\\"title\\\":\\\"%s\\\",\\\"category_id\\\": %s, \\\"tag_id\\\": %s}"}}' % (
        cate_id,show_title[0],show_title[0],cate_id, tag_id)
    return action_p

def get_erji(id):
    cursor = connection.cursor()
    sql = "SELECT name FROM cms_navi_category  WHERE parent_id = 0 AND fatherId = 0 AND type > 0 and id =%s;"
    cursor.execute(sql, [id])
    return cursor.fetchone()


def get_sanji(id):
    cursor = connection.cursor()
    sql = "SELECT c1.NAME FROM cms_navi_category c1 LEFT JOIN cms_navi_category c2 ON c1.fatherId = c2.id " \
          "WHERE c1.fatherId IN (SELECT id FROM cms_navi_category " \
          "WHERE parent_id = 0 AND fatherId = 0 AND type > 0) and c1.id = %s ORDER BY c1.fatherId;"
    cursor.execute(sql, [id])
    return cursor.fetchone()



def decode_dict(cli_data):
    gids = []
    gids_x = []
    cps = []
    cps_x = []
    goods_cat = []
    goods_cat_x = []
    for i in cli_data:
        if not i:
            continue
        if i.get('gids'):
            gids.append(i.get('gids').split(','))
        else:
            gids.append([])
        if i.get('gids_x'):
            gids_x.append(i.get('gids_x').split(','))
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
    gids = reduce(lambda x, y: list(set(x + y)), gids)
    gids_x = reduce(lambda x, y: list(set(x + y)), gids_x)
    cps = reduce(lambda x, y: list(set(x + y)), cps)
    cps_x = reduce(lambda x, y: list(set(x + y)), cps_x)
    goods_cat = reduce(lambda x, y: list(set(x + y)), goods_cat)
    goods_cat_x = reduce(lambda x, y: list(set(x + y)), goods_cat_x)
    return map(lambda x: int(x), gids), map(lambda x: int(x), gids_x), \
           map(lambda x: int(x), cps), \
           map(lambda x: int(x), cps_x), \
           map(lambda x: int(x),
               goods_cat), map(lambda x: int(x), goods_cat_x)


def click_action_url(cli_data):
    """
    跳转规则url,生成
    形如 [{'gids':'1,2,3','gids_x':'11','cps':'','cps_x':'1',
    'goods_cat':[328,332],'goods_cat_x':''},{}]
    :param cli_data: [dict,dict]
    :return: json url,正选商品列表
    """
    urls = ''
    if not cli_data:
        return urls,[]
    goods_list = []
    gid_lists = []
    for i in cli_data:
        if not i:
            continue
        cps = i.get('cps').split(',') if i.get('cps') else []
        cps_x = i.get('cps_x').split(',') if i.get('cps_x') else []
        goods_list.append(get_goods_list_action(cps, cps_x))
    gids, gids_x, cps, cps_x, goods_cat, goods_cat_x = decode_dict(cli_data)
    if len(goods_list) > 1:
        goods_list = reduce(lambda x, y: list(set(x + y)), goods_list)
    else:
        goods_list = goods_list[0]
    if gids or len(gids_x) != 0:
        if len(gids_x) != 0:
            # 正选gids
            gid_list = filter(lambda x: x not in gids_x, goods_list)
            gid_lists = gid_list
            cds = filter_gds_cp(gid_list)
        else:
            gid_list = gids
            gid_lists = gid_list
            cds = filter_gds_cp(gid_list)
        if len(gid_list) >= 2:
            if len(cds[2]) == 1:
                urls = make_url_goodslist(cds[1][0], tag_id=cds[2][0])
            elif len(cds[1]) == 1 and len(cds[2]) != 1:
                urls = make_url_goodslist(cds[1][0])
            else:
                urls = make_url_tab(0)
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
    elif len(goods_cat_x) != 0:
        gid_lists = goods_list
        if len(goods_cat_x) != 0:
            urls = make_url_tab(0)
        else:
            urls = make_url_tab(0)
    elif goods_cat:
        gid_lists = goods_list
        if len(goods_cat) == 1:
            urls = make_url_goodslist(goods_cat[0])
        else:
            urls = make_url_tab(0)
    return urls, gid_lists
