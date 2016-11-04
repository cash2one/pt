#coding: utf-8

"""
    无压单对账明细
"""

from finance_pub import *
from xlwt import *
import time
from django.utils.encoding import *

def get_unpending_data(start_date, end_date, order_type, cp_type, app, daojia_cp_type):
    if not start_date:
        start_date = None
    if not end_date:
        end_date = None
    if not app:
        app = None
    if order_type:
        if int(order_type) == 110:
            if daojia_cp_type:
                cp_type = int(daojia_cp_type);
    cursor = connections['report'].cursor()
    cursor.execute("call `SP_T_RP_DUIZHANG_CP_BILL_APP`(%s, %s, %s, %s, %s)",
                    [start_date, end_date, app, order_type, cp_type])
    objs = cursor.fetchall()
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

    #获取结算单数据
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
def cp_statment(request, template_name):
    app = request.GET.get("app")
    report_check_app(request, app)
    products = get_order_types()
    cp_types = get_cp_types()
    daojia_cp_types = get_full_cp_names()
    cur_order_type = None
    cur_cp_type = None
    cur_daojia_cp_type = None
    try:
        cur_order_type = int(request.GET.get("order_type"))
    except:
        pass
    try:
        cur_cp_type = int(request.GET.get("cp_type"))
    except:
        pass
    try:
        if int(cur_order_type) == 110:
            if cur_cp_type:
                cur_daojia_cp_type = cur_cp_type
    except:
        pass
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
def cp_statment_ajax(request):
    start_date = request.POST["start_date"]
    end_date = request.POST["end_date"]
    order_type = request.POST["ot"]
    app = request.POST.get("app")
    report_check_app(request, app)
    if app:
        app = "^%s$" % app
    else:
        app = get_user_apps(request.user)
    cp_type = request.POST.get("cp_type")
    daojia_cp_type = request.POST.get("daojia_cp_type")
    result = get_unpending_data(start_date, end_date, order_type, cp_type, app, daojia_cp_type)
    return HttpResponse(json.dumps(result))


