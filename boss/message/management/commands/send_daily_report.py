__author__ = 'Administrator'

from django.core.management.base import BaseCommand, CommandError
from message.views.lkl_daily_report import *
from message.views.operation_daily_report import *


class Command(BaseCommand):
    def handle(self, *args, **options):
        send_operation_daily_report()
        send_lkl_daily_report()