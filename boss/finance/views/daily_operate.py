#coding: utf-8

"""
    日报表
"""

from finance_pub import *
import copy

CONST_UNPENDING_URI = '/finance/unpending_order_list'
CONST_NR_URI        = '/finance/nr_account_order'

def get_data(request, start_date, end_date, app):
    print(request)
    print(start_date)
    print(end_date)
    print(app)
    cursor = connections['report'].cursor()
    host_info = request.get_host()

    #cursor.execute("call `SP_T_RP_DUIZHANG_OPERATION_SUMMARY_NEW`(%s, %s, %s)",
                    #[start_date, end_date, app])
    cursor.execute("call `SP_T_RP_DUIZHANG_OPERATION_SUMMARY_APP`(%s, %s, %s)",
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
    #print("objs is ", objs)
    return objs

def get_third_daily_info(objs):
    third_info = {}
    for obj in objs:
        if obj[0] == "3":
            if not obj[2] in third_info.keys():
                third_info[obj[2]] = {}
            if not obj[3] in third_info[obj[2]].keys():
                third_info[obj[2]][obj[3]] = []
            single_info = {}
            single_info["title"] = obj[4]
            single_info["sum"] = obj[6]
            single_info["deal_count"] = obj[5]
            third_info[obj[2]][obj[3]].append(single_info)

    return third_info

def get_second_daily_info(third_info, objs):
    second_info = {}
    for obj in objs:
        if obj[0] == "2":
            if not obj[2] in second_info.keys():
                second_info[obj[2]] = []
            single_info = {}
            single_info["title"] = obj[3]
            single_info["sum"] = obj[6]
            single_info["deal_count"] = obj[5]
            if obj[2] in third_info.keys():
                if obj[3] in third_info[obj[2]].keys():
                    single_info["level3"] = third_info[obj[2]][obj[3]]
            second_info[obj[2]].append(single_info)

    return second_info

def get_first_daily_info(second_info, objs):
    first_info = [[],[],[],[],[],[],[],[],[],[],[],[],[]]
    for obj in objs:
        if obj[0] == "1":
            single_info = {}
            single_info["title"] = obj[2]
            single_info["sum"] = obj[6]
            single_info["deal_count"] = obj[5]
            if obj[2] in second_info.keys():
                single_info["level2"] = second_info[obj[2]]

            if obj[2] == u"应收款":
                first_info[0].append(single_info)
            elif obj[2] == u"实收款":
                first_info[1].append(single_info)
            elif obj[2] == u"应付款":
                first_info[2].append(single_info)
            elif obj[2] == u"实付款":
                first_info[3].append(single_info)
            elif obj[2] == u"应退款":
                first_info[4].append(single_info)
            elif obj[2] == u"实退款":
                first_info[5].append(single_info)
            elif obj[2] == u"营销策略批价运营成本":
                first_info[6].append(single_info)
            elif obj[2] == u"优惠券运营成本":
                first_info[7].append(single_info)
            elif obj[2] == u"优惠券&营销策略批价运营成本":
                first_info[8].append(single_info)
            elif obj[2] == u"交易手续费":
                first_info[9].append(single_info)
            elif obj[2] == u"对账状态":
                if obj[5] == "0":
                    single_info["deal_count"] = u"正常"
                else:
                    single_info["deal_count"] = u"异常"
                first_info[10].append(single_info)
            elif obj[2] == u"实损益":
                first_info[11].append(single_info)
            elif obj[2] == u"应损益":
                first_info[12].append(single_info)

    return first_info

@login_required
@permission_required(u'man.%s' % FinanceConst.FINANCE_OPERATION_OPERATION_SUMMARY, raise_exception=True)
@add_common_var
def daily_operate(request, template_name):
    return report_render(request, template_name, {"currentdate": get_datestr(1, "%Y-%m-%d")})

@login_required
@permission_required(u'man.%s' % FinanceConst.FINANCE_OPERATION_OPERATION_SUMMARY, raise_exception=True)
def daily_operate_ajax(request):
    start_date = request.POST.get("start_date")
    end_date = request.POST.get("end_date")
    print("start_date is ", start_date)
    print("end_date is ", end_date)

    if not start_date:
        print("====================not start_date")
    if not end_date:
        print("+++++++++++++++++++++ not end date")
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
    third_data = gen_third_data(objs, host_info, start_date, end_date)
    second_data = gen_second_data(objs, host_info, start_date, end_date, third_data)
    first_data = gen_first_data(objs, host_info, start_date, end_date)

    for v in first_data:
        t_data.append(v)
    for v in second_data:
        t_data.append(v)
    return t_data

def gen_first_data(objs, host_info, start_date, end_date):
    first_data = [['','','','','','','','','','','','','','','','','','',''],['','','','','','','','','','','','','','','','','','','']]

    for obj in objs:
        if obj[0] == "1":
            if obj[2] == u"应收款":
                first_data[0][0] = obj[1]
                first_data[0][18] = 1
                first_data[1][18] = 1
                first_data[0][3] = obj[8]
                first_data[1][3] = obj[7] + u'笔'
            elif obj[2] == u"实收款":
                first_data[0][0] = obj[1]
                first_data[0][4] = obj[8]
                first_data[1][4] = obj[7] + u'笔'
            elif obj[2] == u"应付款":
                first_data[0][0] = obj[1]
                first_data[0][5] = obj[8]
                first_data[1][5] = obj[7] + u'笔'
            elif obj[2] == u"实付款":
                first_data[0][0] = obj[1]
                first_data[0][6] = obj[8]
                first_data[1][6] = obj[7] + u'笔'
            elif obj[2] == u"应退款":
                first_data[0][7] = obj[8]
                first_data[1][7] = obj[7] + u'笔'
            elif obj[2] == u"实退款":
                first_data[0][8] = obj[8]
                first_data[1][8] = obj[7] + u'笔'
            elif obj[2] == u"营销策略批价运营成本":
                first_data[0][9] = obj[8]
                first_data[1][9] = obj[7] + u'笔'
            elif obj[2] == u"优惠券运营成本":
                first_data[0][10] = obj[8]
                first_data[1][10] = obj[7] + u'笔'
            elif obj[2] == u"优惠券&营销策略批价运营成本":
                first_data[0][11] = obj[8]
                first_data[1][11] = obj[7] + u'笔'
            elif obj[2] == u"交易手续费":
                first_data[0][12] = obj[8]
                first_data[1][12] = obj[7] + u'笔'
            elif obj[2] == u"异常订单金额":
                first_data[0][13] = obj[8]
                first_data[1][13] = obj[7] + u'笔'
            elif obj[2] == u"应损益":
                first_data[0][14] = obj[8]
                first_data[1][14] = obj[7] + u'笔'
            elif obj[2] == u"实损益":
                first_data[0][15] = obj[8]
                first_data[1][15] = obj[7] + u'笔'
            elif obj[2] == u"对账状态":
                if obj[7] == "0":
                    first_data[0][16]  = u"正常"
                else:
                    first_data[0][16] = u"异常"
                    t_url = host_info + CONST_UNPENDING_URI
                    first_data[0][17] = get_url(t_url, start_date=start_date, end_date=end_date)
    return first_data

def gen_second_data(objs, host_info, start_date, end_date, third_data):
    pos_info = {}
    second_data = []
    for obj in objs:
        if obj[0] == "2":
            if obj[3] not in pos_info:
                pos_info[obj[3]] = [['','','','','','','','','','','','','','','','','','','2'],['','','','','','','','','','','','','','','','','','','2']]
            t_data = pos_info[obj[3]]
            if obj[2] == u"应收款":
                #t_data[0][1] = obj[3]
                t_data[0][3] = obj[8]
                t_data[1][3] = obj[7] + u'笔'
            elif obj[2] == u"实收款":
                #t_data[0][1] = obj[3]
                t_data[0][4] = obj[8]
                t_data[1][4] = obj[7] + u'笔'
            elif obj[2] == u"应付款":
                #t_data[0][1] = obj[3]
                t_data[0][5] = obj[8]
                t_data[1][5] = obj[7] + u'笔'
            elif obj[2] == u"实付款":
                #t_data[0][1] = obj[3]
                t_data[0][6] = obj[8]
                t_data[1][6] = obj[7] + u'笔'
            elif obj[2] == u"应退款":
                t_data[0][7] = obj[8]
                t_data[1][7] = obj[7] + u'笔'
            elif obj[2] == u"实退款":
                t_data[0][8] = obj[8]
                t_data[1][8] = obj[7] + u'笔'
            elif obj[2] == u"营销策略批价运营成本":
                t_data[0][9] = obj[8]
                t_data[1][9] = obj[7] + u'笔'
            elif obj[2] == u"优惠券运营成本":
                t_data[0][10] = obj[8]
                t_data[1][10] = obj[7] + u'笔'
            elif obj[2] == u"优惠券&营销策略批价运营成本":
                t_data[0][11] = obj[8]
                t_data[1][11] = obj[7] + u'笔'
            elif obj[2] == u"交易手续费":
                t_data[0][12] = obj[8]
                t_data[1][12] = obj[7] + u'笔'
            elif obj[2] == u"异常订单金额":
                t_data[0][13] = obj[8]
                t_data[1][13] = obj[7] + u'笔'
            elif obj[2] == u"应损益":
                t_data[0][14] = obj[8]
                t_data[1][14] = obj[7] + u'笔'
            elif obj[2] == u"实损益":
                t_data[0][15] = obj[8]
                t_data[1][15] = obj[7] + u'笔'
            elif obj[2] == u"对账状态":
                t_data[0][1] = obj[3]
                try:
                    for v in third_data[obj[3]]:
                        pos_info[obj[3]].append(v)
                except:
                    continue

                if obj[7] == "0":
                    t_data[0][16]  = u"正常"
                else:
                    t_data[0][16] = u"异常"
                    t_url = host_info + CONST_UNPENDING_URI
                    if obj[3] == u'非匹配业务类型':
                        t_url = host_info + CONST_NR_URI
                    t_data[0][17] = get_url(t_url, order_type=obj[4], start_date=start_date, end_date=end_date)

    for k in pos_info:
        for v in pos_info[k]:
            second_data.append(v)

    return second_data

def gen_third_data(objs, host_info, start_date, end_date):
    pos_info = {}
    third_data = {}
    for obj in objs:
        if obj[0] == "3":
            if obj[3] not in pos_info:
                pos_info[obj[3]] = {}
            if obj[5] not in pos_info[obj[3]]:
                pos_info[obj[3]][obj[5]] = [['','','','','','','','','','','','','','','','','','','3'],['','','','','','','','','','','','','','','','','','','']]
            if obj[2] == u"应收款":
                pos_info[obj[3]][obj[5]][0][2] = obj[5]
                pos_info[obj[3]][obj[5]][0][3] = obj[8]
                pos_info[obj[3]][obj[5]][1][3] = obj[7]+ u'笔'
            elif obj[2] == u"实收款":
                pos_info[obj[3]][obj[5]][0][2] = obj[5]
                pos_info[obj[3]][obj[5]][0][4] = obj[8]
                pos_info[obj[3]][obj[5]][1][4] = obj[7]+ u'笔'
            elif obj[2] == u"应付款":
                pos_info[obj[3]][obj[5]][0][2] = obj[5]
                pos_info[obj[3]][obj[5]][0][5] = obj[8]
                pos_info[obj[3]][obj[5]][1][5] = obj[7]+ u'笔'
            elif obj[2] == u"实付款":
                pos_info[obj[3]][obj[5]][0][2] = obj[5]
                pos_info[obj[3]][obj[5]][0][6] = obj[8]
                pos_info[obj[3]][obj[5]][1][6] = obj[7]+ u'笔'
            elif obj[2] == u"应退款":
                pos_info[obj[3]][obj[5]][0][7] = obj[8]
                pos_info[obj[3]][obj[5]][1][7] = obj[7]+ u'笔'
            elif obj[2] == u"实退款":
                pos_info[obj[3]][obj[5]][0][8] = obj[8]
                pos_info[obj[3]][obj[5]][1][8] = obj[7]+ u'笔'
            elif obj[2] == u"营销策略批价运营成本":
                pos_info[obj[3]][obj[5]][0][9] = obj[8]
                pos_info[obj[3]][obj[5]][1][9] = obj[7]+ u'笔'
            elif obj[2] == u"优惠券运营成本":
                pos_info[obj[3]][obj[5]][0][10] = obj[8]
                pos_info[obj[3]][obj[5]][1][10] = obj[7]+ u'笔'
            elif obj[2] == u"优惠券&营销策略批价运营成本":
                pos_info[obj[3]][obj[5]][0][11] = obj[8]
                pos_info[obj[3]][obj[5]][1][11] = obj[7]+ u'笔'
            elif obj[2] == u"交易手续费":
                pos_info[obj[3]][obj[5]][0][12] = obj[8]
                pos_info[obj[3]][obj[5]][1][12] = obj[7]+ u'笔'
            elif obj[2] == u"异常订单金额":
                pos_info[obj[3]][obj[5]][0][13] = obj[8]
                pos_info[obj[3]][obj[5]][1][13] = obj[7]+ u'笔'
            elif obj[2] == u"应损益":
                pos_info[obj[3]][obj[5]][0][14] = obj[8]
                pos_info[obj[3]][obj[5]][1][14] = obj[7]+ u'笔'
            elif obj[2] == u"实损益":
                pos_info[obj[3]][obj[5]][0][15] = obj[8]
                pos_info[obj[3]][obj[5]][1][15] = obj[7]+ u'笔'
            elif obj[2] == u"对账状态":
                if obj[7] == "0":
                    pos_info[obj[3]][obj[5]][0][16]  = u"正常"
                else:
                    pos_info[obj[3]][obj[5]][0][16] = u"异常"
                    t_url = host_info + CONST_UNPENDING_URI
                    if obj[3] == u'非匹配业务类型':
                        t_url = host_info + CONST_NR_URI
                    pos_info[obj[3]][obj[5]][0][17] = get_url(t_url, order_type=obj[4], cp_type=obj[6], start_date=start_date, end_date=end_date)

    for k in pos_info:
        third_data[k] = []
        for sub_k in pos_info[k]:
            third_data[k].append(pos_info[k][sub_k][0])
            third_data[k].append(pos_info[k][sub_k][1])

    return third_data


def get_url(url, **kwargs):
    parameters = ""
    for key in kwargs:
        parameters = str(key)+'='+str(kwargs[key])+'&'+parameters
    return url + '?' + parameters

def sort_data(data):
    return_data = []
    for first_obj in data:
        t_data = [first_obj[0], first_obj[1], first_obj[2], first_obj[3], first_obj[4], first_obj[5], first_obj[6], first_obj[7], first_obj[8], first_obj[9], first_obj[10], first_obj[11], first_obj[12], first_obj[13], first_obj[14], first_obj[15], first_obj[16]]
        return_data.append(t_data)
    return return_data

def get_third_csv_info(objs):
    third_info = {}
    for obj in objs:
        if obj[0] == "3":
            if not obj[2] in third_info.keys():
                third_info[obj[2]] = {}
            if not obj[3] in third_info[obj[2]].keys():
                third_info[obj[2]][obj[3]] = []
            third_info[obj[2]][obj[3]].append(obj)
    return third_info

def get_second_csv_info(third_info, objs):
    second_info = {}
    for obj in objs:
        if obj[0] == "2":
            if not obj[2] in second_info.keys():
                second_info[obj[2]] = []
            second_info[obj[2]].append(obj)
            if obj[2] in third_info.keys():
                if obj[3] in third_info[obj[2]].keys():
                    for single_obj in third_info[obj[2]][obj[3]]:
                        second_info[obj[2]].append(single_obj)
    return second_info

def get_first_csv_info(second_info, objs):
    first_info = [[],[],[],[],[],[],[],[],[],[],[],[],[]]
    for obj in objs:
        if obj[0] == "1":
            if obj[2] == u"应收款":
                first_info[0].append(obj)
                if obj[2] in second_info.keys():
                    for single_obj in second_info[obj[2]]:
                        first_info[0].append(single_obj)
            elif obj[2] == u"实收款":
                first_info[1].append(obj)
                if obj[2] in second_info.keys():
                    for single_obj in second_info[obj[2]]:
                        first_info[1].append(single_obj)
            elif obj[2] == u"应付款":
                first_info[2].append(obj)
                if obj[2] in second_info.keys():
                    for single_obj in second_info[obj[2]]:
                        first_info[2].append(single_obj)
            elif obj[2] == u"实付款":
                first_info[3].append(obj)
                if obj[2] in second_info.keys():
                    for single_obj in second_info[obj[2]]:
                        first_info[3].append(single_obj)
            elif obj[2] == u"应退款":
                first_info[4].append(obj)
                if obj[2] in second_info.keys():
                    for single_obj in second_info[obj[2]]:
                        first_info[4].append(single_obj)
            elif obj[2] == u"实退款":
                first_info[5].append(obj)
                if obj[2] in second_info.keys():
                    for single_obj in second_info[obj[2]]:
                        first_info[5].append(single_obj)
            elif obj[2] == u"营销策略批价运营成本":
                first_info[6].append(obj)
                if obj[2] in second_info.keys():
                    for single_obj in second_info[obj[2]]:
                        first_info[6].append(single_obj)
            elif obj[2] == u"优惠券运营成本":
                first_info[7].append(obj)
                if obj[2] in second_info.keys():
                    for single_obj in second_info[obj[2]]:
                        first_info[7].append(single_obj)
            elif obj[2] == u"优惠券&营销策略批价运营成本":
                first_info[8].append(obj)
                if obj[2] in second_info.keys():
                    for single_obj in second_info[obj[2]]:
                        first_info[8].append(single_obj)
            elif obj[2] == u"交易手续费":
                first_info[9].append(obj)
                if obj[2] in second_info.keys():
                    for single_obj in second_info[obj[2]]:
                        first_info[9].append(single_obj)
            elif obj[2] == u"对账状态":
                if obj[5] == "0":
                    obj[5] = u"正常"
                else:
                    obj[5] = u"异常"
                first_info[10].append(obj)
                if obj[2] in second_info.keys():
                    for single_obj in second_info[obj[2]]:
                        first_info[10].append(single_obj)
            elif obj[2] == u"实损益":
                first_info[11].append(obj)
                if obj[2] in second_info.keys():
                    for single_obj in second_info[obj[2]]:
                        first_info[11].append(single_obj)
            elif obj[2] == u"应损益":
                first_info[12].append(obj)
                if obj[2] in second_info.keys():
                    for single_obj in second_info[obj[2]]:
                        first_info[12].append(single_obj)
    return first_info

@login_required
@permission_required(u'man.%s' % FinanceConst.FINANCE_OPERATION_OPERATION_SUMMARY, raise_exception=True)
def daily_operate_csv(request):
    start_date = request.GET["start_date"]
    end_date = request.GET["end_date"]
    print("start_date is ", start_date)
    print("end_date is ", end_date)

    if not start_date:
        print("====================not start_date")
    if not end_date:
        print("+++++++++++++++++++++ not end date")

    app = request.GET["app"]
    report_check_app(request, app)
    if app:
        app = "^%s$" % app
    else:
        app = get_user_apps(request.user)

    datas = get_data(request, start_date, end_date, app)

    filename = '%s(%s-%s).csv' % ("运营数据汇总表", str(start_date), str(end_date))
    csv_data = [["项目名称",
                "业务名称",
                "运营商名称",
                "应收款",
                "实收款",
                "应付款",
                "实付款",
                "应退款",
                "实退款",
                "批价策略",
                "优惠券",
                "其他",
                "交易手续",
                "异常订单金额",
                "应损益",
                "实损益",
                "对账状态"]]
    return_data = sort_data(datas)
    csv_data.extend(return_data)

    return get_csv_response(filename, csv_data)