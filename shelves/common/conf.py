# -*- coding: utf-8 -*-
# Author:wrd

class CONF:
    http_url = {}
    http_url['local'] = {"shelves": u"http://127.0.0.1:8001/accounts/login/",
                         "boss": u"http://127.0.0.1:8002/accounts/login/",
                         "conf": u"http://127.0.0.1:8003/accounts/login/",
                         }
    http_url['test'] = {"shelves": u"http://shelves.test.putao.so/accounts/login/",
                        "boss": u"http://newboss.test.putao.so/accounts/login/",
                        "conf": u"http://psetting.test.putao.so/accounts/login/",
                        }
    http_url['official'] = {"shelves": u"http://shelves.putao.so/accounts/login/",
                            "boss": u"http://newboss.test.putao.so/accounts/login/",
                            "conf": u"http://127.0.0.1:8003/accounts/login/",
                            }


def get_http_url(type, who):
    return CONF.http_url[type][who]
