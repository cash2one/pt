#!/bin/bash
date
ps -ef|grep cms-uwsgi|grep -v grep|awk '{print $2}'|xargs kill
uwsgi cms-uwsgi.ini
echo "restart done!!"