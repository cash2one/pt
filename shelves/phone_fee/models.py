# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.
# coding:utf-8

from django.db import models

class PtDaojiaOrder(models.Model):
    subject = models.CharField(max_length=256)
    goodsid = models.BigIntegerField(null=True, db_column=u'goodsId', blank=True) # Field name made lowercase.
    cpgoodsid = models.CharField(max_length=64, db_column=u'cpGoodsId', blank=True) # Field name made lowercase.
    order_no = models.CharField(max_length=50)
    cporderno = models.CharField(max_length=100, db_column=u'cpOrderNo', blank=True) # Field name made lowercase.
    provider = models.CharField(max_length=64, blank=True)
    providermobile = models.CharField(max_length=16, db_column=u'providerMobile', blank=True) # Field name made lowercase.
    payway = models.IntegerField(db_column=u'payWay') # Field name made lowercase.
    service_time = models.DateTimeField()
    service_length = models.IntegerField(null=True, blank=True)
    city = models.CharField(max_length=32)
    area = models.CharField(max_length=32, blank=True)
    service_address = models.CharField(max_length=256)
    longtitude = models.FloatField()
    latitude = models.FloatField()
    staffid = models.CharField(max_length=100, db_column=u'staffId', blank=True) # Field name made lowercase.
    staffname = models.CharField(max_length=32, db_column=u'staffName', blank=True) # Field name made lowercase.
    staffphone = models.CharField(max_length=16, db_column=u'staffPhone', blank=True) # Field name made lowercase.
    staffheadurl = models.CharField(max_length=512, db_column=u'staffHeadUrl', blank=True) # Field name made lowercase.
    consumer = models.CharField(max_length=32)
    consumermobile = models.CharField(max_length=16, db_column=u'consumerMobile') # Field name made lowercase.
    pt_username = models.CharField(max_length=50, blank=True)
    quantity = models.IntegerField(null=True, blank=True)
    price = models.IntegerField(null=True, blank=True)
    comment = models.CharField(max_length=1024, blank=True)
    pay_price = models.BigIntegerField()
    create_time = models.DateTimeField()
    modify_time = models.DateTimeField()
    appid = models.BigIntegerField(db_column=u'appId') # Field name made lowercase.
    goodsname = models.CharField(max_length=64, db_column=u'goodsName', blank=True) # Field name made lowercase.
    status = models.IntegerField(null=True, blank=True)
    cancel_by = models.IntegerField(null=True, blank=True)
    cancel_msg = models.CharField(max_length=512, blank=True)
    amount = models.BigIntegerField(null=True, blank=True)
    simple_address = models.CharField(max_length=128, blank=True)
    service_type = models.IntegerField(null=True, blank=True)
    extrainfo = models.CharField(max_length=256, db_column=u'extraInfo', blank=True) # Field name made lowercase.
    sku = models.CharField(max_length=256, blank=True)
    staff_sex = models.IntegerField(null=True, blank=True)
    promotion_activity_info = models.CharField(max_length=1024, blank=True)
    goodscustomizeorderinfo = models.CharField(max_length=1024, db_column=u'goodsCustomizeOrderInfo', blank=True) # Field name made lowercase.
    is_later_pay_order = models.IntegerField()
    status_desc = models.CharField(max_length=255, blank=True)
    pay_status = models.IntegerField()
    set_price_time = models.DateTimeField(null=True, blank=True)
    pt_u_id = models.CharField(max_length=50, blank=True)
    goodsicon = models.CharField(max_length=512, db_column=u'goodsIcon', blank=True) # Field name made lowercase.
    source_channel = models.IntegerField(null=True, blank=True)
    pt_comment = models.CharField(max_length=256, blank=True)
    attr_160314 = models.CharField(max_length=1024, blank=True)
    is_shopping_car = models.IntegerField(null=True, blank=True)
    is_shopping_car_goods = models.IntegerField(null=True, blank=True)
    user_sex = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'pt_daojia_order'

class PtDaojiaOrderGuarantee(models.Model):
    order_no = models.CharField(max_length=50)
    g_type = models.CharField(max_length=50, unique=True)
    status = models.IntegerField(null=True, blank=True)
    g_status = models.IntegerField()
    order_create_time = models.DateTimeField()
    order_modify_time = models.DateTimeField(null=True, blank=True)
    order_service_time = models.DateTimeField()
    check_status = models.IntegerField()
    pt_comment = models.CharField(max_length=1024, blank=True)
    c_time = models.DateTimeField(null=True, blank=True)
    m_time = models.DateTimeField()
    is_notify = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'pt_daojia_order_guarantee'

