#coding: utf-8
__author__ = 'Administrator'


from message_pub import *


reload(sys)
sys.setdefaultencoding('utf8')


def notify_overtime_daojia_order(request, template_name):
    send_overtime_daojia_order_notify()
    return HttpResponse(0)


def send_overtime_daojia_order_notify():
    content, query_date = get_overtime_daojia_order_notify_content()
    if content:
        email = EmailMessage('%s 订单保障超时间接单提醒(Django)' % query_date, content, to=['lzh@putao.cn'])
        email.content_subtype = "html"
        email.send()


def get_overtime_daojia_order_notify_content(query_date=None):
    """
    运行每日报表任务
    :param query_date: 可以指定某一天进行查询，若为空，则默认是昨天！
    :return:
    """
    strdate = lambda d: ("%.2d-%.2d-%.2d" % (d.year, d.month, d.day))
    if not query_date:
        #查询日期默认是今天
        query_date = strdate(datetime.datetime.now()- datetime.timedelta(days = 1))
    #查询最近一个星期的数据
    start_date = strdate(datetime.datetime.now() - datetime.timedelta(days = 7))

    #构建超时接单订单列表
    def __build_overall_report(sql_table_name):
        report_overall_map = [
             ["order_no","订单号","width:100px"],
             ["provider","CP名称","width:100px"],
             ["consumer","消费者","width:100px"],
             ["consumerMobile","消费者电话","width:100px"],
             ["create_time","创建时间","width:100px"],
        ]
        col_str = ",".join([item[0] for item in report_overall_map])
        sql_str = ("select %s from %s ; " % (col_str, sql_table_name))
        print sql_str
        cursor = connections['order'].cursor()
        cursor.execute(sql_str)
        report_overall_data = cursor.fetchall()
        cursor.close()
        return report_overall_map, report_overall_data

    #根据数据，构建html内容
    order_list = __build_overall_report("vw_daojia_overtime_order_notify")
    if order_list[1]:
        html = Html()
        html.p("Hi 小葡萄,")
        html.p("发现超时接单，请及时联系cp跟踪处理！")
        html.table("超时接单列表", *__build_overall_report("vw_daojia_overtime_order_notify"))
        content = html.tail()

        #更新订单提现状态，设置已提醒为1
        cursor = connections['order'].cursor()
        cursor.execute("SET SQL_SAFE_UPDATES = 0;")
        cursor.execute("UPDATE pt_biz_db.pt_daojia_order_guarantee SET is_notify = 1 WHERE g_type = 1 AND g_status = 1;")
        cursor.execute("SET SQL_SAFE_UPDATES = 1;")
        transaction.commit_unless_managed(using='order')
    else:
        content = None

    return content, query_date
