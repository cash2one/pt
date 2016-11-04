#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'putao'
__mtime__ = '2015/8/26'
"""
from django.contrib.auth.decorators import login_required, permission_required
import json
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.http import require_POST

from cms.settings import CMS_CHECK_ON
from common.const import AuthCodeName, CmsModule, CheckOpType
# from .main_pub import *
from common.views import check_submitted_results
from common.views import get_table_paginator
from main.models import CmsImageInfo, CmsCheck
from main.views.main_pub import add_main_var


@login_required
@add_main_var
def images(request, template_name):
    return render_to_response(template_name, context_instance=RequestContext(request))


# 上传图片和查询展示
@login_required
@permission_required(u'%s.%s' % (AuthCodeName.APP_LABEL, AuthCodeName.CONFIG), raise_exception=True)
@add_main_var
@require_POST
# 图片新增
# 请求地址："{% url 'new_image' %}"
# 请求方式：post
# 请求参数 image_list: 格式是：[{'image_name':'value','image_category':'value','image_url':'value'},{}]
def new_image(request, template_name):
    if request.method == 'POST':
        postdata = request.POST.copy()
        try:
            oCmsImageInfos = CmsImageInfo.objects.get_or_create(image_name=postdata['image_name'])
            oCmsImageInfo = oCmsImageInfos[0]
            oCmsImageInfo.image_url = postdata['image_url']
            oCmsImageInfo.image_category = postdata['image_category']
            oCmsImageInfo.save()
            # oCmsImageInfo.save(using="online")
            if CMS_CHECK_ON:
                CmsCheck(module=CmsModule.MAIN_IMAGE,
                         table_name='CmsImageInfo',
                         data_id=oCmsImageInfo.id,
                         op_type=CheckOpType.NEW if oCmsImageInfos[1] else CheckOpType.EDIT).save()
        except Exception as ex:
            print(ex)
        return HttpResponseRedirect(reverse('images'))
    else:
        return render_to_response(template_name)


# 图片搜索
# 版本1
# @login_required
# @add_main_var
# def search_image(request,template_name):
#     data = request.GET.copy()
#     if data['image_name']=='':
#         search_datas = CmsImageInfo.objects.all(image_category=data['image_category'])
#     else:
#         search_datas = CmsImageInfo.objects.filter(image_name__contains=data['image_name'],image_category=data['image_category'])
#     totalnum =int(math.ceil(len(search_datas)/float(data['show_num'])))
#     page_data = search_datas[data['show_num']*(data['page_no']-1):data['show_num']*data['page_no']]
#     c ={"totalnum":totalnum,'page_data':page_data}
#     return render_to_response(template_name,c,context_instance=RequestContext(request))

# 图片搜索和分类查看
# 地址："{% url 'get_images' %}"
# 请求方式：GET
# 请求参数: per_page，cur_page，image_category,key（默认是空）
# 版本2


@login_required
def search_image(request):
    per_page = request.GET.get("per_page", 36)
    cur_page = request.GET.get("cur_page", 1)
    key = request.GET.get("key")
    image_category = request.GET.get('image_category')
    search_datas = CmsImageInfo.objects.filter(image_category=image_category, image_name__contains=key).values_list(
        'image_name', 'image_category', 'image_url', 'id')
    images = check_submitted_results('CmsImageInfo', search_datas, -1)
    result, num_pages = get_table_paginator(images, per_page, cur_page)
    # return HttpResponse(json.dumps([list(result), num_pages]))
    c = json.dumps([list(result), num_pages])
    return HttpResponse(c)


# 分类查看
# @login_required
# @add_main_var
# def category_image(request,template_name):
#     categoryname = request.GET.get('image_category')
#     show_num = request.GET.get('show_num')
#     show_datas = CmsImageInfo.objects.filter(image_category=categoryname)
#
#     totalnum =int(math.ceil(len(show_datas)/float(show_num)))
#     c ={"totalnum":totalnum,'page_data':show_datas}
#     return render_to_response(template_name,c,context_instance=RequestContext(request))


# 图片删除
# 请求地址："{% url 'del_image' %}"
# 请求方式：POST
# 请求参数 列表del_list:格式为['image_url1','image_url2']
@login_required
@permission_required(u'%s.%s' % (AuthCodeName.APP_LABEL, AuthCodeName.CONFIG), raise_exception=True)
@require_POST
def del_image(request):
    data = request.POST.copy()
    delete_list = data.getlist("del_list[]")
    for image_url in delete_list:
        delete_image_obj = CmsImageInfo.objects.get(image_url=image_url)
        if CMS_CHECK_ON:
            CmsCheck(module=CmsModule.MAIN_IMAGE,
                     table_name='CmsImageInfo',
                     data_id=delete_image_obj.id,
                     op_type=CheckOpType.DELETE).save()
        delete_image_obj.delete()
    return HttpResponse(0)
