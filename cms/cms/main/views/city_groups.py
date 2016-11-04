# coding: utf-8

"""
    城市分组
"""
import json
from django.core.urlresolvers import reverse
from django.views.decorators.http import require_GET
from common.const import MainConst
# from .main_pub import *
# from main.forms import *
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from common.const import AuthCodeName
from common.views import filter_none, get_table_paginator, get_check_status_str, search_key
from main.forms import CityGroupForm
from main.models import PtCityCityGroups, PtYellowCitylist, PtCityGroup
from main.views.main_pub import add_main_var, get_city_list, format_form


# 返回城市列表数据
def get_cities(request):
    citylist = get_city_list()
    return HttpResponse(json.dumps(citylist))


# 根据城市分组获取城市列表   传入数据：   city_group_id （城市分组id）    get请求地址 /main/get_city_from_group_id  我返回给你的数据为： city_list （是个城市名称的列表）。
@login_required
@require_GET
def get_city_from_group_id(request):
    city_group_id = request.GET.get('group_id')
    city_list = []
    if city_group_id:
        ptcitycitygroups = PtCityCityGroups.objects.filter(group=city_group_id)
        for ptcitycitygroup in ptcitycitygroups:
            cityname = PtYellowCitylist.objects.get(self_id=ptcitycitygroup.city_id).city_name
            if len(cityname) > 2 and cityname[-1] in ["市", "县"]:
                cityname = cityname[:-1]
            city_list.append(cityname)
    return HttpResponse(json.dumps(city_list))


# 新建城市分组
@login_required
@permission_required(u'%s.%s' % (AuthCodeName.APP_LABEL, AuthCodeName.CONFIG), raise_exception=True)
@add_main_var
def new_city_group(request, template_name):
    if request.method == "POST":
        form = CityGroupForm(request.POST)
        if form.is_valid():
            oCityGroup = form.save()
            # CmsCheck(module=CmsModule.MAIN_CITYGROUP,
            #          table_name='PtCityGroup',
            #          data_id=oCityGroup.id,
            #          op_type=CheckOpType.NEW,
            #          alter_person=request.user.username,
            #          alter_date=time.strftime("%Y-%m-%d %X",time.localtime())).save()
            cities = request.POST.get("city", "").split(",")
            for city in cities:
                citylst = PtYellowCitylist.objects.filter(city_name__startswith=city)
                if len(citylst) > 1:
                    for item in citylst:
                        if item.city_type == 2:
                            city = item
                else:
                    city = citylst[0]
                optcitycitygroups = PtCityCityGroups(group=oCityGroup, city=city)
                optcitycitygroups.save()
                # CmsCheck(module=CmsModule.MAIN_CITYGROUP,
                #          table_name='PtCityCityGroups',
                #          data_id=optcitycitygroups.id,
                #          op_type=CheckOpType.NEW,
                #          is_show=0,
                #          alter_person=request.user.username,
                #          alter_date=time.strftime("%Y-%m-%d %X",time.localtime())).save()
            return HttpResponseRedirect(reverse("city_groups"))
    else:
        form = CityGroupForm()
    errors, fields = format_form(form)
    cities = get_city_list()
    return render_to_response(template_name, {
        "cities": cities,
        "errors": errors,
        "fields": fields
    }, context_instance=RequestContext(request))


