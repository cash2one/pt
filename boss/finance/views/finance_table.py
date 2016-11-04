#coding: utf-8

"""
    财务报表
"""
import copy
from finance_pub import *
import xlwt

@login_required
@add_common_var
def index(request):
    objs = AuthUserUserPermissions.objects.filter(user=request.user)
    permission_modules = {}
    for obj in objs:
        if obj.permission.content_type_id == PermissionType.MODULE:
            permission_modules[obj.permission.codename] = True
    if FinanceConst.FINANCE_ZF_PAYMENT_CHANNEL_REPORT in permission_modules.keys():
        return  report_render(request, "finance_table.html",{"currentdate": get_datestr(1, "%Y-%m-%d")})
    elif FinanceConst.DAILY_SUM in permission_modules.keys():
        return  report_render(request, "daily_operate.html",{"currentdate": get_datestr(1, "%Y-%m-%d")})
    elif FinanceConst.EXCEPT_ORDER_SUM in permission_modules.keys():
        return  report_render(request, "except_order_sum.html",{"currentdate": get_datestr(1, "%Y-%m-%d")})
    elif FinanceConst.CP_EVENT in permission_modules.keys():
        return  report_render(request, "upload_cp_bill.html",{"currentdate": get_datestr(1, "%Y-%m-%d")})
    else:
        raise PermissionDenied



@login_required
@add_common_var
def finance_index(request, template_name):
    return report_render(request, template_name, {"currentdate": get_datestr(1, "%Y-%m-%d")})


@login_required
@permission_required(u'man.%s' % FinanceConst.FINANCE_ZF_PAYMENT_CHANNEL_REPORT, raise_exception=True)
@add_common_var
def finance_table(request, template_name):
    print(template_name)
    return report_render(request, template_name, {"currentdate": get_datestr(1, "%Y-%m-%d")})


def get_zf_first_info(second_info, objs):
    second_copy = copy.deepcopy(second_info)
    first_info = [[{}],[{}],[{}]]
    for obj in objs:
        if obj[0] == "1":
            if obj[5] == "I":
                first_info[0][0]["title"] = obj[2]
                first_info[0][0]["sum"] = obj[4]
                first_info[0][0]["deal_count"] = obj[3]
                if "I" in second_info.keys():
                    first_info[0][0]["level2"] = second_copy["I"]
            elif obj[5] == "O":
                first_info[1][0]["title"] = obj[2]
                first_info[1][0]["sum"] = obj[4]
                first_info[1][0]["deal_count"] = obj[3]
                if "O" in second_info.keys():
                    first_info[1][0]["level2"] = second_copy["O"]
            elif obj[5] == "B":
                first_info[2][0]["title"] = obj[2]
                first_info[2][0]["sum"] = obj[4]
                first_info[2][0]["deal_count"] = obj[3]
                if "B" in second_info.keys():
                    first_info[2][0]["level2"] = second_copy["B"]

    return first_info

def get_zf_second_info(third_info, objs):
    third_copy = copy.deepcopy(third_info)
    second_info = {}
    for obj in objs:
        if obj[0] == "2":
            if not obj[5] in second_info.keys():
                second_info[str(obj[5])] = []
            single_info = {}
            single_info["title"] = obj[2]
            if obj[2] == u"账户余额":
                single_info["title"] = obj[1]
            single_info["sum"] = obj[4]
            single_info["deal_count"] = obj[3]
            if obj[2] in third_copy.keys():
                single_info["level3"] = third_copy[obj[2]]
            second_info[obj[5]].append(single_info)
    return second_info

def get_zf_third_info(objs):
    third_info = {}
    for obj in objs:
        if obj[0] == "3":
            if not obj[2] in third_info.keys():
                third_info[obj[2]] = []
            single_info = {}
            single_info["title"] = obj[1]
            single_info["sum"] = obj[4]
            single_info["deal_count"] = obj[3]
            third_info[obj[2]].append(single_info)
    return third_info

