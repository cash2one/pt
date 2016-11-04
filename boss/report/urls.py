#coding: utf-8

from django.conf.urls import patterns, url

"""
    report应用所有的url
"""

urlpatterns = patterns('report.views.index',
    url(r'^$', 'report_index', {'template_name':'report_index.html'},name='report_index'),
)

urlpatterns += patterns('report.views.realtime_order_reports',
    url(r'^realtime_order_reports/$', 'realtime_order_reports', {'template_name':'realtime_order_reports.html'}, name="realtime_order_reports"),
    url(r'^realtime_order_reports_ajax/$', 'realtime_order_reports_ajax', name="realtime_order_reports_ajax"),
    url(r'^realtime_order_reports_csv/$', 'realtime_order_reports_csv', name="realtime_order_reports_csv"),
)

urlpatterns += patterns('report.views.order_reports',
    url(r'^order_reports/$', 'order_reports', {'template_name':'order_reports.html'}, name="order_reports"),
    url(r'^order_reports_ajax/$', 'order_reports_ajax', name="order_reports_ajax"),
    url(r'^order_reports_csv/$', 'order_reports_csv', name="order_reports_csv"),
)

urlpatterns += patterns('report.views.abnormal_order_report',
    url(r'^abnormal_order_report/$', 'abnormal_order_report', {'template_name':'abnormal_order_report.html'}, name="abnormal_order_report"),
    url(r'^abnormal_order_report_ajax/$', 'abnormal_order_report_ajax', name="abnormal_order_report_ajax"),
    url(r'^abnormal_order_report_csv/$', 'abnormal_order_report_csv', name="abnormal_order_report_csv"),
)

urlpatterns += patterns('report.views.order_sum',
    url(r'^order_sum/$', 'order_sum', {'template_name':'order_sum.html'}, name="order_sum"),
    url(r'^order_sum_ajax/$', 'order_sum_ajax', name="order_sum_ajax"),
    url(r'^order_sum_csv/$', 'order_sum_csv', name="order_sum_csv"),
)

urlpatterns += patterns('report.views.cp',
    url(r'^cp/$', 'cp', {"template_name": "cp.html"}, name="cp"),
    url(r'^cp_ajax/$', 'cp_ajax', name="cp_ajax"),
    url(r'^cp_csv/$', 'cp_csv', name="cp_csv"),
)

urlpatterns += patterns('report.views.failed_orders',
    url(r'^failed_orders/$', 'failed_orders', {"template_name": "failed_orders.html"}, name="failed_orders"),
    url(r'^failed_orders_ajax/$', 'failed_orders_ajax', name="failed_orders_ajax"),
    url(r'^failed_orders_csv/$', 'failed_orders_csv', name="failed_orders_csv"),
)

urlpatterns += patterns('report.views.trade',
    url(r'^trade/$', 'trade', {"template_name": "trade.html"}, name='trade'),
    url(r'^trade_ajax/$', 'trade_ajax', name='trade_ajax'),
    url(r'^trade_csv/$', 'trade_csv', name='trade_csv'),
)

# urlpatterns += patterns('report.views.report_pub',
#     url(r'^change_app_ajax/$', 'change_app_ajax', name='change_app_ajax'),
# )

urlpatterns += patterns('report.views.phone_fee',
    url(r'^phone_fee/$', 'phone_fee', {"template_name": "phone_fee.html"}, name='phone_fee'),
    url(r'^phone_fee_ajax/$', 'phone_fee_ajax', name='phone_fee_ajax'),
    url(r'^phone_fee_csv/$', 'phone_fee_csv', name='phone_fee_csv'),
)

urlpatterns += patterns('report.views.flow',
    url(r'^flow/$', 'flow', {"template_name": "flow.html"}, name='flow'),
    url(r'^flow_ajax/$', 'flow_ajax', name='flow_ajax'),
    url(r'^flow_csv/$', 'flow_csv', name='flow_csv'),
)

urlpatterns += patterns('report.views.qb',
    url(r'^qb/$', 'qb', {"template_name": "qb.html"}, name='qb'),
    url(r'^qb_ajax/$', 'qb_ajax', name='qb_ajax'),
    url(r'^qb_csv/$', 'qb_csv', name='qb_csv'),
)

urlpatterns += patterns('report.views.movie',
    url(r'^movie/$', 'movie', {"template_name": "movie.html"}, name='movie'),
    url(r'^movie_ajax/$', 'movie_ajax', name='movie_ajax'),
    url(r'^movie_csv/$', 'movie_csv', name='movie_csv'),
)

