#coding: utf-8


__author__ = 'Administrator'

import datetime,sys,os,ConfigParser,time
from django.core.mail import EmailMessage
from django.http import HttpResponse, HttpResponseRedirect
from django.db import connections,transaction

class Html(object):
    """根据内容，按照一定样式，简单构建各HTML元素"""

    def __init__(self):
        """头部"""
        self.content = []
        self.content.append(
        """
        <html>
            <head>
	            <style type="text/css">
	                caption{
	                    color:#185CD3;
	                    font-size:26px;
	                    font-weight:bold;
	                    font-style:italic;
	                    margin-bottom:10px;
	                    margin-top:20px;
	                }
	                tr:first-child {
	                    background-color:RGB(216,216,216);
	                }
	                td{
	                    /*word-break:break-all;*/
	                    /*text-align:right;*/
	                }
	            </style>
            </head>
            <body>
        """
        )

    def table(self, caption, ths, tr_tds):
        """
        由普通数据构建统一的table元素，其中列的样式可以单独指定
        :param caption: 表格标题
        :param ths: 列名，格式为[["th1_en", "th1_zh", "style1"], ["th2_en", "th2_zh", "style2"] ...]
        :param tr_tds: 表格内容，格式为[["tr1_td1", "tr1_td2", ...], ["tr2_td1", "tr2_td2", ...], ...]
        :return:
        """
        table_style = """ border="1px" cellspacing="0px" style="border-collapse:collapse;" align="left" """

        self.content.append("<table %s>" % table_style)
        self.content.append("<caption>%s</caption>" % caption)
        #表头处理
        self.content.append("<tr>")
        for th in ths:
            self.content.append("<th style='%s'>%s</th>" % (th[2], th[1]))
        self.content.append("</tr>")
        #表格单元处理
        if tr_tds:
            for tr in tr_tds:
                self.content.append("<tr>")
                for td in tr:
                    self.content.append("<td>%s</td>" % td)
                self.content.append("</tr>")
        else:
            self.content.append("<tr>")
            for i in range(len(ths)):
                self.content.append("<td>空</td>")
            self.content.append("</tr>")

        self.content.append("</table>")

    def p(self, content):
        """
        构建p元素
        :param content: 内容
        :return:
        """
        self.content.append("<p>%s</p>" % content)

    def tail(self):
        """添加尾部，并返回最终结果"""
        self.content.append(
        """
            </body>
        </html>
        """
        )
        return "".join(self.content)