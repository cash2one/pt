#coding: utf-8

"""
    无压单对账明细
"""

from finance_pub import *
from xlwt import *
from django.utils.encoding import *


def get_unpending_data(start_date, end_date, order_type, cp_type, app, daojia_cp_type):
    if not start_date:
        start_date = None
    if not end_date:
        end_date = None
    if not app:
        app = None
    if daojia_cp_type and len(daojia_cp_type) < 1024:
        cp_type = str(daojia_cp_type)
    else:
        cp_type = None
    cursor = connections['report'].cursor()
    cursor.execute("call `SP_T_RP_DUIZHANG_CP_BILL_APP`(%s, %s, %s, %s, %s)",
                    [start_date, end_date, app, order_type, cp_type])
    objs = cursor.fetchall()
    cursor.close()
    data = []
    for obj in objs:
        data.append(
            [
                str(start_date),
                str(end_date),
                str(obj[0]),
                str(obj[2]),
                str(obj[5]),
                str(obj[7]),
                str(obj[9]),
                str(obj[11]),
                str(obj[12]),
            ]
        )
    if not data:
        data.append([Const.NONE] * 9)
    else:
        data.sort(key=lambda o: o[0], reverse=True)

    # 获取结算单数据
    global xls_data
    xls_data = []
    for obj in objs:
        xls_data.append(
            [
                str(obj[0]),
                str(obj[1]),
                str(obj[2]),
                str(obj[3]),
                str(obj[4]),
                str(obj[5]),
                str(obj[6]),
                str(obj[7]),
                str(obj[8]),
                str(obj[9]),
                str(obj[10]),
                str(obj[11]),
                str(obj[12]),
            ]
        )
    if not xls_data:
        xls_data.append([Const.NONE] * 13)
    else:
        xls_data.sort(key=lambda o: o[0], reverse=True)

    return data


@login_required
@permission_required(u'man.%s' % FinanceConst.FINANCE_EVENT_DOWNLOAD_CP_STATMENT, raise_exception=True)
@add_common_var
def batch_cp_statment(request, template_name):
    app = request.GET.get("app")
    report_check_app(request, app)
    products = get_order_types()
    cp_types = get_cp_types()
    daojia_cp_types = get_full_cp_names()
    cur_order_type = None
    cur_cp_type = None
    cur_daojia_cp_type = None
    return report_render(request, template_name, {
        "currentdate": get_datestr(1, "%Y-%m-%d"),
        "products": products,
        "cp_types":cp_types,
        "cur_order_type":cur_order_type,
        "cur_cp_type":cur_cp_type,
        "cur_daojia_cp_type":cur_daojia_cp_type,
        "daojia_cp_types":daojia_cp_types,
    })


@login_required
@permission_required(u'man.%s' % FinanceConst.FINANCE_EVENT_DOWNLOAD_CP_STATMENT, raise_exception=True)
def batch_cp_statment_ajax(request):
    start_date = request.POST["start_date"]
    end_date = request.POST["end_date"]
    order_type = 110
    app = request.POST.get("app")
    report_check_app(request, app)
    if app:
        app = "^%s$" % app
    else:
        app = get_user_apps(request.user)
    cp_type = request.POST.get("cp_type")
    daojia_cp_type = request.POST.getlist("daojia_cp_type[]")
    daojia_cps = "^$"
    for obj in daojia_cp_type:
        appId = obj.strip()
        daojia_cps = daojia_cps + "|" + appId
    if len(daojia_cps) > 1000:
        daojia_cps = None
    print daojia_cps
    result = get_unpending_data(start_date, end_date, order_type, cp_type, app, daojia_cps)
    return HttpResponse(json.dumps(result))


