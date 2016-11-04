# -*- coding: utf-8 -*-
# Author:songroger
# Jul.14.2016
from __future__ import unicode_literals
from __future__ import division
import os
import sys
import traceback
import time
from datetime import datetime
from django.conf import settings
from django.db import connection
from django.core.mail import mail_admins
import hashlib


def get_set(key, value):
    return getattr(settings, key, value)


def list_to_string(a):
    """
    list转连串字符串, 拼sql中的in常用.
    :param : [a,b,c]
    :return: "a","b","c"
    """
    if a:
        return ",".join(map(str, a))
    return "''"


def ptlog(comments=''):
    LOG_VAR = os.path.join(os.path.dirname(settings.BASE_DIR), "var")
    if not os.path.exists(LOG_VAR):
        os.makedirs(LOG_VAR)
    f_name = sys._getframe().f_code.co_name
    traceback.print_exc(file=open('%s/pt.txt' % LOG_VAR, 'a+'))
    _print(file=open('%s/pt.txt' % LOG_VAR, 'a+'),
           str=str(datetime.now()) + comments + '\n')
    mail_admins(get_set('PTLOGSUBJECT', f_name), traceback.format_exc())


def _print(file, str='', terminator=70 * '-' + '\n'):
    file.write(str + terminator)


def check_name_exists(table, column, name):
    cur = connection.cursor()
    sql = "SELECT id FROM %s WHERE TRIM(REPLACE(%s,' ','')) = TRIM(REPLACE('%s',' ',''));" % (
        table, column, name)
    cur.execute(sql)
    row = cur.fetchall()
    return True if row else False


def to_unixtime(otime):
    return time.mktime(otime.timetuple()) * 1000\
        if isinstance(otime, datetime) else ""


def md5str(string):
    return hashlib.md5(string).hexdigest()


def uniquenum(string):
    return int(hashlib.md5(string).hexdigest(), 16)
