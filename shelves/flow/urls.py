# coding:utf-8

from django.conf.urls import include, url, patterns
from django.contrib import admin

urlpatterns = patterns('flow.views.flow_goods_management',
    url(r'^$', 'flow_goods_management', {"template_name": "flow_goods_management.html"}, name='flow_index'),
    url(r'^flow_goods_management/$', 'flow_goods_management', {"template_name": "flow_goods_management.html"}, name='flow_goods_management'),
    url(r'^flow_goods_management_ajax/$', 'flow_goods_management_ajax', name='flow_goods_management_ajax'),
    url(r'^flow_goods_management_csv/$', 'flow_goods_management_csv', name='flow_goods_management_csv'),
    url(r'^flow_edit_guarantee_order_info/$', 'flow_edit_guarantee_order_info', name='flow_edit_guarantee_order_info'),
    url(r'^flow_batch_shelve_ajax/$', 'flow_batch_shelve_ajax', name='flow_batch_shelve_ajax'),
    url(r'^flow_batch_shelve_timing/$', 'flow_batch_shelve_timing', name='flow_batch_shelve_timing'), # 定时上下架
    url(r'^flow_batch_notify_ajax/$', 'flow_batch_notify_ajax', name='flow_batch_notify_ajax'),
    url(r'^flow_batch_sale_price_ajax/$', 'flow_batch_sale_price_ajax', name='flow_batch_sale_price_ajax'),
    url(r'^phone_flow_more_ajax/$', 'phone_flow_more_ajax', name='phone_flow_more_ajax'),
)

urlpatterns += patterns('flow.views.flow_goods_management',
    url(r'^app/$', 'flow_goods_management', {"template_name": "app_flow_goods_management.html"}, name='app_flow_goods_management'),
)