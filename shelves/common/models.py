# coding: utf-8

"""
    rds2seb3yiymjlg8gumzv.mysql.rds.aliyuncs.com
    pt_biz_report
"""

from django.db import models


# class VwPtOrderReportSummaryTotal(models.Model):
#     category = models.CharField(max_length=2, primary_key=True)
#     date = models.CharField(max_length=10, blank=True, primary_key=True)
#     order_normal_status = models.CharField(max_length=2, blank=True)
#     order_total_pay = models.FloatField(null=True, blank=True)
#     order_sum_count = models.DecimalField(null=True, max_digits=42, decimal_places=0, blank=True)
#     order_success_count = models.DecimalField(null=True, max_digits=42, decimal_places=0, blank=True)
#     order_processing_count = models.DecimalField(null=True, max_digits=42, decimal_places=0, blank=True)
#     order_failed_count = models.DecimalField(null=True, max_digits=42, decimal_places=0, blank=True)
#     refund_success_count = models.DecimalField(null=True, max_digits=42, decimal_places=0, blank=True)
#     refund_failed_count = models.DecimalField(null=True, max_digits=42, decimal_places=0, blank=True)
#     refund_processing_count = models.DecimalField(null=True, max_digits=42, decimal_places=0, blank=True)
#     alipay_get_money = models.FloatField(null=True, blank=True)
#     wx_get_money = models.FloatField(null=True, blank=True)
#     other_get_money = models.FloatField(null=True, blank=True)
#     alipay_refund_money = models.FloatField(null=True, blank=True)
#     wx_refund_money = models.FloatField(null=True, blank=True)
#     other_refund_money = models.FloatField(null=True, blank=True)
#     alipay_service_money = models.FloatField(null=True, blank=True)
#     wx_service_money = models.FloatField(null=True, blank=True)
#     cp_should_take_money = models.FloatField(null=True, blank=True)
#     cp_reality_take_money = models.FloatField(null=True, blank=True)
#     cp_refund_money = models.FloatField(null=True, blank=True)
#     operation_cost = models.FloatField(null=True, blank=True)
#     operation_cost_q = models.FloatField(null=True, blank=True)
#     gain_money = models.FloatField(null=True, blank=True)
#     class Meta:
#         db_table = u'vw_pt_order_report_summary_total'


# class VwPtOrderReportSummaryPhoneFee(models.Model):
#     category = models.CharField(max_length=50, blank=True, primary_key=True)
#     date = models.CharField(max_length=10, blank=True, primary_key=True)
#     order_normal_status = models.CharField(max_length=2, blank=True)
#     order_total_pay = models.FloatField(null=True, blank=True)
#     order_sum_count = models.DecimalField(null=True, max_digits=42, decimal_places=0, blank=True)
#     order_success_count = models.DecimalField(null=True, max_digits=42, decimal_places=0, blank=True)
#     order_processing_count = models.DecimalField(null=True, max_digits=42, decimal_places=0, blank=True)
#     order_failed_count = models.DecimalField(null=True, max_digits=42, decimal_places=0, blank=True)
#     refund_success_count = models.DecimalField(null=True, max_digits=42, decimal_places=0, blank=True)
#     refund_failed_count = models.DecimalField(null=True, max_digits=42, decimal_places=0, blank=True)
#     refund_processing_count = models.DecimalField(null=True, max_digits=42, decimal_places=0, blank=True)
#     alipay_get_money = models.FloatField(null=True, blank=True)
#     wx_get_money = models.FloatField(null=True, blank=True)
#     other_get_money = models.FloatField(null=True, blank=True)
#     alipay_refund_money = models.FloatField(null=True, blank=True)
#     wx_refund_money = models.FloatField(null=True, blank=True)
#     other_refund_money = models.FloatField(null=True, blank=True)
#     alipay_service_money = models.FloatField(null=True, blank=True)
#     wx_service_money = models.FloatField(null=True, blank=True)
#     cp_should_take_money = models.FloatField(null=True, blank=True)
#     cp_reality_take_money = models.FloatField(null=True, blank=True)
#     cp_refund_money = models.FloatField(null=True, blank=True)
#     operation_cost = models.FloatField(null=True, blank=True)
#     operation_cost_q = models.FloatField(null=True, blank=True)
#     gain_money = models.FloatField(null=True, blank=True)
#     class Meta:
#         db_table = u'vw_pt_order_report_summary_phone_fee'


