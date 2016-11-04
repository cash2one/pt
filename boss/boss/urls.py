#coding: utf-8

from django.conf.urls import patterns, include, url
from django.contrib.auth.views import logout_then_login, logout
from common.mylogin import login
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'boss.views.home', name='home'),
    # url(r'^boss/', include('boss.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),


    # Uncomment the next line to enable the admin:
    #url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/login/$', login, name="login"),
    url(r'^accounts/logout_then_login/$', logout_then_login, name='logout_then_login'),
)

#只用django，DEBUG = False正式发布的版本需要增加这项
if settings.DEBUG is False:
    urlpatterns += patterns('', url(r'^static/(?P<path>.*)$', 'django.views.static.serve', { 'document_root': settings.STATIC_ROOT,}))

#from django.views.generic.simple import direct_to_template
#urlpatterns += patterns('', (r'^about/$', direct_to_template, {'template': '404.html'}))

urlpatterns += patterns('',
    # url(r'^$', 'main.views.index.index', {"template_name": "wxh.html"}, name='index'),
    url(r'^$', 'report.views.index.report_index', {"template_name": "report_index.html"}, name='report_index'),
    (r'^user/', include('main.urls')),
    (r'^report/', include('report.urls')),
    (r'^man/', include('man.urls')),
    (r'^finance/', include('finance.urls')),
    (r'^order/', include('order.urls')),
    (r'^message/', include('message.urls')),
)

if 1:
    urlpatterns += patterns('main.views.tool',
        (r'^create_permission/', 'create_permission'),
        (r'^reset_pwd/', 'reset_pwd')
    )