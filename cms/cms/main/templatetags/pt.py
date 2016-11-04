# -*- coding: utf-8 -*-
# Author:songroger
# Aug.11.2016
import json
from django import template
register = template.Library()


def pt_json_loads(data):
    """Parse json"""
    return json.loads(data)
register.filter('pt_json', pt_json_loads)


def pt_json_dumps(data):
    """Dumps json"""
    return json.dumps(data)
register.filter('pt_dumps', pt_json_dumps)