# class VwPtOrderReportSummaryFlow(models.Model):
#     category = models.CharField(max_length=50, blank=True, primary_key=True)
#     date = models.CharField(max_length=10, blank=True, primary_key=True)
#     order_normal_status = models.CharField(max_length=2, blank=True)
#     order_total_pay = models.FloatField(null=True, blank=True)
#     order_sum_count = models.DecimalField(null=True, max_digits=42, decimal_places=0, blank=True)
#     order_success_count = models.DecimalField(null=True, max_digits=42, decimal_places=0, blank=True)
#     order_processing_count = models.DecimalField(null=True, max_digits=42, decimal_places=0, blank=True)
#     order_failed_count = models.DecimalField(null=True, max_digits=42, decimal_places=0, blank=True)
#     refund_success_count = models.DecimalField(null=True, max_digits=42, decimal_places=0, blank=True)
#     refund_failed_count = models.DecimalField(null=True, max_digits=42, decimal_places=0, blank=True)
#     refund_processing_count = models.DecimalField(null=True, max_digits=42, decimal_places=0, blank=True)
#     alipay_get_money = models.FloatField(null=True, blank=True)
#     wx_get_money = models.FloatField(null=True, blank=True)
#     other_get_money = models.FloatField(null=True, blank=True)
#     alipay_refund_money = models.FloatField(null=True, blank=True)
#     wx_refund_money = models.FloatField(null=True, blank=True)
#     other_refund_money = models.FloatField(null=True, blank=True)
#     alipay_service_money = models.FloatField(null=True, blank=True)
#     wx_service_money = models.FloatField(null=True, blank=True)
#     cp_should_take_money = models.FloatField(null=True, blank=True)
#     cp_reality_take_money = models.FloatField(null=True, blank=True)
#     cp_refund_money = models.FloatField(null=True, blank=True)
#     operation_cost = models.FloatField(null=True, blank=True)
#     operation_cost_q = models.FloatField(null=True, blank=True)
#     gain_money = models.FloatField(null=True, blank=True)
#     class Meta:
#         db_table = u'vw_pt_order_report_summary_flow'


# class VwPtOrderReportSummaryMovie(models.Model):
#     category = models.CharField(max_length=50, blank=True, primary_key=True)
#     date = models.CharField(max_length=10, blank=True, primary_key=True)
#     order_normal_status = models.CharField(max_length=2, blank=True)
#     order_total_pay = models.FloatField(null=True, blank=True)
#     order_sum_count = models.DecimalField(null=True, max_digits=42, decimal_places=0, blank=True)
#     order_success_count = models.DecimalField(null=True, max_digits=42, decimal_places=0, blank=True)
#     order_processing_count = models.DecimalField(null=True, max_digits=42, decimal_places=0, blank=True)
#     order_failed_count = models.DecimalField(null=True, max_digits=42, decimal_places=0, blank=True)
#     refund_success_count = models.DecimalField(null=True, max_digits=42, decimal_places=0, blank=True)
#     refund_failed_count = models.DecimalField(null=True, max_digits=42, decimal_places=0, blank=True)
#     refund_processing_count = models.DecimalField(null=True, max_digits=42, decimal_places=0, blank=True)
#     alipay_get_money = models.FloatField(null=True, blank=True)
#     wx_get_money = models.FloatField(null=True, blank=True)
#     other_get_money = models.FloatField(null=True, blank=True)
#     alipay_refund_money = models.FloatField(null=True, blank=True)
#     wx_refund_money = models.FloatField(null=True, blank=True)
#     other_refund_money = models.FloatField(null=True, blank=True)
#     alipay_service_money = models.FloatField(null=True, blank=True)
#     wx_service_money = models.FloatField(null=True, blank=True)
#     cp_should_take_money = models.FloatField(null=True, blank=True)
#     cp_reality_take_money = models.FloatField(null=True, blank=True)
#     cp_refund_money = models.FloatField(null=True, blank=True)
#     operation_cost = models.FloatField(null=True, blank=True)
#     operation_cost_q = models.FloatField(null=True, blank=True)
#     gain_money = models.FloatField(null=True, blank=True)
#     class Meta:
#         db_table = u'vw_pt_order_report_summary_movie'