def get_cp_first_info(second_info, objs):
    second_copy = copy.deepcopy(second_info)
    first_info = [[{}],[{}]]
    for obj in objs:
        if obj[0] == "1":
            if obj[5] == "O":
                first_info[1][0]["title"] = obj[2]
                first_info[1][0]["sum"] = obj[4]
                first_info[1][0]["deal_count"] = obj[3]
                if "O" in second_info.keys():
                    first_info[1][0]["level2"] = second_copy["O"]
            elif obj[5] == "B":
                first_info[0][0]["title"] = obj[2]
                first_info[0][0]["sum"] = obj[4]
                first_info[0][0]["deal_count"] = obj[3]
                if "B" in second_info.keys():
                    first_info[0][0]["level2"] = second_copy["B"]

    return first_info

def get_cp_second_info(third_info, objs):
    third_copy = copy.deepcopy(third_info)
    second_info = {}
    for obj in objs:
        if obj[0] == "2":
            if not obj[5] in second_info.keys():
                second_info[obj[5]] = []
            single_info = {}
            single_info["title"] = obj[1]
            single_info["sum"] = obj[4]
            single_info["deal_count"] = obj[3]
            if obj[2] in third_copy.keys():
                single_info["level3"] = third_copy[obj[2]]
            second_info[obj[5]].append(single_info)
    return second_info

def get_pt_first_info(second_info, objs):
    second_copy = copy.deepcopy(second_info)
    first_info = [[{}]]
    for obj in objs:
        if obj[0] == "1":
            if obj[5] == "O":
                first_info[0][0]["title"] = obj[2]
                first_info[0][0]["sum"] = obj[4]
                first_info[0][0]["deal_count"] = obj[3]
                if "O" in second_info.keys():
                    first_info[0][0]["level2"] = second_copy["O"]

    return first_info

def get_pt_second_info(third_info, objs):
    third_copy = copy.deepcopy(third_info)
    second_info = {}
    for obj in objs:
        if obj[0] == "2":
            if not obj[5] in second_info.keys():
                second_info[obj[5]] = []
            single_info = {}
            single_info["title"] = obj[1]
            single_info["sum"] = obj[4]
            single_info["deal_count"] = obj[3]
            if obj[2] in third_copy.keys():
                single_info["level3"] = third_copy[obj[2]]
            second_info[obj[5]].append(single_info)
    return second_info

def string_objs(fet_objs, num):
    objs = []
    for obj in fet_objs:
        str_obj = []
        for i in range(0, num):
            str_obj.append(str(obj[i]))
        objs.append(str_obj)
    #print("objs is ", objs)
    return objs

def get_zf_objs(start_date, end_date, zf):
    cursor = connections['report'].cursor()
    cursor.execute("call `SP_T_RP_D_ZF_ORDER_SUMMARY_ACCOUNT`(%s, %s, %s)",
                    [start_date, end_date, zf])
    fet_objs = cursor.fetchall()
    objs = string_objs(fet_objs, 6)
    cursor.close()
    return objs

def get_zf_data(start_date, end_date, zf):
    '''cursor = connections['report'].cursor()
    cursor.execute("call `SP_T_RP_D_ZF_ORDER_SUMMARY`(%s, %s)",
                    [start_date, end_date])
    fet_objs = cursor.fetchall()
    objs = string_objs(fet_objs, 6)'''
    objs = get_zf_objs(start_date, end_date, zf)
    zf_third_info  = get_zf_third_info(objs)
    zf_second_info = get_zf_second_info(zf_third_info, objs)
    zf_first_info  = get_zf_first_info(zf_second_info, objs)

    return zf_first_info

def get_cp_objs(start_date, end_date, app):
    cursor = connections['report'].cursor()
    cursor.execute("call `SP_T_RP_D_CP_ORDER_SUMMARY_APP`(%s, %s, %s)",
                    [start_date, end_date, app])
    fet_objs = cursor.fetchall()
    objs = string_objs(fet_objs, 6)
    return objs

def get_cp_data(start_date, end_date):
    objs = get_cp_objs(start_date, end_date)
    cp_second_info = get_cp_second_info({}, objs)
    cp_first_info  = get_cp_first_info(cp_second_info, objs)

    return cp_first_info

def get_pt_objs(start_date, end_date, app):
    cursor = connections['report'].cursor()
    cursor.execute("call `SP_T_RP_D_PT_ORDER_SUMMARY_APP`(%s, %s, %s)",
                    [start_date, end_date, app])
    fet_objs = cursor.fetchall()
    objs = string_objs(fet_objs, 6)
    return objs

