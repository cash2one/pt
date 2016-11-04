#coding: utf-8

from django.conf.urls import patterns, url

"""
    man应用所有的url
"""

urlpatterns = patterns('man.views.group_list',
    url(r'^$', 'redirect_per_list', {"template_name": "group_list.html"}, name='man_index'),
    url(r'^group_list/$', 'group_list', {"template_name": "group_list.html"}, name='group_list'),
    url(r'^group_list_ajax/$', 'group_list_ajax', name='group_list_ajax'),
    url(r'^edit_group/$', 'edit_group', {"template_name": "edit_group.html"}, name='edit_group'),
    url(r'^del_group/$', 'del_group', name='del_group'),
    url(r'^view_group/$', 'view_group', {"template_name": "view_group.html"}, name='view_group'),
)

urlpatterns += patterns('man.views.add_group',
    url(r'^add_group/$', 'add_group', {"template_name": "add_group.html"}, name='add_group'),
)

urlpatterns += patterns('man.views.user_list',
    url(r'^user_list/$', 'user_list', {"template_name": "user_list.html"}, name='user_list'),
    url(r'^user_list_ajax/$', 'user_list_ajax', name='user_list_ajax'),
    url(r'^edit_user/$', 'edit_user', {"template_name": "edit_user.html"}, name='edit_user'),
    url(r'^redirect_edit_user/$', 'redirect_edit_user', {"template_name": "group_list.html"}, name='redirect_edit_user'),
    url(r'^del_user/$', 'del_user', name='del_user'),
    url(r'^view_user/$', 'view_user', {"template_name": "view_user.html"}, name='view_user'),
)

urlpatterns += patterns('man.views.add_user',
    url(r'^add_user/$', 'add_user', {"template_name": "add_user.html"}, name='add_user'),
    url(r'^change_group/$', 'change_group', name='change_group'),
)

urlpatterns += patterns('man.views.modify_user',
    url(r'^modify_pwd/$', 'modify_pwd', {"template_name": "modify_pwd.html"}, name='modify_pwd'),
)
urlpatterns += patterns('man.views.modules_group',
    url(r'^modules_group/$', 'modules_group', {"template_name": "modules_group.html"}, name='modules_group'),
    url(r'^modules_group_select/$', 'modules_group_select', name='modules_group_select'),
    url(r'^modules_edit/$', 'modules_edit', name='modules_edit'),
    url(r'^modules_detail/(?P<pk>[0-9]+)$', 'modules_detail', name='modules_detail'),
    url(r'^modules_group_detail/(?P<pk>[0-9]+)$', 'modules_group_detail', name='modules_group_detail'),
    url(r'^modules_list/$', 'modules_list', {"template_name": "modules_list.html"}, name='modules_list'),
)