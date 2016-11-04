#coding: utf-8
#from django.conf.urls import *
from django.conf.urls import url
from server.views.shengchan_111 import index

"""
    blog应用所有的url

"""

urlpatterns = [
    url(r'^$',index, {"template_name": "test.html"}, name='test'),
]