def get_pt_data(start_date, end_date):
    objs = get_pt_objs(start_date, end_date)
    pt_second_info = get_pt_second_info({}, objs)
    pt_first_info  = get_pt_first_info(pt_second_info, objs)

    return pt_first_info

@login_required
@permission_required(u'man.%s' % FinanceConst.FINANCE_ZF_PAYMENT_CHANNEL_REPORT, raise_exception=True)
def finance_table_ajax(request):
    start_date = request.POST["start_date"]
    end_date = request.POST["end_date"]
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

    zf = get_user_zfs(request.user)

    print("app is ", app, "zf is ", zf)
    business_info = []
    zf_info = get_zf_infos(start_date, end_date, zf)
    #print("zf info is ", zf_info)
    cp_info = get_cp_infos(start_date, end_date, app)
    #print("cp info is ", cp_info)

    business_info.append(zf_info)
    business_info.append(cp_info)

    return HttpResponse(json.dumps(business_info))

def get_zf_infos(start_date, end_date, zf):
    zf_infos = []
    objs = get_zf_objs(start_date, end_date, zf)
    sum_info = get_zf_sum_info(objs)
    zf_infos.append(sum_info)

    second_sum_info = get_zf_second_sum_info(objs)
    zf_infos.append(second_sum_info)

    detail_infos = get_zf_detail_info(objs)
    zf_infos.append(detail_infos)

    return zf_infos

def get_cp_infos(start_date, end_date, app):
    cp_infos = []
    cp_objs = get_cp_objs(start_date, end_date, app)
    pt_objs = get_pt_objs(start_date, end_date, app)

    sum_info = get_cp_sum_info(cp_objs, pt_objs)
    cp_infos.append(sum_info)

    detail_infos = get_cp_detail_info(cp_objs, pt_objs)
    for detail_info in detail_infos:
        cp_infos[0].append(detail_info)

    return cp_infos

def get_zf_sum_info(objs):
    sum_info = [['','','',''], ['','','','']]
    for obj in objs:
        if obj[0] == '1':
            if obj[2] == u'总收入':
                sum_info[0][0] = obj[1]
                sum_info[0][1] = obj[4]
                sum_info[1][1] = obj[3] + u'笔'
            elif obj[2] == u'总支出':
                sum_info[0][2] = obj[4]
                sum_info[1][2] = obj[3] + u'笔'
            elif obj[2] == u'账户余额':
                sum_info[0][3] = obj[4]
                #sum_info[1][3] = obj[3] + u'笔'

    return sum_info

def get_zf_second_sum_info(objs):
    second_sum_info = [['','','','','','','',''],['','','','','','','','']]
    for obj in objs:
        if obj[0] == '2' and obj[1] == u"分类汇总":
            if obj[2] == u"订单支付":
                second_sum_info[0][0] = obj[1]
                second_sum_info[0][1] = obj[4]
                second_sum_info[1][1] = obj[3] + u'笔'
            elif obj[2] == u"转账收款":
                second_sum_info[0][2] = obj[4]
                second_sum_info[1][2] = obj[3] + u'笔'
            elif obj[2] == u"在线付款":
                second_sum_info[0][3] = obj[4]
                second_sum_info[1][3] = obj[3] + u'笔'
            elif obj[2] == u"提现":
                second_sum_info[0][4] = obj[4]
                second_sum_info[1][4] = obj[3] + u'笔'
            elif obj[2] == u"订单退款":
                second_sum_info[0][5] = obj[4]
                second_sum_info[1][5] = obj[3] + u'笔'
            elif obj[2] == u"服务费":
                second_sum_info[0][6] = obj[4]
                second_sum_info[1][6] = obj[3] + u'笔'
            elif obj[2] == u"账户余额":
                second_sum_info[0][7] = obj[4]
                second_sum_info[1][7] = obj[3] + u'笔'
    return second_sum_info

