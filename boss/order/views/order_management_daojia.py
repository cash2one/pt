# coding: utf-8


from django.shortcuts import render_to_response
from order.models import PtDaojiaOrder,PtDaojiaOrderGuarantee
from order_pub import *
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.hashers import make_password
from django.template import RequestContext
from django.db import connection,transaction
import time


@login_required
@permission_required(u'man.%s' % ReportConst.ORDER_MANAGEMENT_DAOJIA, raise_exception=True)
@add_common_var
def order_management_daojia(request, template_name):
    cp_names = get_full_cp_names()
    order_status = get_full_order_status()
    test_status = get_test_status()
    daojia_table_columns = get_daojia_table_columns()

    global g_data
    g_data = []
    # type = request.GET.get('type')
    # if type is not None and type == '1':
    #     none_data = [['--']*20]
    #     return report_render(request, template_name, {
    #         "currentdate": get_datestr(0, "%Y-%m-%d"),
    #         "cp_names": cp_names,
    #         "order_status": order_status,
    #         "test_status": test_status,
    #         "daojia_table_columns": daojia_table_columns,
    #         "none_data": none_data,
    #     })
    return report_render(request, template_name,{
        "currentdate": get_datestr(0, "%Y-%m-%d"),
        "cp_names": cp_names,
        "order_status": order_status,
        "test_status": test_status,
        "daojia_table_columns":daojia_table_columns,
    })

def get_order_detail(order_no):
    cursor = connections['report'].cursor()
    cursor.execute("call `SP_T_RP_DAOJIA_ORDER_DETAIL`(%s)",
                    [order_no])
    objs = cursor.fetchall()
    data = [["订单号","活动类型","活动时间","活动消息","获取url","请求参数","返回消息","创建时间","修改时间"]]
    for obj in objs:
        data.append(
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
            ]
        )
    if not data:
        data.append([Const.NONE] * 9)
    else:
        data.sort(key=lambda o: o[0], reverse=True)
    return data

def check_order_info(order, order_status, cp_name, mobile_num, start_date, end_date, g_special_filter,g_order_list):
    if order_status:
        if int(order.status) in ALL_ORDER_STATUS and str(order.status) not in order_status:
            return False

    if cp_name:
        if str(order.appid) not in cp_name:
            return False

    if mobile_num:
        print(order.consumermobile)
        if str(order.consumermobile).find(mobile_num) == -1:
            return False

    if start_date:
        if str(order.create_time)[:10] < start_date:
            return False

    if end_date:
        if str(order.create_time)[:10] > end_date:
            return False

    if g_special_filter:
        #超时接单：用户下单后，超过20分钟CP未接单
        if int(g_special_filter) == 1 and order.order_no not in g_order_list:
            return False
        #上门确认：离服务开始时间前2小时的单
        if int(g_special_filter) == 2 and order.order_no not in g_order_list:
            return False
        #服务回访：订单状态为15, 或者订单状态为14，当前时间晚于服务时间，且当前时间与订单服务时间的时间差大于六个小时
        if int(g_special_filter) == 3 and order.order_no not in g_order_list:
            return False
        #今日服务订单，返回服务状态是今天的所有订单
        elif int(g_special_filter) == 4 \
                and order.service_time.strftime("%Y-%m-%d") != datetime.date.today().strftime("%Y-%m-%d"):
            return False
        if int(g_special_filter) == 5 \
                and order.vip_price == 0:
            return False

    return True

