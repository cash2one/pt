# coding: utf-8


"""
    静态文件替换
"""

import os, re

#把其中的/static/替换为/v2/cms_test/static/

rootdir = "static"
old = "/static/"
new = "/v2/cms_test/static/"


def replace_static(file):
    a = open(file, "r").read()
    if old in a:
        open(file + "_2", "w").write(a.replace(old, new))


for parent, dirnames, filenames in os.walk(rootdir):
    for filename in filenames:
        if re.match('.+\.(css|js)$', filename):
            replace_static(os.path.join(parent, filename))