urlpatterns += patterns('report.views.service',
    url(r'^service/$', 'service', {"template_name": "service.html"}, name='service'),
    url(r'^service_ajax/$', 'service_ajax', name='service_ajax'),
    url(r'^service_csv/$', 'service_csv', name='service_csv'),
)

urlpatterns += patterns('report.views.coupon',
    url(r'^coupon/$', 'coupon', {"template_name": "coupon.html"}, name='coupon'),
    url(r'^coupon_ajax/$', 'coupon_ajax', name='coupon_ajax'),
    url(r'^coupon_csv/$', 'coupon_csv', name='coupon_csv'),
)

urlpatterns += patterns('report.views.full_hosting',
    url(r'^full_hosting/$', 'full_hosting', {"template_name": "full_hosting.html"}, name='full_hosting'),
    url(r'^full_hosting_ajax/$', 'full_hosting_ajax', name='full_hosting_ajax'),
    url(r'^full_hosting_csv/$', 'full_hosting_csv', name='full_hosting_csv'),
)

urlpatterns += patterns('report.views.goods',
    url(r'^goods/$', 'goods', {"template_name": "goods.html"}, name='goods'),
    url(r'^goods_ajax/$', 'goods_ajax', name='goods_ajax'),
    url(r'^goods_csv/$', 'goods_csv', name='goods_csv'),
)

urlpatterns += patterns('report.views.movie_sum',
    url(r'^movie_sum/$', 'movie_sum', {"template_name": "movie_sum.html"}, name='movie_sum'),
    url(r'^movie_sum_ajax/$', 'movie_sum_ajax', name='movie_sum_ajax'),
    url(r'^movie_sum_csv/$', 'movie_sum_csv', name='movie_sum_csv'),
)

urlpatterns += patterns('report.views.exchange',
    url(r'^exchange/$', 'exchange', {"template_name": "exchange.html"}, name='exchange'),
    url(r'^exchange_summaries/$', 'exchange_summaries', name='exchange_summaries'),
    url(r'^get_summary_line_data/$', 'get_summary_line_data', name='get_summary_line_data'),
    url(r'^exchange_reports_csv/$', 'exchange_reports_csv', name='exchange_reports_csv'),
)


#业务分析
urlpatterns += patterns('report.views.business',
    url(r'^bussiness_summary/$', 'bussiness_summary', {"template_name": "business.html"}, name='bussiness_summary'),
    url(r'^search_bussiness_summary/$', 'search_bussiness_summary', name='search_bussiness_summary'),
    url(r'^get_bussiness_line_data/$', 'get_bussiness_line_data', name='get_bussiness_line_data'),
    url(r'^exchange_business_reports_csv/$', 'exchange_business_reports_csv', name='exchange_business_reports_csv'),

)


urlpatterns += patterns('report.views.exchange_volume',
    url(r'^exchange_volume/$', 'exchange_volume', {"template_name": "exchange_volume.html"}, name='exchange_volume'),
    url(r'^exchange_volume_summaries/$', 'exchange_volume_summaries', name='exchange_volume_summaries'),
    url(r'^get_exchange_volume_line_data/$', 'get_exchange_volume_line_data', name='get_exchange_volume_line_data'),
    url(r'^exchange_volume_reports_csv/$', 'exchange_volume_reports_csv', name='exchange_volume_reports_csv'),
)

urlpatterns += patterns('report.views.exchange_order',
    url(r'^exchange_order/$', 'exchange_order', {"template_name": "exchange_order.html"}, name='exchange_order'),
    url(r'^exchange_order_summaries/$', 'exchange_order_summaries', name='exchange_order_summaries'),
    url(r'^get_exchange_order_line_data/$', 'get_exchange_order_line_data', name='get_exchange_order_line_data'),
    url(r'^exchange_order_reports_csv/$', 'exchange_order_reports_csv', name='exchange_order_reports_csv'),
)

urlpatterns += patterns('report.views.exchange_user',
    url(r'^exchange_user/$', 'exchange_user', {"template_name": "exchange_user.html"}, name='exchange_user'),
    url(r'^exchange_user_summaries/$', 'exchange_user_summaries', name='exchange_user_summaries'),
    url(r'^get_exchange_user_line_data/$', 'get_exchange_user_line_data', name='get_exchange_user_line_data'),
    url(r'^exchange_user_reports_csv/$', 'exchange_user_reports_csv', name='exchange_user_reports_csv'),
)

