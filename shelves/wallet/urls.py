from django.conf.urls import include, url, patterns
from django.contrib import admin
from phone_fee.views import phone_fee_goods_management

urlpatterns = patterns('wallet.views.vip_goods',
                       url(r'^$', 'vip_goods', {"template_name": "vip_goods.html"}, name='vip_index'),
                       url(r'^vip_goods/$', 'vip_goods', {"template_name": "vip_goods.html"}, name='vip_goods'),
                       url(r'^vip_goods_ajax/$', 'vip_goods_ajax', name='vip_goods_ajax'),
                       url(r'^vip_goods_csv/$', 'vip_goods_csv', name='vip_goods_csv'),
                       url(r'^batch_edit_guarantee_order_info/$', 'batch_edit_guarantee_order_info', name='batch_edit_guarantee_order_info'),
                       url(r'^normal_edit_recharge_info/$', 'normal_edit_recharge_info', name='normal_edit_recharge_info'),
                       url(r'^edit_top/$', 'edit_top', name='edit_top'),
                       url(r'^edit_vendibility/$', 'edit_vendibility', name='edit_vendibility'),
                       )

urlpatterns += patterns('wallet.views.vip_redeem_codes',
                        url(r'^vip_redeem_codes/$', 'vip_redeem_codes', {"template_name": "vip_redeem_codes.html"}, name='vip_redeem_codes'),
                        url(r'^vip_redeem_codes_ajax/$', 'vip_redeem_codes_ajax', name='vip_redeem_codes_ajax'),
                        url(r'^vip_redeem_codes_csv/$', 'vip_redeem_codes_csv', name='vip_redeem_codes_csv'),
                        )

urlpatterns += patterns('wallet.views.vip_pub',
                        url(r'^edit_vip_card/$', 'edit_vip_card', name='edit_vip_card'),
                        url(r'^get_vip_info_ajax/$', 'get_vip_info_ajax', name='get_vip_info_ajax'),
                        )
