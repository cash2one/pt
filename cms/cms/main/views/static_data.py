#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = "静态数据"
__author__ = "rfd"
__mtime__ = "2015/8/28"
"""
from common.const import AuthCodeName, CmsModule, MainConst
# from .main_pub import *
# from config.views.config_pub import open_type
# from main.forms import *
import time
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required, permission_required
import json
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

from common.const import AuthCodeName, CmsModule, CheckOpType, \
    CheckStatu
from common.views import get_check_status_str, analyze_shop_content, get_table_paginator, search_key
from config.views.config_pub import CMS_CHECK_ON, CmsCheck
from main.forms import CmsCategoryItembeanForm
from main.models import CmsCategoryItembean

from main.views.main_pub import add_main_var, get_city_list, get_city_group, format_form


#静态数据列表
@login_required
@add_main_var
def static_data(request, template_name):
    return render_to_response(template_name, context_instance=RequestContext(request))


#列表（搜索，分页查看），返回总页码和对象列表
@login_required
def search_static_data(request):
    per_page = request.GET.get("per_page")
    if not per_page:
        per_page = MainConst.PER_PAGE
    cur_page = request.GET.get("cur_page")
    if not cur_page:
        cur_page = 1
    objs = CmsCategoryItembean.objects.filter(parent_id=-1)
    shops = []
    for obj in objs:
        photoUrl, photo_str, search_show, s_key, search_category, home, weibo = analyze_shop_content(obj)
        status_str, status_int = get_check_status_str("CmsCategoryItembean", obj.id)
        shops.append([
            photoUrl,
            obj.name,
            photo_str,
            search_show,
            s_key,
            search_category,
            home,
            weibo,
            status_str,
            status_int,
            obj.id
        ])
    key = request.GET.get("key")
    shops = search_key(shops, key, [0, 9, 10])
    result,num_pages = get_table_paginator(shops,per_page,cur_page)
    return HttpResponse(json.dumps([list(result),num_pages]))


#新增商家
@login_required
@permission_required(u'%s.%s' % (AuthCodeName.APP_LABEL,AuthCodeName.CONFIG), raise_exception=True)
@add_main_var
def new_shop(request,template_name):
    """
    新建商户
    url :{% url "new_shop" %}
    :请求方式: Get
    :请求参数：无
    :返回数据： citygroups 城市分组列表，cities 所有城市(列表)
    :[[id,name],[id,name],....]

    :请求方式：Post
    :请求参数：cms_category_itembean字段(input name)
    webSite: #官方主页
    weibo :  #微博主页
    search_key :     搜索词
    search_category：搜索分类
    search_show ：查看附近
    numbers : 电话号码
    格式：
    [{
		"number": "4008111111", #电话号码
		"number_description": "顺丰速运"    #电话描述
	},多个..........]
    """
    if request.method == "POST":
        postcopys = request.POST.copy()
        content = op_content_save(postcopys)
        postcopys["content"] = json.dumps(content,ensure_ascii=False)
        form = CmsCategoryItembeanForm(postcopys)
        if form.is_valid():
            ocategoryitembean = form.save()
            if CMS_CHECK_ON:
                CmsCheck(module=CmsModule.MAIN_SHOP,
                         table_name='CmsCategoryItembean',
                         data_id=ocategoryitembean.id,
                         op_type=CheckOpType.NEW,
                         alter_person=request.user.username,
                         alter_date=time.strftime("%Y-%m-%d %X",time.localtime())).save()
            return HttpResponseRedirect(reverse("static_data"))
    else:
        form = CmsCategoryItembeanForm()
    errors,fields = format_form(form)
    fields = op_content_edit(fields)
    citygroups = get_city_group()
    cities = get_city_list()
    return render_to_response(template_name,{
        "fields": fields,
        "errors":errors,
        "citygroups":citygroups,
        "cities":cities,
    }, context_instance=RequestContext(request))

def op_content_save(postcopys):
    content={
    "webSite": "",    #官方主页
    "weibo": "",    #微博主页
    "name": "", #名称
    "photoUrl": "",  #待确认，跟icon字段的关系
    "search_info": [{
        "search_key": "",   #搜索关键词
        "search_category": "",  #搜索分类
        "search_show": ""   #查看附近
    }],
    "dataSource": "葡萄", #写死的
    "numbers": [{
        "number": "", #电话号码
        "number_description": ""    #电话描述
    }]}
    if postcopys["content"] and isinstance(json.loads(postcopys["content"]),dict):
        content.update(json.loads(postcopys["content"]))
    content["webSite"]=postcopys["webSite"]
    content["weibo"] =postcopys["weibo"]
    content["name"] = postcopys["name"]
    content["photoUrl"]=postcopys["icon"]
    content["search_info"][0]["search_key"]=postcopys["search_key"]
    content["search_info"][0]["search_category"] = postcopys["search_category"]
    content["search_info"][0]["search_show"] = postcopys["search_show"]
    content["numbers"] = json.loads(postcopys["numbers"])
    return content

def op_content_edit(fields):
    if not ('content' in fields and fields['content']):
        return fields
    fields['content'] = json.loads(fields['content'])
    del_keys=["webSite","weibo","name","photoUrl","search_info","dataSource","numbers"]
    if fields['content'] and isinstance(json.loads(fields['content']),dict):
        content = json.loads(fields['content'])
        if 'photoUrl' in content.keys():
            fields['icon'] = json.dumps(content['photoUrl'])
        for key1 in content:
            if key1 =="search_info":
                search_info = content[key1]
                if len(search_info)>0:
                    search_info1=search_info[0]
                    for key2 in search_info1:
                        fields[key2] = json.dumps(search_info1[key2])
            else:
                fields[key1]=json.dumps(content[key1])
        for key in del_keys:
            if key in content.keys():
                del content[key]
        if not content:
            content=""
            fields['content'] = json.dumps(content)
        else:
            fields['content'] = json.dumps(json.dumps(content))

    return fields

#编辑商家
@login_required
@permission_required(u'%s.%s' % (AuthCodeName.APP_LABEL,AuthCodeName.CONFIG), raise_exception=True)
@add_main_var
def edit_shop(request, template_name):
    """
    编辑商户
    url :{% url "edit_shop" %}?id={{ id }}
    :请求方式: Get
    :请求参数：无
    :返回数据： citygroups 城市分组列表，cities 所有城市(列表)
    :[[id,name],[id,name],....]

    :请求方式：Post
    :请求参数：cms_category_itembean字段(input name)
    """
    id = request.GET.get("id")
    categoryitembean = CmsCategoryItembean.objects.get(id=id)
    if request.method == "POST":
        postcopys = request.POST.copy()
        content = op_content_save(postcopys)
        postcopys["content"] = json.dumps(content,ensure_ascii=False)
        form = CmsCategoryItembeanForm(postcopys,instance=categoryitembean)
        if form.is_valid():
            form.save()
            if CMS_CHECK_ON:
                CmsCheck(module=CmsModule.MAIN_SHOP,
                         table_name='CmsCategoryItembean',
                         data_id=id,
                         op_type=CheckOpType.EDIT,
                         alter_person=request.user.username,
                         alter_date=time.strftime("%Y-%m-%d %X",time.localtime())).save()
            return HttpResponseRedirect(reverse("static_data"))
    else:
        form = CmsCategoryItembeanForm(instance=categoryitembean)
    errors,fields = format_form(form)
    fields = op_content_edit(fields)
    citygroups = get_city_group()
    cities = get_city_list()
    return render_to_response(template_name,{
        "fields": fields,
        "errors":errors,
        "citygroups":citygroups,
        "cities":cities,
        "id":id,
    }, context_instance=RequestContext(request))


#删除商家
@login_required
@permission_required(u'%s.%s' % (AuthCodeName.APP_LABEL,AuthCodeName.CONFIG), raise_exception=True)
def delete_shop(request):
    id = request.POST.get("id")
    CmsCategoryItembean.objects.get(id=id).delete()
    if CMS_CHECK_ON:
        check = CmsCheck(
            module=CmsModule.MAIN_SHOP,
            table_name="CmsCategoryItembean",
            data_id=id,
            op_type=CheckOpType.DELETE,
            status=CheckStatu.WAIT_SUBMIT,
            is_show=1,
            alter_person=request.user.username,
            alter_date=time.strftime("%Y-%m-%d %X",time.localtime()))
        check.save()
    return HttpResponse(0)