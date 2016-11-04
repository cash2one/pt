#coding: utf-8
__author__ = 'Administrator'


from message_pub import *


reload(sys)
sys.setdefaultencoding('utf8')


def operation_daily_report(request, template_name):
    send_operation_daily_report()
    return HttpResponse(0)


def send_operation_daily_report():
    content, query_date = get_operation_daily_report_content()
    if content:
        email = EmailMessage('%s 订单报表(Django)' % query_date, content, to=['lzh@putao.cn', '181559732@qq.com'])
        email.content_subtype = "html"
        email.send()


def get_operation_daily_report_content(query_date=None):
    """
    运行每日报表任务
    :param query_date: 可以指定某一天进行查询，若为空，则默认是昨天！
    :return:
    """
    strdate = lambda d: ("%.2d-%.2d-%.2d" % (d.year, d.month, d.day))
    if not query_date:
        # 查询日期默认是昨天
        query_date = strdate(datetime.datetime.now() - datetime.timedelta(days=1))
    # 查询最近一个星期的数据
    start_date = strdate(datetime.datetime.now() - datetime.timedelta(days=7))
    # 构建业务分表

    def __build_sub_report(sql_table_name):
        report_sub_map = [
            ["date", "日期", "width:100px"],
            ["category", "订单种类", "width:80px"],
            ["order_normal_status", "交易是否正常", "width:40px"],
            ["order_total_pay", "总成交额", "width:80px"],
            ["order_sum_count", "总交易笔数", "width:100px"],
            ["order_success_count", "成功笔数", "width:80px"],
            ["order_processing_count", "处理中笔数", "width:100px"],
            ["order_failed_count", "失败笔数", "width:80px"],
            ["refund_success_count", "退款成功笔数", "width:80px"],
            ["refund_failed_count", "退款失败笔数", "width:80px"],
            ["refund_processing_count", "退款中笔数", "width:60px"],
            ["alipay_get_money", "支付宝收款", "width:100px"],
            ["wx_get_money", "微信收款", "width:80px"],
            ["other_get_money", "其他收款", "width:80px"],
            ["alipay_refund_money", "支付宝退款", "width:100px"],
            ["wx_refund_money", "微信退款", "width:80px"],
            ["other_refund_money", "其他退款", "width:80px"],
            ["alipay_service_money", "支付宝费率", "width:100px"],
            ["wx_service_money", "微信费率", "width:80px"],
            ["cp_should_take_money", "CP应扣", "width:60px"],
            ["cp_reality_take_money", "CP实扣", "width:60px"],
            ["cp_refund_money", "CP退款", "width:60px"],
            ["operation_cost", "运营成本", "width:80px"],
            ["operation_cost_q", "运营成本(用券)", "width:80px"],
            ["gain_money", "营收合计", "width:80px"]
        ]
        col_str = ",".join([item[0] for item in report_sub_map])
        sql_str = ("select %s from %s where date between date('%s') and date('%s') "
               "order by date(date) desc " % (col_str, sql_table_name, start_date, query_date))
        cursor = connections['report'].cursor()
        cursor.execute(sql_str)
        report_sub_data = cursor.fetchall()
        return report_sub_map, report_sub_data

    #构建多CP业务分表
    def __build_multi_cps_report(sql_table_name):
        report_multi_cps_map = [
            ["date", "日期", "width:100px"],
            ["category", "订单种类", "width:80px"],
            ["cp_name", "CP名称", "width:100px"],
            ["order_normal_status", "交易是否正常", "width:40px"],
            ["order_total_pay", "总成交额", "width:80px"],
            ["order_sum_count", "总交易笔数", "width:100px"],
            ["order_success_count", "成功笔数", "width:80px"],
            ["order_processing_count", "处理中笔数", "width:100px"],
            ["order_failed_count", "失败笔数", "width:80px"],
            ["refund_success_count", "退款成功笔数", "width:80px"],
            ["refund_failed_count", "退款失败笔数", "width:80px"],
            ["refund_processing_count", "退款中笔数", "width:60px"],
            ["alipay_get_money", "支付宝收款", "width:100px"],
            ["wx_get_money", "微信收款", "width:80px"],
            ["other_get_money", "其他收款", "width:80px"],
            ["alipay_refund_money", "支付宝退款", "width:100px"],
            ["wx_refund_money", "微信退款", "width:80px"],
            ["other_refund_money", "其他退款", "width:80px"],
            ["alipay_service_money", "支付宝费率", "width:100px"],
            ["wx_service_money", "微信费率", "width:80px"],
            ["cp_should_take_money", "CP应扣", "width:60px"],
            ["cp_reality_take_money", "CP实扣", "width:60px"],
            ["cp_refund_money", "CP退款", "width:60px"],
            ["operation_cost", "运营成本", "width:80px"],
            ["operation_cost_q", "运营成本(用券)", "width:80px"],
            ["gain_money", "营收合计", "width:80px"]
        ]
        col_str = ",".join([item[0] for item in report_multi_cps_map])
        sql_str = ("select %s from %s where date between date('%s') and date('%s') "
               "order by date(date) desc " % (col_str, sql_table_name, start_date, query_date))
        cursor = connections['report'].cursor()
        cursor.execute(sql_str)
        report_multi_cps_data = cursor.fetchall()
        return report_multi_cps_map, report_multi_cps_data

    # 构建失败订单-分表
    def __build_failed_report(sql_table_name):
        report_failed_map = [
            ["order_no", "订单号", "width:300px"],
            ["product", "订单种类", "width:100px"],
            ["name", "订单详情", "width:300px"],
            ["price", "支付金额", "width:200px"],
            ["c_time", "创建时间", "width:200px"],
            ["status", "订单状态", "width:100px"],
            ["refund_status", "退款状态", "width:100px"],
            # 数据库没有该字段，也不会在数据库进行查找
            ["", "操作", "width:100px"]
        ]
        col_str = ",".join([item[0] for item in report_failed_map if item[0]])
        sql_str = ("select %s from %s " % (col_str, sql_table_name))
        cursor = connections['report'].cursor()
        cursor.execute(sql_str)
        report_failed_data = cursor.fetchall()
        report_failed_data = [list(i) for i in report_failed_data]
        for td_data in report_failed_data:
            a_href = "<a href='http://pay.putao.so/pay/refund/order?order_no=%s'>点击退款</a>" % td_data[0]
            td_data.append(a_href)
            # 退款状态翻译
            if td_data[6] == "REFUND_PROCESS":
                td_data[6] = "处理中"
            elif td_data[6] == "REFUND_FAIL":
                td_data[6] = "退款失败"
        return report_failed_map, report_failed_data

    # 构建服务信息汇总
    def __build_service_report(sql_table_name):
        report_service_map = [
            ["statdate", "日期", "width:100px"],
            ["name", "服务名称", "width:200px"],
            ["c_usernew", "新增用户", "width:100px"],
            ["c_user", "活跃用户", "width:100px"],
            ["c_event", "事件次数", "width:100px"],
            ["c_useapp", "启动次数", "width:100px"],
            ["c_usetime", "有时长次数", "width:100px"],
            ["s_usetime", "应用使用时长", "width:100px"],
        ]
        col_str = ",".join([item[0] for item in report_service_map])
        sql_str = ("select %s from %s where statdate = date('%s') " % (col_str, sql_table_name, query_date))
        cursor = connections['report'].cursor()
        cursor.execute(sql_str)
        report_service_data = cursor.fetchall()
        return report_service_map, report_service_data

    # 根据数据，构建html内容
    html = Html()
    html.p("Hi all,")
    html.p("总表和各业务分表统计的是最近七天的，失败的订单统计的是所有的，服务信息只统计了昨天的")
    html.p("每日报表内容如下，欢迎查看，有意见请联系<a href='mailto:lzh@putao.cn,mkh@putao.cn'>lzh@putao.cn,mkh@putao.cn</a>")
    # html.p("注：该次仅为测试版，可回传订单报表和所有业务点击报表还在开发中...")
    html.table("%s订单状态报表汇总" % query_date, *__build_sub_report("vw_pt_order_report_summary_total"))
    html.table("%s充话费业务分表" % query_date, *__build_sub_report("vw_pt_order_report_summary_phone_fee"))
    html.table("%s充流量业务分表" % query_date, *__build_sub_report("vw_pt_order_report_summary_flow"))
    # html.table("%s彩票业务分表" % query_date, *__build_sub_report("vw_pt_order_report_summary_lottery"))
    html.table("%s电影票业务分表" % query_date, *__build_sub_report("vw_pt_order_report_summary_movie"))
    html.table("%s火车票业务分表" % query_date, *__build_sub_report("vw_pt_order_report_summary_train"))
    html.table("%s酒店业务分表" % query_date, *__build_sub_report("vw_pt_order_report_summary_hotel"))
    html.table("%s水电煤业务分表" % query_date, *__build_sub_report("vw_pt_order_report_summary_wec"))
    html.table("%s游戏充值业务分表" % query_date, *__build_sub_report("vw_pt_order_report_summary_qb"))
    html.table("%s多CP业务-电影票分表" % query_date, *__build_multi_cps_report("vw_pt_order_report_summary_movie_cp"))
    html.table("所有失败订单汇总", *__build_failed_report("pt_pay_failed_list"))
    html.table("失败订单分表-充话费", *__build_failed_report("vw_pt_failed_order_list_phone_fee"))
    html.table("失败订单分表-充流量", *__build_failed_report("vw_pt_failed_order_list_flow"))
    # html.table("失败订单分表-彩票", *__build_failed_report("vw_pt_failed_order_list_lottery"))
    html.table("失败订单分表-电影票", *__build_failed_report("vw_pt_failed_order_list_movie"))
    html.table("失败订单分表-火车票", *__build_failed_report("vw_pt_failed_order_list_train"))
    html.table("失败订单分表-酒店", *__build_failed_report("vw_pt_failed_order_list_hotel"))
    html.table("失败订单分表-水电煤", *__build_failed_report("vw_pt_failed_order_list_wec"))
    html.table("失败订单分表-游戏充值", *__build_failed_report("vw_pt_failed_order_list_qb"))
    html.table("%s服务信息汇总" % query_date, *__build_service_report("vw_pt_service_summary"))
    content = html.tail()

    return content, query_date
