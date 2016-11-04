# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
# coding: utf-8

from __future__ import unicode_literals

from django.db import models


# class PtGyFlowProduct(models.Model):
#     prodid = models.CharField(max_length=50, blank=True, null=True)
#     prod_content = models.CharField(max_length=30, blank=True, null=True)
#     prod_price = models.CharField(max_length=30, blank=True, null=True)
#     prod_isptype = models.CharField(max_length=30, blank=True, null=True)
#     prod_delaytimes = models.CharField(max_length=30, blank=True, null=True)
#     prod_provinceid = models.CharField(max_length=30, blank=True, null=True)
#     prod_type = models.CharField(max_length=30, blank=True, null=True)
#     putao_price = models.CharField(max_length=30, blank=True, null=True)
#     traffic_value = models.CharField(max_length=30, blank=True, null=True)
#     user_scope = models.CharField(max_length=30, blank=True, null=True)
#     valid_time = models.CharField(max_length=30, blank=True, null=True)
#     charge_count = models.CharField(max_length=255, blank=True, null=True)
#     support_user = models.CharField(max_length=255, blank=True, null=True)
#     charge_scope = models.CharField(max_length=50, blank=True, null=True)
#     traffic_effective_period = models.CharField(max_length=150, blank=True, null=True)
#     c_time = models.DateTimeField(blank=True, null=True)
#     update_time = models.DateTimeField(blank=True, null=True)
#     basic_cp_price = models.CharField(max_length=30, blank=True, null=True)
#     pt_prodid = models.CharField(max_length=50, blank=True, null=True)
#     status = models.IntegerField(blank=True, null=True)
#
#     class Meta:
#         managed = False
#         db_table = 'pt_gy_flow_product'
#
#
# class PtLbFlowProduct(models.Model):
#     id = models.IntegerField(blank=True, null=True)
#     prodid = models.CharField(max_length=150, blank=True, null=True)
#     prod_price = models.CharField(max_length=90, blank=True, null=True)
#     prod_isptype = models.CharField(max_length=90, blank=True, null=True)
#     prod_provinceid = models.CharField(max_length=90, blank=True, null=True)
#     traffic_value = models.CharField(max_length=90, blank=True, null=True)
#     charge_scope = models.CharField(max_length=150, blank=True, null=True)
#     c_time = models.DateTimeField(blank=True, null=True)
#     update_time = models.DateTimeField()
#     basic_cp_price = models.CharField(max_length=90, blank=True, null=True)
#     pt_prodid = models.CharField(max_length=150, blank=True, null=True)
#     status = models.IntegerField(blank=True, null=True)
#
#     class Meta:
#         managed = False
#         db_table = 'pt_lb_flow_product'


class CpPhoneFlowProduct(models.Model):
    id = models.AutoField(primary_key=True)
    cp_id = models.BigIntegerField(blank=True, null=True)
    cp_name = models.CharField(max_length=3)
    prod_id = models.CharField(max_length=50,blank=True, null=True)
    prod_content = models.CharField(max_length=50)
    prod_price = models.DecimalField(max_digits=10, decimal_places=2)
    prod_province_id = models.CharField(max_length=50)
    prod_isptype = models.CharField(max_length=50)
    prod_name = models.CharField(max_length=150, blank=True, null=True)
    putao_price = models.DecimalField(max_digits=10, decimal_places=2)
    is_able = models.BigIntegerField(blank=True, null=True)
    default_message = models.CharField(max_length=100, blank=True, null=True)
    traffic_value = models.CharField(max_length=100)
    c_time = models.DateTimeField(auto_now_add=True)
    m_time = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'cp_phone_flow_product'


class PtPhoneFlowProduct(models.Model):
    id = models.AutoField(primary_key=True)
    prod_name = models.CharField(max_length=50, blank=True, null=True)
    prod_content = models.CharField(max_length=100, blank=True, null=True)
    putao_price = models.CharField(max_length=100, blank=True, null=True)
    traffic_value = models.CharField(max_length=100, blank=True, null=True)
    user_scope = models.CharField(max_length=200, blank=True, null=True)
    valid_time = models.CharField(max_length=200, blank=True, null=True)
    charge_count = models.CharField(max_length=200, blank=True, null=True)
    support_user = models.CharField(max_length=200, blank=True, null=True)
    traffic_effective_period = models.CharField(max_length=200, blank=True, null=True)
    prod_delaytimes = models.CharField(max_length=50)
    message = models.CharField(max_length=200, blank=True, null=True)
    app_id = models.CharField(max_length=50, blank=True, null=True)
    status = models.CharField(max_length=50, blank=True, null=True)
    purchase_price = models.CharField(max_length=50, blank=True, null=True)
    is_special = models.IntegerField(blank=True, null=True)
    start_time = models.CharField(max_length=100, blank=True)
    end_time = models.CharField(max_length=100, blank=True)
    updown_status = models.IntegerField(null=True, blank=True)
    c_time = models.DateTimeField(auto_now_add=True)
    m_time = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'pt_phone_flow_product'


class PtPhoneflowCpRelation(models.Model):
    pt_prod_id = models.BigIntegerField(primary_key=True)
    cp_prod_id = models.BigIntegerField(blank=True, null=True)
    cp_name = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pt_phoneflow_cp_relation'

# class PtXcnewFlowProduct(models.Model):
#     prodid = models.CharField(max_length=50, blank=True, null=True)
#     prod_price = models.CharField(max_length=30, blank=True, null=True)
#     prod_isptype = models.CharField(max_length=30, blank=True, null=True)
#     prod_provinceid = models.CharField(max_length=30, blank=True, null=True)
#     traffic_value = models.CharField(max_length=30, blank=True, null=True)
#     charge_scope = models.CharField(max_length=50, blank=True, null=True)
#     c_time = models.DateTimeField(blank=True, null=True)
#     update_time = models.DateTimeField()
#     basic_cp_price = models.CharField(max_length=30, blank=True, null=True)
#     pt_prodid = models.CharField(max_length=50, blank=True, null=True)
#     status = models.IntegerField(blank=True, null=True)
#
#     class Meta:
#         managed = False
#         db_table = 'pt_xcnew_flow_product'
