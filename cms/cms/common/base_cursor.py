#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author sunq
from math import ceil

# from cache.redis import Singleton
import pymysql.cursors
import cms.settings


class Singleton(object):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            obj = super(Singleton, cls)
            cls._instance = obj.__new__(*args, **kwargs)
        return cls._instance


class BaseCursor(Singleton):

    db = cms.settings.DATABASES['online'] if 'online' in cms.settings.DATABASES else cms.settings.DATABASES['default']

    tupleconn = pymysql.connect(host=db['HOST'], user=db['USER'], password=db['PASSWORD'], db=db['NAME'],
                                charset='utf8', cursorclass=pymysql.cursors.Cursor)
    @classmethod
    def get_dictconn(cls):
        db =cls.db
        return pymysql.connect(host=db['HOST'], user=db['USER'], password=db['PASSWORD'], db=db['NAME'], charset='utf8',
                               cursorclass=pymysql.cursors.DictCursor)
    @classmethod
    def get_tupleconn(cls):
        db =cls.db
        return pymysql.connect(host=db['HOST'], user=db['USER'], password=db['PASSWORD'], db=db['NAME'],
                        charset='utf8', cursorclass=pymysql.cursors.Cursor)
    @classmethod
    def get_tatal_count(cls, sql):
        conn = cls.get_tupleconn()
        cursor = conn.cursor()
        sql = sql.lower()
        bases = sql.split('from')
        bases[0] = 'select count(1) '
        new_sql = 'from'.join(bases)
        cursor.execute(new_sql)
        count = cursor.fetchone()
        conn.close()
        if count and len(count) > 0:
            return count[0]
        else:
            return 0

    @classmethod
    def get_pageinate(cls, page, per_page, sql):
        total_count = cls.get_tatal_count(sql)
        total_page = ceil(total_count / per_page)
        cur = page - 1
        conn = cls.get_tupleconn()
        cursor = conn.cursor()
        sql = sql.lower()
        sql += " limit {0},{1}".format(cur * per_page, per_page)
        cursor.execute(sql)
        result = cursor.fetchall()
        conn.close()
        if result and len(result) > 0:
            return total_page, [list(i) for i in result]
        else:
            return 0, []

    @classmethod
    def get_all(cls, sql):
        conn = cls.get_tupleconn()
        cursor = conn.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        conn.close()
        if result and len(result) > 0:
            return [list(i) for i in result]
        else:
            return []
