# -*- coding: utf-8 -*-
# Author:songroger
# Jun.24.2016
from celery import task


@task()
def add(x, y):
    return x + y
