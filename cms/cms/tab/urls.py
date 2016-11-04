# -*- coding: utf-8 -*-
# Author:songroger
# Aug.13.2016
from django.conf.urls import url

from tab import api

urlpatterns = [

    url(r'^tab/list/$', api.tab_list, name='tab_list'),
    url(r'^tab/$', api.tab, name='tab'),
    url(r'^actions/list/$', api.actions_list, name='actions_list'),

]
