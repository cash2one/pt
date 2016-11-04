#coding: utf-8
import pymysql
#python3 用pymysql 代替mysqldb
# from cache.patch import patch
pymysql.install_as_MySQLdb()

# 开启redis缓存
# patch()
