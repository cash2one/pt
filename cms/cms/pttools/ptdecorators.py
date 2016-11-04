# -*- coding: utf-8 -*-
# Author:songroger
# Aug.9.2016
import logging
from functools import wraps
from django.utils.decorators import available_attrs
from .pthttp import PtHttpResponse
from django.core.exceptions import PermissionDenied
try:
    from ipware.ip import get_ip
except ImportError:
    get_ip = lambda req: req.META.get('HTTP_X_FORWARDED_FOR') if req.META.get(
        'HTTP_X_FORWARDED_FOR') else req.META.get('REMOTE_ADDR')
try:
    from django.conf import settings
    PT_IPLIMIT = settings.PT_IPLIMIT
except AttributeError:
    PT_IPLIMIT = {"default": []}
log = logging.getLogger("main.app")


def require_iplimit(flag="default"):
    """
    ips - 允许访问的IP列表, 可在settings中配置PT_IPLIMIT, 默认为空即不做限制
    """
    def decorator(func):
        @wraps(func, assigned=available_attrs(func))
        def inner(request, *args, **kwargs):

            # if settings.DEBUG:
            #     return func(request, *args, **kwargs)
            ips = PT_IPLIMIT.get(flag, [])
            ip = get_ip(request)
            log.info("Request ip is: %s" % ip)
            if not ips or ip in ips:
                return func(request, *args, **kwargs)
            else:
                raise PermissionDenied

        return inner
    return decorator
