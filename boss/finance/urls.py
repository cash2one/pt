#coding: utf-8
from django.conf.urls import  patterns, url

"""
    finance模块所有的url
"""

urlpatterns = patterns('finance.views.unpending_order',
    url(r'^unpending_order_list/$', 'unpending_order',   {"template_name":"finance_list.html"}, name='unpending_order'),
    url(r'^unpending_order_ajax/$', 'unpending_order_ajax', name='unpending_order_ajax'),
    url(r'^unpending_order_csv/$',  'unpending_order_csv',  name='unpending_order_csv'),
)

urlpatterns += patterns('finance.views.except_order_sum',
    url(r'^except_order_sum/$', 'except_order_sum',   {"template_name":"except_order_sum.html"}, name='except_order_sum'),
    url(r'^except_order_sum_ajax/$', 'except_order_sum_ajax', name='except_order_sum_ajax'),
    url(r'^except_order_sum_csv/$',  'except_order_sum_csv',  name='except_order_sum_csv'),
)

urlpatterns += patterns('finance.views.pending_order',
    url(r'^pending_order/$',       'pending_order', {"template_name":"pending_order.html"}, name='pending_order'),
    url(r'^pending_order_ajax/$', 'pending_order_ajax', name='pending_order_ajax'),
    url(r'^pending_order_csv/$',  'pending_order_csv',   name='pending_order_csv'),
    url(r'^pending_order_detail_ajax/$', 'pending_order_detail_ajax', name='pending_order_detail_ajax'),
)

urlpatterns += patterns('finance.views.nr_account_order',
    url(r'^nr_account_order/$',       'nr_account_order', {"template_name":"nr_account_order.html"}, name='nr_account_order'),
    url(r'^nr_account_order_ajax/$', 'nr_account_order_ajax', name='nr_account_order_ajax'),
    url(r'^nr_account_order_csv/$',  'nr_account_order_csv',   name='nr_account_order_csv'),
)

urlpatterns += patterns('finance.views.over_month_order',
    url(r'^over_month_order/$',       'over_month_order', {"template_name":"over_month_order.html"}, name='over_month_order'),
    url(r'^over_month_order_ajax/$', 'over_month_order_ajax', name='over_month_order_ajax'),
    url(r'^over_month_order_csv/$',  'over_month_order_csv',   name='over_month_order_csv'),
)

urlpatterns += patterns('finance.views.cp_bill',
    url(r'^upload_cp_bill/$', 'upload_cp_bill', {"template_name":"upload_cp_bill.html"}, name='upload_cp_bill'),
    url(r'^upload_cp_csv/$',  'upload_cp_csv', name='upload_cp_csv'),
	url(r'^upload_balance_ajax/$', 'upload_balance_ajax', name='upload_balance_ajax'),
    url(r'^refresh_cp_summary/$', 'refresh_cp_summary', name='refresh_cp_summary'),
)

urlpatterns += patterns('finance.views.cp_pay',
    url(r'^upload_cp_pay/$', 'upload_cp_pay', {"template_name":"upload_cp_pay.html"}, name='upload_cp_pay'),
    url(r'^upload_cp_pay_csv/$',  'upload_cp_pay_csv', name='upload_cp_pay_csv'),
	url(r'^upload_balance_pay_ajax/$', 'upload_balance_pay_ajax', name='upload_balance_pay_ajax'),
	url(r'^refresh_zf_summary/$', 'refresh_zf_summary', name='refresh_zf_summary'),
)

urlpatterns += patterns('finance.views.finance_table',
    url(r'^$', 'finance_index', {"template_name":"finance_index.html"}, name='finance_index'),
    url(r'^finance_table/$',       'finance_table', {"template_name":"finance_table.html"}, name='finance_table'),
    url(r'^finance_table_ajax/$',       'finance_table_ajax', name='finance_table_ajax'),
    url(r'^finance_table_csv/$', 'finance_table_csv', name='finance_table_csv'),
)

urlpatterns += patterns('finance.views.daily_operate',
    url(r'^daily_operate/$', 'daily_operate', {"template_name":"daily_operate.html"}, name='daily_operate'),
    url(r'^daily_operate_ajax/$', 'daily_operate_ajax',  name='daily_operate_ajax'),
    url(r'^daily_operate_csv/$', 'daily_operate_csv',  name='daily_operate_csv'),
)

urlpatterns += patterns('finance.views.daily_operate_daojia',
    url(r'^daily_operate_daojia/$', 'daily_operate_daojia', {"template_name":"daily_operate_daojia.html"}, name='daily_operate_daojia'),
    url(r'^daily_operate_daojia_ajax/$', 'daily_operate_daojia_ajax',  name='daily_operate_daojia_ajax'),
    url(r'^daily_operate_daojia_csv/$', 'daily_operate_daojia_csv',  name='daily_operate_daojia_csv'),
)

