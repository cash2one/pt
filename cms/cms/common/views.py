# coding: utf-8


"""
    一些公共函数
"""
import time
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# from main.models import *
import string

import json
from django.db.models import Q
from cms.settings import CMS_CHECK_ON, INSTALL_TYPE
from common.const import CheckOpType, check_status, CheckStatu
from main.models import CmsChannelChannel, get_valid_time, get_city_str, CmsCheck, CmsActions, CmsCP


def get_table_paginator(objs, per_page, cur_page):
    """
    获取分页
    :param objs: list
    :param per_page: 每页个数
    :param cur_page: 当前页码
    :return: 当前页数据和总得页数
    """
    paginator = Paginator(objs, per_page)
    try:
        result = paginator.page(cur_page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        result = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        result = paginator.page(paginator.num_pages)
    return result, paginator.num_pages


def search_key(data, key, exclude):
    """
    搜索关键字
    :param data: 数据，list
    :param key: 关键字
    :param exclude: 排除在外的列，索引
    :return: [[序号,id,...], [序号,id,...] ... ]
    """
    result = []
    for i, row in enumerate(data):
        has = False
        no = str(i + 1)
        new_row = [no]
        for j, col in enumerate(row):
            col = str(col) if col is not None else ""
            new_row.append(col)
            if not key or (j not in exclude and key.lower() in col.lower()) or key in no:
                has = True
        if has:
            result.append(new_row)
    return result


def timestamp2str(timestamp):
    t = time.localtime(float(timestamp))
    return time.strftime('%Y-%m-%dT%H:%M', t)


def timestamp2str_h(timestamp):
    t = time.localtime(float(timestamp))
    return time.strftime('%Y-%m-%d %H:%M:%S', t)


def make_timestamp(strtime):
    return int(time.mktime(time.strptime(strtime, '%Y-%m-%dT%H:%M')))


def make_timestamp_h(strtime):
    import time
    return int(time.mktime(time.strptime(strtime + ".000", '%Y-%m-%d %H:%M:%S.%f')))


def filter_none(a):
    if isinstance(a, list):
        for i, item in enumerate(a):
            if item == None:
                a[i] = ""
            else:
                filter_none(item)
    elif isinstance(a, dict):
        for key, value in a.items():
            if value == None:
                a[key] = ""
            else:
                filter_none(value)


def get_relate_channel_list(channel_id, config_item, db="default"):
    c = CmsChannelChannel.objects.using(db).filter(Q(channel_id1=channel_id) | Q(channel_id2=channel_id), op_type=0,
                                                   config_items__contains=',%s,' % config_item).values_list(
        'channel_id1', 'channel_id2')
    result = set()
    for id1, id2 in c:
        if int(id1) != int(channel_id):
            result.add(int(id1))
        if int(id2) != int(channel_id):
            result.add(int(id2))
    return list(result)


def analyze_shop_content(obj):
    # 头像
    photoUrl = ""
    # 获取电话
    photo_str = ""
    # 获取附近分店名称
    search_show = ""
    # 获取搜索词
    s_key = ""
    # 获取搜索词分类
    search_category = ""
    # 获取官方主页
    home = ""
    # 获取微薄主页
    weibo = ""
    try:
        if obj.content:
            content = json.loads(obj.content)
            photoUrl = content.get("photoUrl", "")
            numbers = content.get("numbers", [])
            for i, d in enumerate(numbers):
                photo_str += "电话" + str(i + 1) + ": " + d.get("number", "") + "<br />"
                photo_str += "电话描述" + str(i + 1) + ": " + d.get("number_description", "") + "<br />"
            if len(content.get("search_info", [])):
                search = content.get("search_info")[0]
                search_show = search.get("search_show", "")
                s_key = search.get("search_key", "")
                search_category = search.get("search_category", "")
            home = content.get("webSite", "")
            weibo = content.get("weibo", "")
    except:
        pass
    return photoUrl if photoUrl else obj.icon, photo_str, search_show, s_key, search_category, home, weibo


class CheckManager(object):
    @classmethod
    def wrap_style(cls, text):
        return "<span style='font-size:16px;color:rgb(66, 149, 192)'>%s</span>" % text

    @classmethod
    def __get_title(cls, obj, remark):
        title = ""
        for field in obj._meta.fields:
            if field.name == remark:
                title = field.verbose_name
                break
        special_text = remark + "__text__"
        value = getattr(obj, special_text)() if hasattr(obj, special_text) else obj.__dict__[remark]
        value = "" if value is None else value
        # 是渠道，还要加个版本号
        if remark == "channel_no":
            value = "%s版本下的%s" % (obj.app_version.app_version, value)
        return title, value

    @classmethod
    def __get_new_content(cls, obj):
        content = ""
        for field in obj._meta.fields:
            special_text = field.name + "__text__"
            if field.verbose_name and field.name in obj.__dict__:
                text = getattr(obj, special_text)() if hasattr(obj, special_text) else obj.__dict__[field.name]
                text = "" if text is None else text
                content += "%s: %s<br />" % (field.verbose_name, text)
        return content

    @classmethod
    def new_obj(cls, record):
        """显示新增对象"""
        try:
            if record.remark:
                content = record.remark
            else:
                content = cls.wrap_style(cls.__get_new_content(eval(record.table_name).objects.get(id=record.data_id)))
            d = {
                "type": CheckOpType.NEW,
                "content": content
            }
            return d
        except:
            pass

    @classmethod
    def edit_obj(cls, record):
        """显示修改项"""
        try:
            content = ""
            obj_backup = eval(record.table_name).objects.get(id=record.data_id)
            obj_online = eval(record.table_name).objects.using("online").get(id=record.data_id)
            check_title = obj_online.get_check_title() if hasattr(obj_online, "get_check_title") else ""
            if check_title:
                title, value = cls.__get_title(obj_online, check_title)
                if value:
                    content += "编辑%s为%s的项<br />" % (cls.wrap_style(title), cls.wrap_style(value))
                else:
                    content += "编辑<br />%s的项<br />" % cls.wrap_style(cls.__get_new_content(obj_online))
            else:
                content += "编辑<br />%s的项<br />" % cls.wrap_style(cls.__get_new_content(obj_online))
            for field in obj_backup._meta.fields:
                special_text = field.name + "__text__"
                if field.verbose_name and field.name in obj_backup.__dict__:
                    value_backup = getattr(obj_backup, special_text)() if hasattr(obj_backup, special_text) else \
                        obj_backup.__dict__[field.name]
                    value_online = getattr(obj_online, special_text)() if hasattr(obj_online, special_text) else \
                        obj_online.__dict__[field.name]
                    if value_backup != value_online and (value_backup or value_online):
                        content += "修改%s，由 %s 改为 %s<br />" % (cls.wrap_style(field.verbose_name),
                                                              cls.wrap_style(value_online if value_online else "空"),
                                                              cls.wrap_style(value_backup if value_backup else "空"))
            d = {
                "type": CheckOpType.EDIT,
                "content": content
            }
            return d
        except Exception as e:
            print(e)
            pass

    @classmethod
    def delete_obj(cls, record):
        """显示删除项"""
        try:
            if record.remark:
                content = record.remark
            else:
                obj_online = eval(record.table_name).objects.using("online").get(id=record.data_id)
                check_title = obj_online.get_check_title() if hasattr(obj_online, "get_check_title") else ""
                if check_title:
                    title, value = cls.__get_title(obj_online, check_title)
                    if value:
                        content = "删除了%s为%s的项" % (cls.wrap_style(title), cls.wrap_style(value))
                    else:
                        content = "删除<br />%s的项<br />" % cls.wrap_style(cls.__get_new_content(obj_online))
                else:
                    content = "删除<br />%s的项<br />" % cls.wrap_style(cls.__get_new_content(obj_online))
            d = {
                "type": CheckOpType.DELETE,
                "content": content
            }
            return d
        except:
            pass

    @classmethod
    def get_record(cls, record):
        d = {
            CheckOpType.NEW: cls.new_obj,
            CheckOpType.EDIT: cls.edit_obj,
            CheckOpType.DELETE: cls.delete_obj
        }
        return d.get(str(record.op_type))(record)

        # @classmethod
        # def copy_version(cls, ver_id1, ver_id2):
        #     """拷贝版本"""
        #     pass
        #
        # @classmethod
        # def copy_channel(cls, channel_id1, channel_id2):
        #     """拷贝渠道"""
        #     pass
        #
        # @classmethod
        # def relate_channel(cls, channel_id1, channel_id2):
        #     """关联渠道"""
        #     pass


def handle_valid_time_city(objs, index_time=None, index_city=None):
    result = []
    for obj in objs:
        item = list(obj)
        if index_time is not None:
            item[index_time] = get_valid_time(item[index_time])
        if index_city is not None:
            item[index_city] = get_city_str(item[index_city])
        result.append(item)
    return result


# def is_insert_check_table(table_name, data_id, op_type):
#     """新增、编辑、删除，判断该函数"""
#     #新增
#     if op_type == CheckOpType.NEW:
#         return True
#     #编辑
#     elif op_type == CheckOpType.EDIT:
#         if CmsCheck.objects.filter(table_name=table_name, data_id=data_id, op_type=CheckOpType.NEW, status=CheckStatu.SUBMIT):
#             #有新增-已提交，编辑不显示
#             return False
#         else:
#             #编辑的老数据，显示出来
#             return True
#     elif op_type == CheckOpType.DELETE:
#         new_checks = CmsCheck.objects.filter(table_name=table_name, data_id=data_id, op_type=CheckOpType.NEW, status=CheckStatu.SUBMIT)
#         if new_checks:
#             #有新增-已提交，把新增的数据干掉，删除不显示
#             new_checks.delete()
#             return False
#         edit_checks = CmsCheck.objects.filter(table_name=table_name, data_id=data_id, op_type=CheckOpType.EDIT, status=CheckStatu.SUBMIT)
#         if edit_checks:
#             #有编辑-已提交，把编辑的数据干掉，删除不显示
#             edit_checks.delete()
#             return False
#         #删除的老数据
#         return True
#     raise Exception("is_insert_check_table error")


# def get_check_status_str(table_name, data_id):
#     if CmsCheck.objects.filter(table_name=table_name, data_id=data_id, status=CheckStatu.SUBMIT):
#         status = get_2array_value(check_status, CheckStatu.SUBMIT)
#         can_change = 0
#     elif CmsCheck.objects.filter(table_name=table_name, data_id=data_id, status=CheckStatu.WAIT_SUBMIT):
#         status = get_2array_value(check_status, CheckStatu.WAIT_SUBMIT)
#         can_change = 1
#     else:
#         status = ""
#         can_change = 1
#     return status, can_change


def get_check_status_str(table_name, data_id):
    # 主要联想生活在使用
    """

    :param table_name:
    :param data_id:
    :return:
    """
    if CMS_CHECK_ON:
        checks = CmsCheck.objects.filter(table_name=table_name, data_id=data_id)
        # 以最后一次修改的为主
        if checks:
            check = checks[len(checks) - 1]
            status = dict(check_status)[str(check.status)]
            can_change = 1
            if str(check.status) == CheckStatu.SUBMIT:
                can_change = 0
        else:
            status = ""
            can_change = 1
        return status, can_change
    else:
        return "", 1


def is_submitted(table_name, data_id):
    if CMS_CHECK_ON and CmsCheck.objects.filter(table_name=table_name, data_id=data_id, status=CheckStatu.SUBMIT):
        return True
    else:
        return False


def check_submitted_results(table_name, lstobjs, index_id):
    results = []
    for obj in lstobjs:
        obj = list(obj)
        if CMS_CHECK_ON:
            if CmsCheck.objects.filter(table_name=table_name, data_id=obj[index_id], status=CheckStatu.SUBMIT):
                obj.append(0)
            elif CmsCheck.objects.filter(table_name=table_name, data_id=obj[index_id], status=CheckStatu.WAIT_SUBMIT):
                obj.append(1)
            else:
                obj.append(-1)
        else:
            obj.append(-1)
        results.append(obj)
    return results


def checked_results(table_name, lstobjs, index_id):
    if CMS_CHECK_ON:
        results = []
        for obj in lstobjs:
            if not CmsCheck.objects.filter(~Q(status=CheckStatu.PASS), table_name=table_name, data_id=obj[index_id]):
                results.append(list(obj))
        return results
    else:
        return lstobjs


def channel_status(channel_id):
    status = ""
    can_change = 1
    if CMS_CHECK_ON:
        channel_channels = CmsChannelChannel.objects.filter(
            Q(channel_id1=channel_id) | Q(channel_id2=channel_id)).values_list("id")
        channel_channel_ids = [channel_channel[0] for channel_channel in channel_channels]
        # 配置项下面已提交的不能进行删除和编辑
        # 包括本身所在表的已提交也不能进行删除和编辑
        # 包括渠道关联表已经提交的也不能进行删除和编辑
        checks = CmsCheck.objects.filter(
            Q(channel_id=channel_id) | Q(table_name="CmsChannels", data_id=channel_id) | Q(channel_id=0,
                                                                                           table_name="CmsChannelChannel",
                                                                                           data_id__in=channel_channel_ids))
        for check in checks:
            # 判断这个表里面的状态
            if check.table_name == "CmsChannels":
                status = dict(check_status)[str(check.status)]
            if check.status == 2:
                can_change = 0
                # 如果是审核成功或者""可以进入到该渠道,否则不能进入到该渠道
    return status, can_change


def channels_status(channels):
    new_channels = []
    show_channels = []
    for channel in channels:
        status = channel_status(channel[0])
        if status[0] == "" or status[0] == dict(check_status)[CheckStatu.PASS]:
            show_channels.append(channel)
        new_channel = channel + status
        new_channels.append(new_channel)
    return new_channels, show_channels


def vers_status(ver_id):
    status = ""
    can_change = 1
    if CMS_CHECK_ON:
        checks = CmsCheck.objects.filter(table_name='CmsChannelsAppVersion', data_id=ver_id)
        for check in checks:
            status = dict(check_status)[str(check.status)]
            if check.status == 2:
                can_change = 0
                # for channel in channels:
                #     if channel[4] == 0:
                #         can_change = 0
                #         break
    return status, can_change


def setCpAction(cp_id, action_id):
    cp_id = int(cp_id)
    if (len(action_id) > 0):
        action_id = int(action_id)
    else:
        action_id = -1
    if (INSTALL_TYPE == 1 and action_id == 268) or (INSTALL_TYPE == 2 and action_id == 465) or (
                    INSTALL_TYPE == 3 and action_id == 474):
        action = CmsActions.objects.get(id=action_id)
        result = {
            "click_type": 1,
            "dest_activity": action.dest_activity,
            "action_params": json.dumps({"cp_id": cp_id}),
            "pt_h5": 0
        }
        cp = CmsCP.objects.get(id=cp_id)
        cp.action_json = json.dumps(result)
        cp.save()


def get_url_arg(request, key, arg_type, default):
    """
    获取url中的参数,一般使用get,delete等需要在url中传参的请求
    :param request: request请求
    :param key: 要获取的参数键
    :param arg_type: 获取的参数的类型工厂函数
    :param default: 获取不到参数的默认值
    :return: 获取的参数值
    """
    value = request.GET.get(key)
    if value:
        value = value.strip()
        return arg_type(value)
    return default


def get_body_arg(request, key, arg_type, default):
    value = request.POST.get(key)
    if value:
        value = value.strip()
        if arg_type == 'json_array':
            try:
                value = json.loads(value)
            except:
                value = []
        else:
            value = arg_type(value)
        return value
    return default


def check_token(id,token):
    try:
        from main.models import AuthToken
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