def update_order_info(orders,cur_page,per_page,order_g_info,g_special_filter):
    result = []
    category = ""
    rownum = 0 + (cur_page - 1) * per_page;
    category_info = get_daojia_goods_category()
    for order in orders:
        try:
            category = category_info[str(order.appid)]
        except:
            pass
        if order.status == 0:
            status = "订单取消"
        elif order.status == 5:
            status = "退款中"
        elif order.status == 6:
            status = "退款成功"
        elif order.status == 9:
            status = "待支付"
        elif order.status == 10:
            status = "订单关闭"
        elif order.status == 11:
            status = "订单受理中"
        elif order.status == 12:
            status = "订单确认"
        elif order.status == 13:
            status = "服务人员出发"
        elif order.status == 14:
            status = "服务中"
        elif order.status == 15:
            status = "已服务"
        elif order.status == 16:
            status = "退款失败"
        elif order.status == 17:
            status = "预约成功"
        elif order.status == 18:
            status = "预约失败"
        elif order.status == 19:
            status = "订单取消中"
        elif order.status == 20:
            status = "订单取消成功"
            if order.cancel_by == 0:
                status += "(用户取消)"
            elif order.cancel_by == 1:
                status += "(CP取消)"
        elif order.status == 22:
            status = "服务方取消订单"
        elif order.status == 25:
            status = "订单服务完成"
        else:
            status = "未知状态"
        if order.payway == 0:
            payway = "在线"
        elif order.payway == 1:
            payway = "线下"
        else:
            payway = "未知"
        promotion_activity_info = ""
        if order.promotion_activity_info:
            obj = json.loads(order.promotion_activity_info)
            if "price" in obj:
                promotion_activity_info += "促销价：" + str(obj["price"]) + "分<br />"
            if "applyUser" in obj:
                if obj["applyUser"] == 0:
                    promotion_activity_info += "全部用户"
                elif obj["applyUser"] == 1:
                    promotion_activity_info += "新用户"
                elif obj["applyUser"] == 2:
                    promotion_activity_info += "老用户"
                promotion_activity_info += "<br />"
            if "promotionType" in obj:
                if obj["promotionType"] == 1:
                    promotion_activity_info += "定价型"
                elif obj["promotionType"] == 2:
                    promotion_activity_info += "立减型"
                promotion_activity_info += "<br />"
        status_overtime = ""
        status_order_confirm = ""
        status_feedback = ""
        comment_overtime = ""
        comment_order_confirm = ""
        comment_feedback = ""
        g_type = -1
        #获取订单保障状态
        for obj in order_g_info:
            if obj:
                if order.order_no == obj.order_no:
                    if obj.g_type == u"1":
                        g_type = 1
                        if obj.check_status == 0:
                            status_overtime += "<span style=""color:red"">待处理</span>"
                            comment_overtime += obj.pt_comment
                        elif obj.check_status == 1:
                            status_overtime += "<span style=""color:green"">已处理</span>"
                            comment_overtime += obj.pt_comment
                    if obj.g_type == u"2":
                        g_type = 2
                        if obj.check_status == 0:
                            status_order_confirm += "<span style=""color:red"">待确认</span>"
                            comment_order_confirm += obj.pt_comment
                        elif obj.check_status == 1:
                            status_order_confirm += "<span style=""color:green"">已确认</span>"
                            comment_order_confirm += obj.pt_comment
                    if obj.g_type == u"3":
                        g_type = 3
                        if obj.check_status == 0:
                            status_feedback += "<span style=""color:red"">待回访</span>"
                            comment_feedback += obj.pt_comment
                        elif obj.check_status == 1:
                            status_feedback += "<span style=""color:green"">已回访</span>"
                            comment_feedback += obj.pt_comment
        #
        # if g_type != -1:
        #     if g_special_filter:
        #         if g_type != int(g_special_filter):
        #             break;
        rownum += 1;
        result.append([
            str(order.id),
            category,
            str(order.order_no),
            str(order.cporderno),
            str(order.goodsname),
            str(order.provider),
            str(order.providermobile),
            payway,
            str(order.service_time_show),
            str(order.service_length),
            str(order.city),
            str(order.service_address),
            str(order.consumer),
            str(order.consumermobile),
            str(order.pt_username),
            int(order.quantity),
            float(order.price)/100,
            float(order.vip_price)/100,
            str(order.comment),
            float(order.pay_price)/100,
            str(order.create_time)[:19],
            str(order.modify_time)[:19],
            status,
            promotion_activity_info,
            status_overtime,
            status_order_confirm,
            status_feedback,
            comment_overtime,
            comment_order_confirm,
            comment_feedback,
            str(order.staffname),
            str(order.staffphone),
            str(order.trade_no),
            str(order.channel_no),
            str(order.cancel_msg),
            str(order.favo_price),
            str(order.user_pay_price),
            str(round(order.diff_price,2)),
            str(order.u_id),
        ])
    return result

def show_selected_columns(result,selected_columns):
    daojia_table_columns = get_daojia_table_columns()
    show_columns = []
    show_result = []
    row = []
    for col in selected_columns:
        for d_col in daojia_table_columns:
            if col == d_col[1]:
                show_columns.append(d_col[0])
    for obj in result:
        for s_col in show_columns:
            row.append(obj[s_col])
        show_result.append(row)
        row = []
    return show_result

