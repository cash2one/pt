#coding: utf-8

from django.conf.urls import patterns, url

"""
    order应用所有的url
"""

urlpatterns = patterns('order.views.order_management_recharge',
    url(r'^$', 'order_index', {"template_name": "order_index.html"}, name='order_index'),
    url(r'^order_management_recharge/$', 'order_management_recharge', {"template_name": "order_management_recharge.html"}, name='order_management_recharge'),
    url(r'^order_management_recharge_ajax/$', 'order_management_recharge_ajax', name='order_management_recharge_ajax'),
    url(r'^order_management_recharge_detail_ajax/$', 'order_management_recharge_detail_ajax', name="order_management_recharge_detail_ajax"),
    url(r'^order_management_recharge_csv/$', 'order_management_recharge_csv', name='order_management_recharge_csv'),
    url(r'^order_management_coupon_ids/$', 'order_management_coupon_ids', name='order_management_coupon_ids'),
    # url(r'^order_management_recharge_edit_order/$', 'order_management_recharge_edit_order', {"template_name": "order_management_recharge_edit_order.html"}, name='order_management_recharge_edit_order'),
)

urlpatterns += patterns('order.views.order_management_movie',
    url(r'^order_management_movie/$', 'order_management_movie', {"template_name": "order_management_movie.html"}, name='order_management_movie'),
    url(r'^order_management_movie_ajax/$', 'order_management_movie_ajax', name='order_management_movie_ajax'),
    url(r'^order_management_movie_detail_ajax/$', 'order_management_movie_detail_ajax', name="order_management_movie_detail_ajax"),
    url(r'^order_management_movie_csv/$', 'order_management_movie_csv', name='order_management_movie_csv'),
    # url(r'^order_management_movie_edit_order/$', 'order_management_movie_edit_order', {"template_name": "order_management_movie_edit_order.html"}, name='order_management_movie_edit_order'),
)

urlpatterns += patterns('order.views.order_management_daojia',
    url(r'^order_management_daojia/$', 'order_management_daojia', {"template_name": "order_management_daojia.html"}, name='order_management_daojia'),
    url(r'^order_management_daojia_select/$', 'order_management_daojia', {"template_name": "order_management_daojia_select.html"}, name='order_management_daojia_select'),
    url(r'^order_management_daojia_ajax/$', 'order_management_daojia_ajax', name='order_management_daojia_ajax'),
    url(r'^order_management_daojia_detail_ajax/$', 'order_management_daojia_detail_ajax', name="order_management_daojia_detail_ajax"),
    url(r'^order_management_daojia_csv/$', 'order_management_daojia_csv', name='order_management_daojia_csv'),
    url(r'^order_management_daojia_edit_order/$', 'order_management_daojia_edit_order', {"template_name": "order_management_daojia_edit_order.html"}, name='order_management_daojia_edit_order'),
    url(r'^get_guarantee_order_info/$', 'get_guarantee_order_info', name='get_guarantee_order_info'),
    url(r'^batch_edit_guarantee_order_info/$', 'batch_edit_guarantee_order_info', name='batch_edit_guarantee_order_info'),
    url(r'^normal_edit_guarantee_order_info/$', 'normal_edit_guarantee_order_info', name='normal_edit_guarantee_order_info'),
)


urlpatterns += patterns('order.views.order_management_vip',
    url(r'^order_management_vip/$', 'order_management_vip', {"template_name": "order_management_vip.html"}, name='order_management_vip'),
    url(r'^order_management_vip_ajax/$', 'order_management_vip_ajax', name='order_management_vip_ajax'),
    url(r'^order_management_vip_csv/$', 'order_management_vip_csv', name='order_management_vip_csv'),
)

urlpatterns += patterns('order.views.order_coupons_query',
    url(r'^order_coupons_query_info/$', 'order_coupons_query_info', {"template_name": "order_coupons_query.html"}, name='order_coupons_query_info'),
    url(r'^order_coupons_query_list/$', 'order_coupons_query_list', name='order_coupons_query_list'),
    url(r'^order_coupons_query_csv/$', 'order_coupons_query_csv', name='order_coupons_query_csv'),
)