@login_required
@permission_required(u'man.%s' % FinanceConst.FINANCE_EVENT_DOWNLOAD_CP_STATMENT, raise_exception=True)
def cp_statment_csv(request):
    #接收参数
    start_date = request.GET.get("start_date")
    start_date = start_date.replace("-","")
    end_date = request.GET.get("end_date")
    end_date = end_date.replace("-","")
    order_type = request.GET.get("ot")
    app = request.GET.get("app")
    report_check_app(request, app)
    if app:
        app = "^%s$" % app
    else:
        app = get_user_apps(request.user)
    cp_type = request.GET.get("cp_type")
    daojia_cp_type = request.GET.get("daojia_cp_type")
    if order_type:
        if int(order_type) == 110:
            cp_type = daojia_cp_type

    #设置结算单参数
    cp_bill_product = smart_unicode(xls_data[0][0])
    cp_bill_cp = smart_unicode(xls_data[0][2])
    cp_bill_zf_pay_c = xls_data[0][4]
    cp_bill_zf_pay_m = xls_data[0][5]
    cp_bill_zf_refund_c = xls_data[0][6]
    cp_bill_zf_refund_m = xls_data[0][7]
    cp_bill_cp_pay_c = xls_data[0][8]
    cp_bill_cp_pay_m = xls_data[0][9]
    cp_bill_operation_cost_m = xls_data[0][11]

    #绘制结算单表格

    wb = Workbook()

    #设置表格名称
    wt = wb.add_sheet(u'葡萄信息技术有限公司对账单')
    wt_overdays = wb.add_sheet(u'跨时段订单明细')
    wt_abnormal = wb.add_sheet(u'异常订单明细',cell_overwrite_ok = True)
    if order_type:
        if int(order_type) == 110:
            wt_analysis = wb.add_sheet(u'运营数据分析')
            wt_analysis_detail = wb.add_sheet(u'运营数据分析详情')

    ###绘制对账单汇总表格###

    #  一般标题
    fnt= Font()
    fnt.name= 'Arial'
    fnt.colour_index= 0
    fnt.bold = False
    fnt.height = 220

    #  标题标题
    fnt_header =Font()
    fnt_header.name= 'Arial'
    fnt_header.colour_index= 0
    fnt_header.bold = True
    fnt_header.height = 220

    # 一般边框
    borders= Borders()
    borders.left= 1
    borders.right= 1
    borders.top= 1
    borders.bottom= 1

    #一般风格
    style= XFStyle()
    style.font= fnt
    style.borders = borders
    style.alignment.horz = 2
    style.alignment.vert = 1

    #主表头风格
    main_header_style = XFStyle()
    main_header_style.font = fnt_header
    main_header_style.borders = borders
    main_header_style.alignment.horz = 2
    main_header_style.alignment.vert = 1

    #表头风格
    header_style = XFStyle()
    header_style = easyxf('pattern: pattern solid, fore_colour sky_blue;')
    header_style.font = fnt_header
    header_style.borders = borders
    header_style.alignment.horz = 2
    header_style.alignment.vert = 1

    #表头部分
    wt.write_merge(0,0,0, 4, u'葡萄对账单', main_header_style)
    wt.write(1,0, u'CP名称', main_header_style)
    wt.write(2,0, u'对账期间', main_header_style)
    wt.write(3,0, u'差异率', main_header_style)
    if order_type == '110':
        wt.write(3, 1, Formula("ROUND(C15/A8*100,2)&\"%\""), style)
    else:
        wt.write(3, 1, Formula("ROUND(C15/B8*100,2)&\"%\""), style)
    wt.write(3,2, u'单位：元', main_header_style)
    wt.write_merge(3,3,3,4,'',style)
    wt.col(0).width = 10000
    wt.col(1).width = 7000
    wt.col(2).width = 7000
    wt.col(3).width = 7000
    wt.col(4).width = 10000

    wt.row(0).set_style(easyxf('font:height 360;'))
    if order_type != '110':
        #葡萄数据
        wt.write_merge(5,5,0, 4, u'葡萄数据', header_style)
        wt.write(6,0,u'业务类型',style)
        wt.write(6,1,u'订单实收金额',style)
        wt.write(6,2,u'实退金额',style)
        wt.write(6,3,u'订单交易笔数',style)
        wt.write(6,4,u'失败订单笔数',style)


        #CP数据
        wt.write_merge(8,8,0, 4, u'CP数据', header_style)
        wt.write(9,0,u'业务类型',style)
        wt.write(9,1,u'实付金额',style)
        wt.write(9,2,u'实退金额',style)
        wt.write(9,3,u'交单交易笔数',style)
        wt.write(9,4,u'失败订单笔数',style)

        #差异
        wt.write_merge(11,11,0, 4, u'差异', header_style)
        wt.write_merge(12,13,0, 0, u'业务类型', style)
        wt.write_merge(12,12,1, 2, u'金额差异', style)
        wt.write_merge(12,12,3, 4, u'订单笔数差异', style)
        wt.write(13,1,u'营销成本',style)
        wt.write(13,2,u'异常金额',style)
        wt.write(13,3,u'处理中',main_header_style)
        wt.write(13,4,u'退款中',main_header_style,)
        wt.write(14,2,Formula("(B8-C8)+B15-(B11-C11)"),style)


        #差异
        wt.write_merge(22,22,0, 4, u'异常金额分析', header_style)
        wt.write(23,0,u'异常类型',style)
        wt.write(23,1,u'笔数',style)
        wt.write(23,2,u'金额',style)
        wt.write_merge(23,23,3,4,u'备注:',style)


        #最终结算金额
        wt.write(18,0,u'结算金额',main_header_style)
        wt.write(18,1,Formula("B11+C11"),main_header_style)

        ############填写表格数据#############

        #填写表头信息
        wt.write_merge(1,1, 1, 4, cp_bill_cp, style)
        wt.write_merge(2,2, 1, 4, start_date+"-"+end_date, style)

        #填写实收数据
        # wt.write(7,0,u'充话费',style)
        # wt.write(7,1,u'实付金额',style)
        # wt.write(7,2,u'实退款',style)
        # wt.write(7,3,u'交单交易笔数',style)
        # wt.write(7,4,u'失败订单笔数',style)

        wt.write(7,0,cp_bill_product,style)
        wt.write(7,1,cp_bill_zf_pay_m,style)
        wt.write(7,2,cp_bill_zf_refund_m,style)
        wt.write(7,3,cp_bill_zf_pay_c,style)
        wt.write(7,4,cp_bill_zf_refund_c,style)

        #填写CP数据
        # wt.write(10,0,u'充话费',style)
        # wt.write(10,1,u'实付金额',style)
        # wt.write(10,2,u'实退款',style)
        # wt.write(10,3,u'交单交易笔数',style)
        # wt.write(10,4,u'失败订单笔数',style)

        wt.write(10,0,cp_bill_product,style)
        wt.write(10,1,cp_bill_cp_pay_m,style)
        wt.write(10,2,0,style)
        wt.write(10,3,cp_bill_cp_pay_c,style)
        wt.write(10,4,0,style)

        #填写差异数据数据
        # wt.write(14,0,u'充话费',style)
        # wt.write(14,1,u'营销成本',style)
        # wt.write(14,3,u'处理中',style)
        # wt.write(14,4,u'退款中',style)

        wt.write(14,0,cp_bill_product,style)
        wt.write(14,1,cp_bill_operation_cost_m,style)
        wt.write(14,3,0,style)
        wt.write(14,4,0,style)

        #填写差异信息
        cursor = connections['report'].cursor()
        cursor.execute("call `SP_T_RP_D_ACCOUNT_CHECK_SUMMARY_APP_REASON`(%s, %s, %s, %s, %s)",
                        [start_date, end_date, app, order_type, cp_type])
                        # [start_date, end_date, app, order_type, cp_type])
        objs = cursor.fetchall()
        rownum = 24
        for obj in objs:
            t_datas = obj[1].split('|')
            for data in t_datas:
                except_data = data.split(':')
                wt.write(rownum,0,except_data[0],style)
                wt.write(rownum,1,except_data[1],style)
                wt.write(rownum,2,float(except_data[2]) if except_data[2] is not None else 0,style)
                wt.write_merge(rownum,rownum,3,4,u"",style)
                rownum+=1

        #填写可能的实付款跨时段信息,rp_type 为 2, 获取跨天实付款
        cursor = connections['report'].cursor()
        cursor.execute("call `SP_T_RP_D_OPERATION_DATA_SUMMARY_OVER_MONTH_APP`(%s, %s, %s, %s, %s, %s)",
                        [start_date, end_date, app, order_type, cp_type, 2])
        objs = cursor.fetchall()
        for obj in objs:
            wt.write(rownum,0,u"跨天%s"%obj[1],style)
            wt.write(rownum,1,obj[4],style)
            wt.write(rownum,2,obj[5],style)
            wt.write_merge(rownum,rownum,3,4,u"",style)
            rownum+=1

        #填写合计数据
        if rownum!=24:
            wt.write(rownum,0,u"合计:",style)
            wt.write(rownum,1,u"",style)
            wt.write(rownum,2,Formula("SUM(C25:C%s)"%rownum),style)
            wt.write_merge(rownum,rownum,3,4,u"",style)

        ###绘制跨时段订单详情###

        # 设置标题
        wt_overdays.write(0, 0, u'订单号', main_header_style)
        wt_overdays.write(0, 1, u'业务名称', main_header_style)
        wt_overdays.write(0, 2, u'CP名称', main_header_style)
        wt_overdays.write(0, 3, u'订单创建时间', main_header_style)
        wt_overdays.write(0, 4, u'订单支付时间', main_header_style)
        wt_overdays.write(0, 5, u'订单退款时间', main_header_style)
        wt_overdays.write(0, 6, u'运营商扣款时间', main_header_style)
        wt_overdays.write(0, 7, u'实收款', main_header_style)
        wt_overdays.write(0, 8, u'实退款', main_header_style)
        wt_overdays.write(0, 9, u'实付款', main_header_style)

        # 获取跨时段订单数据,rp_type 为 1，获取跨时段订单详情
        cursor = connections['report'].cursor()
        cursor.execute("call `SP_T_RP_D_OPERATION_DATA_SUMMARY_OVER_MONTH_APP`(%s, %s, %s, %s, %s, %s)",
                       [start_date, end_date, app, order_type, cp_type, 1])
        objs = cursor.fetchall()
        rownum = 1

        # 将跨时段订单写入表格
        for obj in objs:
            wt_overdays.write(rownum, 0, smart_unicode(obj[0]))
            wt_overdays.write(rownum, 1, smart_unicode(obj[1]))
            wt_overdays.write(rownum, 2, smart_unicode(obj[2]))
            wt_overdays.write(rownum, 3, smart_unicode(obj[3]))
            wt_overdays.write(rownum, 4, smart_unicode(obj[4]))
            wt_overdays.write(rownum, 5, smart_unicode(obj[5]))
            wt_overdays.write(rownum, 6, smart_unicode(obj[6]))
            wt_overdays.write(rownum, 7, smart_unicode(obj[7]))
            wt_overdays.write(rownum, 8, smart_unicode(obj[8]))
            wt_overdays.write(rownum, 9, smart_unicode(obj[9]))
            rownum += 1
            col = 0
            # 调整列宽
            while col <= 9:
                if obj[col] and wt_overdays.col(col).width < len(str(obj[col])) * 367:
                    wt_overdays.col(col).width = len(str(obj[col])) * 367
                col += 1

        ###绘制异常订单详情###

        # 设置标题
        wt_abnormal.write(0, 0, u'订单号', main_header_style)
        wt_abnormal.write(0, 1, u'订单创建时间', main_header_style)
        wt_abnormal.write(0, 2, u'商品名称', main_header_style)
        wt_abnormal.write(0, 3, u'服务提供商', main_header_style)
        wt_abnormal.write(0, 4, u'支付方式', main_header_style)
        wt_abnormal.write(0, 5, u'商品定价', main_header_style)
        wt_abnormal.write(0, 6, u'商品成本价', main_header_style)
        wt_abnormal.write(0, 7, u'营销策略编号', main_header_style)
        wt_abnormal.write(0, 8, u'营销策略减免金额', main_header_style)
        wt_abnormal.write(0, 9, u'优惠券编号', main_header_style)
        wt_abnormal.write(0, 10, u'优惠券面值', main_header_style)
        wt_abnormal.write(0, 11, u'优惠券消耗价格', main_header_style)
        wt_abnormal.write(0, 12, u'交易状态', main_header_style)
        wt_abnormal.write(0, 13, u'应退款', main_header_style)
        wt_abnormal.write(0, 14, u'实收款', main_header_style)
        wt_abnormal.write(0, 15, u'实际退款', main_header_style)
        wt_abnormal.write(0, 16, u'交易服务费', main_header_style)
        wt_abnormal.write(0, 17, u'实际付款', main_header_style)
        wt_abnormal.write(0, 18, u'是否异常', main_header_style)
        wt_abnormal.write(0, 19, u'异常原因', main_header_style)
        wt_abnormal.write(0, 20, u'订单来源', main_header_style)

        # 获取异常订单数据
        cursor = connections['report'].cursor()
        cursor.execute("call `SP_T_RP_D_ACCOUNT_CHECKING`(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                       [start_date, end_date, order_type, cp_type, None, 1, None, None, None, app])
        objs = cursor.fetchall()
        rownum = 1

        # 将跨异常订单写入表格
        for obj in objs:
            wt_abnormal.write(rownum, 0, smart_unicode(obj[0]))
            wt_abnormal.write(rownum, 1, smart_unicode(obj[1]))
            wt_abnormal.write(rownum, 2, smart_unicode(obj[2]))
            wt_abnormal.write(rownum, 3, smart_unicode(obj[3]))
            wt_abnormal.write(rownum, 4, smart_unicode(obj[4]))
            wt_abnormal.write(rownum, 5, smart_unicode(obj[5]))
            wt_abnormal.write(rownum, 6, smart_unicode(obj[6]))
            wt_abnormal.write(rownum, 7, smart_unicode(obj[7]))
            wt_abnormal.write(rownum, 8, smart_unicode(obj[8]))
            wt_abnormal.write(rownum, 9, smart_unicode(obj[9]))
            wt_abnormal.write(rownum, 10, smart_unicode(obj[10]))
            wt_abnormal.write(rownum, 11, smart_unicode(obj[11]))
            wt_abnormal.write(rownum, 12, smart_unicode(obj[12]))
            wt_abnormal.write(rownum, 13, smart_unicode(obj[13]))
            wt_abnormal.write(rownum, 14, smart_unicode(obj[14]))
            wt_abnormal.write(rownum, 15, smart_unicode(obj[15]))
            wt_abnormal.write(rownum, 16, smart_unicode(obj[16]))
            wt_abnormal.write(rownum, 17, smart_unicode(obj[17]))
            wt_abnormal.write(rownum, 18, smart_unicode(obj[18]))
            wt_abnormal.write(rownum, 19, smart_unicode(obj[19]))
            wt_abnormal.write(rownum, 20, smart_unicode(obj[20]))
            rownum += 1
            col = 0
            # 调整列宽
            while col <= 20:
                if obj[col] and wt_abnormal.col(col).width < len(str(obj[col])) * 367:
                    wt_abnormal.col(col).width = len(str(obj[col])) * 367
                col += 1

    else:
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
        wt.write(14, 1, cp_u, style) #  营销成本

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

        




        ###绘制跨时段订单详情###

        #设置标题
        wt_overdays.write(0,0,u'订单号',main_header_style)
        wt_overdays.write(0,1,u'业务名称',main_header_style)
        wt_overdays.write(0,2,u'创建时间',main_header_style)
        wt_overdays.write(0,3,u'修改时间',main_header_style)
        wt_overdays.write(0,4,u'支付状态',main_header_style)
        wt_overdays.write(0,5,u'订单状态',main_header_style)
        wt_overdays.write(0,6,u'服务时间',main_header_style)
        wt_overdays.write(0,7,u'售价',main_header_style)
        wt_overdays.write(0,8,u'数量',main_header_style)
        wt_overdays.write(0,9,u'cp成本价',main_header_style)
        wt_overdays.write(0,10,u'cp补贴',main_header_style)
        wt_overdays.write(0,11,u'pt补贴',main_header_style)
        wt_overdays.write(0,12,u'订单金额',main_header_style)
        wt_overdays.write(0,13,u'结算金额',main_header_style)
        wt_overdays.write(0,14,u'优惠券id',main_header_style)
        wt_overdays.write(0,15,u'优惠券面额',main_header_style)
        wt_overdays.write(0,16,u'优惠券抵扣',main_header_style)
        wt_overdays.write(0,17,u'银行实收',main_header_style)
        wt_overdays.write(0,18,u'VIP卡付款',main_header_style)
        wt_overdays.write(0,19,u'次卡id',main_header_style)
        wt_overdays.write(0,20,u'主单号',main_header_style)
        wt_overdays.write(0,21,u'主单号',main_header_style)

        #获取跨时段订单数据,rp_type 为 1，获取跨时段订单详情
        cursor = connections['report'].cursor()
        cursor.execute("call `SP_T_RP_D_OPERATION_DATA_SUMMARY_OVER_MONTH_APP_NEW`(%s, %s, %s, %s)",
                        [start_date, end_date, app, cp_type])
        objs = cursor.fetchall()
        rownum = 1

        #将跨时段订单写入表格
        for obj in objs:
            wt_overdays.write(rownum,0,smart_unicode(obj[0]))
            wt_overdays.write(rownum,1,smart_unicode(obj[1]))
            wt_overdays.write(rownum,2,smart_unicode(obj[2]))
            wt_overdays.write(rownum,3,smart_unicode(obj[3]))
            wt_overdays.write(rownum,4,smart_unicode(obj[4]))
            wt_overdays.write(rownum,5,smart_unicode(obj[5]))
            wt_overdays.write(rownum,6,smart_unicode(obj[6]))
            wt_overdays.write(rownum,7,smart_unicode(obj[7]))
            wt_overdays.write(rownum,8,smart_unicode(obj[8]))
            wt_overdays.write(rownum,9,smart_unicode(obj[9]))
            wt_overdays.write(rownum,10,smart_unicode(obj[10]))
            wt_overdays.write(rownum,11,smart_unicode(obj[11]))
            wt_overdays.write(rownum,12,smart_unicode(obj[12]))
            wt_overdays.write(rownum,13,smart_unicode(obj[13]))
            wt_overdays.write(rownum,14,smart_unicode(obj[14]))
            wt_overdays.write(rownum,15,smart_unicode(obj[15]))
            wt_overdays.write(rownum,16,smart_unicode(obj[16]))
            wt_overdays.write(rownum,17,smart_unicode(obj[17]))
            wt_overdays.write(rownum,18,smart_unicode(obj[18]))
            wt_overdays.write(rownum,19,smart_unicode(obj[19]))
            wt_overdays.write(rownum,20,smart_unicode(obj[20]))
            rownum+=1
            col = 0
            #调整列宽
            while col <= 20:
                if obj[col] and wt_overdays.col(col).width < len(str(obj[col]))*367:
                    wt_overdays.col(col).width = len(str(obj[col]))*367
                col+=1


        ###绘制异常订单详情###

        #设置标题
        wt_abnormal.write(0, 0, u'订单号', main_header_style)
        wt_abnormal.write(0, 1, u'业务名称', main_header_style)
        wt_abnormal.write(0, 2, u'创建时间', main_header_style)
        wt_abnormal.write(0, 3, u'修改时间', main_header_style)
        wt_abnormal.write(0, 4, u'支付状态', main_header_style)
        wt_abnormal.write(0, 5, u'订单状态', main_header_style)
        wt_abnormal.write(0, 6, u'服务时间', main_header_style)
        wt_abnormal.write(0, 7, u'售价', main_header_style)
        wt_abnormal.write(0, 8, u'数量', main_header_style)
        wt_abnormal.write(0, 9, u'cp成本价', main_header_style)
        wt_abnormal.write(0, 10, u'cp补贴', main_header_style)
        wt_abnormal.write(0, 11, u'pt补贴', main_header_style)
        wt_abnormal.write(0,12,u'银行收款',main_header_style)
        wt_abnormal.write(0,13,u'银行退款',main_header_style)
        wt_abnormal.write(0,14,u'VIP收款',main_header_style)
        wt_abnormal.write(0,15,u'VIP退款',main_header_style)
        wt_abnormal.write(0,16,u'主单号',main_header_style)


        #获取异常订单数据
        cursor = connections['report'].cursor()
        cursor.execute("call `SP_T_RP_D_ACCOUNT_CHECKING_NEW`(%s, %s, %s, %s)",
                        [start_date, end_date, app, cp_type])
        objs = cursor.fetchall()
        rownum = 1

        #将跨异常订单写入表格
        for obj in objs:
            wt_abnormal.write(rownum,0,smart_unicode(obj[0]))
            wt_abnormal.write(rownum,1,smart_unicode(obj[1]))
            wt_abnormal.write(rownum,2,smart_unicode(obj[2]))
            wt_abnormal.write(rownum,3,smart_unicode(obj[3]))
            wt_abnormal.write(rownum,4,smart_unicode(obj[4]))
            wt_abnormal.write(rownum,5,smart_unicode(obj[5]))
            wt_abnormal.write(rownum,6,smart_unicode(obj[6]))
            wt_abnormal.write(rownum,7,smart_unicode(obj[7]))
            wt_abnormal.write(rownum,8,smart_unicode(obj[8]))
            wt_abnormal.write(rownum,9,smart_unicode(obj[9]))
            wt_abnormal.write(rownum,10,smart_unicode(obj[10]))
            wt_abnormal.write(rownum,11,smart_unicode(obj[11]))
            wt_abnormal.write(rownum,12,smart_unicode(obj[12]))
            wt_abnormal.write(rownum,13,smart_unicode(obj[13]))
            wt_abnormal.write(rownum,14,smart_unicode(obj[14]))
            wt_abnormal.write(rownum,15,smart_unicode(obj[15]))
            wt_abnormal.write(rownum,16,smart_unicode(obj[16]))
            rownum+=1
            col = 0
            #调整列宽
            while col <= 16:
                if obj[col] and wt_abnormal.col(col).width < len(str(obj[col]))*367:
                    wt_abnormal.col(col).width = len(str(obj[col]))*367
                col+=1

    ###运营数据分析###

    if order_type:
        if int(order_type) == 110:
            #表头部分
            wt_analysis.write_merge(0,0,0, 4, u'运营数据分析', main_header_style)
            wt_analysis.col(0).width = 10000
            wt_analysis.col(1).width = 7000
            wt_analysis.col(2).width = 7000
            wt_analysis.col(3).width = 7000
            wt_analysis.col(4).width = 10000

            wt_analysis.row(0).set_style(easyxf('font:height 360;'))

            #葡萄数据
            wt_analysis.write_merge(2,2,0, 4, u'葡萄数据', header_style)
            wt_analysis.write(3,0,u'业务类型',style)
            wt_analysis.write_merge(3,3,1,2,u'订单金额',style)
            wt_analysis.write_merge(3,3,3,4,u'订单交易笔数',style)


            #CP数据
            wt_analysis.write_merge(5,5,0, 4, u'CP数据', header_style)
            wt_analysis.write(6,0,u'业务类型',style)
            wt_analysis.write_merge(6,6,1,2,u'实付金额',style)
            wt_analysis.write_merge(6,6,3,4,u'订单交易笔数',style)

            #差异
            wt_analysis.write_merge(8,8,0, 4, u'收款渠道', header_style)
            wt_analysis.write_merge(9,10,0, 0, u'银行实收', style)
            wt_analysis.write_merge(9,10,1,2,u'VIP卡',style)
            wt_analysis.write_merge(9,10,3,3,u'次卡',style)
            wt_analysis.write_merge(9,10,4,4,u'优惠券',style)

            wt_analysis.write(13, 0, u'毛利', style)
            wt_analysis.write(13, 1, Formula("B5-B8"), style)
            # wt_analysis.write_merge(11,11,3,4,Formula("B5-B8"),style)


            #营销成本分析
            wt_analysis.write_merge(15,15,0, 4, u'营销成本分析', header_style)
            wt_analysis.write(16,0,u'营销成本类型',style)
            wt_analysis.write(16,1,u'活动名称',style)
            wt_analysis.write(16,2,u'订单数',style)
            wt_analysis.write(16,3,u'营销成本',style)
            wt_analysis.write(16,4,u'葡萄盈亏',style)

            #获取主表格信息
            cursor = connections['report'].cursor()
            cursor.execute("call `SP_T_RP_DUIZHANG_CP_BILL_ANALYSIS_APP_NEW`(%s, %s, %s, %s, %s)",
                            [start_date, end_date, app, order_type, cp_type])
            objs = cursor.fetchall()

            #设置结算单参数
            cp_bill_product = objs[0][3]  # 银行实收
            cp_bill_cp = smart_unicode(get_cp_name(cp_type))
            cp_bill_pt_pay_c = objs[0][2]
            cp_bill_pt_pay_m = objs[0][0]
            cp_bill_cp_pay_c = objs[0][2]
            cp_bill_cp_pay_m = objs[0][1]
            cp_bill_operation_cost_m = objs[0][4] # VIP卡付款
            cp_bill_cika = objs[0][5] # 次卡
            cp_bill_coupon = objs[0][6] # 优惠券

            #填写销售数据
            wt_analysis.write(4,0,u'全托管线上支付',style)
            wt_analysis.write_merge(4,4,1,2,cp_bill_pt_pay_m,style)
            wt_analysis.write_merge(4,4,3,4,cp_bill_pt_pay_c,style)

            #填写CP数据
            wt_analysis.write(7,0,u'全托管线上支付',style)
            wt_analysis.write_merge(7,7,1,2,cp_bill_cp_pay_m,style)
            wt_analysis.write_merge(7,7,3,4,cp_bill_cp_pay_c,style)

            #填写差异数据数据
            wt_analysis.write(11,0,cp_bill_product,style)
            wt_analysis.write_merge(11,11,1,2,cp_bill_operation_cost_m,style)
            wt_analysis.write(11,3,cp_bill_cika,style)
            wt_analysis.write(11,4,cp_bill_coupon,style)

            #获取营销费用分析信息
            cursor = connections['report'].cursor()
            cursor.execute("call `SP_T_RP_DUIZHANG_CP_BILL_DAOJIA_OPERATION_COST_APP_NEW`(%s, %s, %s, %s, %s)",
                            [start_date, end_date, app, order_type, cp_type])
            objs = cursor.fetchall()
            rownum = 17
            #将营销费用明细写入表格
            for obj in objs:
                wt_analysis.write(rownum,0,smart_unicode(obj[0]),style)
                wt_analysis.write(rownum,1,smart_unicode(obj[1]),style)
                wt_analysis.write(rownum,2,obj[2],style)
                wt_analysis.write(rownum,3,round(obj[3],2) if obj[3] is not None else 0,style)
                wt_analysis.write(rownum,4,round(obj[4],2) if obj[4] is not None else 0,style)
                rownum+=1
                col = 0
                #调整列宽
                while col < 4:
                    if obj[col] and wt_analysis.col(col).width < len(str(obj[col]))*367:
                        wt_analysis.col(col).width = len(str(obj[col]))*367
                    col+=1
            print rownum
            #填写合计数据
            if rownum!=17:
                wt_analysis.write(rownum,0,u"合计:",style)
                wt_analysis.write(rownum,1,u"",style)
                wt_analysis.write(rownum,2,Formula("SUM(C18:C%s)"%rownum),style)
                wt_analysis.write(rownum,3,Formula("SUM(D18:D%s)"%rownum),style)
                wt_analysis.write(rownum,4,Formula("SUM(E18:E%s)"%rownum),style)

            wt_analysis_detail.write(0,0,u'订单号',style)
            wt_analysis_detail.write(0,1,u'名称',style)
            wt_analysis_detail.write(0,2,u'创建时间',style)
            wt_analysis_detail.write(0,3,u'修改时间',style)
            wt_analysis_detail.write(0,4,u'订单状态',style)
            wt_analysis_detail.write(0,5,u'服务时间',style)
            wt_analysis_detail.write(0,6,u'售价',style)
            wt_analysis_detail.write(0,7,u'数量',style)
            wt_analysis_detail.write(0,8,u'cp成本价',style)
            wt_analysis_detail.write(0,9,u'cp补贴',style)
            wt_analysis_detail.write(0,10,u'pt补贴',style)
            wt_analysis_detail.write(0,11,u'订单金额',style)
            wt_analysis_detail.write(0,12,u'结算金额',style)
            wt_analysis_detail.write(0,13,u'优惠券id',style)
            wt_analysis_detail.write(0,14,u'优惠券面额',style)
            wt_analysis_detail.write(0,15,u'优惠券抵扣',style)
            wt_analysis_detail.write(0,16,u'银行实收',style)
            wt_analysis_detail.write(0,17,u'VIP卡付款',style)
            wt_analysis_detail.write(0,18,u'次卡id',style)
            wt_analysis_detail.write(0,19,u'主单号',style)

            rownum = 1
            # 获取营销费用分析信息明细
            cursor = connections['report'].cursor()
            cursor.execute("call `SP_T_RP_DUIZHANG_CP_BILL_ANALYSIS_APP_NEW_DETAIL`(%s, %s, %s, %s, %s)",
                           [start_date, end_date, app, order_type, cp_type])
            objs = cursor.fetchall()
            # 将营销费用明细写入表格
            for obj in objs:
                wt_analysis_detail.write(rownum, 0, smart_unicode(obj[0]), style)
                wt_analysis_detail.write(rownum, 1, smart_unicode(obj[1]), style)
                wt_analysis_detail.write(rownum, 2, smart_unicode(obj[2]), style)
                wt_analysis_detail.write(rownum, 3, smart_unicode(obj[3]), style)
                wt_analysis_detail.write(rownum, 4, obj[4], style)
                wt_analysis_detail.write(rownum, 5, obj[5].strftime('%Y-%m-%d %H:%M:%S'), style)
                wt_analysis_detail.write(rownum, 6, obj[6], style)
                wt_analysis_detail.write(rownum, 7, obj[7], style)
                wt_analysis_detail.write(rownum, 8, obj[8], style)
                wt_analysis_detail.write(rownum, 9, obj[9], style)
                wt_analysis_detail.write(rownum, 10, obj[10], style)
                wt_analysis_detail.write(rownum, 11, obj[11], style)
                wt_analysis_detail.write(rownum, 12, obj[12], style)
                wt_analysis_detail.write(rownum, 13, obj[13], style)
                wt_analysis_detail.write(rownum, 14, obj[14], style)
                wt_analysis_detail.write(rownum, 15, obj[15], style)
                wt_analysis_detail.write(rownum, 16, obj[16], style)
                wt_analysis_detail.write(rownum, 17, obj[17], style)
                wt_analysis_detail.write(rownum, 18, smart_unicode(obj[18]), style)
                wt_analysis_detail.write(rownum, 19, smart_unicode(obj[19]), style)
                rownum += 1


    #设置结算单名称
    name =smart_str("%s(%s-%s)结算单.xls" % (cp_bill_cp, start_date, end_date))

    #返回Http Response
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=%s' % name
    wb.save(response)

    return response