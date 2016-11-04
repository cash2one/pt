#coding: utf-8
__author__ = 'Administrator'


from message_pub import *


reload(sys)
sys.setdefaultencoding('utf8')


def warning_abnormal_order(request, template_name):
    send_abnormal_order_warning()
    return HttpResponse(0)


def send_abnormal_order_warning():
    content, query_date = get_abnormal_order_warning_content()
    if content:
        email = EmailMessage('%s 异常订单状态预警(Django)' % query_date, content, to=['lzh@putao.cn'])
        email.content_subtype = "html"
        email.send()


def get_abnormal_order_warning_content(query_date=None):
    """
    运行每日报表任务
    :param query_date: 可以指定某一天进行查询，若为空，则默认是昨天！
    :return:
    """
    strdate = lambda d: ("%.2d-%.2d-%.2d" % (d.year, d.month, d.day))
    if not query_date:
        #查询日期默认是今天
        query_date = strdate(datetime.datetime.now()- datetime.timedelta(days = 1))

    # 获取异常订单统计信息
    sql_str = """
               SELECT o.product_type
                     ,SUM(CASE WHEN o.status IN (5,6) THEN 1 ELSE 0 END) AS f_count
                     ,SUM(CASE WHEN g.order_no IS NOT NULL AND o.status NOT IN (5,6) THEN 1 ELSE 0 END) AS p_count
               FROM pt_biz_db.pt_pay_order o
               LEFT JOIN pt_biz_db.pt_pay_order_guarantee g
                      ON o.order_no = g.order_no
               WHERE o.product_type IN (2,3,4,6,18,22,110)
                 AND o.c_time >= DATE_FORMAT(NOW() - INTERVAL 1 HOUR,'%%Y-%%m-%%d %%H:00:00')
                 AND o.c_time <= DATE_FORMAT(NOW(),'%%Y-%%m-%%d %%H:00:00')
               GROUP BY product_type
    """
    cursor = connections['order'].cursor()
    cursor.execute(sql_str)
    abnormal_product_list = cursor.fetchall()
    print "get abnormal summary list "


    # 获取异常订单列表
    cursor = connections['order'].cursor()
    cursor.execute("CALL `pt_biz_db`.`SP_T_RP_D_FAILED_ORDER_REPORT`(DATE_FORMAT(NOW() - INTERVAL 1 HOUR,'%%Y-%%m-%%d %%H:00:00'), DATE_FORMAT(NOW(),'%%Y-%%m-%%d %%H:00:00'), %s, %s, %s,%s);",
                   [None,None,None,None])
    abnormal_order_list = cursor.fetchall()
    print "get abnormal detail list "


    # 获取预警内容
    def __get_warning_product(abnormal_product_list):
        warning_list = []
        for obj in abnormal_product_list:
            sql_str = ("CALL `pt_biz_report`.`SP_T_UPDATE_WARNING_FAILED_ORDERS`(%s, %s, %s);" % (obj[0], obj[1], obj[2]))
            cursor = connections['report'].cursor()
            cursor.execute(sql_str)
            warning_info = cursor.fetchall()
            cursor.close()
            transaction.commit_unless_managed(using='report')
            if warning_info[0][2] == 1:
                warning_list.append(warning_info[0])
        print "get warning_list "
        return warning_list

    # 构建超时接单汇总表
    def __build_summary_report(warning_list, abnormal_product_list):
        report_overall_data = []
        report_overall_map = [
             ["product_name","业务名称","width:300px"],
             ["f_count","失败订单数","width:300px"],
             ["p_count","处理中订单数","width:300px"],
        ]
        for product in warning_list:
            for obj in abnormal_product_list:
                if int(product[1]) == obj[0]:
                    report_overall_data.append(
                        [
                            str(product[0]),
                            str(obj[1]),
                            str(obj[2]),
                        ]
                    )
        print "get summary_report"
        return report_overall_map, report_overall_data

    # 构建超时接单订单列表
    def __build_overall_report(warning_list, abnormal_order_list):
        report_overall_data = []
        report_overall_map = [
             ["id","ID","width:100px"],
             ["statdate","订单日期","width:100px"],
             ["order_no","订单号","width:100px"],
             ["c_time","订单创建时间","width:100px"],
             ["m_time","订单更新时间","width:100px"],
             ["name","商品名称","width:100px"],
             ["price","支付价格","width:100px"],
             ["product","业务类型","width:100px"],
             ["cp_name","CP名称","width:100px"],
             ["app_name","渠道名称","width:100px"],
             ["order_status","当前状态","width:100px"],
             ["status_tag","超时处理标记","width:100px"],
        ]
        for product in warning_list:
            for order in abnormal_order_list:
                if int(product[1]) == order[12]:
                    report_overall_data.append(
                        [
                            str(order[0]),
                            str(order[1]),
                            str(order[2]),
                            str(order[3]),
                            str(order[4]),
                            str(order[5]),
                            str(order[6]),
                            str(order[7]),
                            str(order[8]),
                            str(order[9]),
                            str(order[10]),
                            str(order[11]),
                        ]
                    )
        print "get overall_report"
        return report_overall_map, report_overall_data

    #根据数据，构建html内容
    warning_list = __get_warning_product(abnormal_product_list)
    print "This is warning list %s" % warning_list
    map,order_list = __build_overall_report(warning_list, abnormal_order_list)
    print "This is order list %s" % order_list
    if order_list:
        html = Html()
        html.p("Hi ALL!")
        html.p("以下业务，在最近一小时内，单个业务失败订单及处理中订单超过30笔，请及时处理。有任何疑问，请联系lzh@putao.cn.")
        html.table("异常订单汇总", *__build_summary_report(warning_list, abnormal_product_list))
        html.table("异常订单列表", *__build_overall_report(warning_list, abnormal_order_list))
        content = html.tail()
    else:
        content = None

    return content, query_date
