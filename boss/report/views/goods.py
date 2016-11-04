# coding: utf-8
from django.shortcuts import render_to_response
from report_pub import *


@login_required
@permission_required(u'man.%s' % ReportConst.GOODS, raise_exception=True)
@add_common_var
def goods(request, template_name):
    return report_render(request, template_name,{
    })


def __get_arr(arr, val):
    for a in arr:
        if a[0] == val:
            return a


def __get_goods_data(key, per_page, cur_page):
    cms_cursor = connections['cms'].cursor()
    cms_cursor.execute("""select category1.name as 一级分类, category2.name as 二级分类, new_category1.name as 新一级分类, new_category2.name as 新二级分类, cms_goods.name as 商品名, cms_goods.cp_name as 服务商, cms_goods.city as 覆盖城市,
      cms_goods.price as 原价, cms_goods.fav_price as 优惠价, cms_goods.goods_id as 商品id
      from cms_goods
      left join cms_navi_category as category1 on cms_goods.category = category1.id
      left join cms_navi_category as category2 on cms_goods.second_category = category2.id
      left join cms_navi_category as new_category1 on cms_goods.new_category = new_category1.id
      left join cms_navi_category as new_category2 on cms_goods.new_second_category = new_category2.id
      where (cms_goods.mobile is null or cms_goods.mobile = "") and (category1.name like '%%""" + key + """%%' or category2.name like '%%""" + key + """%%' or cms_goods.cp_name like '%%""" + key + """%%' or cms_goods.name like '%%""" + key + """%%')
      group by goods_id
    """)
    goods = cms_cursor.fetchall()
    num_pages = 0
    if per_page and cur_page:
        goods, num_pages = pag(goods, per_page, cur_page)
    ids = []
    for good in goods:
        ids.append(str(good[-1]))
    if not ids:
        return [], 1
    ids_str = "(" + ",".join(ids) + ")"
    open_cursor = connections['open'].cursor()
    open_cursor.execute("""SELECT
      `pid` 商品id,
      `name` 商品名称,
      (SELECT
        GROUP_CONCAT(`desc`)
      FROM
        p_coupon c
      WHERE (
          c.gids LIKE CONCAT(goods.pid, ',%%')
          OR c.gids LIKE CONCAT('%%,', goods.pid)
          OR c.gids LIKE CONCAT('%%,', goods.pid, ',%%')
        )
        AND NOW() BETWEEN c.start_time
        AND c.end_time) 支持的优惠券信息,
      (SELECT
        GROUP_CONCAT(
          CASE
            psub.`apply_user`
            WHEN 0
            THEN '全部用户'
            WHEN 1
            THEN '新用户'
            WHEN 2
            THEN '老用户'
          END,
          CASE
            psub.`promotion_type`
            WHEN 1
            THEN '定价型'
            WHEN 2
            THEN '立减型'
          END,
          ':',
          psub.`price` / 100,
          '元'
        )
      FROM
        p_promotion_activity_master pmst
        INNER JOIN p_promotion_activity psub
          ON pmst.`id` = psub.`master_id`
      WHERE pmst.`gid` = goods.`pid`
        AND pmst.`visible` = 1
        AND NOW() BETWEEN psub.`begin_date`
        AND psub.`end_date`) 促销活动信息,
      CASE
        `status`
        WHEN 0
        THEN '草稿状态'
        WHEN 1
        THEN '审核中'
        WHEN 2
        THEN '审核成功'
        WHEN 3
        THEN '审核失败'
        WHEN 4
        THEN '测试中'
      END 商品当前状态,
      (SELECT
        MIN(verify_time)
      FROM
        p_goods_verify gv
      WHERE gv.gid = goods.pid
        AND gv.verify_result = 2) 上架时间
    FROM
      p_goods_info goods
    WHERE goods.pid in """ + ids_str)
    opens = open_cursor.fetchall()
    result = []
    for i, good in enumerate(goods):
        temp = __get_arr(opens, good[-1])
        if temp:
            no = i + 1
            if per_page and cur_page:
                no = str(i + (int(cur_page) - 1) * int(per_page) + 1)
            item = [
                no,
                str(good[0]),
                str(good[1]),
                str(good[2]),
                str(good[3]),
                str(good[4]),
                str(good[5]),
                str(good[6]),
                str(good[7]),
                str(good[8]),
                str(temp[2]),
                str(temp[3]),
                str(temp[4]),
                str(temp[5])
            ]
            result.append(item)
    filter_none(result)
    return result, num_pages


@login_required
@permission_required(u'man.%s' % ReportConst.GOODS, raise_exception=True)
def goods_ajax(request):
    per_page = request.POST.get("per_page")
    cur_page = request.POST.get("cur_page")
    key = request.POST.get("key")
    result, num_pages = __get_goods_data(key, per_page, cur_page)
    return HttpResponse(json.dumps([result, num_pages]))


@login_required
@permission_required(u'man.%s' % ReportConst.GOODS, raise_exception=True)
def goods_csv(request):
    result, num_pages = __get_goods_data("", None, None)
    csv_data = [["序号","一级分类","二级分类","新一级分类","新二级分类","商品名","服务商","覆盖城市","原价","优惠价","支持的优惠券信息","促销活动信息","状态","上架时间"]]
    csv_data.extend(result)
    name = "商品统计明细表"
    filename = '%s.csv' % (name)
    return get_csv_response(filename, csv_data)