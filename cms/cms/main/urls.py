# coding: utf-8

from django.conf.urls import url
from main.views import ver_channels, city_groups, services, actions, scenes, images, goods, category, coupons, \
    specialtopic, static_data, quick_order, category_index
from main.views import op_channel, man, check, record
from main.views import interface_category, interface_cpinfo
from main.views import cp
from main.views import problem
from pt_open.api import synch_skus


# 版本渠道
urlpatterns = [
    url(r'^new_version/$', ver_channels.new_version, name='new_version'),
    url(r'^edit_version/$', ver_channels.edit_version, name='edit_version'),
    url(r'^new_channel/$', ver_channels.new_channel, name='new_channel'),
    url(r'^edit_channel/$', ver_channels.edit_channel, name='edit_channel'),
    url(r'^del_ver_channels/$', ver_channels.del_ver_channels, name='del_ver_channels'),
    url(r'^ver_channels_test/$', ver_channels.ver_channels_test, name='ver_channels_test'),
]

# 城市分组
urlpatterns += [
    url(r'^new_city_group/$', city_groups.new_city_group, {"template_name": "city_groups/new_city_group.html"},
        name='new_city_group'),
    url(r'^edit_city_group/$', city_groups.edit_city_group, {"template_name": "city_groups/edit_city_group.html"},
        name='edit_city_group'),
    url(r'^city_groups/$', city_groups.city_groups, {"template_name": "city_groups/city_groups.html"},
        name='city_groups'),
    url(r'^get_city_group_list/$', city_groups.get_city_group_list, name='get_city_group_list'),
    url(r'^del_city_group/$', city_groups.del_city_group, name='del_city_group'),
    url(r'^get_cities/$', city_groups.get_cities),
    url(r'^get_city_from_group_id/$', city_groups.get_city_from_group_id, name='get_city_from_group_id'),
    url(r'^search_city_groups/$', city_groups.search_city_groups, name='search_city_groups'),
]

# 服务
urlpatterns += [
    url(r'^services/$', services.services, {"template_name": "services/services.html"}, name='services'),
    url(r'^new_service/$', services.new_service, {"template_name": "services/new_service.html"}, name='new_service'),
    url(r'^edit_service/$', services.edit_service, {"template_name": "services/edit_service.html"},
        name='edit_service'),
    url(r'^del_service/$', services.del_service, name='del_service'),
    url(r'^get_services/$', services.search_services, name='get_services'),
]

# 动作
urlpatterns += [
    url(r'^actions/$', actions.actions, {"template_name": "actions/actions.html"}, name='actions'),
    # url(r'^get_actions_select/$', actions.get_actions_select, name='get_actions_select'),
    url(r'^search_actions/$', actions.search_actions, name='search_actions'),
    url(r'^get_actions_table/$', actions.get_actions_select, name='get_actions_table'),
    url(r'^new_action/$', actions.new_action, {"template_name": "actions/new_action.html"}, name='new_action'),
    url(r'^edit_action/$', actions.edit_action, {"template_name": "actions/edit_action.html"}, name='edit_action'),
    url(r'^del_action/$', actions.del_action, name='del_action'),
    url(r'^ajax_actions/$', actions.ajax_actions, name='ajax_actions'),
]

# 图片
urlpatterns += [
    url(r'^images/$', images.images, {"template_name": "images.html"}, name='images'),
    url(r'^new_image/$', images.new_image, {"template_name": "new_image.html"}, name='new_image'),
    url(r'^del_image/$', images.del_image, name='del_image'),
    url(r'^get_images/$', images.search_image, name='get_images'),

]

# 场景
urlpatterns += [
    url(r'^get_scenes/$', scenes.get_scenes, name='get_scenes'),
]

# 商品
urlpatterns += [
    url(r'^goods/$', goods.goods, {"template_name": "goods/goods.html"}, name='goods'),
    url(r'^search_goods/$', goods.search_goods, name='search_goods'),
    url(r'^new_goods/$', goods.new_goods, {"template_name": "goods/new_goods.html"}, name='new_goods'),
    url(r'^edit_goods/$', goods.edit_goods, {"template_name": "goods/edit_goods.html"}, name='edit_goods'),
    url(r'^del_goods/$', goods.del_goods, name='del_goods'),
    url(r'^exchange_sort/$', goods.exchange_sort, name='exchange_sort'),
    url(r'^ajax_goods/$', goods.ajax_goods, name='ajax_goods'),
    url(r'^ajax_desc_goods/$', goods.ajax_desc_goods, name='ajax_desc_goods'),

]

