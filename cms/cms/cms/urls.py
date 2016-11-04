# coding: utf-8
"""cms URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url, patterns
from django.contrib import admin
from django.contrib.auth.views import  logout_then_login
from common.mylogin import login
from main.views import tools, show_relate

from django.conf import settings


urlpatterns = [
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/login/$',
        login, {"template_name": "login.html"}, name="login"),
    url(r'^%saccounts/logout_then_login/$' %
        settings.CMS_URL_ROOT, logout_then_login, name='logout_then_login'),
]

# 只用django，DEBUG = False正式发布的版本需要增加这项
if settings.DEBUG is False:
    urlpatterns += patterns('', url(r'^%sstatic/(?P<path>.*)$'
                                    % settings.CMS_URL_ROOT,
                                    'django.views.static.serve',
                                    {'document_root': settings.STATIC_ROOT, }))

urlpatterns += [
    url(r'^%s$' % settings.CMS_URL_ROOT, 'main.views.index.index',
        {"template_name": "wxh.html"}, name='main_index'),
    url(r'^%smain/' % settings.CMS_URL_ROOT, include('main.urls')),
    url(r'^%sconfig/' % settings.CMS_URL_ROOT, include('config.urls')),
    url(r'', include('activity.urls')),
    url(r'', include('urls.urls')),
    url(r'', include('tags.urls')),
    url(r'', include('tab.urls')),
    url(r'', include('ads.urls')),
    url(r'', include('man.urls')),

]

urlpatterns += [
    url(r'^%sshow_relate$' % settings.CMS_URL_ROOT, show_relate.show_relate, {
        "template_name": "show_relate.html"}, name="show_relate"),
]

# if 1:
urlpatterns += [
    url(r'^%screate_scenes/$' % settings.CMS_URL_ROOT, tools.create_scenes),
    # url(r'^create_city/$',tools.create_city),
    url(r'^%screate_permissions/$' %
        settings.CMS_URL_ROOT, tools.create_permissions),
    url(r'^%smodify_actionjson/$' %
        settings.CMS_URL_ROOT, tools.modify_actionjson),
]

if settings.DEBUG:
    try:
        import debug_toolbar
        urlpatterns += [
            url(r'^debug/', include(debug_toolbar.urls)),
        ]
    except ImportError:
        pass
