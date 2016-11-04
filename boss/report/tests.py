"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

# from django.test import TestCase
#
#
# class SimpleTest(TestCase):
#     def test_basic_addition(self):
#         """
#         Tests that 1 + 1 always equals 2.
#         """
#         self.assertEqual(1 + 1, 2)

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE","boss.settings")
from man.models import AuthUser, AuthPermission, AuthUserUserPermissions
from report.models import *
from man.models import AuthPermission
from django.db.models import Sum
# users = AuthUser.objects.all()
# permissions = AuthPermission.objects.filter(content_type_id=204)
# for user in users:
#     for permission in permissions:
#         AuthUserUserPermissions(user=user, permission=permission).save()

# business_sumamries = TongjiRpDTurnoverBusinessSummary.objects.filter(app_id="10").values("channel_no").annotate(Sum("total_order_count")).\
#     annotate(Sum("total_pay_price")).annotate(Sum("total_user_count")).annotate(Sum("avg_user_order_count")).annotate(Sum("avg_order_pay")).\
#     annotate(Sum("arpu"))
# for summary in business_sumamries:
#     print(summary)
AuthUserUserPermissions.objects.filter(user_id=1).delete()
authpermissions = AuthPermission.objects.filter(id__gte=34)
for authpermission in authpermissions:
    AuthUserUserPermissions(user_id=1, permission=authpermission).save()