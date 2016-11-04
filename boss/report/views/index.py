#coding: utf-8

"""
    订单分CP报表
"""

from man.models import AuthUserUserPermissions
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.exceptions import PermissionDenied
from report_pub import *



@login_required
@add_common_var
def index(request):
    app = request.GET.get("app")
    user = auth.get_user(request)
    objs = AuthUserUserPermissions.objects.filter(user__id__exact=user.id)
    for obj in objs:
        if obj.permission.content_type_id == PermissionType.MODULE:
            return HttpResponseRedirect(reverse(obj.permission.name) + "?app=" + app)
    raise PermissionDenied

@login_required
@add_common_var
def report_index(request, template_name):
    app = request.GET.get("app")
    vers = get_app_versions(app)
    channels = get_app_channels(app)
    products = get_order_types()
    today = datetime.datetime.now()
    if not app:
        app = 'PLUS99'
    summary = TongjiRpDTurnoverSummary.objects.filter(app_id=app, app_version='PLUS99',
                                                      channel_no='PLUS99', product_type='PLUS99', stathour='PLUS99',
                                                      statdate=today.strftime("%Y-%m-%d"))
    if summary:
        summary = summary[0]
    last_summary = TongjiRpDTurnoverSummary.objects.filter(app_id=app, app_version='PLUS99',
                                                           channel_no='PLUS99', product_type='PLUS99',
                                                           stathour='PLUS99', statdate=get_datestr(1, "%Y-%m-%d"))
    if last_summary:
        last_summary = last_summary[0]
    return report_render(request, template_name, {
        "currentdate": get_datestr(1, "%Y-%m-%d"),
        "vers": vers,
        "channels": channels,
        "products": products,
        "summary": summary,
        "last_summary": last_summary
    })

