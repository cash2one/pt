from __future__ import unicode_literals

from django.db import models

# Create your models here.
class ServerService(models.Model):
    user = models.CharField(max_length=50)
    pid   = models.CharField(max_length=10)
    command = models.CharField(max_length=200)
    fileServer = models.CharField(max_length=200)
