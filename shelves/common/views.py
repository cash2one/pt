# coding: utf-8

"""
    存放views中的一些共有的方法
"""
from __future__ import unicode_literals
import csv, datetime
import codecs

import functools

from django.contrib import auth
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http.response import StreamingHttpResponse

from common.conf import get_http_url
from main.models import AuthUserUserPermissions, AuthToken


class Const:
    PHONE_FEE = u"充话费"
    FLOW = u"充流量"
    MOVIE = u"电影票"
    QB = u"游戏充值"
    TRAIN = u"火车票"
    HOTEL = u"酒店"
    WEC = u"水电煤"
    SHOW_SHELVES_URL = u"显示货架平台url"

    # 空字符串
    NONE = u"--"
    # 全部应用
    PLUS99 = u"PLUS99"
    # 提示选择某个具体应用
    TEMPLATE_PLUS99 = u"plus99.html"


class PermissionType(object):
    MODULE = 199
    APP = 200
    USER_ON = 201
    STAFF_ON = 202
    ZF = 204


def pag(objs, per_page, cur_page):
    paginator = Paginator(objs, per_page)  # Show 25 contacts per page
    try:
        result = paginator.page(cur_page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        result = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        result = paginator.page(paginator.num_pages)
    return result, paginator.num_pages


get_datestr = lambda a, f: (datetime.datetime.now() - datetime.timedelta(days=a)).strftime(f)


def get_csv_response(filename, csv_data):
    """
    根据文件名和内容生成csv文件
    :param filename: 文件名
    :param csv_data: csv内容，数据类型为[[]]
    :return:
    """
    response = HttpResponse(content_type='text/csv')
    # 在response的最开头写入BOM标记，避免中文乱码
    response.write(codecs.BOM_UTF8)
    # gb2312避免ie浏览器，文件名称乱码
    response['Content-Disposition'] = 'attachment; filename=%s' % filename
    writer = csv.writer(response)
    for row in csv_data:
        writer.writerow(row)
    return response

def check_token(id,token):
    try:
        i = AuthToken.objects.using('auth_db').filter(user_id=id)
        if i[0].token == token:
            return True
        else:
            return False
    except :
        return False

def make_token(id,pd):
    from datetime import date
    import hashlib
    ts = (date.today() - date(2001, 1, 1)).days
    st = str(id) + str(pd) + str(ts)
    return str(hashlib.sha1(st).hexdigest())

def add_common_var(f):
    @functools.wraps(f)
    def _(*args, **kwargs):
        result = f(*args, **kwargs)
        # 查找所有的应用
        objs = AuthUserUserPermissions.objects.filter(user=args[0].user.id)
        items = []
        for obj in objs:
            if obj.permission.content_type_id == PermissionType.APP:
                items.append("['%s', '%s']" % (obj.permission.name, obj.permission.codename))
        apps_str = "[%s]" % ",".join(items)
        vars = {
            "user": auth.get_user(args[0]).username,
            # "lasturl": args[0].path,
            "lasturl": args[0].get_full_path(),
            "apps": apps_str
        }
        from django.contrib.auth.tokens import default_token_generator
        from pt_shelves.settings import MY_URL
        host_url = MY_URL
        boss_url = get_http_url(host_url,'boss')
        conf_url = get_http_url(host_url,'conf')
        user_id = str(auth.get_user(args[0]).id)
        token = make_token(user_id,auth.get_user(args[0]).password)
        at = AuthToken.objects.using('auth_db').filter(user_id=user_id)
        if at:
            at.update(token=token)
        else:
            try:
                at = AuthToken.objects.using('auth_db').create(user_id=user_id, token=token)
                at.save()
            except:
                pass
        boss_url = boss_url+'?user='+user_id+'&token='+token+'&next=/'
        conf_url = conf_url+'?user='+user_id+'&token='+token+'&next=/'
        result.content = result.content.replace("{boss_url_}", boss_url)
        result.content = result.content.replace("{conf_url_}", conf_url)
        for key in vars:
            result.content = result.content.replace("{_tongji_begin_%s_end_}" % key, vars[key])
        return result

    return _


def report_render(request, template, context = None,context_instance=None):
    """
    增加权限控制
    :param request:
    :param template:
    :param context:
    :return:
    """
    context = context if context is not None else {}
    context_instance = context_instance if context_instance is not None else {}
    objs = AuthUserUserPermissions.objects.using('auth_db').filter(user__username=request.user.username)
    for obj in objs:
        if obj.permission.content_type_id == PermissionType.MODULE or obj.permission.content_type_id == PermissionType.USER_ON:
            context[obj.permission.name] = True
    from django.shortcuts import render_to_response
    return render_to_response(template, context,context_instance=context_instance)