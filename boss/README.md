一、部署运行
1.更改setting.py里面debug=False
2.停止运行boss-uwsgi进程 kill -9 进程号

3.运行
cd /root/pt_boss
uwsgi boss-uwsgi.ini



二、重启
cd /root/pt_boss
touch reload