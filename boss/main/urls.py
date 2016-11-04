#coding: utf-8

from django.conf.urls import patterns, url

"""
    main应用所有的url
"""

urlpatterns = patterns('main.views.all_trend',
    url(r'^$', 'user_index', {"template_name": "user_index.html"}, name='user_index'),
    url(r'^all_trend/$', 'all_trend', {"template_name": "all_trend.html"}, name='all_trend'),
    url(r'^all_trend_csv/$', 'all_trend_csv', name='all_trend_csv'),
    url(r'^all_trend_ajax/$', 'all_trend_ajax', name='all_trend_ajax'),
)

urlpatterns += patterns('main.views.real_time',
    url(r'^real_time/$', 'real_time', {"template_name": "real_time.html"}, name='real_time'),
    url(r'^real_time_ajax/$', 'real_time_ajax', name='real_time_ajax'),
    url(r'^real_time_csv/$', 'real_time_csv', name='real_time_csv'),
)

urlpatterns += patterns('main.views.new_users',
    url(r'^new_users/$', 'new_users', {"template_name": "new_users.html"}, name='new_users'),
    url(r'^new_users_csv/$', 'new_users_csv', name='new_users_csv'),
    url(r'^new_users_ajax/$', 'new_users_ajax', name='new_users_ajax'),
)

urlpatterns += patterns('main.views.active_users',
    url(r'^active_users/$', 'active_users', {"template_name": "active_users.html"}, name='active_users'),
    url(r'^active_users_csv/$', 'active_users_csv', name='active_users_csv'),
    url(r'^active_users_ajax/$', 'active_users_ajax', name='active_users_ajax'),
)

urlpatterns += patterns('main.views.start_times',
    url(r'^start_times/$', 'start_times', {"template_name": "start_times.html"}, name='start_times'),
    url(r'^start_times_csv/$', 'start_times_csv', name='start_times_csv'),
    url(r'^start_times_ajax/$', 'start_times_ajax', name='start_times_ajax'),
)


urlpatterns += patterns('main.views.ver_pro',
    url(r'^ver_pro/$', 'ver_pro', {"template_name": "ver_pro.html"}, name='ver_pro'),
    url(r'^ver_pro_csv/$', 'ver_pro_csv', name='ver_pro_csv'),
    url(r'^ver_pro_ajax/$', 'ver_pro_ajax', name='ver_pro_ajax'),
)

urlpatterns += patterns('main.views.lave_users',
    url(r'^lave_users/$', 'lave_users', {"template_name": "lave_users.html"}, name='lave_users'),
    url(r'^lave_users_csv/$', 'lave_users_csv', name='lave_users_csv'),
    url(r'^lave_users_ajax/$', 'lave_users_ajax', name='lave_users_ajax'),
)

urlpatterns += patterns('main.views.period_details',
    url(r'^period_details/$', 'period_details', {"template_name": "period_details.html"}, name='period_details'),
    url(r'^period_details_csv/$', 'period_details_csv', name='period_details_csv'),
    url(r'^period_details_ajax/$', 'period_details_ajax', name='period_details_ajax'),
)

urlpatterns += patterns('main.views.channel_list',
    url(r'^channel_list/$', 'channel_list', {"template_name": "channel_list.html"}, name='channel_list'),
    url(r'^channel_list_csv/$', 'channel_list_csv', name='channel_list_csv'),
    url(r'^channel_list_ajax/$', 'channel_list_ajax', name='channel_list_ajax'),
)

urlpatterns += patterns('main.views.one_channel',
    url(r'^one_channel/$', 'one_channel', {"template_name": "one_channel.html"}, name='one_channel'),
    url(r'^one_channel_csv/$', 'one_channel_csv', name='one_channel_csv'),
    url(r'^one_channel_ajax/$', 'one_channel_ajax', name='one_channel_ajax'),
)

urlpatterns += patterns('main.views.used_time',
    url(r'^used_time/$', 'used_time', {"template_name": "used_time.html"}, name='used_time'),
    url(r'^used_time_ajax/$', 'used_time_ajax', name='used_time_ajax'),
    url(r'^used_time_once_csv/$', 'used_time_once_csv', name='used_time_once_csv'),
    url(r'^used_time_day_csv/$', 'used_time_day_csv', name='used_time_day_csv'),
)

urlpatterns += patterns('main.views.used_frequency',
    url(r'^used_frequency/$', 'used_frequency', {"template_name": "used_frequency.html"}, name='used_frequency'),
    url(r'^used_frequency_d_csv/$', 'used_frequency_d_csv', name='used_frequency_d_csv'),
    url(r'^used_frequency_w_csv/$', 'used_frequency_w_csv', name='used_frequency_w_csv'),
    url(r'^used_frequency_m_csv/$', 'used_frequency_m_csv', name='used_frequency_m_csv'),
    url(r'^used_frequency_ajax/$', 'used_frequency_ajax', name='used_frequency_ajax'),
)

urlpatterns += patterns('main.views.custom_event',
    url(r'^custom_event/$', 'custom_event', {"template_name": "custom_event.html"}, name='custom_event'),
    url(r'^custom_event_ajax/$', 'custom_event_ajax', name='custom_event_ajax'),
    url(r'^custom_event_csv/$', 'custom_event_csv', name='custom_event_csv'),
)

urlpatterns += patterns('main.views.event_detail',
    url(r'^event_detail/$', 'event_detail', {"template_name": "event_detail.html"}, name='event_detail'),
    url(r'^event_detail_ajax/$', 'event_detail_ajax', name='event_detail_ajax'),
    url(r'^event_detail_csv/$', 'event_detail_csv', name='event_detail_csv'),
    url(r'^event_param_csv/$', 'event_param_csv', name='event_param_csv'),
)

urlpatterns += patterns('main.views.page_access_path',
    url(r'^page_access_path/$', 'page_access_path', {"template_name": "page_access_path.html"}, name='page_access_path'),
)

urlpatterns += patterns('main.views.events',
    url(r'^events/$', 'events', {"template_name": "events.html"}, name='events'),
    url(r'^events_ajax/$', 'events_ajax', name='events_ajax'),
    url(r'^del_event/$', 'del_event', name='del_event'),
    url(r'^clear_event/$', 'clear_event', name='clear_event'),
    url(r'^edit_event/$', 'edit_event', {"template_name": "events.html"}, name='edit_event'),
    url(r'^upload_event_file/$', 'upload_event_file', name='upload_event_file'),
)

urlpatterns += patterns('main.views.loudou',
    url(r'^loudou/$', 'loudou_index', {"template_name": "loudou_index.html"}, name='loudou_index'),
    url(r'^loudou_main/$', 'loudou_main', name='loudou_main'),
    url(r'^loudou_main_csv/$', 'loudou_main_csv', name='loudou_main_csv'),
)
urlpatterns += patterns('main.views.loudou_detail',
    url(r'^loudou_detail_index/$', 'loudou_detail_index', {"template_name": "loudou_detail.html"}, name='loudou_detail_index'),
    url(r'^loudou_detail/$', 'loudou_detail', name='loudou_detail'),
    url(r'^loudou_detail_csv/$', 'loudou_detail_csv', name='loudou_detail_csv'),
)