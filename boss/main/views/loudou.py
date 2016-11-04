# -*- coding: utf-8 -*-
# Author:wrd
import datetime
import json

from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator
from django.db import connection
from django.db.models import Sum
from django.http import HttpResponse
from common.views import get_datestr, add_common_var
from main.views.main_pub import   get_ument_app, add_main_var, get_csv_response, \
    get_umeng_cate_tab, get_main_gojs, MainConst,report_render


def filter_data(m_data,launches_count):
    f_data = {}
    for i in m_data:
        if not i[4] in f_data.keys():
            f_data[i[4]] = {}
            f_data[i[4]]['page_count'] = int(i[2])
            f_data[i[4]]['device_count'] = int(i[3])
        else:
            f_data[i[4]]['page_count'] += int(i[2])
            f_data[i[4]]['device_count'] += int(i[3])
    for j in f_data:
        if j == 'd_maincategory' or j == 'd_tabcategory' or j == 'd_sales' or j == 'd_contents':
            f_data[j]['p_percent'] = str(round(f_data[j]['page_count']/float(launches_count)*100,2)) + '%'
            f_data[j]['d_percent'] = str(round(f_data[j]['device_count']/float(launches_count)*100,2)) + '%'
        elif j == 'd_details':
            try:
                f_data[j]['p_percent'] = str(round(f_data['d_order']['page_count']/float(f_data[j]['page_count'])*100,2)) + '%'
            except:
                f_data[j]['p_percent'] = '0%'
            try:
                f_data[j]['d_percent'] = str(round(f_data['d_order']['device_count']/float(f_data[j]['device_count'])*100,2)) + '%'
            except:
                f_data[j]['d_percent'] = '0%'
        elif j == 'd_order':
            try:
                f_data[j]['p_percent'] = str(round(f_data['d_pay']['page_count']/float(f_data[j]['page_count'])*100,2)) + '%'
            except:
                f_data[j]['p_percent'] = '0%'
            try:
                f_data[j]['d_percent'] = str(round(f_data['d_pay']['device_count']/float(f_data[j]['device_count'])*100,2)) + '%'
            except:
                f_data[j]['d_percent'] = '0%'
        elif j == 'd_pay':
            try:
                f_data[j]['p_percent'] = str(round(f_data['d_payresult']['page_count']/float(f_data[j]['page_count'])*100,2)) + '%'
            except:
                f_data[j]['p_percent'] = '0%'
            try:
                f_data[j]['d_percent'] = str(round(f_data['d_payresult']['device_count']/float(f_data[j]['device_count'])*100,2)) + '%'
            except:
                f_data[j]['d_percent'] = '0%'
        elif j == 'd_homecategory' or j == 'd_lists' or j == 'd_payresult':
            f_data[j]['p_percent'] = '0%'
            f_data[j]['d_percent'] = '0%'
    return f_data


def get_main_data(start_date, end_date, app, cate_type):
    try:

        cursor = connection.cursor()
        launches_sql = "SELECT startdate,sum(launches_count) FROM pt_biz_report.umeng_app_launches where startdate >=%s and startdate <= %s and app_key = %s group by startdate;"
        cursor.execute(launches_sql, [start_date, end_date, app])
        r_data = cursor.fetchall()
        every_date = [i[0].strftime("%Y-%m-%d") for i in r_data]
        launches_count = [int(i[1]) for i in r_data]
        launches_counts = reduce(lambda x,y:int(x)+int(y),launches_count)
        # start_date_d = (datetime.datetime.strptime(start_date, "%Y-%m-%d") + datetime.timedelta(days=-1)).strftime("%Y-%m-%d")
        main_sql = "CALL `pt_biz_report`.`SP_T_RP_D_UMENG_PAGE_CONVERSION_MAIN`(%s, %s, %s, %s);"
        cursor.execute(main_sql, [start_date, end_date, app, cate_type])
        m_data = cursor.fetchall()
    except Exception as e:
        raise e
    return int(launches_counts), m_data,launches_count,every_date


def format_gojs(gojs, f_data, type, launches_count):
    percent = 'p_percent' if type == 'page_count' else 'd_percent'
    for i in gojs['nodeDataArray']:
        if i['name'] in f_data.keys():
            i['text'] += str(f_data[i['name']][type])
        elif i['name'] == 'launches_count':
            i['text'] += str(launches_count)
    for i in gojs['linkDataArray']:
        if i['name'] in f_data.keys():
            i['text'] = str(f_data[i['name']][percent])
    return gojs