#根据订单保障类型，获取订单保障的订单列表
def get_g_order_list(g_special_filter):
    g_order_list = []
    g_order_info = PtDaojiaOrderGuarantee.objects.filter(g_type__exact=g_special_filter,g_status__exact=1)
    for obj in g_order_info:
        g_order_list.append(str(obj.order_no))
    return g_order_list


@login_required
@permission_required(u'man.%s' % ReportConst.ORDER_MANAGEMENT_DAOJIA, raise_exception=True)
def order_management_daojia_ajax(request):
    per_page = request.POST.get("per_page")
    cur_page = request.POST.get("cur_page")
    key = request.POST.get("key",'')
    order_status = request.POST.getlist("order_status[]")
    test_status = request.POST.get("test_status")
    cp_name = request.POST.getlist("cp_name[]")
    mobile_num = request.POST.get("mobile_num",'')
    trade_no = request.POST.get("trade_no",'')
    start_date = request.POST.get("start_date",'2000-01-01')
    today = datetime.date.today()
    end_date = request.POST.get("end_date",today.strftime('%Y-%m-%d'))
    g_special_filter =request.POST.get("g_special_filter")
    g_order_list = []
    selected_columns = request.POST.getlist("daojia_table[]")
    end_date_d = datetime.datetime.strptime(end_date, "%Y-%m-%d")+datetime.timedelta(days=1)
    type = request.POST.get('type',0)
    if len(key) == 0 and len(trade_no) == 0 and len(mobile_num) == 0 and type == '1':
        return HttpResponse(json.dumps([[['--']*len(selected_columns)], 1]))
    # print end_date_d
    if not cur_page:
        cur_page = 1
    if test_status == '0':
        if len(key) == 0 and len(trade_no) == 0 and len(mobile_num) == 0 and type == 0:
            orders = PtDaojiaOrder.objects.filter(consumer__contains="测试") \
                .filter(
                create_time__gte=start_date,
                create_time__lte=end_date_d).order_by('-create_time')
        else:
            orders = PtDaojiaOrder.objects.filter(consumer__contains="测试")\
                .filter(order_no__contains=key,
                        create_time__gte=start_date,
                        create_time__lte=end_date_d,
                        trade_no__contains=trade_no,
                        consumermobile__contains=mobile_num)\
                .order_by('-create_time')
    elif test_status == '1':
        if len(key) == 0 and len(trade_no) == 0 and len(mobile_num) == 0 and type == 0:
            orders = PtDaojiaOrder.objects.exclude(consumer__contains="测试")\
                .filter(
                        create_time__gte=start_date,
                        create_time__lte=end_date_d).order_by('-create_time')
        else:
            orders = PtDaojiaOrder.objects.exclude(consumer__contains="测试") \
                .filter(order_no__contains=key,
                        create_time__gte=start_date,
                        create_time__lte=end_date_d,
                        trade_no__contains=trade_no,
                        consumermobile__contains=mobile_num) \
                .order_by('-create_time')
    else:
        if len(key) == 0 and len(trade_no) == 0 and len(mobile_num) == 0 and type == 0:
            orders = PtDaojiaOrder.objects.filter(create_time__gte=start_date,create_time__lte=end_date_d).order_by('-create_time')
        else:
            orders = PtDaojiaOrder.objects.filter(order_no__contains=key,
                        create_time__gte=start_date,
                        create_time__lte=end_date_d,
                        trade_no__contains=trade_no,
                        consumermobile__contains=mobile_num)\
                .order_by('-create_time')

    #获取订单保障信息列表
    if g_special_filter != -1:
         g_order_list = get_g_order_list(g_special_filter)

    #有效订单校验
    tt_orders = []
    order_list = []
    for order in orders:
        if check_order_info(order, order_status, cp_name, mobile_num, start_date, end_date, g_special_filter,g_order_list):
            tt_orders.append(order)
        order_list.append(str(order.order_no));

   # 获取订单保障信息
    order_g_info = PtDaojiaOrderGuarantee.objects.filter(order_no__in=order_list,g_status__exact=1)

   #获取订单列表下载信息
    global g_data
    g_data = []
    g_data = update_order_info(tt_orders, 0, 0, order_g_info,g_special_filter)

   #列表展示信息
    orders, num_pages = pag(tt_orders, per_page, cur_page)
    result = update_order_info(orders, int(cur_page), int(per_page), order_g_info,g_special_filter)

    #仅展示被选中的列表信息
    show_result = show_selected_columns(result,selected_columns)

    return HttpResponse(json.dumps([show_result, num_pages]))

