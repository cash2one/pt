from django.conf.urls import include, url
from django.contrib import admin
from main.views.modify_pwd import modify_pwd

urlpatterns = [
    # Examples:
    # url(r'^$', 'pt_shelves.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^modify_pwd/$', 'main.views.modify_pwd.modify_pwd', {"template_name": "modify_pwd.html"}, name='modify_pwd'),

]
