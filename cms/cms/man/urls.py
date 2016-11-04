from django.conf.urls import include, url
from django.contrib import admin
import man

urlpatterns = [
    url(r'^man/$', man.man, {"template_name": "man/man.html"}, name="man"),
    url(r'^delete_operators/$', man.delete_operators, name="delete_operators"),
    url(r'^delete_staffs/$', man.delete_staffs, name="delete_staffs"),
    url(r'^new_staff/', man.new_staff, name='new_staff'),
    url(r'^new_operator/', man.new_operator, name='new_operator'),
    url(r'^edit_staff/', man.edit_staff, name='edit_staff'),
    url(r'^edit_operator/', man.edit_operator, name='edit_operator'),
]