urlpatterns += patterns('report.views.exchange_daojia',
    url(r'^exchange_daojia/$', 'exchange_daojia', {"template_name": "exchange_daojia.html"}, name='exchange_daojia'),
    url(r'^exchange_daojia_summaries/$', 'exchange_daojia_summaries', name='exchange_daojia_summaries'),
    url(r'^get_exchange_daojia_line_data/$', 'get_exchange_daojia_line_data', name='get_exchange_daojia_line_data'),
    url(r'^exchange_daojia_reports_csv/$', 'exchange_daojia_reports_csv', name='exchange_daojia_reports_csv'),
    #到家cp展示
    url(r'^exchange_daojia_cp/$', 'exchange_daojia_cp',{"template_name": "exchange_daojia_cp.html"}, name='exchange_daojia_cp'),
    url(r'^exchange_daojia_cp_reports_csv/$', 'exchange_daojia_cp_reports_csv', name='exchange_daojia_cp_reports_csv'),

)

urlpatterns += patterns('report.views.exchange_activity',
    url(r'^exchange_activity/$', 'exchange_activity', {"template_name": "exchange_activity.html"}, name='exchange_activity'),
    url(r'^exchange_activity_summaries/$', 'exchange_activity_summaries', name='exchange_activity_summaries'),
    url(r'^get_exchange_activity_line_data/$', 'get_exchange_activity_line_data', name='get_exchange_activity_line_data'),
    url(r'^exchange_activity_reports_csv/$', 'exchange_activity_reports_csv', name='exchange_activity_reports_csv'),
)

urlpatterns += patterns('report.views.exchange_overview',
    url(r'^exchange_overview/$', 'exchange_overview', {"template_name": "exchange_overview.html"}, name='exchange_overview'),
    url(r'^exchange_overview_summaries/$', 'exchange_overview_summaries', name='exchange_overview_summaries'),
    url(r'^get_exchange_overview_table_data/$', 'get_exchange_overview_table_data', name='get_exchange_overview_table_data'),
    url(r'^exchange_overview_reports_csv/$', 'exchange_overview_reports_csv', name='exchange_overview_reports_csv'),
)

urlpatterns += patterns('report.views.exchange_self_order',
    url(r'^exchange_self_order/$', 'exchange_self_order', {"template_name": "exchange_self_order.html"}, name='exchange_self_order'),
    url(r'^exchange_self_order_summaries/$', 'exchange_self_order_summaries', name='exchange_self_order_summaries'),
    url(r'^get_exchange_self_order_table_data/$', 'get_exchange_self_order_table_data', name='get_exchange_self_order_table_data'),
    url(r'^exchange_self_order_reports_csv/$', 'exchange_self_order_reports_csv', name='exchange_self_order_reports_csv'),
)

urlpatterns += patterns('report.views.exchange_vip_order',
    url(r'^exchange_vip_order/$', 'exchange_vip_order', {"template_name": "exchange_vip_order.html"}, name='exchange_vip_order'),
    url(r'^exchange_vip_order_summaries/$', 'exchange_vip_order_summaries', name='exchange_vip_order_summaries'),
    url(r'^get_exchange_vip_order_table_data/$', 'get_exchange_vip_order_table_data', name='get_exchange_vip_order_table_data'),
    url(r'^exchange_vip_order_reports_csv/$', 'exchange_vip_order_reports_csv', name='exchange_vip_order_reports_csv'),
)

urlpatterns += patterns('report.views.exchange_daojia_order',
    url(r'^exchange_daojia_order/$', 'exchange_daojia_order', {"template_name": "exchange_daojia_order.html"}, name='exchange_daojia_order'),
    url(r'^exchange_daojia_order_summaries/$', 'exchange_daojia_order_summaries', name='exchange_daojia_order_summaries'),
    url(r'^exchange_daojia_order_evemonth/$', 'exchange_daojia_order_evemonth', name='exchange_daojia_order_evemonth'),
    url(r'^exchange_daojia_order_evemonth_csv/$', 'exchange_daojia_order_evemonth_csv', name='exchange_daojia_order_evemonth_csv'),
    url(r'^get_exchange_daojia_order_table_data/$', 'get_exchange_daojia_order_table_data', name='get_exchange_daojia_order_table_data'),
    url(r'^exchange_daojia_order_reports_csv/$', 'exchange_daojia_order_reports_csv', name='exchange_daojia_order_reports_csv'),
)

