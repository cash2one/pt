#coding: utf-8

"""
    存放views中的一些共有的方法
"""
import functools

from django.contrib import auth
from django.http import HttpResponse
import sys, csv, datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from common.conf import get_http_url
from man.models import AuthUserUserPermissions, AuthToken

reload(sys)
sys.setdefaultencoding('utf8')


class PermissionType(object):
    MODULE = 199
    APP = 200
    USER_ON = 201
    STAFF_ON = 202
    ZF = 204


class Const:
    #空字符串
    NONE = "--"
    #全部应用
    PLUS99 = "PLUS99"
    #提示选择某个具体应用
    TEMPLATE_PLUS99 = "plus99.html"


get_datestr = lambda a, f: (datetime.datetime.now() - datetime.timedelta(days = a)).strftime(f)
get_objp_sum = lambda s, p: sum(o.__dict__[p] for o in s if o.__dict__[p])
get_dictp_sum = lambda s, p: sum(o[p] for o in s if o[p])


def get_csv_response(filename, csv_data):
    """
    根据文件名和内容生成csv文件
    :param filename: 文件名
    :param csv_data: csv内容，数据类型为[[]]
    :return:
    """
    response = HttpResponse(mimetype='text/csv')
    #在response的最开头写入BOM标记，避免中文乱码
    response.write('\xEF\xBB\xBF')
    #gb2312避免ie浏览器，文件名称乱码
    response['Content-Disposition'] = 'attachment; filename=%s' % filename
    writer = csv.writer(response)
    for row in csv_data:
        writer.writerow(row)
    return response


class Cal(object):
    """主要是处理一些空的计算"""
    NONE = Const.NONE

    @classmethod
    def is_none(cls, a):
        return a is None or a == cls.NONE

    @classmethod
    def int(cls, num):
        return cls.NONE if cls.is_none(num) else int(num)

    @classmethod
    def precision(cls, a):
        """保留小数点后一位"""
        return cls.NONE if cls.is_none(a) else "%.1f" % a

    @classmethod
    def percent(cls, a, b):
        """
        计算百分比，保留小数点后一位
        :param a: 分子
        :param b: 分母
        :return:
        """
        if cls.is_none(a) or cls.is_none(b):
            return cls.NONE
        elif b == 0:
            return "0.0%"
        else:
            return "%.1f" % (100 * float(a) / float(b)) + "%"

    @classmethod
    def sum(cls, a, b):
        """
        计算两个数的和
        :param a:
        :param b:
        :return:
        """
        return cls.NONE if cls.is_none(a) or cls.is_none(b) else int(a + b)

    @classmethod
    def sec2time(cls, secs):
        """
        把秒数转为可看的时间格式
        :param secs: 秒数
        :return: "01:01:01"格式字符串
        """
        if cls.is_none(secs):
            return cls.NONE
        secs = cls.int(secs)
        h = secs / 3600
        m = (secs - 3600 * h) / 60
        s = secs - h * 3600 - m * 60
        return "%.2d:%.2d:%.2d" % (h, m, s)

    @classmethod
    def dev(cls, a, b):
        """
        计算两个数的除
        :param a:
        :param b:
        :return:
        """
        if cls.is_none(a) or cls.is_none(b):
            return cls.NONE
        elif b == 0:
            return 0
        else:
            return float(a) / float(b)


def pag(objs, per_page, cur_page):
    paginator = Paginator(objs, per_page) # Show 25 contacts per page
    try:
        result = paginator.page(cur_page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        result = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        result = paginator.page(paginator.num_pages)
    return result, paginator.num_pages

def filter_none(a):
    if isinstance(a, list):
        for i, item in enumerate(a):
            if item == None or item == str(None):
                a[i] = ""
            else:
                filter_none(item)
    elif isinstance(a, dict):
        for key, value in a.items():
            if value == None or value == str(None):
                a[key] = ""
            else:
                filter_none(value)

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
        #查找所有的应用
        objs = AuthUserUserPermissions.objects.filter(user=args[0].user)
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
        from boss.settings import MY_URL
        host_url = MY_URL
        shelves_url = get_http_url(host_url,'shelves')
        conf_url = get_http_url(host_url,'conf')
        cms_url = get_http_url(host_url,'cms')
        user_id = str(auth.get_user(args[0]).id)
        token = make_token(user_id, auth.get_user(args[0]).password)
        at = AuthToken.objects.using('auth_db').filter(user_id=user_id)
        if at :
            at.update(token=token)
        else:
            try:
                at = AuthToken.objects.using('auth_db').create(user_id=user_id,token=token)
                at.save()
            except:
                pass
        shelves_url = shelves_url+'?user='+user_id+'&token='+token+'&next=/'
        conf_url = conf_url+'?user='+user_id+'&token='+token+'&next=/'
        cms_url = cms_url+'?user='+user_id+'&token='+token+'&next=/'
        result.content = result.content.replace("{shelves_url_}", shelves_url)
        result.content = result.content.replace("{conf_url_}", conf_url)
        result.content = result.content.replace("{cms_url_}", cms_url)
        for key in vars:
            result.content = result.content.replace("{_tongji_begin_%s_end_}" % key, vars[key])
        return result
    return _

def check_token(id,token):
    try:
        i = AuthToken.objects.using('auth_db').filter(user_id=id)
        if i[0].token == token:
            return True
        else:
            return False
    except :
        return False

