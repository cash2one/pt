# -*- coding: utf-8 -*-
# Author:songroger
# Mar.5.2016
from celery import task

from phone_fee.views.phone_fee_pub import updown_shelves, updown_shelves_app


@task()
def add(x, y):
    return x + y

# 上架
@task()
def fee_updown_shelves_timing(app, goods, is_updown, str_time, end_time, updown_status):
    updown_shelves(app, goods, '1', is_updown,start_time=str_time,end_time=end_time,updown_status=updown_status)
    return

# 上下架指定app
@task()
def fee_updown_shelves_timing_app(app, goods, is_updown,str_time,end_time,updown_status):
    updown_shelves_app(app, goods, is_updown, str_time, end_time, updown_status)
    return
