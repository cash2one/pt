#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'putao'
__mtime__ = '2015/9/22'
"""
import time
from django.contrib.auth.decorators import login_required, permission_required
import json
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

from cms.settings import CMS_CHECK_ON
from common.base_cursor import BaseCursor
from common.const import AuthCodeName, CmsModule, MainConst, CheckOpType, CheckStatu, CATE_TYPE
# from .main_pub import *
# from main.forms import *
from common.views import get_check_status_str, search_key, get_table_paginator, filter_none, get_url_arg
from main.forms import CmsCategoryGroupForm, NaviCategoryForm
from main.models import CmsCheck, CmsNaviCategory, CmsCategoryGroup, CmsViewGroupCategory
from main.views.main_pub import add_main_var, format_form, get_city_group, get_city_list, get_scenes, \
    get_actions_select, \
    show_style_list, get_first_categories


@login_required
@add_main_var
def category(request, template_name):
    return render_to_response(template_name, context_instance=RequestContext(request))


@login_required
def search_categories(request):
    per_page = request.GET.get("per_page")
    if not per_page:
        per_page = MainConst.PER_PAGE
    cur_page = request.GET.get("cur_page")
    if not cur_page:
        cur_page = 1
    key = request.GET.get("key")
    categories = list(CmsNaviCategory.objects.filter(parent_id=0, fatherid=0))
    try:
        categories.sort(key=lambda o: (CmsCategoryGroup.objects.get(cmsviewgroupcategory__category=o).name))
    except:
        pass
    result = []
    temp = ""
    for category in categories:
        # used_by_op = "是" if category.used_by_op else "否"
        # show_style = get_show_style(category.show_style)
        status_str, status_int = get_check_status_str("CmsNaviCategory", category.id)
        try:
            group_name = CmsCategoryGroup.objects.get(cmsviewgroupcategory__category=category).name
            if temp != group_name:
                group = group_name
            else:
                group = ""
            temp = group_name
        except:
            group = ""
        if category.type == 0:
            category_type = "旧分类"
        else:
            category_type = "新分类"
        result.append([
            group,
            category.name,
            category.name_style,
            category.desc,
            category.desc_style,
            category.search_keyword,
            # used_by_op,
            # show_style,
            category_type,
            status_str,
            0,
            status_int,
            category.id
        ])
        children = CmsNaviCategory.objects.filter(parent_id=0, fatherid=category.id)
        for c in children:
            # used_by_op = "是" if c.used_by_op else "否"
            # show_style = get_show_style(category.show_style)
            status_str, status_int = get_check_status_str("CmsNaviCategory", c.id)
            result.append([
                "",
                c.name,
                c.name_style,
                c.desc,
                c.desc_style,
                c.search_keyword,
                # used_by_op,
                # show_style,
                "",
                status_str,
                1,
                status_int,
                c.id
            ])
    result = search_key(result, key, [2, 4, 8, 9, 10])
    result, num_pages = get_table_paginator(result, per_page, cur_page)
    filter_none(result)
    return HttpResponse(json.dumps([list(result), num_pages]))


@login_required
@add_main_var
def new_cate_group(request, template_name):
    if request.method == "POST":
        form = CmsCategoryGroupForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect(reverse('category'))
    else:
        form = CmsCategoryGroupForm()
    citygroups = get_city_group()
    cities = get_city_list()
    errors, fields = format_form(form)
    return render_to_response(template_name, {
        "errors": errors,
        "fields": fields,
        "citygroups": citygroups,
        "cities": cities
    }, context_instance=RequestContext(request))


@login_required
@add_main_var
def edit_cate_group(request, template_name):
    id = request.GET.get("id")
    ins_categroup = CmsCategoryGroup.objects.get(id=id)
    if request.method == "POST":
        form = CmsCategoryGroupForm(request.POST, instance=ins_categroup)
        if form.is_valid():
            return HttpResponseRedirect(reverse('category'))
    else:
        form = CmsCategoryGroupForm(instance=ins_categroup)
    errors, fields = format_form(form)
    citygroups = get_city_group()
    cities = get_city_list()
    return render_to_response(template_name, {
        "id": id,
        "errors": errors,
        "fields": fields,
        "citygroups": citygroups,
        "cities": cities
    }, context_instance=RequestContext(request))


@login_required
@permission_required(u'%s.%s' % (AuthCodeName.APP_LABEL, AuthCodeName.CONFIG), raise_exception=True)
@add_main_var
def new_category_first(request, template_name):
    if request.method == "POST":
        form = NaviCategoryForm(request.POST)
        if form.is_valid():
            category = form.save()
            cate_group_id = request.POST.get("cate_group_id")
            CmsViewGroupCategory(group_id=cate_group_id, category=category).save()
            if CMS_CHECK_ON:
                CmsCheck(module=CmsModule.MAIN_CATEGORY,
                         table_name='CmsNaviCategory',
                         data_id=category.id,
                         op_type=CheckOpType.NEW,
                         alter_person=request.user.username,
                         alter_date=time.strftime("%Y-%m-%d %X", time.localtime())).save()
            return HttpResponseRedirect(reverse('category'))
    else:
        form = NaviCategoryForm()
    errors, fields = format_form(form)
    scenes = get_scenes()
    actions = get_actions_select()
    citygroups = get_city_group()
    cities = get_city_list()
    cate_groups = CmsCategoryGroup.objects.all()
    return render_to_response(template_name, {
        "cate_groups": cate_groups,
        "scenes": scenes,
        "actions": actions,
        "citygroups": citygroups,
        "show_style_list": show_style_list,
        "cities": cities,
        "fields": fields,
        "errors": errors,
        "CATE_TYPE": CATE_TYPE
    }, context_instance=RequestContext(request))


@login_required
@permission_required(u'%s.%s' % (AuthCodeName.APP_LABEL, AuthCodeName.CONFIG), raise_exception=True)
@add_main_var
def edit_category_first(request, template_name):
    id = request.GET.get("id")
    category = CmsNaviCategory.objects.get(id=id)
    if request.method == "POST":
        form = NaviCategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            cate_group_id = request.POST.get("cate_group_id")
            if CmsViewGroupCategory.objects.filter(category=category):
                ins_viewgroupcate = CmsViewGroupCategory.objects.get(category=category)
                ins_viewgroupcate.group_id = cate_group_id
                ins_viewgroupcate.save()
            else:
                CmsViewGroupCategory(category=category, group_id=cate_group_id).save()
            if CMS_CHECK_ON:
                CmsCheck(module=CmsModule.MAIN_CATEGORY,
                         table_name='CmsNaviCategory',
                         data_id=id,
                         op_type=CheckOpType.EDIT,
                         alter_person=request.user.username,
                         alter_date=time.strftime("%Y-%m-%d %X", time.localtime())).save()
            return HttpResponseRedirect(reverse('category'))
    else:

        form = NaviCategoryForm(instance=category)
    errors, fields = format_form(form)
    if CmsViewGroupCategory.objects.filter(category=category):
        ins_viewgroupcate = CmsViewGroupCategory.objects.get(category=category)
        fields["cate_group_id"] = json.dumps(ins_viewgroupcate.group_id)
    scenes = get_scenes()
    actions = get_actions_select()
    citygroups = get_city_group()
    cities = get_city_list()
    cate_groups = CmsCategoryGroup.objects.all()
    return render_to_response(template_name, {
        "scenes": scenes,
        "actions": actions,
        "citygroups": citygroups,
        "cities": cities,
        "show_style_list": show_style_list,
        "id": id,
        "fields": fields,
        "errors": errors,
        "cate_groups": cate_groups,
        "CATE_TYPE": CATE_TYPE
    }, context_instance=RequestContext(request))


@login_required
@permission_required(u'%s.%s' % (AuthCodeName.APP_LABEL, AuthCodeName.CONFIG), raise_exception=True)
def del_category(request):
    id = request.POST.get("id")
    # 删除二级分类
    children = CmsNaviCategory.objects.filter(parent_id=0, fatherid=id)
    if CMS_CHECK_ON:
        for child in children:
            check = CmsCheck(
                module=CmsModule.MAIN_CATEGORY,
                table_name="CmsNaviCategory",
                data_id=child.id,
                op_type=CheckOpType.DELETE,
                status=CheckStatu.WAIT_SUBMIT,
                is_show=0,
                alter_person=request.user.username,
                alter_date=time.strftime("%Y-%m-%d %X", time.localtime()))
            check.save()
    children.delete()
    # 删除一级分类
    parent = CmsNaviCategory.objects.filter(id=id)
    if CMS_CHECK_ON:
        check = CmsCheck(
            module=CmsModule.MAIN_CATEGORY,
            table_name="CmsNaviCategory",
            data_id=id,
            op_type=CheckOpType.DELETE,
            status=CheckStatu.WAIT_SUBMIT,
            is_show=1,
            alter_person=request.user.username,
            alter_date=time.strftime("%Y-%m-%d %X", time.localtime()))
        check.save()
    parent.delete()
    return HttpResponse(0)


@login_required
@permission_required(u'%s.%s' % (AuthCodeName.APP_LABEL, AuthCodeName.CONFIG), raise_exception=True)
@add_main_var
def new_category_second(request, template_name):
    if request.method == "POST":
        form = NaviCategoryForm(request.POST)
        if form.is_valid():
            category = form.save()
            if CMS_CHECK_ON:
                CmsCheck(module=CmsModule.MAIN_CATEGORY,
                         table_name='CmsNaviCategory',
                         data_id=category.id,
                         op_type=CheckOpType.NEW,
                         alter_person=request.user.username,
                         alter_date=time.strftime("%Y-%m-%d %X", time.localtime())).save()
            return HttpResponseRedirect(reverse('category'))
    else:
        form = NaviCategoryForm()
    errors, fields = format_form(form)
    scenes = get_scenes()
    actions = get_actions_select()
    citygroups = get_city_group()
    cities = get_city_list()
    cate2s = get_first_categories()
    # first_categories = get_first_categories()
    return render_to_response(template_name, {
        "scenes": scenes,
        "actions": actions,
        "citygroups": citygroups,
        "show_style_list": show_style_list,
        "cities": cities,
        "cate2s": cate2s,
        # "first_categories":first_categories,
        "fields": fields,
        "errors": errors
    }, context_instance=RequestContext(request))


@login_required
@permission_required(u'%s.%s' % (AuthCodeName.APP_LABEL, AuthCodeName.CONFIG), raise_exception=True)
@add_main_var
def edit_category_second(request, template_name):
    id = request.GET.get("id")
    if request.method == "POST":
        goods = CmsNaviCategory.objects.get(id=id)
        form = NaviCategoryForm(request.POST, instance=goods)
        if form.is_valid():
            form.save()
            if CMS_CHECK_ON:
                CmsCheck(module=CmsModule.MAIN_CATEGORY,
                         table_name='CmsNaviCategory',
                         data_id=id,
                         op_type=CheckOpType.EDIT,
                         alter_person=request.user.username,
                         alter_date=time.strftime("%Y-%m-%d %X", time.localtime())).save()
            return HttpResponseRedirect(reverse('category'))
    else:
        navicategory = CmsNaviCategory.objects.get(id=id)
        form = NaviCategoryForm(instance=navicategory)
    errors, fields = format_form(form)
    scenes = get_scenes()
    actions = get_actions_select()
    citygroups = get_city_group()
    cities = get_city_list()
    cate2s = get_first_categories()
    return render_to_response(template_name, {
        "scenes": scenes,
        "actions": actions,
        "goods_form": form,
        "citygroups": citygroups,
        "show_style_list": show_style_list,
        "cities": cities,
        "id": id,
        "fields": fields,
        "errors": errors,
        "cate2s": cate2s,
        # "first_categories":first_categories
    }, context_instance=RequestContext(request))


def search_second_category(request):
    page = get_url_arg(request, 'page', int, 1)
    per_page = get_url_arg(request, 'per_page', int, 15)
    search_key = get_url_arg(request, 'search_key', str, None)
    total_page, actions = _slice_category_select(search_key, page=page, per_page=per_page)
    result = {'total_page': total_page, 'cur_page': page, "actions": actions}
    json_str = json.dumps(result)

    return HttpResponse(json_str)


def _slice_category_select(key, page=1, per_page=10):
    if key and len(key) > 0:
        categories = r"select `id`,`name` from `cms_navi_category` where `parent_id` =0 and `fatherId`=0 and `type`<>0 and id not in (select category_id from cms_category_index) and (`id` like '%{0}%' or `name` like '%{0}%')".format(
            key)
    else:
        categories = r"select `id`,`name` from `cms_navi_category` where `parent_id` =0 and `fatherId`=0 and `type`<>0 and id not in (select category_id from cms_category_index)"
    total_page, result = BaseCursor.get_pageinate(page, per_page, categories)
    return total_page, result
