# -*- coding: utf-8 -*-
from __future__ import absolute_import
import os
from django.conf import settings
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pt_shelves.settings')

app = Celery('cache')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
