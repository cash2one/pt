# coding: utf-8
"""
    记录中心
"""
import time
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.core.mail import send_mail
import json
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.http import require_POST

from cms.settings import EMAIL_HOST_USER
from common.const import AuthCodeName, CheckStatu, CheckOpType, check_status, get_2array_value

# from .main_pub import *
# from main.forms import *
from common.views import filter_none
from main.models import CmsCheck, AuthUser, CmsCheckHistory
from main.views.main_pub import add_main_var, show_cvt, set_id_into_records, get_record_detail


def filter_unsubmitted():
    checks = CmsCheck.objects.filter(status=CheckStatu.WAIT_SUBMIT, op_type=CheckOpType.EDIT)
    # 多个编辑的保留一个
    # 先看编辑的，如果有新建的未提交去除编辑的记录
    for check in checks:
        objs = CmsCheck.objects.filter(status=CheckStatu.WAIT_SUBMIT, table_name=check.table_name,
                                       data_id=check.data_id, op_type=CheckOpType.NEW)
        if objs:
            check.delete()
        # 只保留一个编辑，不能删除自身的
        elif CmsCheck.objects.filter(~Q(id=check.id), status=CheckStatu.WAIT_SUBMIT, table_name=check.table_name,
                                     data_id=check.data_id, op_type=CheckOpType.EDIT):
            check.delete()
    # 如果是删除未提交
    # 看是否存在新建的，如果存在新建的待提交，干掉所有包括删除未提交的
    # 否则看是否存在编辑的，如果存在编辑的，干掉编辑的。
    checks = CmsCheck.objects.filter(status=CheckStatu.WAIT_SUBMIT, op_type=CheckOpType.DELETE)
    for check in checks:
        objs = CmsCheck.objects.filter(op_type=CheckOpType.NEW, status=CheckStatu.WAIT_SUBMIT,
                                       table_name=check.table_name, data_id=check.data_id)
        if objs:
            CmsCheck.objects.filter(status=CheckStatu.WAIT_SUBMIT, table_name=check.table_name,
                                    data_id=check.data_id).delete()
        else:
            CmsCheck.objects.filter(op_type=CheckOpType.EDIT, status=CheckStatu.WAIT_SUBMIT,
                                    table_name=check.table_name, data_id=check.data_id).delete()


@login_required
@permission_required(u'%s.%s' % (AuthCodeName.APP_LABEL, AuthCodeName.CONFIG), raise_exception=True)
@add_main_var
def record(request, template_name):
    staffs = AuthUser.objects.filter(is_staff=1).values_list('username', 'email')
    return render_to_response(template_name, {
        "staffs": staffs
    }, context_instance=RequestContext(request))


@login_required
@permission_required(u'%s.%s' % (AuthCodeName.APP_LABEL, AuthCodeName.CONFIG), raise_exception=True)
def record_handle(request):
    filter_unsubmitted()
    records = CmsCheck.objects.filter(Q(status=CheckStatu.WAIT_SUBMIT) | Q(status=CheckStatu.SUBMIT))
    result = []
    for record in records:
        try:
            type, version, channel_no = show_cvt(record.channel_id, record.module)
            if str(record.status) == CheckStatu.SUBMIT:
                person = CmsCheck.objects.filter(channel_id=record.channel_id, module=record.module,
                                                 status=record.status).last().submit_person
            else:
                person = ""
            data = [
                get_2array_value(check_status, str(record.status)),
                person,
                type,
                version,
                channel_no,
                record.module
            ]
        except:
            continue
        set_id_into_records(result, data, record.id)
    result.sort(key=lambda o: (o["record"][0], o["record"][2], o["record"][3], o["record"][4], o["record"][5]),
                reverse=True)
    filter_none(result)
    return HttpResponse(json.dumps(result))


@login_required
@permission_required(u'%s.%s' % (AuthCodeName.APP_LABEL, AuthCodeName.CONFIG), raise_exception=True)
@add_main_var
def record_detail(request, template_name):
    return render_to_response(template_name, context_instance=RequestContext(request))


@login_required
@permission_required(u'%s.%s' % (AuthCodeName.APP_LABEL, AuthCodeName.CONFIG), raise_exception=True)
def record_detail_data(request):
    ids_str = request.GET.get("ids")
    ids = ids_str.split(",")
    result = get_record_detail(ids)
    return HttpResponse(json.dumps(result))


@login_required
@permission_required(u'%s.%s' % (AuthCodeName.APP_LABEL, AuthCodeName.CONFIG), raise_exception=True)
def record_history(request):
    hs = CmsCheckHistory.objects.all()
    result = []
    for h in hs:
        item = [
            h.status,
            h.check_person,
            h.check_date,
            h.type,
            h.version,
            h.channel_no,
            h.module,
            h.submit_person,
            h.submit_date,
            h.id
        ]
        result.append(item)
    return HttpResponse(json.dumps(result))


@login_required
@permission_required(u'%s.%s' % (AuthCodeName.APP_LABEL, AuthCodeName.CONFIG), raise_exception=True)
def record_history_detail(request):
    id = request.GET.get("id")
    content = CmsCheckHistory.objects.get(id=id).content
    return HttpResponse(content)


@require_POST
@login_required
@add_main_var
@permission_required(u'%s.%s' % (AuthCodeName.APP_LABEL, AuthCodeName.CONFIG), raise_exception=True)
def record_submit(request):
    """
    提交审核
    :param url: {% url 'record_submit' %}
    :param ids: 审核表id列表
            message:提交审核的信息
            recipient_list 收件人列表
    :return: 0 表示成功
    """
    try:
        ids = json.loads(request.POST.get("ids"))
        submit_time = time.strftime("%Y-%m-%d %X", time.localtime())
        subject = "提交审核 提交人：%s 提交时间：%s" % (request.user.username, submit_time)
        message = request.POST.get("message")
        recipient_list = json.loads(request.POST.get("recipient_list"))
        send_mail(subject=subject, message=message, from_email=EMAIL_HOST_USER, recipient_list=recipient_list)
        for id in ids:
            oCmsCheck = CmsCheck.objects.get(id=id)
            oCmsCheck.status = CheckStatu.SUBMIT
            oCmsCheck.submit_person = request.user.username
            oCmsCheck.submit_date = submit_time
            oCmsCheck.save()
        return HttpResponse(0)
    except Exception as ex:
        print(ex)
        return HttpResponse(-1)


@login_required
@permission_required(u'%s.%s' % (AuthCodeName.APP_LABEL, AuthCodeName.CONFIG), raise_exception=True)
def record_revert(request):
    """
    撤销提交
    :param url: {% url 'record_revert' %}
    :param ids: 审核表id列表
    :return: 0 表示成功
    """
    ids = json.loads(request.POST.get("ids"))
    for id in ids:
        CmsCheck.objects.filter(id=id).update(status=CheckStatu.WAIT_SUBMIT)
    return HttpResponse(0)