# 分类
urlpatterns += [
    url(r'^category/$', category.category, {"template_name": "category/category.html"}, name='category'),
    url(r'^search_categories/$', category.search_categories, name='search_categories'),
    url(r'^new_cate_group/$', category.new_cate_group, {"template_name": "category/new_cate_group.html"},
        name="new_cate_group"),

    url(r'^edit_cate_group/$', category.edit_cate_group, {"template_name": "category/edit_cate_group.html"},
        name="edit_cate_group"),

    url(r'^new_category_first/$', category.new_category_first, {"template_name": "category/new_category_first.html"},
        name='new_category_first'),
    url(r'^new_category_second/$', category.new_category_second, {"template_name": "category/new_category_second.html"},
        name='new_category_second'),

    url(r'^edit_category_first/$', category.edit_category_first, {"template_name": "category/edit_category_first.html"},
        name='edit_category_first'),
    url(r'^edit_category_second/$', category.edit_category_second,
        {"template_name": "category/edit_category_second.html"}, name='edit_category_second'),
    url(r'^del_category/$', category.del_category, name='del_category'),
    # 快捷入口
    url(r'^quick_order/$', quick_order.quick_order, {"template_name": "quick_order/quick_order.html"},
        name='quick_order'),
    url(r'^edit_quick_order/$', quick_order.edit_quick_order, {"template_name": "quick_order/edit_quick_order.html"},
        name='edit_quick_order'),
    url(r'^delete_quick_order/$', quick_order.delete_quick_order, name='delete_quick_order'),
    url(r'^search_quick_orders/$', quick_order.search_quick_orders, name='search_quick_orders'),
    url(r'^update_quick_order/$', quick_order.update_quick_order, name='update_quick_order'),

    url(r'^ajax_second_categories/$', quick_order.search_second_category, name='ajax_second_categories'),
    url(r'^insert_quick_order/$', quick_order.insert_quick_order, name="insert_quick_order"),
    url(r'^ajax_quick_order/$', quick_order.ajax_quick_order, name="ajax_quick_order"),

    # 分类首页
    url(r'^category_index/$', category_index.category_index, {"template_name": "category_index/category_index.html"},
        name='category_index'),
    url(r'^edit_category_index/$', category_index.edit_category_index,
        {"template_name": "category_index/edit_category_index.html"},
        name='edit_category_index'),
    url(r'^search_category_index/$', category_index.search_category_index, name='search_category_index'),
    url(r'^insert_category_index/$', category_index.insert_category_index, name='insert_category_index'),
    url(r'^delete_category_index/$', category_index.delete_category_index, name='delete_category_index'),
    url(r'^update_category_index/$', category_index.update_category_index, name='update_category_index'),
    url(r'^ajax_second_categories_ci/$', category.search_second_category, name='ajax_second_categories_ci'),

]

# 优惠券
urlpatterns += [
    url(r'^coupons/$', coupons.coupons, {"template_name": "coupons/coupons.html"}, name="coupons"),
    url(r'^search_coupons/$', coupons.search_coupons, name='search_coupons'),
    url(r'^new_coupons/$', coupons.new_coupons, {"template_name": "coupons/new_coupons.html"}, name="new_coupons"),
    url(r'^edit_coupons/$', coupons.edit_coupons, {"template_name": "coupons/edit_coupons.html"}, name="edit_coupons"),
    url(r'^delete_coupons/$', coupons.delete_coupons, name="delete_coupons"),
]

# HEAD

#静态数据
# urlpatterns+=[
#     url(r'^static_data/$',static_data.static_data,{"template_name":"static_data/static_data.html"},name="static_data"),
#     url(r'^search_static_data/$',static_data.search_static_data, name='search_static_data'),
#     url(r'^new_shop/$',static_data.new_shop,{"template_name":"static_data/new_shop.html"},name="new_shop"),
#     url(r'^edit_shop/$',static_data.edit_shop,{"template_name":"static_data/edit_shop.html"},name="edit_shop"),
#     url(r'^delete_shop/$',static_data.delete_shop,name="delete_shop"),
# end HEAD

# 专题
urlpatterns += [
    url(r'^specialtopics/$', specialtopic.specialtopics, {"template_name": "specialtopic/specialtopics.html"},
        name="specialtopics"),
    url(r'^search_specialtopic/$', specialtopic.search_specialtopic, name='search_specialtopic'),
    url(r'^new_specialtopic/$', specialtopic.new_specialtopic, {"template_name": "specialtopic/new_specialtopic.html"},
        name="new_specialtopic"),
    url(r'^edit_specialtopic/$', specialtopic.edit_specialtopic,
        {"template_name": "specialtopic/edit_specialtopic.html"}, name="edit_specialtopic"),
    url(r'^delete_specialtopic/$', specialtopic.delete_specialtopic, name="delete_specialtopic"),
]

# 静态数据
urlpatterns += [
    url(r'^static_data/$', static_data.static_data, {"template_name": "static_data/static_data.html"},
        name="static_data"),
    url(r'^search_static_data/$', static_data.search_static_data, name='search_static_data'),
    url(r'^new_shop/$', static_data.new_shop, {"template_name": "static_data/new_shop.html"}, name="new_shop"),
    url(r'^edit_shop/$', static_data.edit_shop, {"template_name": "static_data/edit_shop.html"}, name="edit_shop"),
    url(r'^delete_shop/$', static_data.delete_shop, name="delete_shop"),
]

