# coding:utf-8

from django.conf.urls import include, url, patterns
from django.contrib import admin

urlpatterns = patterns('phone_fee.views.phone_fee_goods_management',
    url(r'^$', 'phone_fee_goods_management', {"template_name": "phone_fee_goods_management.html"}, name='phone_fee_index'),
    url(r'^phone_fee_goods_management/$', 'phone_fee_goods_management', {"template_name": "phone_fee_goods_management.html"}, name='phone_fee_goods_management'),
    url(r'^phone_fee_goods_management_ajax/$', 'phone_fee_goods_management_ajax', name='phone_fee_goods_management_ajax'),
    url(r'^phone_fee_goods_management_csv/$', 'phone_fee_goods_management_csv', name='phone_fee_goods_management_csv'),
    url(r'^batch_edit_guarantee_order_info/$', 'batch_edit_guarantee_order_info', name='batch_edit_guarantee_order_info'),
    url(r'^normal_edit_guarantee_order_info/$', 'normal_edit_guarantee_order_info', name='normal_edit_guarantee_order_info'),
    url(r'^phone_fee_batch_shelve_ajax/$', 'phone_fee_batch_shelve_ajax', name='phone_fee_batch_shelve_ajax'),
    url(r'^phone_fee_batch_shelve_timing/$', 'phone_fee_batch_shelve_timing', name='phone_fee_batch_shelve_timing'), # 定时上下架
    url(r'^phone_fee_batch_notify_ajax/$', 'phone_fee_batch_notify_ajax', name='phone_fee_batch_notify_ajax'),
    url(r'^phone_fee_batch_sale_price_ajax/$', 'phone_fee_batch_sale_price_ajax', name='phone_fee_batch_sale_price_ajax'),
    url(r'^phone_fee_more_ajax/$', 'phone_fee_more_ajax', name='phone_fee_more_ajax'),
)

urlpatterns += patterns('phone_fee.views.phone_fee_goods_management',
    url(r'^app/$', 'phone_fee_goods_management', {"template_name": "app_phone_fee_goods_management.html"}, name='app_phone_fee_goods_management'),
)

