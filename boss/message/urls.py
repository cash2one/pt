#coding: utf-8
from django.conf.urls import  patterns, url

"""
    finance模块所有的url
"""

urlpatterns = patterns('message.views.operation_daily_report',
    url(r'^$', 'operation_daily_report', {"template_name":"operation_daily_report.html"}, name='operation_daily_report'),
    url(r'^operation_daily_report/$', 'operation_daily_report', {"template_name":"operation_daily_report.html"}, name='operation_daily_report'),
)

urlpatterns += patterns('message.views.lkl_daily_report',
    url(r'^lkl_daily_report/$', 'lkl_daily_report', {"template_name":"operation_daily_report.html"}, name='lkl_daily_report'),
)

urlpatterns += patterns('message.views.warning_abnormal_order',
    url(r'^warning_abnormal_order/$', 'warning_abnormal_order', {"template_name":"operation_daily_report.html"}, name='warning_abnormal_order'),
)

urlpatterns += patterns('message.views.notify_overtime_daojia_order',
    url(r'^notify_overtime_daojia_order/$', 'notify_overtime_daojia_order', {"template_name":"operation_daily_report.html"}, name='notify_overtime_daojia_order'),
)