# class VwPtOrderReportSummaryTrain(models.Model):
#     category = models.CharField(max_length=50, blank=True, primary_key=True)
#     date = models.CharField(max_length=10, blank=True, primary_key=True)
#     order_normal_status = models.CharField(max_length=2, blank=True)
#     order_total_pay = models.FloatField(null=True, blank=True)
#     order_sum_count = models.DecimalField(null=True, max_digits=42, decimal_places=0, blank=True)
#     order_success_count = models.DecimalField(null=True, max_digits=42, decimal_places=0, blank=True)
#     order_processing_count = models.DecimalField(null=True, max_digits=42, decimal_places=0, blank=True)
#     order_failed_count = models.DecimalField(null=True, max_digits=42, decimal_places=0, blank=True)
#     refund_success_count = models.DecimalField(null=True, max_digits=42, decimal_places=0, blank=True)
#     refund_failed_count = models.DecimalField(null=True, max_digits=42, decimal_places=0, blank=True)
#     refund_processing_count = models.DecimalField(null=True, max_digits=42, decimal_places=0, blank=True)
#     alipay_get_money = models.FloatField(null=True, blank=True)
#     wx_get_money = models.FloatField(null=True, blank=True)
#     other_get_money = models.FloatField(null=True, blank=True)
#     alipay_refund_money = models.FloatField(null=True, blank=True)
#     wx_refund_money = models.FloatField(null=True, blank=True)
#     other_refund_money = models.FloatField(null=True, blank=True)
#     alipay_service_money = models.FloatField(null=True, blank=True)
#     wx_service_money = models.FloatField(null=True, blank=True)
#     cp_should_take_money = models.FloatField(null=True, blank=True)
#     cp_reality_take_money = models.FloatField(null=True, blank=True)
#     cp_refund_money = models.FloatField(null=True, blank=True)
#     operation_cost = models.FloatField(null=True, blank=True)
#     operation_cost_q = models.FloatField(null=True, blank=True)
#     gain_money = models.FloatField(null=True, blank=True)
#     class Meta:
#         db_table = u'vw_pt_order_report_summary_train'


# class VwPtOrderReportSummaryHotel(models.Model):
#     category = models.CharField(max_length=50, blank=True, primary_key=True)
#     date = models.CharField(max_length=10, blank=True, primary_key=True)
#     order_normal_status = models.CharField(max_length=2, blank=True)
#     order_total_pay = models.FloatField(null=True, blank=True)
#     order_sum_count = models.DecimalField(null=True, max_digits=42, decimal_places=0, blank=True)
#     order_success_count = models.DecimalField(null=True, max_digits=42, decimal_places=0, blank=True)
#     order_processing_count = models.DecimalField(null=True, max_digits=42, decimal_places=0, blank=True)
#     order_failed_count = models.DecimalField(null=True, max_digits=42, decimal_places=0, blank=True)
#     refund_success_count = models.DecimalField(null=True, max_digits=42, decimal_places=0, blank=True)
#     refund_failed_count = models.DecimalField(null=True, max_digits=42, decimal_places=0, blank=True)
#     refund_processing_count = models.DecimalField(null=True, max_digits=42, decimal_places=0, blank=True)
#     alipay_get_money = models.FloatField(null=True, blank=True)
#     wx_get_money = models.FloatField(null=True, blank=True)
#     other_get_money = models.FloatField(null=True, blank=True)
#     alipay_refund_money = models.FloatField(null=True, blank=True)
#     wx_refund_money = models.FloatField(null=True, blank=True)
#     other_refund_money = models.FloatField(null=True, blank=True)
#     alipay_service_money = models.FloatField(null=True, blank=True)
#     wx_service_money = models.FloatField(null=True, blank=True)
#     cp_should_take_money = models.FloatField(null=True, blank=True)
#     cp_reality_take_money = models.FloatField(null=True, blank=True)
#     cp_refund_money = models.FloatField(null=True, blank=True)
#     operation_cost = models.FloatField(null=True, blank=True)
#     operation_cost_q = models.FloatField(null=True, blank=True)
#     gain_money = models.FloatField(null=True, blank=True)
#     class Meta:
#         db_table = u'vw_pt_order_report_summary_hotel'