# 渠道关联和复制
urlpatterns += [
    url(r'^copy_associate/$', op_channel.copy_associate, {"template_name": "copy_associate.html"},
        name="copy_associate"),
    url(r'^channel_op/$', op_channel.channel_op, name="channel_op"),
]


# 审核中心
urlpatterns += [
    url(r'^check/$', check.check, {"template_name": "check/check.html"}, name="check"),
    url(r'^check_pass/$', check.check_pass, name="check_pass"),
    url(r'^check_reject/$', check.check_reject, name="check_reject"),
    url(r'^check_handle/$', check.check_handle, name="check_handle"),
    url(r'^check_history/$', check.check_history, name="check_history"),
    url(r'^check_history_detail/$', check.check_history_detail, name="check_history_detail"),
    url(r'^check_detail/$', check.check_detail, {"template_name": "check/detail.html"}, name="check_detail"),
    url(r'^check_detail_data/$', check.check_detail_data, name="check_detail_data"),
]

# 记录中心
urlpatterns += [
    url(r'^record/$', record.record, {"template_name": "record/record.html"}, name="record"),
    url(r'^record_submit/$', record.record_submit, name="record_submit"),
    url(r'^record_revert/$', record.record_revert, name="record_revert"),
    url(r'^record_handle/$', record.record_handle, name="record_handle"),
    url(r'^record_history/$', record.record_history, name="record_history"),
    url(r'^record_history_detail/$', record.record_history_detail, name="record_history_detail"),
    url(r'^record_detail/$', record.record_detail, {"template_name": "record/detail.html"}, name="record_detail"),
    url(r'^record_detail_data/$', record.record_detail_data, name="record_detail_data"),
]

# 分类接口
urlpatterns += [
    url(r'^count_first_category/$', interface_category.count_first_category, name="count_first_category"),
    url(r'^count_second_category/$', interface_category.count_second_category, name="count_second_category"),
    url(r'^get_category_info/$', interface_category.get_category_info, name="get_category_info"),
    url(r'^synch_goods/$', interface_category.synch_goods, name='synch_goods'),
    url(r'^synch_skus/$', synch_skus, name='synch_skus'),
    url(r'^synch_cpinfo/$', interface_cpinfo.synch_cpinfo, name='synch_cpinfo'),

]

# 品牌管理
urlpatterns += [
    # 品牌列表
    url(r'^cp_list/$', cp.cp_list, {"template_name": "cp/cps.html"}, name="cp_list"),
    # 编辑品牌
    url(r'^edit_cp/$', cp.edit_cp, {"template_name": "cp/edit_cp.html"}, name="edit_cp"),
    # 删除品牌
    url(r'^del_cp/$', cp.del_cp, name="del_cp"),
    # 新增品牌分类
    url(r'^new_cp_category/$', cp.new_cp_category, {"template_name": "cp/new_cp_category.html"},
        name="new_cp_category"),
    # 编辑品牌分类
    url(r'^edit_cp_category/$', cp.edit_cp_category, {"template_name": "cp/edit_cp_category.html"},
        name="edit_cp_category"),
    # 删除品牌分类
    url(r'^del_cp_category/$', cp.del_cp_category, name="del_cp_category"),

    url(r'^cp_category_list/$', cp.cp_category_list, {"template_name": "cp/cp_category.html"}, name="cp_category_list"),
    url(r'^search_cps/$', cp.search_cps, name="search_cps"),
    url(r'^exchange_sort_cp/$', cp.exchange_sort, name="exchange_sort_cp"),
    url(r'^search_cp_category/$', cp.search_cp_category, name="search_cp_category"),
]

# 常见问题
urlpatterns += [
    url(r'^problem/$', problem.problem, {"template_name": "problem/problem.html"}, name='problems'),
    url(r'^search_problem/$', problem.search_problem, name='search_problem'),
    url(r'^new_problem/$', problem.new, {"template_name": "problem/new_problem.html"}, name='new_problem'),
    url(r'^edit_problem/$', problem.edit, {"template_name": "problem/edit_problem.html"}, name='edit_problem'),
    url(r'^del_problem/$', problem.delelte, name='del_problem'),

]

#优惠券
urlpatterns+=[
    url(r'^coupons/$',coupons.coupons,{"template_name":"newcoupons/coupons.html"},name="coupons"),
    url(r'^search_coupons/$',coupons.search_coupons, name='search_coupons'),
    url(r'^new_coupons/$',coupons.new_coupons,{"template_name":"coupons/new_coupons.html"},name="new_coupons"),
    url(r'^edit_coupons/$',coupons.edit_coupons,{"template_name":"coupons/edit_coupons.html"},name="edit_coupons"),
    url(r'^delete_coupons/$',coupons.delete_coupons,name="delete_coupons"),
]


