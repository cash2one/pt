# -*-coding:utf-8 -*-
from django.conf.urls import include, url, patterns
from django.contrib import admin
from phone_fee.views import phone_fee_goods_management

# 葡萄卡
urlpatterns = patterns('pt_card.views.putao_card',
                       url(r'^$', 'putao_card_info', {"template_name": "putao_card.html"}, name='putao_card_index'),
                       url(r'^putao_card_info/$', 'putao_card_info', {"template_name": "putao_card.html"},
                           name='putao_card_info'),
                       url(r'^putao_card_edit/$', 'putao_card_edit', {"template_name": "putao_card_edit.html"},
                           name='putao_card_edit'),
                       url(r'^putao_card_goods/$', 'putao_card_goods', name='putao_card_goods'),
                       url(r'^putao_card_goods_detail/$', 'putao_card_goods_detail', name='putao_card_goods_detail'),
                       )
# 实体卡
urlpatterns += patterns('pt_card.views.entity_putao_card',
                        url(r'^entity_putao_card_info/$', 'entity_putao_card_info',
                            {"template_name": "entity_putao_card.html"}, name='entity_putao_card_info'),
                        url(r'^entity_putao_card_goods/$', 'entity_putao_card_goods', name='entity_putao_card_goods'),
                        url(r'^entity_putao_card_goods_detail/$', 'entity_putao_card_goods_detail',
                            name='entity_putao_card_goods_detail'),
                        url(r'^entity/codes/list/$', 'entity_codes_list',
                            name='entity_codes_list'),
                        url(r'^entity/codes/down/$', 'entity_codes_down',
                            name='entity_codes_down'),
                        )
# 葡萄商品
urlpatterns += patterns('pt_card.views.pt_card_goods',
                        url(r'^pt_card_goods_index/$', 'pt_card_goods_index',
                            {"template_name": "pt_card_goods_index.html"}, name='pt_card_goods_index'),
                        url(r'^pt_card_goods_info/$', 'pt_card_goods_info', name='pt_card_goods_info'),
                        url(r'^pt_card_goods_info_detail/$', 'pt_card_goods_info_detail',
                            name='pt_card_goods_info_detail'),
                        )
# 获取图片
urlpatterns += patterns('pt_card.views.pt_card_pub',
                        url(r'^get_images/$', 'search_image', name='get_images'),
                        )
# 获取二级三级商品
urlpatterns += patterns('pt_card.views.pt_card_pub',
                        url(r'^category/list/$', 'get_category_list', name='get_category_list'),# 二级所有列表
                        url(r'^get_sanji_list/$', 'get_sanji_list', name='get_sanji_list'),# 二级筛三级
                        url(r'^cps/list/$', 'get_cps_list', name='get_cps_list'),  # 用三级筛cp
                        url(r'^goods/list/$', 'get_goods_list', name='get_goods_list'), # 用cp筛商品
                        url(r'^get_all_sanji/$', 'get_all_sanji', name='get_all_sanji'), # 所有三级
                        url(r'^get_all_cps/$', 'get_all_cps', name='get_all_cps'), # 所有cp
                        url(r'^get_serch_goods/$', 'get_serch_goods', name='get_serch_goods'), # 关键词查商品
                        url(r'^get_sanji_cp_goods/$', 'get_goods_san_cp', name='get_goods_san_cp'), # 根据三级和cp找商品
                        url(r'^get_all_goods/$', 'get_all_goods', name='get_all_goods'), # 获取所有商品
                        )