# class VwPtOrderReportSummaryWec(models.Model):
#     category = models.CharField(max_length=50, blank=True, primary_key=True)
#     date = models.CharField(max_length=10, blank=True, primary_key=True)
#     order_normal_status = models.CharField(max_length=2, blank=True)
#     order_total_pay = models.FloatField(null=True, blank=True)
#     order_sum_count = models.DecimalField(null=True, max_digits=42, decimal_places=0, blank=True)
#     order_success_count = models.DecimalField(null=True, max_digits=42, decimal_places=0, blank=True)
#     order_processing_count = models.DecimalField(null=True, max_digits=42, decimal_places=0, blank=True)
#     order_failed_count = models.DecimalField(null=True, max_digits=42, decimal_places=0, blank=True)
#     refund_success_count = models.DecimalField(null=True, max_digits=42, decimal_places=0, blank=True)
#     refund_failed_count = models.DecimalField(null=True, max_digits=42, decimal_places=0, blank=True)
#     refund_processing_count = models.DecimalField(null=True, max_digits=42, decimal_places=0, blank=True)
#     alipay_get_money = models.FloatField(null=True, blank=True)
#     wx_get_money = models.FloatField(null=True, blank=True)
#     other_get_money = models.FloatField(null=True, blank=True)
#     alipay_refund_money = models.FloatField(null=True, blank=True)
#     wx_refund_money = models.FloatField(null=True, blank=True)
#     other_refund_money = models.FloatField(null=True, blank=True)
#     alipay_service_money = models.FloatField(null=True, blank=True)
#     wx_service_money = models.FloatField(null=True, blank=True)
#     cp_should_take_money = models.FloatField(null=True, blank=True)
#     cp_reality_take_money = models.FloatField(null=True, blank=True)
#     cp_refund_money = models.FloatField(null=True, blank=True)
#     operation_cost = models.FloatField(null=True, blank=True)
#     operation_cost_q = models.FloatField(null=True, blank=True)
#     gain_money = models.FloatField(null=True, blank=True)
#     class Meta:
#         db_table = u'vw_pt_order_report_summary_wec'


# class VwPtOrderReportSummaryQb(models.Model):
#     category = models.CharField(max_length=50, blank=True, primary_key=True)
#     date = models.CharField(max_length=10, blank=True, primary_key=True)
#     order_normal_status = models.CharField(max_length=2, blank=True)
#     order_total_pay = models.FloatField(null=True, blank=True)
#     order_sum_count = models.DecimalField(null=True, max_digits=42, decimal_places=0, blank=True)
#     order_success_count = models.DecimalField(null=True, max_digits=42, decimal_places=0, blank=True)
#     order_processing_count = models.DecimalField(null=True, max_digits=42, decimal_places=0, blank=True)
#     order_failed_count = models.DecimalField(null=True, max_digits=42, decimal_places=0, blank=True)
#     refund_success_count = models.DecimalField(null=True, max_digits=42, decimal_places=0, blank=True)
#     refund_failed_count = models.DecimalField(null=True, max_digits=42, decimal_places=0, blank=True)
#     refund_processing_count = models.DecimalField(null=True, max_digits=42, decimal_places=0, blank=True)
#     alipay_get_money = models.FloatField(null=True, blank=True)
#     wx_get_money = models.FloatField(null=True, blank=True)
#     other_get_money = models.FloatField(null=True, blank=True)
#     alipay_refund_money = models.FloatField(null=True, blank=True)
#     wx_refund_money = models.FloatField(null=True, blank=True)
#     other_refund_money = models.FloatField(null=True, blank=True)
#     alipay_service_money = models.FloatField(null=True, blank=True)
#     wx_service_money = models.FloatField(null=True, blank=True)
#     cp_should_take_money = models.FloatField(null=True, blank=True)
#     cp_reality_take_money = models.FloatField(null=True, blank=True)
#     cp_refund_money = models.FloatField(null=True, blank=True)
#     operation_cost = models.FloatField(null=True, blank=True)
#     operation_cost_q = models.FloatField(null=True, blank=True)
#     gain_money = models.FloatField(null=True, blank=True)
#     class Meta:
#         db_table = u'vw_pt_order_report_summary_qb'


