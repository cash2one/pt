#coding: utf-8

"""
    rds2seb3yiymjlg8gumzv.mysql.rds.aliyuncs.com
    pt_biz_report
"""

from django.db import models

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
    app_id = models.CharField(max_length=20, db_column='APP_ID', primary_key=True) # Field name made lowercase.
    app_version = models.CharField(max_length=100, db_column='APP_VERSION', primary_key=True) # Field name made lowercase.
    class Meta:
        db_table = u'vw_pt_app_version_filter'


class VwPtAppChannelNoFilter(models.Model):
    app_id = models.CharField(max_length=20, db_column='APP_ID', primary_key=True) # Field name made lowercase.
    channel_no = models.CharField(max_length=60, db_column='CHANNEL_NO', primary_key=True) # Field name made lowercase.
    class Meta:
        db_table = u'vw_pt_app_channel_no_filter'

class VmPtCpBillsFilter(models.Model):
    cp_id = models.BigIntegerField(max_length=20, db_column='id')
    '''server_key = models.CharField(max_length=100, db_column='server_key', blank=True)
    secret = models.CharField(max_length=20, db_column='secret', blank=True)
    c_time = models.DateTimeField()'''
    remark = models.CharField(max_length=1000, db_column='remark')
    product_type = models.CharField(max_length=100, db_column='product_type')
    '''movie_is_sell_code = models.IntegerField(max_length=10, db_column='movie_is_sell_code')
    logo_url = models.CharField(max_length=100, db_column='logo_url', blank=True)
    status = models.IntegerField(max_length=10, db_column='status', blank=True)
    tele = models.CharField(max_length=20, db_column='tele', blank=True)
    comment = models.CharField(max_length=200, db_column='comment', blank=True)
    m_time = models.TimeField()'''
    class Meta:
        db_table = u'pt_cp_info'

class VmPtCpPaysFilter(models.Model):
    cp_id = models.BigIntegerField(max_length=20, db_column='id')
    remark = models.CharField(max_length=1000, db_column='account_name')
    product_type = models.CharField(max_length=100, db_column='payment_type')
    class Meta:
        db_table = u'finance_zf_accounts'


class VmPtVipCardFinanceSummary(models.Model):
    pt_user_id=models.CharField(max_length=50,primary_key=True)
    vip_card_id=models.CharField(max_length=50)
    vip_card_type=models.CharField(max_length=8)
    vip_pay_money=models.DecimalField(max_digits=32, decimal_places=0)
    current_money=models.IntegerField()
    order_limits=models.SmallIntegerField()
    order_count = models.DecimalField(max_digits=32, decimal_places=0)
    c_time = models.CharField(max_length=100)
    m_time = models.CharField(max_length=100)

    class Meta:
        db_table = u'vw_pt_vip_card_finance_summary'


class VmPtVipCardSubOrdersSummary(models.Model):
    pt_user_id=models.CharField(max_length=50,primary_key=True)
    vip_card_id=models.CharField(max_length=50)
    order_no=models.CharField(max_length=50)
    provider=models.CharField(max_length=64)
    name=models.CharField(max_length=100)
    cp_sell_price=models.IntegerField()
    pt_sell_price = models.IntegerField()
    pay_price = models.BigIntegerField()
    refund_price = models.BigIntegerField()
    pt_should_pay_price = models.BigIntegerField()
    pt_favo_price = models.IntegerField()
    cp_favo_price = models.IntegerField()

    class Meta:
        db_table = u'vw_pt_vip_card_sub_orders_summary'


class FinanceCpPfLlk(models.Model):
    llk_order_id = models.CharField(max_length=128, primary_key=True)
    client_code = models.CharField(max_length=128, blank=True)
    putao_order_no = models.CharField(max_length=128)
    llk_trade_no = models.CharField(max_length=128)
    order_type = models.CharField(max_length=45, blank=True)
    add_time = models.CharField(max_length=128)
    moblie = models.CharField(max_length=45, blank=True)
    service_provide = models.CharField(max_length=128, blank=True)
    province = models.CharField(max_length=128, blank=True)
    city = models.CharField(max_length=128, blank=True)
    user_info = models.CharField(max_length=128, blank=True)
    face_value = models.CharField(max_length=128)
    actual_pay = models.DecimalField(null=True, max_digits=25, decimal_places=4, blank=True)
    order_state = models.CharField(max_length=45)

    class Meta:
        db_table = u'finance_cp_pf_llk'




class CpSettlement(models.Model):
    id = models.AutoField(u"id",primary_key=True)
    order_no = models.CharField(u"订单号", max_length=255, blank=True, null=True)
    cp_id = models.CharField(u"商家id", max_length=255,blank=True, null=True)
    settlement_price = models.IntegerField(u"总金额,分",blank=True, null=True)
    settlement_time = models.CharField(u"更改时间",max_length=255,blank=True, null=True)

    class Meta:
        db_table = 'vw_pt_daojia_cp_settlement'