from django.conf.urls import include, url
from django.contrib.auth.views import  logout_then_login
from common.mylogin import login
from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    # Examples:
    # url(r'^$', 'pt_shelves.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^accounts/login/$', login, name='login'),
    url(r'^accounts/logout_then_login/$', logout_then_login, name='logout_then_login'),
    url(r'^$', 'main.views.index.shelves_index', {'template_name': 'wxh.html'}, name='shelves_index'),
]
urlpatterns += [
    url(r'^phone_fee/', include('phone_fee.urls')),
    url(r'^flow/', include('flow.urls')),
    url(r'^main/', include('main.urls')),
    url(r'^wallet/', include('wallet.urls')),
    url(r'^pt_card/', include('pt_card.urls')),
]
