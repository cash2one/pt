# coding: utf-8


# from .main_pub import *
# from main.forms import *
# from common.views import CONFIG_ITEMS
import time
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext

from common.const import CONFIG_ITEMS
from main.forms import NewVerForm, NewChannelForm
from main.models import CmsChannelsType
from main.views.main_pub import add_main_var, get_type_ver_channels


@login_required
@add_main_var
def index(request, template_name):
    types = CmsChannelsType.objects.all()
    # 默认是APP
    type_id = request.GET.get("t")
    if not type_id:
        type_id = "1"
    type_name = CmsChannelsType.objects.get(id=type_id).name
    # ver_channels = get_ver_channels(type_id)
    # type_ver_channels = get_type_ver_channels()
    # type_vers = get_type_vers()
    start = time.time()
    type_ver_channels, ver_channels, type_vers = get_type_ver_channels(int(type_id))
    end = time.time()
    print("index loads spend time about: %d.s" % (end - start))
    new_ver_form = NewVerForm()
    new_channel_form = NewChannelForm()
    return render_to_response(template_name, {
        "types": types,
        "CONFIG_ITEMS": CONFIG_ITEMS,
        "ver_channels": ver_channels,
        "new_ver_form": new_ver_form,
        "new_channel_form": new_channel_form,
        "cur_t_id": type_id,
        "cur_t_name": type_name,
        "type_ver_channels": type_ver_channels,
        "type_vers": type_vers,
    }, context_instance=RequestContext(request))