class VwPtTongjiPayFailedList(models.Model):
    order_no = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=100, blank=True)
    price = models.DecimalField(null=True, max_digits=25, decimal_places=2, blank=True)
    c_time = models.CharField(max_length=48)
    product = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=6)
    refund_status = models.CharField(max_length=100, blank=True)
    product_type = models.IntegerField(null=True, blank=True)
    app_id = models.CharField(max_length=20, blank=True)
    app_version = models.CharField(max_length=100, blank=True)
    channel_no = models.CharField(max_length=60, blank=True)

    class Meta:
        db_table = u'vw_pt_tongji_pay_failed_list'


# class VwPtOrderReportSummaryMovieCp(models.Model):
#     category = models.CharField(max_length=50, blank=True, primary_key=True)
#     cp_name = models.CharField(max_length=255, blank=True, primary_key=True)
#     date = models.CharField(max_length=10, blank=True, primary_key=True)
#     order_normal_status = models.CharField(max_length=2, blank=True)
#     order_total_pay = models.FloatField(null=True, blank=True)
#     order_sum_count = models.IntegerField(null=True, blank=True)
#     order_success_count = models.IntegerField(null=True, blank=True)
#     order_processing_count = models.IntegerField(null=True, blank=True)
#     order_failed_count = models.IntegerField(null=True, blank=True)
#     refund_success_count = models.IntegerField(null=True, blank=True)
#     refund_failed_count = models.IntegerField(null=True, blank=True)
#     refund_processing_count = models.IntegerField(null=True, blank=True)
#     alipay_get_money = models.FloatField(null=True, blank=True)
#     wx_get_money = models.FloatField(null=True, blank=True)
#     other_get_money = models.FloatField(null=True, blank=True)
#     alipay_refund_money = models.FloatField(null=True, blank=True)
#     wx_refund_money = models.FloatField(null=True, blank=True)
#     other_refund_money = models.FloatField(null=True, blank=True)
#     alipay_service_money = models.FloatField(null=True, blank=True)
#     wx_service_money = models.FloatField(null=True, blank=True)
#     cp_should_take_money = models.FloatField(null=True, blank=True)
#     cp_reality_take_money = models.FloatField(null=True, blank=True)
#     cp_refund_money = models.FloatField(null=True, blank=True)
#     operation_cost = models.FloatField(null=True, blank=True)
#     operation_cost_q = models.FloatField(null=True, blank=True)
#     gain_money = models.FloatField(null=True, blank=True)
#     class Meta:
#         db_table = u'vw_pt_order_report_summary_movie_cp'


# class VwPtOperationCost(models.Model):
#     statdate = models.DateField(primary_key=True)
#     product_type = models.BigIntegerField(primary_key=True)
#     operation_cost_q = models.DecimalField(null=True, max_digits=47, decimal_places=4, blank=True)
#     gain_money = models.DecimalField(null=True, max_digits=47, decimal_places=4, blank=True)
#     cp_should_take_money = models.FloatField(null=True, blank=True)
#     cp_refund_money = models.BigIntegerField()
#     operation_cost = models.FloatField(null=True, blank=True)
#     class Meta:
#         db_table = u'vw_pt_operation_cost'


class TongjiPayProduct(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=100, blank=True)
    mark_price = models.IntegerField(null=True, blank=True)
    discount = models.IntegerField(null=True, blank=True)
    type = models.IntegerField(null=True, blank=True)
    shipper_code = models.CharField(max_length=20, blank=True)
    c_time = models.DateTimeField(null=True, blank=True)
    m_time = models.DateTimeField()

    class Meta:
        db_table = u'tongji_pay_product'


