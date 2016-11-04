# -*- coding: utf-8 -*-
# Author:songroger
# Jul.26.2016
# Python module render a page for frontend
# to allow html templates in Python to be added

from django.conf.urls import url
from .view import url_test, render_page

# render_page() is a view function to help render
# different pages. It allowed different parameters to render different pages.
# The differences are showed below.
# render_page 可传uptoken参数， True时模板中可返回上传七牛图片的token，
# 页面中可用{{ token }}获得. 默认为False.
# 可传channel参数, 如果为True, 要求url中传t(app_version_type_id),
# v(app_version), c(channel_no)参数，模板中返回channel_id. 用{{ channel }}获取.
# 默认为False.


urlpatterns = [

    # url(r'^url/test/$', url_test,
    #     {"template_name": "newcoupons/coupons.html"}, name='open'),
    url(r'^render/page1/$', render_page,
        {"template_name": "newcoupons/coupons.html", "channel": True,
         "uptoken": True}, name='test1'),


    # 标签组&标签
    url(r'^tags/$', render_page,
        {"template_name": "tags/wxh.html", "uptoken": True}, name='tags'),

    url(r'^main/tag_quick_order/$', render_page,
        {"template_name": "quick_order/quick_tag.html"}, name='quick_tag'),

    # tab配置选项
    url(r'^main/tab/config/$', render_page,
        {"template_name": "tab/wxh.html", "channel": True}, name='tab_config'),

    # ads配置选项
    url(r'^main/ads/config/$', render_page,
        {"template_name": "cover_ads/wxh.html", "channel": True, "city": True}, name='cover_ads_config'),
]
