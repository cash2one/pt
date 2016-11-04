# coding: utf-8


from django.shortcuts import render_to_response
from order.models import PtDaojiaOrderNewUser,PtDaojiaOrderGuarantee
from order.views.order_pub import get_daojia_goods_category
from report_pub import *
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.hashers import make_password
from django.template import RequestContext
from django.db import connection,transaction
import time


@login_required
@permission_required(u'man.%s' % ReportConst.FULL_HOSTING, raise_exception=True)
@add_common_var
def full_hosting(request, template_name):
    cp_names = get_full_cp_names()
    order_status = get_full_order_status()
    test_status = get_test_status()
    daojia_table_columns = get_daojia_table_columns()
    activity_channels = get_activity_channels()
    citys = get_citys()

    return report_render(request, template_name,{
        "currentdate": get_datestr(0, "%Y-%m-%d"),
        "cp_names": cp_names,
        "order_status": order_status,
        "test_status": test_status,
        "daojia_table_columns":daojia_table_columns,
        "activity_channels":activity_channels,
        "citys": citys,
    })


def check_order_info(order, order_status, cp_name, mobile_num, start_date, end_date, g_special_filter, g_order_list, activity_channels,citys_select):
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

    if activity_channels:
        if not order.activity_channel:
            return  False
        elif str(order.activity_channel) not in activity_channels:
            return False

    if citys_select:
        if not order.city:
            return  False
        elif str(order.city) not in citys_select:
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
                and order.appid in [100219,100264]:
            return False
        if int(g_special_filter) == 6 \
                and not order.ditui_responser:
            return False

    return True


