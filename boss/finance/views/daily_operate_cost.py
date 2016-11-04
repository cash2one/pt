#coding: utf-8

"""
    日报表
"""

from finance_pub import *
import copy

CONST_UNPENDING_URI = '/finance/unpending_order_list'
CONST_NR_URI        = '/finance/nr_account_order'

def get_data(request, start_date, end_date, app):
    cursor = connections['report'].cursor()
    host_info = request.get_host()

    cursor.execute("call `SP_T_RP_DUIZHANG_DAOJIA_OPERATION_COST_APP`(%s, %s, %s)",
                    [start_date, end_date, app])
    fet_objs = cursor.fetchall()
    objs = string_objs(fet_objs, 9)
    datas = gen_data(objs, host_info, start_date, end_date)
    return datas

def string_objs(fet_objs, num):
    objs = []
    for obj in fet_objs:
        str_obj = []
        for i in range(0, num):
            str_obj.append(str(obj[i]))
        objs.append(str_obj)
    return objs

@login_required
@permission_required(u'man.%s' % FinanceConst.FINANCE_OPERATION_DAOJIA_OPERATION_COST_SUMMARY, raise_exception=True)
@add_common_var
def daily_operate_cost(request, template_name):
    return report_render(request, template_name, {"currentdate": get_datestr(1, "%Y-%m-%d")})

@login_required
@permission_required(u'man.%s' % FinanceConst.FINANCE_OPERATION_DAOJIA_OPERATION_COST_SUMMARY, raise_exception=True)
def daily_operate_cost_ajax(request):
    start_date = request.POST.get("start_date")
    end_date = request.POST.get("end_date")
    app = request.POST.get("app")
    report_check_app(request, app)
    if app:
        app = "^%s$" % app
    else:
        app = get_user_apps(request.user)
    datas = get_data(request, start_date, end_date, app)
    return HttpResponse(json.dumps(datas))

def gen_data(objs, host_info, start_date, end_date):
    t_data = []
    third_data = gen_third_data(objs)
    second_data = gen_second_data(objs,third_data)
    first_data = gen_first_data(objs)

    for v in first_data:
        t_data.append(v)
    for v in second_data:
        t_data.append(v)
    return t_data

def gen_first_data(objs):
    first_data = [['','','','','','','','',''],['','','','','','','','','']]

    for obj in objs:
        if obj[0] == "1":
            if obj[2] == u"运营成本":
                first_data[0][0] = obj[1]
                first_data[0][8] = 1
                first_data[1][8] = 1
                first_data[0][3] = obj[8]
                first_data[1][3] = obj[7] + u'笔'
            elif obj[2] == u"公司福利":
                first_data[0][0] = obj[1]
                first_data[0][4] = obj[8]
                first_data[1][4] = obj[7] + u'笔'
            elif obj[2] == u"用户赔偿":
                first_data[0][0] = obj[1]
                first_data[0][5] = obj[8]
                first_data[1][5] = obj[7] + u'笔'
            elif obj[2] == u"未知分类":
                first_data[0][0] = obj[1]
                first_data[0][6] = obj[8]
                first_data[1][6] = obj[7] + u'笔'

    return first_data

def gen_second_data(objs,third_data):
    pos_info = {}
    second_data = []
    for obj in objs:
        if obj[0] == "2":
            if obj[3] not in pos_info:
                pos_info[obj[3]] = [['','','','','','','','','2'],['','','','','','','','','2']]
            t_data = pos_info[obj[3]]
            if obj[2] == u"运营成本":
                #t_data[0][1] = obj[3]
                t_data[0][3] = obj[8]
                t_data[1][3] = obj[7] + u'笔'
            elif obj[2] == u"公司福利":
                #t_data[0][1] = obj[3]
                t_data[0][4] = obj[8]
                t_data[1][4] = obj[7] + u'笔'
            elif obj[2] == u"用户赔偿":
                #t_data[0][1] = obj[3]
                t_data[0][5] = obj[8]
                t_data[1][5] = obj[7] + u'笔'
            elif obj[2] == u"未知分类":
                t_data[0][1] = obj[3]
                t_data[0][6] = obj[8]
                t_data[1][6] = obj[7] + u'笔'
                try:
                    for v in third_data[obj[3]]:
                        pos_info[obj[3]].append(v)
                except:
                    continue

    for k in pos_info:
        for v in pos_info[k]:
            second_data.append(v)

    return second_data

def gen_third_data(objs):
    pos_info = {}
    third_data = {}
    for obj in objs:
        if obj[0] == "3":
            if obj[3] not in pos_info:
                pos_info[obj[3]] = {}
            if obj[5] not in pos_info[obj[3]]:
                pos_info[obj[3]][obj[5]] = [['','','','','','','','','3'],['','','','','','','','','3']]
            if obj[2] == u"运营成本":
                pos_info[obj[3]][obj[5]][0][2] = obj[5]
                pos_info[obj[3]][obj[5]][0][3] = obj[8]
                pos_info[obj[3]][obj[5]][1][3] = obj[7]+ u'笔'
            elif obj[2] == u"公司福利":
                pos_info[obj[3]][obj[5]][0][2] = obj[5]
                pos_info[obj[3]][obj[5]][0][4] = obj[8]
                pos_info[obj[3]][obj[5]][1][4] = obj[7]+ u'笔'
            elif obj[2] == u"用户赔偿":
                pos_info[obj[3]][obj[5]][0][2] = obj[5]
                pos_info[obj[3]][obj[5]][0][5] = obj[8]
                pos_info[obj[3]][obj[5]][1][5] = obj[7]+ u'笔'
            elif obj[2] == u"未知分类":
                pos_info[obj[3]][obj[5]][0][2] = obj[5]
                pos_info[obj[3]][obj[5]][0][6] = obj[8]
                pos_info[obj[3]][obj[5]][1][6] = obj[7]+ u'笔'

    for k in pos_info:
        third_data[k] = []
        for sub_k in pos_info[k]:
            third_data[k].append(pos_info[k][sub_k][0])
            third_data[k].append(pos_info[k][sub_k][1])

    return third_data


