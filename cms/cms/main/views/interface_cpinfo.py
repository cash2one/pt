# coding: utf-8
# from .main_pub import *
# from main.forms import *

import logging

import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from main.models import CmsCP, CmsCpinfo

log = logging.getLogger('django')


# 同步cp信息（开放平台）
@csrf_exempt
def synch_cpinfo(request):
    """
    :请求地址:http://192.168.1.153:8000/main/synch_cpinfo/
    :请求方式：DELETE: 参数id 接在请求url后面
              :POST :参数id,name,icon
    """
    log.info('synch cpinfo........')
    result = {}
    try:
        if request.method == "GET":
            return HttpResponse(0)
        if request.method == "DELETE":
            id = request.GET.get("id")
            log.info('delete from id=:' + id)
            try:
                CmsCP.objects.get(id=id).delete()
            except:
                pass

            try:
                CmsCpinfo.objects.get(id=id).delete()
            except:
                pass
        if request.method == "PUT" or request.method == "POST":
            id = request.POST.get('id')
            name = request.POST.get("name")
            icon = request.POST.get("icon")
            adver_icon = request.POST.get("adver_icon")
            desc = request.POST.get("desc")
            company_name = request.POST.get("company_name")

            try:
                obj, status = CmsCP.objects.get_or_create(id=id)
                obj.name = name
                obj.icon = icon
                obj.adver_icon = adver_icon
                obj.desc = desc
                obj.company_name = company_name
                obj.save()
            except:
                pass

            try:
                obj, status = CmsCpinfo.objects.get_or_create(id=id)
                obj.name = name
                obj.icon = icon
                obj.save()
            except:
                pass
            result['ret_code'] = 0
    except Exception as ex:
        log.error(ex)
        result['ret_code'] = -1
        result['errors'] = ex.args[0]
    return HttpResponse(json.dumps(result))
