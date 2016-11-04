#!/usr/bin/env python

import paramiko

hostname = '192.168.1.240'
port     = 22
username = 'root'
password = 'putao123'
Known_host = "C:\\Users\\Administrator\\.ssh\\known_hosts"


if __name__ == "__main__":
            paramiko.util.log_to_file('paramiko.log')
            s = paramiko.SSHClient()
            s.load_system_host_keys(Known_host)
            s.connect(hostname, port, username, password)
            s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            stdin, stdout, stderr = s.exec_command('ps aux |grep -E "java|nginx|uwsgi" |grep -v grep')

            a = stdout.read()
            lists = a.split('\n')
            for i in lists:
                i = i.split(' ')
                def not_empty(i):
                    return i and i.strip()
                ret = filter(not_empty, i)
                if len(ret) < 10: continue
                b = [ret[0], ret[1], ret[10]]
                print b
            s.close()