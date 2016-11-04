#coding: utf-8
__author__ = 'Administrator'


from message_pub import *


reload(sys)
sys.setdefaultencoding('utf8')


def lkl_daily_report(request, template_name):
    send_lkl_daily_report()
    return HttpResponse(0)


def send_lkl_daily_report():
    content, query_date = get_lkl_daily_report_content()
    if content:
        email = EmailMessage('%s 拉卡拉电影订单报表(Django)' % query_date, content, to=['lzh@putao.cn'])
        email.content_subtype = "html"
        email.send()


def get_lkl_daily_report_content(query_date=None):
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
             ["id","序号","width:100px"],
             ["c_time","订票时间","width:100px"],
             ["order_no","葡萄订单号","width:100px"],
             ["quantity","张数","width:100px"],
             ["trade_no","CP订单号","width:100px"],
             ["pt_u_id","用户ID","width:100px"],
             ["consumer_phone_number","取票手机号","width:100px"],
             ["face_value","交易金额","width:100px"],
             ["favo_price","用券金额","width:100px"],
             ["pay_price","用户实付","width:100px"],
             ["city_name","影院城市","width:100px"],
             ["cinema_name","影院名称","width:100px"],
             ["movie_name","电影名称","width:100px"],
        ]
        col_str = ",".join([item[0] for item in report_overall_map])
        sql_str = ("select concat(@rownum:=@rownum+1,'') as id,c_time ,order_no,quantity, trade_no, pt_u_id, consumer_phone_number, face_value, favo_price, pay_price,city_name,cinema_name,movie_name from (select ( @rownum:=0) as rownum,lkl.* from %s lkl) t;" % (sql_table_name))
        # print sql_str
        cursor = connections['order'].cursor()
        cursor.execute(sql_str)
        report_overall_data = cursor.fetchall()
        return report_overall_map, report_overall_data

    #根据数据，构建html内容
    order_list = __build_overall_report("vw_lkl_daily_movie_report")
    cursor = connections['order'].cursor()
    cursor.execute("select count(distinct order_no) as order_count,sum(quantity) as quantity_count from pt_biz_db.vw_lkl_daily_movie_report;")
    lkl_order_count = cursor.fetchall()
    if order_list[1]:
        html = Html()
        html.p("Hi ALL!")
        html.p("拉卡拉渠道电影业务，%s 共成交 %s 笔订单，%s 张电影票"%(query_date, lkl_order_count[0][0], lkl_order_count[0][1]))
        html.p("拉卡拉渠道电影每日交易明细报表内容如下，欢迎查看。有任何疑问，请联系lhn@putao.cn.")
        html.table("拉卡拉电影订单报表", *__build_overall_report("vw_lkl_daily_movie_report"))
        content = html.tail()

    else:
        content = None

    return content, query_date