def get_zf_detail_info(objs):
    detail_infos = []
    pos_info = {}
    for obj in objs:
        if obj[0] == '3':
            if obj[1] not in pos_info.keys():
                single_info = [[obj[1],'','','','','','',''],['','','','','','','','']]
                detail_infos.append(single_info)
                pos_info[obj[1]] = len(detail_infos) - 1
            if obj[2] == u'订单支付':
                detail_infos[pos_info[obj[1]]][0][1] = obj[4]
                detail_infos[pos_info[obj[1]]][1][1] = obj[3] + u'笔'
            elif obj[2] == u'转账收款':
                detail_infos[pos_info[obj[1]]][0][2] = obj[4]
                detail_infos[pos_info[obj[1]]][1][2] = obj[3] + u'笔'
            elif obj[2] == u'在线付款':
                detail_infos[pos_info[obj[1]]][0][3] = obj[4]
                detail_infos[pos_info[obj[1]]][1][3] = obj[3] + u'笔'
            elif obj[2] == u'提现':
                detail_infos[pos_info[obj[1]]][0][4] = obj[4]
                detail_infos[pos_info[obj[1]]][1][4] = obj[3] + u'笔'
            elif obj[2] == u'订单退款':
                detail_infos[pos_info[obj[1]]][0][5] = obj[4]
                detail_infos[pos_info[obj[1]]][1][5] = obj[3] + u'笔'
            elif obj[2] == u'服务费':
                detail_infos[pos_info[obj[1]]][0][6] = obj[4]
                detail_infos[pos_info[obj[1]]][1][6] = obj[3] + u'笔'

    for obj in objs:
        if obj[0] == '2' and obj[2] == u'账户余额':
            if obj[1] not in pos_info.keys():
                single_info = [[obj[1],'','','','','','',''],['','','','','','','','']]
                detail_infos.append(single_info)
                pos_info[obj[1]] = len(detail_infos) - 1

            detail_infos[pos_info[obj[1]]][0][7] = obj[4]
            #detail_infos[pos_info[obj[1]]][1][7] = obj[3] + u'笔'

    t_infos = []
    for detail_info in detail_infos:
        t_infos.append(detail_info[0])
        t_infos.append(detail_info[1])
    return t_infos


def get_cp_sum_info(cp_objs, pt_objs):
    sum_info = [['','','',''],['','','','']]
    for cp_obj in cp_objs:
        if cp_obj[0] == '1':
            if cp_obj[2] == u'实付CP款':
                sum_info[0][0] = cp_obj[1]
                sum_info[0][2] = cp_obj[4]
                sum_info[1][2] = cp_obj[3] + u'笔'
            elif cp_obj[2] == u'CP平台余额':
                sum_info[0][3] = cp_obj[4]
                #sum_info[1][3] = cp_obj[3] + u'笔'

    for pt_obj in pt_objs:
        if pt_obj[0] == '1':
            sum_info[0][1] = pt_obj[4]
            sum_info[1][1] = pt_obj[3] + u'笔'

    return sum_info

def get_cp_detail_info(cp_objs, pt_objs):
    detail_infos = []
    pos_info = {}

    for cp_obj in cp_objs:
        if cp_obj[0] == '2':
            if cp_obj[1] not in pos_info.keys():
                single_info = [[cp_obj[1],'','',''],['','','','']]
                detail_infos.append(single_info)
                pos_info[cp_obj[1]] = len(detail_infos) - 1

            if cp_obj[2] == u'实付CP款':
                detail_infos[pos_info[cp_obj[1]]][0][2] = cp_obj[4]
                detail_infos[pos_info[cp_obj[1]]][1][2] = cp_obj[3] + u'笔'
            elif cp_obj[2] == u'CP平台余额':
                detail_infos[pos_info[cp_obj[1]]][0][3] = cp_obj[4]
                #detail_infos[pos_info[cp_obj[1]]][1][3] = cp_obj[3] + u'笔'

    for pt_obj in pt_objs:
        if pt_obj[0] == '2' and pt_obj[2] == u'应付CP款':
            if pt_obj[1] not in pos_info.keys():
                single_info = [[pt_obj[1],'','',''],['','','','']]
                detail_infos.append(single_info)
                pos_info[pt_obj[1]] = len(detail_infos) - 1

            detail_infos[pos_info[pt_obj[1]]][0][1] = pt_obj[4]
            detail_infos[pos_info[pt_obj[1]]][1][1] = pt_obj[3] + u'笔'

    t_infos = []
    for detail_info in detail_infos:
        t_infos.append(detail_info[0])
        t_infos.append(detail_info[1])

    return t_infos

