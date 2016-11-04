# -*- coding: utf-8 -*-
# Author:songroger
# Jun.23.2016
import json
import csv
from django.http import HttpResponse, JsonResponse
import requests
import traceback
import urllib2


def PtHttpResponse(data, dump=True, status=200):
    return HttpResponse(
        json.dumps(data) if dump else data,
        content_type="application/json",
        status=status,
    )


def get_csv_response(filename, csv_data):
    """
    根据文件名和内容生成csv文件
    :param filename: 文件名
    :param csv_data: csv内容，数据类型为[[]]
    :return:
    """
    response = HttpResponse(content_type='text/csv')
    # 在response的最开头写入BOM标记，避免中文乱码
    # response.write('\xEF\xBB\xBF')
    # gb2312避免ie浏览器，文件名称乱码
    response['Content-Disposition'] = 'attachment; filename=%s' % filename
    writer = csv.writer(response)
    for row in csv_data:
        writer.writerow(row)
    return response


def check_parameter(request_data, required_data):
    data = {"msg": u"SUCCESS", "code": 0}
    for d in required_data:
        if isinstance(request_data.get(d, ''), int):
            continue
        if isinstance(request_data.get(d, ''), list):
            continue
        if request_data.get(d, '').replace(" ", "") == '':
            data = {"msg": u"参数%s必填" % d, "code": 1}
            break
    return data


class PtException(Exception):
    pass


def get_requests_json(url, params={}, timeout=1):
    try:
        r = requests.get(url, params=params, timeout=timeout)
        return r.status_code, r.json()
    except:
        return 1, {}


def get_response_json(url, params={}, timeout=1):
    data = {}
    str_para = "?"
    for k, v in params.iteritems():
        if isinstance(v, list):
            for l in v:
                str_para += str(k) + "=" + str(l) + "&"
        if isinstance(v, (str, int, unicode)):
            str_para += str(k) + "=" + str(v) + "&"
    try:
        resp = urllib2.urlopen(urllib2.Request(
            (url + str_para).rstrip('?&')), timeout=timeout)
        code, data = resp.getcode(), json.loads(resp.read())
        return code, data
    except Exception, e:
        print e
    return None, None
