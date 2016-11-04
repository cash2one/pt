# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render_to_response
from django.template import RequestContext

from common.views import Const, add_common_var, report_render


@login_required
@add_common_var
@permission_required(u'man.%s' % Const.SHOW_SHELVES_URL, raise_exception=True)
def shelves_index(request, template_name):
    pass
    return report_render(request,template_name, context_instance=RequestContext(request))