def sort_data(zf_csv_data, cp_csv_data, pt_csv_data):
    return_data = []
    for zf_data in zf_csv_data:
        for single_data in zf_data:
            return_data.append(single_data)

    for single_data in cp_csv_data[0]:
        return_data.append(single_data)

    for single_data in pt_csv_data[0]:
        return_data.append(single_data)

    for single_data in cp_csv_data[1]:
        return_data.append(single_data)

    return return_data

def get_zf_csv_first_info(second_info, objs):
    second_copy = copy.deepcopy(second_info)
    first_info = [[],[],[]]
    for obj in objs:
        if obj[0] == "1":
            if obj[5] == "I":
                first_info[0].append(obj)
                if "I" in second_info.keys():
                    for second_obj in second_info["I"]:
                        first_info[0].append(second_obj)
            elif obj[5] == "O":
                first_info[1].append(obj)
                if "O" in second_info.keys():
                    for second_obj in second_info["O"]:
                        first_info[1].append(second_obj)
            elif obj[5] == "B":
                first_info[2].append(obj)
                if "B" in second_info.keys():
                    for second_obj in second_info["B"]:
                        first_info[2].append(second_obj)

    return first_info

def get_zf_csv_second_info(third_info, objs):
    third_copy = copy.deepcopy(third_info)
    second_info = {}
    for obj in objs:
        if obj[0] == "2":
            if not obj[5] in second_info.keys():
                second_info[str(obj[5])] = []
            second_info[obj[5]].append(obj)
            if obj[2] in third_copy.keys():
                for third_obj in third_copy[obj[2]]:
                    second_info[obj[5]].append(third_obj)

    return second_info

def get_zf_csv_third_info(objs):
    third_info = {}
    for obj in objs:
        if obj[0] == "3":
            if not obj[2] in third_info.keys():
                third_info[obj[2]] = []
            third_info[obj[2]].append(obj)

    return third_info

def get_cp_csv_first_info(second_info, objs):
    second_copy = copy.deepcopy(second_info)
    first_info = [[],[]]
    for obj in objs:
        if obj[0] == "1":
            if obj[5] == "O":
                first_info[1].append(obj)
                if "O" in second_info.keys():
                    for second_obj in second_info["O"]:
                        first_info[1].append(second_obj)
            elif obj[5] == "B":
                first_info[0].append(obj)
                if "B" in second_info.keys():
                    for second_obj in second_info["B"]:
                        first_info[0].append(second_obj)

    return first_info

def get_cp_csv_second_info(third_info, objs):
    third_copy = copy.deepcopy(third_info)
    second_info = {}
    for obj in objs:
        if obj[0] == "2":
            if not obj[5] in second_info.keys():
                second_info[str(obj[5])] = []
            second_info[obj[5]].append(obj)
            if obj[2] in third_copy.keys():
                for third_obj in third_copy[obj[2]]:
                    second_info[obj[5]].append(third_obj)
    return second_info

def get_pt_csv_first_info(second_info, objs):
    second_copy = copy.deepcopy(second_info)
    first_info = [[]]
    for obj in objs:
        if obj[0] == "1":
            if obj[5] == "O":
                first_info[0].append(obj)
                if "O" in second_info.keys():
                    for second_obj in second_info["O"]:
                        first_info[0].append(second_obj)

    return first_info

def get_pt_csv_second_info(third_info, objs):
    third_copy = copy.deepcopy(third_info)
    second_info = {}
    for obj in objs:
        if obj[0] == "2":
            if not obj[5] in second_info.keys():
                second_info[str(obj[5])] = []
            second_info[obj[5]].append(obj)
            if obj[2] in third_copy.keys():
                for third_obj in third_copy[obj[2]]:
                    second_info[obj[5]].append(third_obj)
    return second_info

def get_zf_csv_data(start_date, end_date):
    objs = get_zf_objs(start_date, end_date)
    third_info = get_zf_csv_third_info(objs)
    second_info = get_zf_csv_second_info(third_info, objs)
    first_info = get_zf_csv_first_info(second_info, objs)

    return first_info

def get_cp_csv_data(start_date, end_date):
    objs = get_cp_objs(start_date, end_date)
    second_info = get_cp_csv_second_info({}, objs)
    first_info = get_cp_csv_first_info(second_info, objs)
    return first_info