def update_order_info(orders,cur_page,per_page,g_special_filter):
    result = []
    rownum = 0 + (cur_page - 1) * per_page
    category = get_daojia_goods_category()
    for order in orders:
        cate_name = '未获取分类'
        if str(order.appid) in category.keys():
            cate_name = category[str(order.appid)]
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
        elif order.status == 25:
            status = "订单服务完成"
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
        else:
            status = "未知状态"
        if order.payway == 0:
            payway = "在线"
        elif order.payway == 1:
            payway = "线下"
        else:
            payway = "未知"
        if order.cancel_by == 0:
            cancel_by = '用户取消'
        else:
            cancel_by = 'CP取消'
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
        if order.is_first_order == 0:
            f_order_type = u"复购"
        elif order.is_first_order == 1:
            f_order_type = u"首购"
        elif order.is_first_order == 2:
            f_order_type = u"未成单"
        rownum += 1;
        result.append([
            str(order.id),
            str(order.order_no),
            str(order.cporderno),
            str(order.goodsname),
            str(order.goodsid),
            str(cate_name),
            str(order.provider),
            str(order.providermobile),
            payway,
            str(order.service_time)[:19],
            str(order.service_length),
            str(order.city),
            str(order.service_address),
            str(order.consumer),
            str(order.consumermobile),
            str(order.pt_username),
            int(order.quantity),
            float(order.price)/100,
            str(order.comment),
            float(order.pay_price)/100,
            str(order.create_time)[:19],
            str(order.modify_time)[:19],
            status,
            cancel_by,
            promotion_activity_info,
            str(order.staffname),
            str(order.staffphone),
            str(order.channel_no),
            f_order_type,
            str(order.ditui_area),
            str(order.ditui_responser),
            str(order.ditui_action_time),
            str(order.activity_channel),
            str(order.user_pay_price),
            str(order.prod_price),
            str(order.coupon_real_cost),
            str(order.promotion_favo_price),
            str(order.pt_cost),
            str(order.cp_cost),
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


@login_required
@permission_required(u'man.%s' % ReportConst.FULL_HOSTING, raise_exception=True)
def full_hosting_ajax(request):
    per_page = request.POST.get("per_page")
    cur_page = request.POST.get("cur_page")
    key = request.POST.get("key")
    order_status = request.POST.getlist("order_status[]")
    test_status = request.POST.get("test_status")
    cp_name = request.POST.getlist("cp_name[]")
    mobile_num = request.POST.get("mobile_num")
    start_date = request.POST.get("start_date")
    end_date = request.POST.get("end_date")
    g_special_filter =request.POST.get("g_special_filter")
    g_order_list = []
    selected_columns = request.POST.getlist("daojia_table[]")
    activity_channels = request.POST.getlist("activity_channels[]")
    citys_select = request.POST.getlist("citys_select[]")
    time_type = request.POST.get("time_type",'0')
    now = datetime.datetime.now()
    end_date_d = datetime.datetime.strptime(end_date, "%Y-%m-%d")+datetime.timedelta(days=1)
    print end_date_d

    if not cur_page:
        cur_page = 1
    if test_status == '0':
        if time_type == '0':
            orders = PtDaojiaOrderNewUser.objects.using('report').filter(consumer__contains="测试")\
                .filter(order_no__contains=key,
                        create_time__gte=start_date,
                        create_time__lte=end_date_d,
                        consumermobile__contains=mobile_num)\
                .exclude(order_source__contains="PT_TEST")\
                .order_by('-create_time')
        else:
            orders = PtDaojiaOrderNewUser.objects.using('report').filter(consumer__contains="测试") \
                .filter(order_no__contains=key,
                        service_time__gte=start_date,
                        service_time__lte=end_date_d,
                        consumermobile__contains=mobile_num) \
                .exclude(order_source__contains="PT_TEST") \
                .order_by('-service_time')
    elif test_status == '1':
        if time_type == '0':
            orders = PtDaojiaOrderNewUser.objects.using('report').exclude(consumer__contains="测试")\
                .filter(order_no__contains=key,
                        create_time__gte=start_date,
                        create_time__lte=end_date_d,
                        consumermobile__contains=mobile_num)\
                .exclude(order_source__contains="PT_TEST")\
                .order_by('-create_time')
        else:
            orders = PtDaojiaOrderNewUser.objects.using('report').exclude(consumer__contains="测试") \
                .filter(order_no__contains=key,
                        service_time__gte=start_date,
                        service_time__lte=end_date_d,
                        consumermobile__contains=mobile_num) \
                .exclude(order_source__contains="PT_TEST") \
                .order_by('-service_time')
    else:
        if time_type == '0':
            orders = PtDaojiaOrderNewUser.objects.using('report').filter(order_no__contains=key,
                        create_time__gte=start_date,
                        create_time__lte=end_date_d,
                        consumermobile__contains=mobile_num)\
                .exclude(order_source__contains="PT_TEST")\
                .order_by('-create_time')
        else:
            orders = PtDaojiaOrderNewUser.objects.using('report').filter(order_no__contains=key,
                                                                         service_time__gte=start_date,
                                                                         service_time__lte=end_date_d,
                                                                         consumermobile__contains=mobile_num) \
                .exclude(order_source__contains="PT_TEST") \
                .order_by('-service_time')

    #有效订单校验
    tt_orders = []
    order_list = []
    for order in orders:
        if check_order_info(order, order_status, cp_name, mobile_num, start_date, end_date, g_special_filter, g_order_list, activity_channels,citys_select):
            tt_orders.append(order)
        order_list.append(str(order.order_no));

   #获取订单列表下载信息
    global g_data
    g_data = []
    g_data = update_order_info(tt_orders, 0, 0, g_special_filter)

   #列表展示信息
    orders, num_pages = pag(tt_orders, per_page, cur_page)
    result = update_order_info(orders, int(cur_page), int(per_page), g_special_filter)

    #仅展示被选中的列表信息
    show_result = show_selected_columns(result,selected_columns)

    return HttpResponse(json.dumps([show_result, num_pages]))


@login_required
@permission_required(u'man.%s' % ReportConst.FULL_HOSTING, raise_exception=True)
def full_hosting_csv(request):
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")
    name = "全托管订单详情".encode('utf-8')
    filename = '%s(%s-%s).csv' % (name, str(start_date), str(end_date))
    csv_data = [["ID",
                     "订单号",
                     "CP订单号",
                     "商品名称",
                     "gid",
                     "分类",
                     "CP",
                     "CP电话",
                     "支付类型",
                     "服务开始时间",
                     "服务时长",
                     "服务预约城市",
                     "服务预约地址",
                     "消费者",
                     "消费者电话",
                     "下单人电话",
                     "数量",
                     "价格（元）",
                     "用户备注",
                     "订单金额（元）",
                     "创建时间",
                     "更新时间",
                     "状态",
                     "取消方",
                     "促销活动信息",
                     "服务人员名称",
                     "服务人员联系方式",
                     "渠道",
                     "首单/复购",
                     "地推小区",
                     "地推负责人",
                     "地推时间",
                     "活动渠道",
                     "用户支付金额金额",
                     "结算金额",
                     "优惠券实耗",
                     "活动营销费用",
                     "优惠券葡萄承担费用",
                     "优惠券CP承担费用"]]
    csv_data.extend(g_data)
    return get_csv_response(filename, csv_data)