urlpatterns += patterns('report.views.exchange_daojia_order_service',
    url(r'^exchange_daojia_order_service/$', 'exchange_daojia_order_service', {"template_name": "exchange_daojia_order_service.html"}, name='exchange_daojia_order_service'),
    url(r'^exchange_daojia_order_service_ajax/$', 'exchange_daojia_order_service_ajax', name='exchange_daojia_order_service_ajax'),
    url(r'^exchange_daojia_order_service_csv/$', 'exchange_daojia_order_service_csv', name='exchange_daojia_order_service_csv'),
)

urlpatterns += patterns('report.views.exchange_daojia_order_marketing',
    url(r'^exchange_daojia_order_marketing/$', 'exchange_daojia_order_marketing', {"template_name": "exchange_daojia_order_marketing.html"}, name='exchange_daojia_order_marketing'),
    url(r'^exchange_daojia_order_marketing_ajax/$', 'exchange_daojia_order_marketing_ajax', name='exchange_daojia_order_marketing_ajax'),
    url(r'^exchange_daojia_order_marketing_csv/$', 'exchange_daojia_order_marketing_csv', name='exchange_daojia_order_marketing_csv'),
)

urlpatterns += patterns('report.views.exchange_daojia_order_area',
    url(r'^exchange_daojia_order_area/$', 'exchange_daojia_order_area', {"template_name": "exchange_daojia_order_area.html"}, name='exchange_daojia_order_area'),
    url(r'^exchange_daojia_order_area_ajax/$', 'exchange_daojia_order_area_ajax', name='exchange_daojia_order_area_ajax'),
    url(r'^exchange_daojia_order_area_csv/$', 'exchange_daojia_order_area_csv', name='exchange_daojia_order_area_csv'),
)

urlpatterns += patterns('report.views.exchange_daojia_order_activity',
    url(r'^exchange_daojia_order_activity/$', 'exchange_daojia_order_activity', {"template_name": "exchange_daojia_order_activity.html"}, name='exchange_daojia_order_activity'),
    url(r'^exchange_daojia_order_activity_ajax/$', 'exchange_daojia_order_activity_ajax', name='exchange_daojia_order_activity_ajax'),
    url(r'^exchange_daojia_order_activity_csv/$', 'exchange_daojia_order_activity_csv', name='exchange_daojia_order_activity_csv'),
)


urlpatterns += patterns('report.views.ditui_manage',
                        url(r'^ditui_info/$', 'ditui_info', {"template_name": "ditui_manage.html"}, name='ditui_info'),
                        url(r'^ditui_list/$', 'ditui_list',  name='ditui_list'),
                        url(r'^ditui_detail/(?P<pk>[0-9]+)$', 'ditui_detail',  name='ditui_detail'),
                        url(r'^ditui_deletelist/$', 'ditui_deletelist',  name='ditui_deletelist'),
                        url(r'^ditui_up_csv/$', 'ditui_up_csv',  name='ditui_up_csv'),
                        )

urlpatterns += patterns('report.views.invite_gift',
    url(r'^invite/(?P<who>[0-9]+)$', 'invite_index', {"template_name": "invite.html"}, name='invite_index'),
    url(r'^invite_list/$', 'invite_list', name='invite_list'),
    url(r'^invite_csv/$', 'invite_csv', name='invite_csv'),
    url(r'^invite_detail/$', 'invite_detail',  {"template_name": "invite_detail.html"},name='invite_detail'),
    url(r'^invite_detail_list/$', 'invite_detail_list',name='invite_detail_list'),
    url(r'^invite_detail_csv/$', 'invite_detail_csv', name='invite_detail_csv'),
)


urlpatterns += patterns('report.views.invite_overview',
    url(r'^invite_overview/$', 'invite_overview', {"template_name": "invite_overview.html"}, name='invite_overview'),
    url(r'^get_invite_overview_table_data/$', 'get_invite_overview_table_data', name='get_invite_overview_table_data'),
    url(r'^invite_overview_reports_csv/$', 'invite_overview_reports_csv', name='invite_overview_reports_csv'),
)


urlpatterns += patterns('report.views.invite_vip_overview',
    url(r'^invite_vip_overview/$', 'invite_vip_overview', {"template_name": "invite_vip_overview.html"}, name='invite_vip_overview'),
    url(r'^get_invite_vip_overview_table_data/$', 'get_invite_vip_overview_table_data', name='get_invite_vip_overview_table_data'),
    url(r'^invite_vip_overview_reports_csv/$', 'invite_vip_overview_reports_csv', name='invite_vip_overview_reports_csv'),
)