# class TongjiPayOrder(models.Model):
#     statdate = models.DateField(db_column='STATDATE', primary_key=True) # Field name made lowercase.
#     order_no = models.CharField(max_length=50, db_column='ORDER_NO', primary_key=True) # Field name made lowercase.
# Field name made lowercase.
#     pay_price = models.DecimalField(decimal_places=4, null=True, max_digits=25, db_column='PAY_PRICE', blank=True)
#     prod_price = models.CharField(max_length=53, db_column='PROD_PRICE', blank=True) # Field name made lowercase.
#     product_type = models.IntegerField(null=True, db_column='PRODUCT_TYPE', blank=True) # Field name made lowercase.
#     status = models.IntegerField(null=True, db_column='STATUS', blank=True) # Field name made lowercase.
#     pt_u_id = models.CharField(max_length=50, db_column='PT_U_ID', blank=True) # Field name made lowercase.
#     is_new_user = models.BigIntegerField(null=True, db_column='IS_NEW_USER', blank=True) # Field name made lowercase.
#     app_id = models.CharField(max_length=20, db_column='APP_ID', blank=True) # Field name made lowercase.
#     channel_no = models.CharField(max_length=60, db_column='CHANNEL_NO', blank=True) # Field name made lowercase.
#     app_version = models.CharField(max_length=100, db_column='APP_VERSION', blank=True) # Field name made lowercase.
#     c_time = models.DateTimeField(null=True, db_column='C_TIME', blank=True) # Field name made lowercase.
#     m_time = models.DateTimeField(null=True, db_column='M_TIME', blank=True) # Field name made lowercase.
# Field name made lowercase.
#     order_process_time = models.BigIntegerField(null=True, db_column='ORDER_PROCESS_TIME', blank=True)
#     payment_type = models.IntegerField(null=True, db_column='PAYMENT_TYPE', blank=True) # Field name made lowercase.
#     cp_id = models.CharField(max_length=10, db_column='CP_ID', blank=True) # Field name made lowercase.
# Field name made lowercase
#     favo_price = models.DecimalField(decimal_places=4, null=True, max_digits=25, db_column='FAVO_PRICE', blank=True).
#     class Meta:
#         db_table = u'tongji_pay_order'
#
#
# class TongjiGyFeeOrder(models.Model):
#     statdate = models.DateField(db_column='STATDATE', primary_key=True) # Field name made lowercase.
#     order_no = models.CharField(max_length=50, db_column='ORDER_NO', primary_key=True) # Field name made lowercase.
#     prod_province = models.CharField(max_length=50, blank=True)
#     prod_content = models.CharField(max_length=50, blank=True)
#     prod_isptype = models.CharField(max_length=50, blank=True)
#     class Meta:
#         db_table = u'tongji_gy_fee_order'


class VwPtTongjiFilter(models.Model):
    filter_name = models.CharField(max_length=21, primary_key=True)
    filter_content = models.CharField(max_length=341)

    class Meta:
        db_table = u'vw_pt_tongji_filter'


class PtCpInfo(models.Model):
    id = models.BigIntegerField(primary_key=True)
    server_key = models.CharField(max_length=100, blank=True)
    secret = models.CharField(max_length=20)
    c_time = models.DateField()
    remark = models.CharField(max_length=1000)
    product_type = models.CharField(max_length=100, blank=True)
    movie_is_sell_code = models.IntegerField(null=True, blank=True)
    logo_url = models.CharField(max_length=100, blank=True)
    status = models.IntegerField(null=True, blank=True)
    tele = models.CharField(max_length=20, blank=True)
    comment = models.CharField(max_length=200, blank=True)
    m_time = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = u'pt_cp_info'


class TongjiSysApp(models.Model):
    id = models.BigIntegerField(primary_key=True)
    app_id = models.BigIntegerField(null=True, blank=True)
    app_name = models.CharField(max_length=50, blank=True)
    app_key = models.CharField(max_length=50, unique=True, blank=True)
    app_type = models.CharField(max_length=32, blank=True)
    platform = models.CharField(max_length=20, blank=True)
    description = models.CharField(max_length=80, blank=True)
    status = models.IntegerField(null=True, blank=True)
    m_time = models.DateTimeField()
    c_time = models.DateTimeField()
    user_id = models.CharField(max_length=100)

    class Meta:
        db_table = u'tongji_sys_app'


class VwPtAppVersionFilter(models.Model):
    app_id = models.CharField(max_length=20, db_column='APP_ID', primary_key=True)  # Field name made lowercase.
    app_version = models.CharField(max_length=100, db_column='APP_VERSION',
                                   primary_key=True)  # Field name made lowercase.

    class Meta:
        db_table = u'vw_pt_app_version_filter'


class VwPtAppChannelNoFilter(models.Model):
    app_id = models.CharField(max_length=20, db_column='APP_ID', primary_key=True)  # Field name made lowercase.
    channel_no = models.CharField(max_length=60, db_column='CHANNEL_NO', primary_key=True)  # Field name made lowercase.

    class Meta:
        db_table = u'vw_pt_app_channel_no_filter'