urlpatterns += patterns('finance.views.daojia_coupon_detail',
    url(r'^daojia_coupon_detail/$', 'daojia_coupon_detail', {"template_name":"daojia_coupon_detail.html"}, name='daojia_coupon_detail'),
    url(r'^daojia_coupon_detail_ajax/$', 'daojia_coupon_detail_ajax',  name='daojia_coupon_detail_ajax'),
    url(r'^daojia_coupon_detail_csv/$', 'daojia_coupon_detail_csv',  name='daojia_coupon_detail_csv'),
)

urlpatterns += patterns('finance.views.daily_operate_cost',
    url(r'^daily_operate_cost/$', 'daily_operate_cost', {"template_name":"daily_operate_cost.html"}, name='daily_operate_cost'),
    url(r'^daily_operate_cost_ajax/$', 'daily_operate_cost_ajax',  name='daily_operate_cost_ajax'),
)

urlpatterns += patterns('finance.views.daily_operate_vip',
    url(r'^daily_operate_vip/$', 'daily_operate_vip', {"template_name":"daily_operate_vip.html"}, name='daily_operate_vip'),
    url(r'^daily_operate_vip_ajax/$', 'daily_operate_vip_ajax',  name='daily_operate_vip_ajax'),
    url(r'^daily_operate_vip_csv/$', 'daily_operate_vip_csv',  name='daily_operate_vip_csv'),
    url(r'^daily_operate_vip_detail/$', 'daily_operate_vip_detail', {"template_name":"daily_operate_vip_detail.html"}, name='daily_operate_vip_detail'),
    url(r'^daily_operate_vip_detail_ajax/$', 'daily_operate_vip_detail_ajax', name='daily_operate_vip_detail_ajax'),
    url(r'^daily_operate_vip_detail_csv/$', 'daily_operate_vip_detail_csv', name='daily_operate_vip_detail_csv'),
)

urlpatterns += patterns('finance.views.pay_summary_by_cp',
    url(r'^pay_summary_by_cp/$',       'pay_summary_by_cp', {"template_name":"pay_summary_by_cp.html"}, name='pay_summary_by_cp'),
    url(r'^pay_summary_by_cp_ajax/$', 'pay_summary_by_cp_ajax', name='pay_summary_by_cp_ajax'),
    url(r'^pay_summary_by_cp_csv/$',  'pay_summary_by_cp_csv',   name='pay_summary_by_cp_csv'),
)

urlpatterns += patterns('finance.views.pay_summary_by_daojia_cp',
    url(r'^pay_summary_by_daojia_cp/$',       'pay_summary_by_daojia_cp', {"template_name":"pay_summary_by_daojia_cp.html"}, name='pay_summary_by_daojia_cp'),
    url(r'^pay_summary_by_daojia_cp_ajax/$', 'pay_summary_by_daojia_cp_ajax', name='pay_summary_by_daojia_cp_ajax'),
    url(r'^pay_summary_by_daojia_cp_csv/$',  'pay_summary_by_daojia_cp_csv',   name='pay_summary_by_daojia_cp_csv'),
)

urlpatterns += patterns('finance.views.cp_statment',
    url(r'^cp_statment_list/$', 'cp_statment',   {"template_name":"cp_statment.html"}, name='cp_statment'),
    url(r'^cp_statment_ajax/$', 'cp_statment_ajax', name='cp_statment_ajax'),
    url(r'^cp_statment_csv/$',  'cp_statment_csv',  name='cp_statment_csv'),
)

urlpatterns += patterns('finance.views.over_month_daojia_order',
    url(r'^over_month_daojia_order/$',       'over_month_daojia_order', {"template_name":"over_month_daojia_order.html"}, name='over_month_daojia_order'),
    url(r'^over_month_daojia_order_ajax/$', 'over_month_daojia_order_ajax', name='over_month_daojia_order_ajax'),
    url(r'^over_month_daojia_order_csv/$',  'over_month_daojia_order_csv',   name='over_month_daojia_order_csv'),
)

urlpatterns += patterns('finance.views.batch_cp_statment',
    url(r'^batch_cp_statment_list/$', 'batch_cp_statment',   {"template_name":"batch_cp_statment.html"}, name='batch_cp_statment'),
    url(r'^batch_cp_statment_ajax/$', 'batch_cp_statment_ajax', name='batch_cp_statment_ajax'),
    url(r'^batch_cp_statment_csv/$',  'batch_cp_statment_csv',  name='batch_cp_statment_csv'),
)

urlpatterns += patterns('finance.views.nnk_orders_edit',
    url(r'^nnk_orders_edit/$',       'nnk_orders_edit', {"template_name":"nnk_orders_edit.html"}, name='nnk_orders_edit'),
    url(r'^nnk_orders_edit_ajax/$', 'nnk_orders_edit_ajax', name='nnk_orders_edit_ajax'),
    url(r'^nnk_orders_update_ajax/$', 'nnk_orders_update_ajax', name='nnk_orders_update_ajax'),
    url(r'^nnk_orders_edit_csv/$',  'nnk_orders_edit_csv',   name='nnk_orders_edit_csv'),
)


urlpatterns += patterns('finance.views.finance_pub',
    url(r'^order_settlement_amount/$', 'order_settlement_amount', name='order_settlement_amount'),
)