urlpatterns += patterns('report.views.exchange_vip_activity',
    url(r'^exchange_vip_activity/$', 'exchange_vip_activity', {"template_name":"exchange_vip_activity.html"}, name='exchange_vip_activity'),
    url(r'^exchange_vip_activity_ajax/$', 'exchange_vip_activity_ajax',  name='exchange_vip_activity_ajax'),
    url(r'^exchange_vip_activity_csv/$', 'exchange_vip_activity_csv',  name='exchange_vip_activity_csv'),
    url(r'^exchange_vip_activity_detail/$', 'exchange_vip_activity_detail', {"template_name":"exchange_vip_activity_detail.html"}, name='exchange_vip_activity_detail'),
    url(r'^exchange_vip_activity_detail_ajax/$', 'exchange_vip_activity_detail_ajax', name='exchange_vip_activity_detail_ajax'),
    url(r'^exchange_vip_activity_detail_csv/$', 'exchange_vip_activity_detail_csv', name='exchange_vip_activity_detail_csv'),
)


urlpatterns += patterns('report.views.exchange_entity_card_summary',
    url(r'^exchange_entity_card_summary/$', 'exchange_entity_card_summary', {"template_name":"exchange_entity_card_summary.html"}, name='exchange_entity_card_summary'),
    url(r'^exchange_entity_card_summary_ajax/$', 'exchange_entity_card_summary_ajax',  name='exchange_entity_card_summary_ajax'),
    url(r'^exchange_entity_card_summary_csv/$', 'exchange_entity_card_summary_csv',  name='exchange_entity_card_summary_csv'),
    url(r'^exchange_entity_card_summary_detail/$', 'exchange_entity_card_summary_detail', {"template_name":"exchange_entity_card_summary_detail.html"}, name='exchange_entity_card_summary_detail'),
    url(r'^exchange_entity_card_summary_detail_ajax/$', 'exchange_entity_card_summary_detail_ajax', name='exchange_entity_card_summary_detail_ajax'),
    url(r'^exchange_entity_card_summary_detail_csv/$', 'exchange_entity_card_summary_detail_csv', name='exchange_entity_card_summary_detail_csv'),
)


urlpatterns += patterns('report.views.exchange_daojia_order_summary',
    url(r'^exchange_daojia_order_summary/$', 'exchange_daojia_order_summary', {"template_name": "exchange_daojia_order_summary.html"}, name='exchange_daojia_order_summary'),
    url(r'^exchange_daojia_order_summary_evemonth/$', 'exchange_daojia_order_summary_evemonth', name='exchange_daojia_order_summary_evemonth'),
    url(r'^exchange_daojia_order_summary_linedata/$', 'exchange_daojia_order_summary_linedata', name='exchange_daojia_order_summary_linedata'),
    url(r'^exchange_daojia_order_summary_evemonth_csv/$', 'exchange_daojia_order_summary_evemonth_csv', name='exchange_daojia_order_summary_evemonth_csv'),
    url(r'^get_exchange_daojia_order_summary_table_data/$', 'get_exchange_daojia_order_summary_table_data', name='get_exchange_daojia_order_summary_table_data'),
    url(r'^exchange_daojia_order_summary_reports_csv/$', 'exchange_daojia_order_summary_reports_csv', name='exchange_daojia_order_summary_reports_csv'),
)
urlpatterns += patterns('report.views.exchange_daojia_order_cash',
    url(r'^exchange_daojia_order_cash/$', 'exchange_daojia_order_cash', {"template_name": "exchange_daojia_order_cash.html"}, name='exchange_daojia_order_cash'),
    url(r'^exchange_daojia_order_cash_evemonth/$', 'exchange_daojia_order_cash_evemonth', name='exchange_daojia_order_cash_evemonth'),
    url(r'^exchange_daojia_order_cash_evemonth_csv/$', 'exchange_daojia_order_cash_evemonth_csv', name='exchange_daojia_order_cash_evemonth_csv'),
    url(r'^get_exchange_daojia_order_cash_table_data/$', 'get_exchange_daojia_order_cash_table_data', name='get_exchange_daojia_order_cash_table_data'),
    url(r'^exchange_daojia_order_cash_reports_csv/$', 'exchange_daojia_order_cash_reports_csv', name='exchange_daojia_order_cash_reports_csv'),
)