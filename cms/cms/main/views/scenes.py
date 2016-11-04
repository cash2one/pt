# coding: utf-8

"""
    场景
"""


# from .main_pub import *
from django.contrib.auth.decorators import login_required
import json
from django.http import HttpResponse

from main.models import CmsScene


@login_required
def get_scenes(request):
    scenes = CmsScene.objects.values_list("name", flat=True)
    return HttpResponse(json.dumps(list(scenes)))