# class PtGyPhoneFeeProduct(models.Model):
#     id = models.BigIntegerField(primary_key=True)
#     prod_id = models.CharField(max_length=50, blank=True)
#     prod_content = models.CharField(max_length=50, blank=True)
#     prod_price = models.CharField(max_length=50, blank=True)
#     prod_province_id = models.CharField(max_length=50, blank=True)
#     prod_delaytimes = models.CharField(max_length=50, blank=True)
#     prod_isptype = models.CharField(max_length=50, blank=True)
#     prod_type = models.CharField(max_length=50, blank=True)
#     putao_price = models.CharField(max_length=50, blank=True)
#     margin_price = models.CharField(max_length=50, blank=True)
#     prod_name = models.CharField(max_length=150, blank=True)
#     c_time = models.DateTimeField(null=True, blank=True)
#     update_time = models.DateTimeField(null=True, blank=True)
#     subject = models.CharField(max_length=100, blank=True)
#     body = models.CharField(max_length=100, blank=True)
#     basic_cp_price = models.CharField(max_length=30, blank=True)
#     pt_prodid = models.CharField(max_length=50, blank=True)
#     status = models.IntegerField(null=True, blank=True)
#     class Meta:
#         db_table = u'pt_gy_phone_fee_product'
#
# class PtNnkPhoneFeeProduct(models.Model):
#     id = models.BigIntegerField(primary_key=True)
#     prod_id = models.CharField(max_length=50, blank=True)
#     prod_price = models.CharField(max_length=50, blank=True)
#     prod_content = models.CharField(max_length=50, blank=True)
#     prod_province_id = models.CharField(max_length=50, blank=True)
#     prod_isptype = models.CharField(max_length=50, blank=True)
#     prod_name = models.CharField(max_length=150, blank=True)
#     c_time = models.DateTimeField(null=True, blank=True)
#     update_time = models.DateTimeField()
#     basic_cp_price = models.CharField(max_length=30, blank=True)
#     pt_prodid = models.CharField(max_length=50, blank=True)
#     status = models.IntegerField()
#     class Meta:
#         db_table = u'pt_nnk_phone_fee_product'
#
# class PtPayOrder(models.Model):
#     id = models.BigIntegerField(primary_key=True)
#     order_no = models.CharField(max_length=50, blank=True)
#     name = models.CharField(max_length=100, blank=True)
#     mark_price = models.CharField(max_length=30, blank=True)
#     discount = models.IntegerField(null=True, blank=True)
#     product_id = models.BigIntegerField(null=True, blank=True)
#     product_type = models.IntegerField(null=True, blank=True)
#     pay_price = models.BigIntegerField(null=True, blank=True)
#     pt_u_id = models.CharField(max_length=50, blank=True)
#     dev_no = models.CharField(max_length=100, blank=True)
#     coupon_ids = models.CharField(max_length=50, blank=True)
#     favo_price = models.BigIntegerField(null=True, blank=True)
#     c_time = models.DateTimeField(null=True, blank=True)
#     m_time = models.DateTimeField()
#     product_name = models.CharField(max_length=100, blank=True)
#     payment_type = models.IntegerField(null=True, blank=True)
#     shipper_code = models.CharField(max_length=50, blank=True)
#     status = models.IntegerField(null=True, blank=True)
#     sub_item_info = models.TextField(blank=True)
#     channel_no = models.CharField(max_length=256, blank=True)
#     channel_version = models.CharField(max_length=256, blank=True)
#     channel_id = models.IntegerField(null=True, blank=True)
#     pay_channel_no = models.CharField(max_length=50, blank=True)
#     app_id = models.CharField(max_length=20, blank=True)
#     is_active_cancel = models.IntegerField(null=True, blank=True)
#     cp_id = models.CharField(max_length=10, blank=True)
#     not_show = models.IntegerField(null=True, blank=True)
#     parent_channel = models.CharField(max_length=50, blank=True)
#     class Meta:
#         db_table = u'pt_pay_order'
#
# class PtPayRefund(models.Model):
#     id = models.BigIntegerField(primary_key=True)
#     order_no = models.CharField(max_length=50)
#     refund_status = models.CharField(max_length=100, blank=True)
#     pt_u_id = models.CharField(max_length=50, blank=True)
#     status = models.CharField(max_length=100, blank=True)
#     is_send_refund_email = models.IntegerField()
#     refund_amount = models.BigIntegerField()
#     refund_time = models.DateTimeField(null=True, blank=True)
#     c_time = models.DateTimeField(null=True, blank=True)
#     m_time = models.DateTimeField(null=True, blank=True)
#     refund_count = models.IntegerField(null=True, blank=True)
#     remark = models.CharField(max_length=255, blank=True)
#     payment_type = models.IntegerField(null=True, blank=True)
#     product_type = models.IntegerField(null=True, blank=True)
#     is_option = models.IntegerField(null=True, blank=True)
#     class Meta:
#         db_table = u'pt_pay_refund'
#
class PtPhoneFeeProduct(models.Model):
    id = models.BigIntegerField(primary_key=True)
    prod_name = models.CharField(max_length=150, blank=True)
    prod_content = models.CharField(max_length=50, blank=True)
    prod_price = models.CharField(max_length=50, blank=True)
    purchase_price = models.CharField(max_length=50, blank=True)
    app_id = models.CharField(max_length=50, blank=True)
    status = models.IntegerField(null=True, blank=True)
    message = models.CharField(max_length=200, blank=True)
    is_special = models.IntegerField(null=True, blank=True)
    start_time = models.CharField(max_length=100, blank=True)
    end_time = models.CharField(max_length=100, blank=True)
    updown_status = models.IntegerField(null=True, blank=True)
    c_time = models.DateTimeField(auto_now_add=True)
    m_time = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = u'pt_phone_fee_product'
#
class PtPhonefeeCpRelation(models.Model):
    pt_prod_id = models.BigIntegerField(primary_key=True)
    cp_prod_id = models.BigIntegerField(null=True, blank=True)
    cp_name = models.CharField(max_length=50, blank=True)
    class Meta:
        db_table = u'pt_phonefee_cp_relation'
#
# class VwDaojiaOvertimeOrderNotify(models.Model):
#     order_no = models.CharField(max_length=50)
#     provider = models.CharField(max_length=64, blank=True)
#     consumer = models.CharField(max_length=32, blank=True)
#     consumermobile = models.CharField(max_length=16, db_column=u'consumerMobile', blank=True) # Field name made lowercase.
#     create_time = models.DateTimeField(null=True, blank=True)
#     class Meta:
#         db_table = u'vw_daojia_overtime_order_notify'
#

class CpPhoneFeeProduct(models.Model):
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
    c_time = models.DateTimeField(auto_now_add=True)
    m_time = models.DateTimeField(auto_now=True)
    class Meta:
        managed = False
        db_table = 'cp_phone_fee_product'
