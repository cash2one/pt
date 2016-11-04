__author__ = 'Administrator'

from django.core.management.base import BaseCommand, CommandError
from message.views.warning_abnormal_order import *
from message.views.notify_overtime_daojia_order import *

class Command(BaseCommand):
    def handle(self, *args, **options):
        send_abnormal_order_warning()
        send_overtime_daojia_order_notify()