# class TongjiCouponUse(models.Model):
#     statdate = models.DateField(primary_key=True)
#     activity_id = models.CharField(max_length=4, primary_key=True)
#     resource_id = models.BigIntegerField(primary_key=True)
#     description = models.CharField(max_length=255, blank=True)
#     money = models.FloatField(null=True, blank=True)
#     scope = models.CharField(max_length=64, blank=True)
#     resource_get = models.BigIntegerField()
#     resource_consume = models.BigIntegerField(null=True, blank=True)
#     class Meta:
#         db_table = u'tongji_coupon_use'

class TongjiRpDTurnoverSummary(models.Model):
    statdate = models.DateField(null=True, blank=True)
    stathour = models.CharField(max_length=20)
    app_id = models.CharField(max_length=60)
    app_version = models.CharField(max_length=300)
    channel_no = models.CharField(max_length=180)
    product_type = models.CharField(max_length=21)
    total_order_count = models.IntegerField(null=True, blank=True, verbose_name=u'交易数')
    total_prod_price = models.DecimalField(null=True, max_digits=47, decimal_places=4, blank=True, verbose_name=u'交易额')
    total_user_count = models.BigIntegerField(verbose_name=u'用户数')
    total_coupon_count = models.IntegerField(null=True, blank=True, verbose_name=u'用券数')
    total_coupon_cost = models.DecimalField(null=True, max_digits=47, decimal_places=4, blank=True, verbose_name=u'用券额')
    coupon_use_ratio = models.DecimalField(max_digits=28, decimal_places=2, verbose_name=u'交易占比')
    total_coupon_bring_order = models.DecimalField(null=True, max_digits=47, decimal_places=4, blank=True,
                                                   verbose_name=u'券带动消费金额')

    class Meta:
        db_table = u'tongji_rp_d_turnover_summary'


class TongjiRpDTurnoverTradeVolumeSummary(models.Model):
    statdate = models.DateField(null=True, blank=True)
    app_id = models.CharField(max_length=60)
    app_version = models.CharField(max_length=300)
    channel_no = models.CharField(max_length=180)
    product_type = models.CharField(max_length=21)
    total_pay_price = models.DecimalField(null=True, max_digits=45, decimal_places=4, blank=True, verbose_name=u'交易金额')
    total_order_success_price = models.DecimalField(null=True, max_digits=45, decimal_places=4, blank=True,
                                                    verbose_name=u'成功订单金额')
    total_order_failed_price = models.DecimalField(null=True, max_digits=45, decimal_places=4, blank=True,
                                                   verbose_name=u'失败订单金额')
    total_order_processing_price = models.DecimalField(null=True, max_digits=45, decimal_places=4, blank=True,
                                                       verbose_name=u'处理中订单金额')
    total_refund_processing_price = models.DecimalField(null=True, max_digits=45, decimal_places=4, blank=True,
                                                        verbose_name=u'退款中订单金额')
    total_refund_success_price = models.DecimalField(null=True, max_digits=45, decimal_places=4, blank=True,
                                                     verbose_name=u'退款成功订单金额')
    total_coupon_cost = models.DecimalField(null=True, max_digits=45, decimal_places=4, blank=True,
                                            verbose_name=u'用券核销额')

    class Meta:
        db_table = u'tongji_rp_d_turnover_trade_volume_summary'


class TongjiRpDTurnoverBusinessSummary(models.Model):
    statdate = models.DateField(null=True, blank=True)
    app_id = models.CharField(max_length=60)
    app_version = models.CharField(max_length=300)
    channel_no = models.CharField(max_length=180)
    product_type = models.CharField(max_length=21)
    total_order_count = models.IntegerField(null=True, blank=True, verbose_name=u'订单总数')
    total_pay_price = models.DecimalField(null=True, max_digits=45, decimal_places=4, blank=True, verbose_name=u'订单总金额')
    total_user_count = models.IntegerField(null=True, blank=True, verbose_name=u'用户数')
    total_order_pay_count = models.IntegerField(null=True, blank=True, verbose_name=u'订单支付数')
    total_order_success_count = models.IntegerField(null=True, blank=True, verbose_name=u'成功订单数')
    total_order_failed_count = models.IntegerField(null=True, blank=True, verbose_name=u'失败订单数')
    total_order_processing_count = models.IntegerField(null=True, blank=True, verbose_name=u'处理中订单数')
    total_refund_processing_count = models.IntegerField(null=True, blank=True, verbose_name=u'退款中订单数')
    total_refund_success_count = models.IntegerField(null=True, blank=True, verbose_name=u'退款成功订单数')
    total_coupon_count = models.IntegerField(null=True, blank=True, verbose_name=u'用券订单数')
    avg_user_order_count = models.DecimalField(null=True, max_digits=23, decimal_places=2, blank=True,
                                               verbose_name=u'人均笔数')
    avg_order_pay = models.DecimalField(null=True, max_digits=44, decimal_places=2, blank=True, verbose_name=u'客单价')
    arpu = models.DecimalField(null=True, max_digits=44, decimal_places=2, blank=True, verbose_name=u'ARPU值')

    class Meta:
        db_table = u'tongji_rp_d_turnover_business_summary'