@login_required
@permission_required(u'man.%s' % ReportConst.ORDER_MANAGEMENT_DAOJIA, raise_exception=True)
def order_management_daojia_detail_ajax(request):
    order_no = request.POST["order_no"]
    result = get_order_detail(order_no)
    return HttpResponse(json.dumps(result))

@login_required
@permission_required(u'man.%s' % ReportConst.ORDER_MANAGEMENT_DAOJIA, raise_exception=True)
def order_management_daojia_csv(request):
    start_date = request.GET.get("start_date",'')
    end_date = request.GET.get("end_date",'')
    filename = '%s(%s-%s).csv' % ("全托管订单详情", str(start_date), str(end_date))
    csv_data = [["ID",
                 "分类",
                 "订单号",
                 "CP订单号",
                 "商品名称",
                 "CP名称",
                 "CP电话",
                 "支付类型",
                 "服务开始时间",
                 "服务时长",
                 "服务预约城市",
                 "服务预约地址",
                 "消费者",
                 "消费者电话",
                 "下单者电话",
                 "数量",
                 "价格（元）",
                 "VIP价格（元）",
                 "用户备注",
                 "订单金额（元）",
                 "创建时间",
                 "更新时间",
                 "状态",
                 "促销活动信息",
                 "超时接单状态",
                 "上门确认状态",
                 "服务回访状态",
                 "超时接单评论",
                 "上们确认评论",
                 "服务回访评论",
                 "服务人员名称",
                 "服务人员联系方式",
                 "交易流水号",
                 "订单渠道",
                 "CP取消原因",
                 "优惠券金额",
                 "用户实付金额",
                 "补差价",
                 'u_id'
                 ]]
    csv_data.extend(g_data)
    return get_csv_response(filename, csv_data)

@login_required
@permission_required(u'man.%s' % ReportConst.ORDER_MANAGEMENT_DAOJIA, raise_exception=True)
def order_management_daojia_edit_order(request, template_name):

    #声明订单保障接收变量
    order_overtime = []
    order_confirm = []
    order_feedback = []

   #获取订单保障相关信息
    orderNo = request.GET.get("u")
    order_g_info = PtDaojiaOrderGuarantee.objects.filter(order_no=orderNo,g_status__exact=1)
    for obj in order_g_info:
        if obj:
            if obj.g_type == u"1":
                order_overtime.append(obj)
            if obj.g_type == u"2":
                order_confirm.append(obj)
            if obj.g_type == u"3":
                order_feedback.append(obj)

   #设置订单返回值
    comment_overtime=""
    comment_order_confirm=""
    comment_feedback=""
    check_overtime=0
    check_order_confirm=0
    check_feedback=0
    show_overtime = None
    show_order_confirm = None
    show_feedback = None

    if order_overtime:
        comment_overtime = order_overtime[0].pt_comment
        check_overtime = order_overtime[0].check_status
        show_overtime = 1
    if order_confirm:
        comment_order_confirm = order_confirm[0].pt_comment
        check_order_confirm = order_confirm[0].check_status
        show_order_confirm = 1
    if order_feedback:
        comment_feedback = order_feedback[0].pt_comment
        check_feedback = order_feedback[0].check_status
        show_feedback = 1

    #根据页面返回值，修改订单保障状态
    if request.method == 'POST':
        u_comment_overtime = request.POST.get("comment_overtime", "无评论")
        u_comment_order_confirm = request.POST.get("comment_order_confirm", "无评论")
        u_comment_feedback = request.POST.get("comment_feedback", "无评论")
        u_check_overtime = request.POST.get("check_overtime", "")
        u_check_order_confirm = request.POST.get("check_order_confirm", "")
        u_check_feedback = request.POST.get("check_feedback", "")
        print u_check_feedback

        if u_check_overtime == u"on":
            u_check_overtime = 1;
        else:
            u_check_overtime = 0;

        if u_check_order_confirm == u"on":
            u_check_order_confirm = 1;
        else:
            u_check_order_confirm = 0;

        if u_check_feedback == u"on":
            u_check_feedback = 1;
        else:
            u_check_feedback = 0;

        print u_check_overtime,u_check_order_confirm,u_check_feedback,u_comment_overtime,u_comment_order_confirm,u_comment_feedback

        if show_overtime:
            cursor = connections['order'].cursor()
            sql = "UPDATE pt_biz_db.pt_daojia_order_guarantee SET check_status = "+str(u_check_overtime)+" ,pt_comment = \""+str(u_comment_overtime)+"\" WHERE order_no = \""+str(orderNo)+"\"   AND g_type = 1"
            print(sql)
            cursor.execute(sql)
            transaction.commit_unless_managed(using='order')
        if show_order_confirm:
            cursor = connections['order'].cursor()
            sql = "UPDATE pt_biz_db.pt_daojia_order_guarantee SET check_status = "+str(u_check_order_confirm)+" ,pt_comment = \""+str(u_comment_order_confirm)+"\" WHERE order_no = \""+str(orderNo)+"\"   AND g_type = 2"
            print(sql)
            cursor.execute(sql)
            transaction.commit_unless_managed(using='order')
        if show_feedback:
            cursor = connections['order'].cursor()
            sql = "UPDATE pt_biz_db.pt_daojia_order_guarantee SET check_status = "+str(u_check_feedback)+" ,pt_comment = \""+str(u_comment_feedback)+"\" WHERE order_no = \""+str(orderNo)+"\"   AND g_type = 3"
            print(sql)
            cursor.execute(sql)
            transaction.commit_unless_managed(using='order')

        return HttpResponseRedirect(reverse("full_hosting"))

    return render_to_response(template_name, {
        "order_no": orderNo,
        "comment_overtime": comment_overtime,
        "comment_order_confirm": comment_order_confirm,
        "comment_feedback": comment_feedback,
        "check_overtime": check_overtime,
        "check_order_confirm": check_order_confirm,
        "check_feedback": check_feedback,
        "show_overtime": show_overtime,
        "show_order_confirm": show_order_confirm,
        "show_feedback": show_feedback,
        "errors": "",
    },context_instance=RequestContext(request))

