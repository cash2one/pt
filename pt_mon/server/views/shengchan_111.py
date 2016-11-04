# -*- coding: utf-8 -*-
import paramiko
#from django.template import Template ,Context
from django.shortcuts import render_to_response
#from django.http import HttpResponse
import time

def index(req,template_name):
        hostname = '120.26.42.111'
        port     = 22
        username = 'root'
        password = 'Putao2015'
        Known_host = "C:\\Users\\Administrator\\.ssh\\known_hosts"
        #Known_host = "/root/.ssh/known_hosts"
        paramiko.util.log_to_file('paramiko.log')
        s = paramiko.SSHClient()
        s.load_system_host_keys(Known_host)
        s.connect(hostname, port, username, password)
        s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        stdin, stdout, stderr = s.exec_command('ps aux |grep -E "java|nginx|uwsgi" |grep -v grep')

        a = stdout.read()
        lists = a.split('\n')
        cs_111 = []
        for i in lists:
            i = i.split(' ')
            def not_empty(i):
                return i and i.strip()
            b = filter(not_empty,i)
            if len(b) < 10:continue
            ret = [b[0], b[1], b[10],b[11]]
            cs_111.append(ret)

        cs_111.append(['121.40.44.169'])

        hostname = '121.40.44.169'
        port = 22
        username = 'root'
        password = 'Putao2015hw'
        Known_host = "C:\\Users\\Administrator\\.ssh\\known_hosts"
        # Known_host = "/root/.ssh/known_hosts"
        paramiko.util.log_to_file('paramiko.log')
        s = paramiko.SSHClient()
        s.load_system_host_keys(Known_host)
        s.connect(hostname, port, username, password)
        s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        stdin, stdout, stderr = s.exec_command('ps aux |grep -E "java|nginx|uwsgi" |grep -v grep')

        a = stdout.read()
        listss = a.split('\n')
        for l in listss:
            l = l.split(' ')

            def not_empty(l):
                return l and l.strip()

            c = filter(not_empty, l)
            if len(c) < 10: continue
            rete = [c[0], c[1], c[10], c[11]]
            cs_111.append(rete)

            #print c
        return render_to_response('test.html',{'cs_111':cs_111})
        #return HttpResponse(c)