class TongjiRpDTurnoverUserSummary(models.Model):
    statdate = models.DateField(null=True, blank=True)
    app_id = models.CharField(max_length=60)
    app_version = models.CharField(max_length=300)
    channel_no = models.CharField(max_length=180)
    product_type = models.CharField(max_length=21)
    total_user_count = models.IntegerField(null=True, blank=True, verbose_name=u'总用户数')
    total_pay_user_count = models.IntegerField(null=True, blank=True, verbose_name=u'交易用户数')
    first_order_user_count = models.IntegerField(null=True, blank=True, verbose_name=u'平台首购用户')
    reorder_user_count = models.IntegerField(null=True, blank=True, verbose_name=u'平台复购用户')
    first_product_order_user_count = models.IntegerField(null=True, blank=True, verbose_name=u'业务首购用户')
    product_reorder_user_count = models.IntegerField(null=True, blank=True, verbose_name=u'业务复购用户')

    class Meta:
        db_table = u'tongji_rp_d_turnover_user_summary'


class TongjiRpDTurnoverDaojiaServiceQuality(models.Model):
    statdate = models.DateField(null=True, blank=True)
    cp_name = models.CharField(max_length=45)
    app_id = models.CharField(max_length=60)
    app_version = models.CharField(max_length=300)
    channel_no = models.CharField(max_length=180)
    self_order_count = models.IntegerField(null=True, blank=True, verbose_name=u'订单总量')
    open_order_count = models.IntegerField(null=True, blank=True, verbose_name=u'成单转化')
    open_order_rate = models.DecimalField(null=True, max_digits=24, decimal_places=2, blank=True, verbose_name=u'成单转化率')
    cancel_order_count = models.IntegerField(null=True, blank=True, verbose_name=u'订单取消笔数')
    cancel_order_rate = models.DecimalField(null=True, max_digits=24, decimal_places=2, blank=True,
                                            verbose_name=u'订单取消率')
    cp_cancel_order_count = models.IntegerField(null=True, blank=True, verbose_name=u'商家取消笔数')
    cp_cancel_order_rate = models.DecimalField(null=True, max_digits=24, decimal_places=2, blank=True,
                                               verbose_name=u'商家取消率')
    error_order_count = models.IntegerField(null=True, blank=True, verbose_name=u'接口报警次数')
    avg_appointment_process_time = models.CharField(null=True, max_length=46, blank=True, verbose_name=u'接单时长')
    service_time_incorrect_count = models.IntegerField(null=True, blank=True, verbose_name=u'状态更新不及时次数')

    class Meta:
        db_table = u'tongji_rp_d_turnover_daojia_service_quality'


class TongjiRpDTurnoverActivitySummary(models.Model):
    statdate = models.DateField(null=True, blank=True)
    activity_id = models.CharField(max_length=60)
    app_id = models.CharField(max_length=60)
    app_version = models.CharField(max_length=300)
    channel_no = models.CharField(max_length=180)
    pv = models.IntegerField(null=True, blank=True, verbose_name=u'PV')
    uv = models.IntegerField(null=True, blank=True, verbose_name=u'UV')
    coupon_get_count = models.IntegerField(null=True, blank=True, verbose_name=u'优惠券领券次数')
    unique_user_coupon_get_count = models.IntegerField(null=True, blank=True, verbose_name=u'独立用户领券数')
    converted_order_count = models.IntegerField(null=True, blank=True, verbose_name=u'订单转化')
    convertion_rate = models.DecimalField(null=True, max_digits=24, decimal_places=2, blank=True, verbose_name=u'转化率')
    activity_name = models.CharField(max_length=255)

    class Meta:
        db_table = u'tongji_rp_d_turnover_activity_summary'