def get_main_list(data,per_page,cur_page,every_count,type,every_date):
    f_data = []
    # days_list = []
    # for i in range(days_cha):
    #     days_list.append((datetime.datetime.strptime(start_date, "%Y-%m-%d") + datetime.timedelta(days=i)).strftime("%Y-%m-%d"))
    num = 0
    for i in every_date:
        f_json = {}
        f_json['launches'] = every_count[num]
        num += 1
        for j in data:
            if j[1].strftime("%Y-%m-%d") == i:
                f_json['time'] = j[1].strftime("%Y-%m-%d")
                f_json[j[4]] = int(j[2]) if type == 'page_count' else int(j[3])
        f_data.append(f_json)

    global csv_data
    csv_data = []
    csv_data = f_data

    p = Paginator(f_data, per_page)
    num_pags = p.num_pages
    if cur_page > num_pags:
        return [],num_pags
    main_data = p.page(cur_page)
    re_data = um_csv_data(main_data)
    return re_data,num_pags


def um_csv_data(orders):
    c_data = []
    for i in orders:
        c_data.append(
            [
                str(i['time']) if 'time' in i.keys() else '--',
                str(i['launches']) if 'launches' in i.keys() else '--',
                str(i['d_maincategory']) if 'd_maincategory' in i.keys() else '--',
                str(i['d_tabcategory']) if 'd_tabcategory' in i.keys() else '--',
                str(i['d_sales']) if 'd_sales' in i.keys() else '--',
                str(i['d_contents']) if 'd_contents' in i.keys() else '--',
                str(i['d_homecategory']) if 'd_homecategory' in i.keys() else '--',
                str(i['d_lists']) if 'd_lists' in i.keys() else '--',
                str(i['d_details']) if 'd_details' in i.keys() else '--',
                str(i['d_order']) if 'd_order' in i.keys() else '--',
                str(i['d_pay']) if 'd_pay' in i.keys() else '--',
                str(i['d_payresult']) if 'd_payresult' in i.keys() else '--',
            ]
        )
    return c_data


@login_required
@add_common_var
@permission_required(u'man.%s' % MainConst.USER_ON, raise_exception=True)
def loudou_index(request, template_name):
    app_keys = get_ument_app()
    cate_tab = get_umeng_cate_tab()
    return report_render(request, template_name, {
        "currentdate": get_datestr(0, "%Y-%m-%d"),
        'app_keys': app_keys,
        'cate_tabs': cate_tab,
    })


@login_required
@add_common_var
@permission_required(u'man.%s' % MainConst.USER_ON, raise_exception=True)
def loudou_main(request):
    ret_data = {}
    app_key = request.POST.get('apps_key')
    start_date = request.POST.get('start_date')
    end_date = request.POST.get('end_date')
    type = request.POST.get('type')
    cate_tab = request.POST.get('cate_tab') if request.POST.get('cate_tab') != '0' else None
    per_page = int(request.POST.get("per_page"))
    cur_page = int(request.POST.get("cur_page"))
    launches_count, m_data, every_count,every_date = get_main_data(start_date, end_date, app_key, cate_tab)
    # days_cha = (datetime.datetime.strptime(end_date, "%Y-%m-%d") - datetime.datetime.strptime(start_date, "%Y-%m-%d")).days+1
    ret_data['r_data'],ret_data['page'] = get_main_list(m_data,per_page,cur_page,every_count,type,every_date)
    gj = get_main_gojs()
    m_data = filter_data(m_data,launches_count)
    format_gj = format_gojs(gj, m_data, type, launches_count)
    ret_data['gojs'] = json.dumps(format_gj)
    return HttpResponse(json.dumps(ret_data))

@login_required
@permission_required(u'man.%s' % MainConst.USER_ON, raise_exception=True)
@add_common_var
def loudou_main_csv(request):
    appname = request.GET.get('appname').encode('utf-8')
    cate_tab = request.GET.get('cate_tab').encode('utf-8')
    type = request.GET.get('type').encode('utf-8')
    filename = '%s.csv' % (appname+'主流程'+'-'+cate_tab+'-'+type)
    ucsv_data = [[
        "日期",
        "启动次数",
        "首页分类入口",
        "分类页分类入口",
        "秒杀",
        "内容流",
        "分类首页",
        "商品列表页",
        "商品详情页",
        "预约页",
        "支付页",
        "支付结果页",
    ]]
    ucsv_data.extend(um_csv_data(csv_data))
    return get_csv_response(filename, ucsv_data)