@login_required
@permission_required(u'man.%s' % FinanceConst.FINANCE_EVENT_DOWNLOAD_CP_STATMENT, raise_exception=True)
def batch_cp_statment_csv(request):
    #接收参数
    start_date = request.GET.get("start_date")
    start_date = start_date.replace("-","")
    end_date = request.GET.get("end_date")
    end_date = end_date.replace("-","")
    order_type = 110
    app = request.GET.get("app")
    report_check_app(request, app)
    if app:
        app = "^%s$" % app
    else:
        app = get_user_apps(request.user)
    daojia_cp_type = request.GET.get("daojia_cp_type")
    if daojia_cp_type:
        daojia_cp_type = daojia_cp_type.replace(' ,','|')

    # 生成结算单文件
    wb = Workbook()

    # 定义结算单风格

    #  一般标题
    fnt = Font()
    fnt.name = 'Arial'
    fnt.colour_index = 0
    fnt.bold = False
    fnt.height = 220

    #  标题标题
    fnt_header = Font()
    fnt_header.name = 'Arial'
    fnt_header.colour_index = 0
    fnt_header.bold = True
    fnt_header.height = 220

    # 一般边框
    borders = Borders()
    borders.left = 1
    borders.right = 1
    borders.top = 1
    borders.bottom = 1

    # 一般风格
    style = XFStyle()
    style.font = fnt
    style.borders = borders
    style.alignment.horz = 2
    style.alignment.vert = 1

    # 主表头风格
    main_header_style = XFStyle()
    main_header_style.font = fnt_header
    main_header_style.borders = borders
    main_header_style.alignment.horz = 2
    main_header_style.alignment.vert = 1

    # 表头风格
    header_style = XFStyle()
    header_style = easyxf('pattern: pattern solid, fore_colour sky_blue;')
    header_style.font = fnt_header
    header_style.borders = borders
    header_style.alignment.horz = 2
    header_style.alignment.vert = 1

    #
    wt_analysis = wb.add_sheet(u'运营数据分析')

    #营销成本分析
    wt_analysis.write_merge(0,0,0, 4, u'营销成本分析', header_style)
    wt_analysis.write(1,0,u'营销成本类型',style)
    wt_analysis.write(1,1,u'CP名称',style)
    wt_analysis.write(1,2,u'笔数',style)
    wt_analysis.write(1,3,u'金额:',style)
    wt_analysis.write(1,4,u'是否地推渠道:',style)

    #获取营销费用分析信息
    cursor = connections['report'].cursor()
    cursor.execute("call `SP_T_RP_DUIZHANG_CP_BILL_DAOJIA_OPERATION_COST_APP`(%s, %s, %s, %s, %s)",
                    [start_date, end_date, app, order_type, None])
    objs = cursor.fetchall()
    rownum = 2
    #将跨时段订单写入表格
    for obj in objs:
        wt_analysis.write(rownum,0,smart_unicode(obj[3]),style)
        wt_analysis.write(rownum,1,smart_unicode(obj[1]),style)
        wt_analysis.write(rownum,2,smart_unicode(obj[6]),style)
        wt_analysis.write(rownum,3,smart_unicode(obj[5]),style)
        wt_analysis.write(rownum,4,smart_unicode(obj[4]),style)
        rownum+=1
        col = 0
        #调整列宽
        while col <= 6:
            if obj[col] and wt_analysis.col(col).width < len(str(obj[col]))*367:
                wt_analysis.col(col).width = len(str(obj[col]))*367
            col+=1

    for obj in xls_data:

        # 设置结算单参数
        cp_bill_product = smart_unicode(obj[0])
        cp_bill_cp = smart_unicode(obj[2])
        cp_type = int(obj[3])
        cp_bill_zf_pay_c = obj[4]
        cp_bill_zf_pay_m = obj[5]
        cp_bill_zf_refund_c = obj[6]
        cp_bill_zf_refund_m = obj[7]
        cp_bill_cp_pay_c = obj[8]
        cp_bill_cp_pay_m = obj[9]
        cp_bill_operation_cost_m = obj[11]

        # 设置表格名称
        wt = wb.add_sheet(u'%s(%s)对账单' % (cp_bill_cp, cp_type))
        wt_analysis = wb.add_sheet(u'%s(%s)运营数据分析' % (cp_bill_cp, cp_type))
        #  ##绘制对账单汇总表格##  #

        # 表头部分
        wt.write_merge(0,0,0, 4, u'葡萄对账单', main_header_style)
        wt.write(1,0, u'CP名称', main_header_style)
        wt.write(2,0, u'对账期间', main_header_style)
        wt.write(3,0, u'差异率', main_header_style)
        wt.write(3,1,Formula("ROUND(C15/A8*100,2)&\"%\""),style)
        wt.write(3,2, u'单位：元', main_header_style)
        wt.write_merge(3,3,3,4,'',style)
        wt.col(0).width = 10000
        wt.col(1).width = 7000
        wt.col(2).width = 7000
        wt.col(3).width = 7000
        wt.col(4).width = 10000
        wt.row(0).set_style(easyxf('font:height 360;'))

        # 到家下载单修改
        # 葡萄数据
        wt.write_merge(5, 5, 0, 4, u'葡萄数据', header_style)
        wt.write(6, 0, u'银行实收', style)
        wt.write(6, 1, u'银行实退', style)
        wt.write(6, 2, u'vip支付', style)
        wt.write(6, 3, u'次卡', style)
        wt.write(6, 4, u'优惠券', style)

        # CP数据
        wt.write_merge(8, 8, 0, 4, u'CP数据', header_style)
        wt.write(9, 0, u'业务类型', style)
        wt.write(9, 1, u'实付金额', style)

        # 差异
        wt.write_merge(11, 11, 0, 4, u'差异', header_style)
        wt.write_merge(12, 13, 0, 0, u'业务类型', style)
        wt.write_merge(12, 12, 1, 2, u'金额差异', style)
        wt.write(13, 1, u'营销成本', style)
        wt.write(13, 2, u'异常金额', style)
        wt.write(14, 2, Formula("A8-B8+C8+D8+E8-B11"), style)

        # 差异
        wt.write_merge(22, 22, 0, 4, u'异常金额分析', header_style)
        wt.write(23, 0, u'异常类型', style)
        wt.write(23, 1, u'笔数', style)
        wt.write(23, 2, u'金额', style)
        wt.write_merge(23, 23, 3, 4, u'备注:', style)

        # 最终结算金额
        wt.write(18, 0, u'结算金额', main_header_style)
        wt.write(18, 1, Formula("B11"), main_header_style)

        # 获取主表格信息
        cursor = connections['report'].cursor()
        cursor.execute("call `SP_T_RP_DUIZHANG_CP_BILL_ANALYSIS_APP_NEW`(%s, %s, %s, %s, %s)",
                       [start_date, end_date, app, order_type, cp_type])
        objs = cursor.fetchall()

        rel_pay = objs[0][1]  # 实付

        cursor = connections['report'].cursor()
        cursor.execute("call `SP_T_RP_DUIZHANG_CP_BILL_APP_NEW`(%s, %s, %s, %s)",
                       [start_date, end_date, app, cp_type])
        objs = cursor.fetchone()
        rel_show = objs[0]
        rel_tui = objs[1]
        vip_pay = objs[2]
        cika = objs[3]
        coupon = objs[4]
        cp_u = objs[5]

        ############填写表格数据#############

        # 填写表头信息
        wt.write_merge(1, 1, 1, 4, cp_bill_cp, style)
        wt.write_merge(2, 2, 1, 4, start_date + "-" + end_date, style)

        # 填写实收数据
        # wt.write(7,0,u'充话费',style)
        # wt.write(7,1,u'实付金额',style)
        # wt.write(7,2,u'实退款',style)
        # wt.write(7,3,u'交单交易笔数',style)
        # wt.write(7,4,u'失败订单笔数',style)

        wt.write(7, 0, rel_show, style)
        wt.write(7, 1, rel_tui, style)
        wt.write(7, 2, vip_pay, style)
        wt.write(7, 3, cika, style)
        wt.write(7, 4, coupon, style)

        # 填写CP数据
        # wt.write(10,0,u'充话费',style)
        # wt.write(10,1,u'实付金额',style)
        # wt.write(10,2,u'实退款',style)
        # wt.write(10,3,u'交单交易笔数',style)
        # wt.write(10,4,u'失败订单笔数',style)

        wt.write(10, 0, cp_bill_product, style)
        wt.write(10, 1, rel_pay, style)

        # 填写差异数据数据
        # wt.write(14,0,u'充话费',style)
        # wt.write(14,1,u'营销成本',style)
        # wt.write(14,3,u'处理中',style)
        # wt.write(14,4,u'退款中',style)

        wt.write(14, 0, cp_bill_product, style)
        wt.write(14, 1, cp_u, style)

        # 填写差异信息
        cursor = connections['report'].cursor()
        cursor.execute("call `SP_T_RP_D_ACCOUNT_CHECK_SUMMARY_APP_REASON_NEW`(%s, %s, %s, %s)",
                       [start_date, end_date, app, cp_type])
        # [start_date, end_date, app, order_type, cp_type])
        objs = cursor.fetchall()
        rownum = 24
        for obj in objs:
            wt.write(rownum, 0, obj[0], style)
            wt.write(rownum, 1, obj[1], style)
            wt.write(rownum, 2, float(obj[2]) if obj[2] is not None else 0, style)
            wt.write_merge(rownum, rownum, 3, 4, u"", style)
            rownum += 1

        # 填写合计数据
        if rownum != 24:
            wt.write(rownum, 0, u"合计:", style)
            wt.write(rownum, 1, u"", style)
            wt.write(rownum, 2, Formula("SUM(C25:C%s)" % rownum), style)
            wt.write_merge(rownum, rownum, 3, 4, u"", style)

        ###运营数据分析###

        # 表头部分
        wt_analysis.write_merge(0, 0, 0, 4, u'运营数据分析', main_header_style)
        wt_analysis.col(0).width = 10000
        wt_analysis.col(1).width = 7000
        wt_analysis.col(2).width = 7000
        wt_analysis.col(3).width = 7000
        wt_analysis.col(4).width = 10000

        wt_analysis.row(0).set_style(easyxf('font:height 360;'))

        # 葡萄数据
        wt_analysis.write_merge(2, 2, 0, 4, u'葡萄数据', header_style)
        wt_analysis.write(3, 0, u'业务类型', style)
        wt_analysis.write_merge(3, 3, 1, 2, u'订单金额', style)
        wt_analysis.write_merge(3, 3, 3, 4, u'订单交易笔数', style)

        # CP数据
        wt_analysis.write_merge(5, 5, 0, 4, u'CP数据', header_style)
        wt_analysis.write(6, 0, u'业务类型', style)
        wt_analysis.write_merge(6, 6, 1, 2, u'实付金额', style)
        wt_analysis.write_merge(6, 6, 3, 4, u'订单交易笔数', style)

        # 差异
        wt_analysis.write_merge(8, 8, 0, 4, u'收款渠道', header_style)
        wt_analysis.write_merge(9, 10, 0, 0, u'银行实收', style)
        wt_analysis.write_merge(9, 10, 1, 2, u'VIP卡', style)
        wt_analysis.write_merge(9, 10, 3, 3, u'次卡', style)
        wt_analysis.write_merge(9, 10, 4, 4, u'优惠券', style)

        wt_analysis.write(13, 0, u'毛利', style)
        wt_analysis.write(13, 1, Formula("B5-B8"), style)
        # wt_analysis.write_merge(11,11,3,4,Formula("B5-B8"),style)


        # 营销成本分析
        wt_analysis.write_merge(15, 15, 0, 4, u'营销成本分析', header_style)
        wt_analysis.write(16, 0, u'营销成本类型', style)
        wt_analysis.write(16, 1, u'活动名称', style)
        wt_analysis.write(16, 2, u'订单数', style)
        wt_analysis.write(16, 3, u'营销成本', style)
        wt_analysis.write(16, 4, u'葡萄盈亏', style)

        # 获取主表格信息
        cursor = connections['report'].cursor()
        cursor.execute("call `SP_T_RP_DUIZHANG_CP_BILL_ANALYSIS_APP_NEW`(%s, %s, %s, %s, %s)",
                       [start_date, end_date, app, order_type, cp_type])
        objs = cursor.fetchall()

        # 设置结算单参数
        cp_bill_product = objs[0][3]  # 银行实收
        cp_bill_cp = smart_unicode(get_cp_name(cp_type))
        cp_bill_pt_pay_c = objs[0][2]
        cp_bill_pt_pay_m = objs[0][0]
        cp_bill_cp_pay_c = objs[0][2]
        cp_bill_cp_pay_m = objs[0][1]
        cp_bill_operation_cost_m = objs[0][4]  # VIP卡付款
        cp_bill_cika = objs[0][5]  # 次卡
        cp_bill_coupon = objs[0][6]  # 优惠券

        # 填写销售数据
        wt_analysis.write(4, 0, u'全托管线上支付', style)
        wt_analysis.write_merge(4, 4, 1, 2, cp_bill_pt_pay_m, style)
        wt_analysis.write_merge(4, 4, 3, 4, cp_bill_pt_pay_c, style)

        # 填写CP数据
        wt_analysis.write(7, 0, u'全托管线上支付', style)
        wt_analysis.write_merge(7, 7, 1, 2, cp_bill_cp_pay_m, style)
        wt_analysis.write_merge(7, 7, 3, 4, cp_bill_cp_pay_c, style)

        # 填写差异数据数据
        wt_analysis.write(11, 0, cp_bill_product, style)
        wt_analysis.write_merge(11, 11, 1, 2, cp_bill_operation_cost_m, style)
        wt_analysis.write(11, 3, cp_bill_cika, style)
        wt_analysis.write(11, 4, cp_bill_coupon, style)

        # 获取营销费用分析信息
        cursor = connections['report'].cursor()
        cursor.execute("call `SP_T_RP_DUIZHANG_CP_BILL_DAOJIA_OPERATION_COST_APP_NEW`(%s, %s, %s, %s, %s)",
                       [start_date, end_date, app, order_type, cp_type])
        objs = cursor.fetchall()
        rownum = 17
        # 将营销费用明细写入表格
        for obj in objs:
            wt_analysis.write(rownum, 0, smart_unicode(obj[0]), style)
            wt_analysis.write(rownum, 1, smart_unicode(obj[1]), style)
            wt_analysis.write(rownum, 2, obj[2], style)
            wt_analysis.write(rownum, 3, round(obj[3], 2) if obj[3] is not None else 0, style)
            wt_analysis.write(rownum, 4, round(obj[4], 2) if obj[4] is not None else 0, style)
            rownum += 1
            col = 0
            # 调整列宽
            while col < 4:
                if obj[col] and wt_analysis.col(col).width < len(str(obj[col])) * 367:
                    wt_analysis.col(col).width = len(str(obj[col])) * 367
                col += 1
        print rownum
        # 填写合计数据
        if rownum != 17:
            wt_analysis.write(rownum, 0, u"合计:", style)
            wt_analysis.write(rownum, 1, u"", style)
            wt_analysis.write(rownum, 2, Formula("SUM(C18:C%s)" % rownum), style)
            wt_analysis.write(rownum, 3, Formula("SUM(D18:D%s)" % rownum), style)
            wt_analysis.write(rownum, 4, Formula("SUM(E18:E%s)" % rownum), style)

    # 设置结算单名称
    name =smart_str("到家业务(%s-%s)结算单.xls" % (start_date, end_date))

    # 返回Http Response
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=%s' % name
    wb.save(response)

    return response