@login_required
@permission_required(u'man.%s' % ReportConst.ORDER_MANAGEMENT_DAOJIA, raise_exception=True)
def get_guarantee_order_info(request):
    order_no = request.POST.get("order_no")
    g_special_filter =request.POST.get("g_special_filter")
    result = []
    objs = PtDaojiaOrderGuarantee.objects.filter(order_no=order_no,g_status__exact=1,g_type__exact=g_special_filter)
    for obj in objs:
        if obj:
            result.append(str(obj.pt_comment));
    return HttpResponse(json.dumps(result))

@login_required
@permission_required(u'man.%s' % ReportConst.ORDER_MANAGEMENT_DAOJIA, raise_exception=True)
def batch_edit_guarantee_order_info(request):
    edit_order_list = request.POST.get("edit_order_list")
    g_special_filter =request.POST.get("g_special_filter")
    check_status =request.POST.get("check_status")
    msg = 'no data update!'

    if edit_order_list and g_special_filter:
        cursor = connections['order'].cursor()
        sql = "UPDATE pt_biz_db.pt_daojia_order_guarantee SET check_status = "+str(check_status)+" WHERE g_type = "+str(g_special_filter)+"  AND order_no IN ( "+str(edit_order_list)+" );"
        print(sql)
        cursor.execute(sql)
        transaction.commit_unless_managed(using='order')
        msg = 'order update successfully!'

    return HttpResponse(json.dumps(msg))

@login_required
@permission_required(u'man.%s' % ReportConst.ORDER_MANAGEMENT_DAOJIA, raise_exception=True)
def normal_edit_guarantee_order_info(request):
    order_no = request.POST.get("order_no")
    g_special_filter =request.POST.get("g_special_filter")
    pt_comment =request.POST.get("pt_comment")
    msg = 'no data update!'

    if order_no and g_special_filter and pt_comment != "":
        cursor = connections['order'].cursor()
        sql = "UPDATE pt_biz_db.pt_daojia_order_guarantee SET pt_comment = \""+str(pt_comment)+"\" WHERE g_type = "+str(g_special_filter)+"  AND order_no IN ( \""+str(order_no)+"\" );"
        print(sql)
        cursor.execute(sql)
        transaction.commit_unless_managed(using='order')
        msg = 'order update successfully!'

    return HttpResponse(json.dumps(msg))