def get_pt_csv_data(start_date, end_date):
    objs = get_pt_objs(start_date, end_date)
    second_info = get_pt_csv_second_info({}, objs)
    first_info = get_pt_csv_first_info(second_info, objs)
    return first_info

@login_required
@permission_required(u'man.%s' % FinanceConst.FINANCE_ZF_PAYMENT_CHANNEL_REPORT, raise_exception=True)
def finance_table_csv(request):
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

    zf = get_user_zfs(request.user)


    business_info = []
    zf_info = get_zf_infos(start_date, end_date, zf)
    cp_info = get_cp_infos(start_date, end_date, app)

    business_info.append(zf_info)
    business_info.append(cp_info)

    wb = xlwt.Workbook(encoding = 'utf-8')
    ws = wb.add_sheet(u"支付渠道数据汇总",cell_overwrite_ok=True)
    ws.write(1, 0, u"名称")
    ws.write(1, 7, u"余额")
    ws.write_merge(0,0,0,7,u"支付渠道数据汇总",set_style('Times New Roman',220,True, True))
    ws.write_merge(1,1,1,2,u"收入")
    ws.write_merge(1,1,3,6,u"支出")

    ws.write_merge(2,3,0,0,business_info[0][0][0][0])
    ws.write_merge(2,2,1,2,business_info[0][0][0][1])
    ws.write_merge(3,3,1,2,business_info[0][0][1][1])
    ws.write_merge(2,2,3,6,business_info[0][0][0][2])
    ws.write_merge(3,3,3,6,business_info[0][0][1][2])
    ws.write(2, 7,  business_info[0][0][0][3])
    ws.write(3, 7,  business_info[0][0][1][3])

    ws.write(4, 0, u"名称")
    ws.write(4, 1, u"订单支付")
    ws.write(4, 2, u"转账收款")
    ws.write(4, 3, u"在线支付")
    ws.write(4, 4, u"提现")
    ws.write(4, 5, u"订单退款")
    ws.write(4, 6, u"服务费")
    ws.write(4, 7, u"帐户余额")
    for i in range(0, 8):
        ws.write(5, i,  business_info[0][1][0][i])
        ws.write(6, i,  business_info[0][1][1][i])
    ws.write_merge(5,6,0,0,business_info[0][1][0][0])
    ws.write(7, 0, u"渠道名称")
    ws.write(7, 1, u"订单支付")
    ws.write(7, 2, u"转账收款")
    ws.write(7, 3, u"在线支付")
    ws.write(7, 4, u"提现")
    ws.write(7, 5, u"订单退款")
    ws.write(7, 6, u"服务费")
    ws.write(7, 7, u"帐户余额")
    t_len = len(business_info[0][2])
    for i in range(0, t_len):
        for j in range(0, 8):
            ws.write(i+8, j, business_info[0][2][i][j])
        if i % 2 == 1:
            ws.write_merge(i+7, i+8,0,0, business_info[0][2][i-1][0])

    second_ws = wb.add_sheet(u"CP数据汇总",cell_overwrite_ok=True)
    second_ws.write_merge(0,0,0,3,u"CP数据汇总",set_style('Times New Roman',220,True, True))
    second_ws.write(1, 0, u"项目名称")
    second_ws.write(1, 1, u"应付CP")
    second_ws.write(1, 2, u"实付CP")
    second_ws.write(1, 3, u"CP余额")
    t_len = len(business_info[1][0])
    for i in range(0, t_len):
        for j in range(1, 4):
            second_ws.write(i+2, j,  business_info[1][0][i][j])
        if i % 2 == 1:
            second_ws.write_merge(i+1, i+2,0,0, business_info[1][0][i-1][0])

    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=report.xlt'
    wb.save(response)
    return response

def WriteToExcel(weather_period, town):
    return

def set_style(name,height,bold=False, alignment=False):
    style = xlwt.XFStyle()  # 初始化样式

    font = xlwt.Font()  # 为样式创建字体
    font.name = name # 'Times New Roman'
    font.bold = bold
    #f.underline= Font.UNDERLINE_DOUBLE
    font.color_index = 4
    font.height = height
    font.alignment = 'center'


    borders= xlwt.Borders()
    borders.alignment = alignment
    # borders.left= 6
    # borders.right= 6
    # borders.top= 6
    # borders.bottom= 6

    style.font = font
    #style.alignment = alignment
    style.borders = borders

    return style