# 编辑城市分组
@login_required
@permission_required(u'%s.%s' % (AuthCodeName.APP_LABEL, AuthCodeName.CONFIG), raise_exception=True)
@add_main_var
def edit_city_group(request, template_name):
    id = request.GET.get("id")
    markcities = []
    if request.method == "POST":
        city_group = PtCityGroup.objects.get(id=id)
        city_groups = PtCityCityGroups.objects.filter(group_id=id)  # 删除对应关系中的分组列表
        # for item in city_groups:
        #     check = CmsCheck(
        #         module=CmsModule.MAIN_CITYGROUP,
        #         table_name="PtCityCityGroups",
        #         data_id=item.id,
        #         op_type=CheckOpType.DELETE,
        #         status=CheckStatu.WAIT_SUBMIT,
        #         is_show=0,
        #         alter_person=request.user.username,
        #         alter_date=time.strftime("%Y-%m-%d %X",time.localtime()))
        #     check.save()
        city_groups.delete()
        form = CityGroupForm(request.POST, instance=city_group)
        if form.is_valid():
            oCityGroup = form.save()
            # CmsCheck(module=CmsModule.MAIN_CITYGROUP,
            #          table_name='PtCityGroup',
            #          data_id=oCityGroup.id,
            #          op_type=CheckOpType.EDIT,
            #          alter_person=request.user.username,
            #          alter_date=time.strftime("%Y-%m-%d %X",time.localtime())).save()
            cities = request.POST.get("city", "").split(",")
            for city in cities:
                citylst = PtYellowCitylist.objects.filter(city_name__startswith=city)
                if len(citylst) > 1:
                    for item in citylst:
                        if item.city_type == 2:
                            city = item
                else:
                    city = citylst[0]
                optcitycitygroups = PtCityCityGroups(group=oCityGroup, city=city)
                optcitycitygroups.save()
                # CmsCheck(module=CmsModule.MAIN_CITYGROUP,
                #          table_name='PtCityCityGroups',
                #          data_id=optcitycitygroups.id,
                #          op_type=CheckOpType.EDIT,
                #          is_show=0,
                #          alter_person=request.user.username,
                #          alter_date=time.strftime("%Y-%m-%d %X",time.localtime())).save()
            return HttpResponseRedirect(reverse("city_groups"))
    else:
        city_group = PtCityGroup.objects.get(id=id)
        for PtCityCityGroup in PtCityCityGroups.objects.filter(group=id):
            ptyellowcitylist = PtYellowCitylist.objects.get(self_id=PtCityCityGroup.city_id)
            cityname = ptyellowcitylist.city_name
            if len(cityname) > 2 and cityname[-1] in ["市", "县"]:
                cityname = cityname[:-1]
            markcities.append(cityname)
        form = CityGroupForm(instance=city_group)
    errors, fields = format_form(form)
    cities = get_city_list()
    return render_to_response(template_name, {
        "cities": cities,
        "markcities": markcities,
        "id": id,
        "errors": errors,
        "fields": fields
    }, context_instance=RequestContext(request))


# 城市列表
@login_required
@add_main_var
def city_groups(request, template_name):
    return render_to_response(template_name, context_instance=RequestContext(request))


@login_required
def get_city_group_list(request):
    per_page = request.GET.get("per_page")
    if not per_page:
        per_page = MainConst.PER_PAGE
    cur_page = request.GET.get("cur_page")
    if not cur_page:
        cur_page = 1
    groups = PtCityGroup.objects.all()
    citylist = []
    for group in groups:
        cities = PtYellowCitylist.objects.filter(ptcitycitygroups__group=group)
        temp = []
        for city in cities:
            temp.append({
                "id": city.self_id,
                "name": city.city_name
            })
        citylist.append({
            "id": group.id,
            "name": group.name,
            "cities": temp
        })
    citypage, num_pages = get_table_paginator(citylist, per_page, cur_page)
    return HttpResponse(json.dumps([
        list(citypage),
        num_pages
    ]))


@login_required
@permission_required(u'%s.%s' % (AuthCodeName.APP_LABEL, AuthCodeName.CONFIG), raise_exception=True)
def del_city_group(request):
    """
    删除城市分组
    :param request:
    :return:
    """
    id = request.POST.get("id")

    city_groups = PtCityCityGroups.objects.filter(group__id=id)
    # for city_group in city_groups:
    #     check = CmsCheck(
    #         module=CmsModule.MAIN_CITYGROUP,
    #         table_name="PtCityCityGroups",
    #         data_id=city_group.id,
    #         op_type=CheckOpType.DELETE,
    #         status=CheckStatu.WAIT_SUBMIT,
    #         is_show=0,
    #         alter_person=request.user.username,
    #         alter_date=time.strftime("%Y-%m-%d %X",time.localtime()))
    #     check.save()
    city_groups.delete()

    group = PtCityGroup.objects.get(id=id)
    # check = CmsCheck(
    #     module=CmsModule.MAIN_CITYGROUP,
    #     table_name="PtCityGroup",
    #     data_id=id,
    #     op_type=CheckOpType.DELETE,
    #     status=CheckStatu.WAIT_SUBMIT,
    #     is_show=1,
    #     alter_person=request.user.username,
    #     alter_date=time.strftime("%Y-%m-%d %X",time.localtime()))
    # check.save()
    group.delete()
    return HttpResponse(0)


@login_required
def search_city_groups(request):
    per_page = request.GET.get("per_page")
    cur_page = request.GET.get("cur_page")
    key = request.GET.get("key")
    city_groups = PtCityGroup.objects.all()
    result = []
    for city_group in city_groups:
        cities = PtYellowCitylist.objects.filter(ptcitycitygroups__group=city_group).values_list('city_name', flat=True)
        status_str, status_int = get_check_status_str("PtCityGroup", city_group.id)
        result.append([
            city_group.name,
            city_group.remark,
            ",".join(cities),
            status_str,
            status_int,
            city_group.id
        ])
    result = search_key(result, key, [4, 5])
    result, num_pages = get_table_paginator(result, per_page, cur_page)
    filter_none(result)
    return HttpResponse(json.dumps([list(result), num_pages]))
