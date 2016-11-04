# -*- coding: utf-8 -*-
# Author:songroger
# Jul.28.2016
from __future__ import unicode_literals
from django.contrib import admin
from tags.models import Groups, Tags


class GroupsAdmin(admin.ModelAdmin):

    list_display = ('id', 'tag_group_name')
    # raw_id_fields = ('user',)
    search_fields = ('tag_group_name',)
    list_per_page = 10
    # list_filter = ('state', )
admin.site.register(Groups, GroupsAdmin)


class TagsAdmin(admin.ModelAdmin):

    list_display = ('id', 'name')
    # raw_id_fields = ('user',)
    search_fields = ('name',)
    list_per_page = 10
    # list_filter = ('state', )
admin.site.register(Tags, TagsAdmin)
