#coding: utf-8

"""
    sp505adcda1564f.mysql.rds.aliyuncs.com
    pt_op_total
"""

from django.db import models


class TSysApp(models.Model):
    id = models.BigIntegerField(primary_key=True)
    app_name = models.CharField(max_length=50, blank=True)
    app_key = models.CharField(max_length=50, unique=True, blank=True)
    app_type = models.CharField(max_length=32, blank=True)
    platform = models.CharField(max_length=20, blank=True)
    description = models.CharField(max_length=80, blank=True)
    status = models.IntegerField(null=True, blank=True)
    m_time = models.DateTimeField()
    c_time = models.DateTimeField()
    user_id = models.CharField(max_length=100)
    app_id = models.BigIntegerField(null=True, blank=True)
    class Meta:
        db_table = u't_sys_app'
    def __unicode__(self):
        return self.app_name


class TRpDAppuseSum(models.Model):
    app_key = models.CharField(max_length=40, primary_key=True)
    channel_no = models.CharField(max_length=100, primary_key=True)
    app_version = models.CharField(max_length=50, primary_key=True)
    subtype = models.CharField(max_length=50, primary_key=True)
    c_usernew = models.DecimalField(null=True, max_digits=22, decimal_places=4, blank=True)
    c_user = models.DecimalField(null=True, max_digits=22, decimal_places=4, blank=True)
    c_useapp = models.DecimalField(null=True, max_digits=22, decimal_places=4, blank=True)
    c_usetime = models.DecimalField(null=True, max_digits=22, decimal_places=4, blank=True)
    s_usetime = models.DecimalField(null=True, max_digits=22, decimal_places=4, blank=True)
    loadtime = models.DateTimeField()
    statdate = models.IntegerField(primary_key=True)
    class Meta:
        db_table = u't_rp_d_appuse_sum'
    def __unicode__(self):
        return self.app_key


class TRpDAppuseTrend(models.Model):
    app_key = models.CharField(max_length=40, primary_key=True)
    channel_no = models.CharField(max_length=100, primary_key=True)
    app_version = models.CharField(max_length=50, primary_key=True)
    subtype = models.CharField(max_length=50, primary_key=True)
    c_useracc = models.DecimalField(null=True, max_digits=22, decimal_places=4, blank=True)
    c_user_p7 = models.DecimalField(null=True, max_digits=22, decimal_places=4, blank=True)
    c_user_p30 = models.DecimalField(null=True, max_digits=22, decimal_places=4, blank=True)
    s_usetime_p7 = models.DecimalField(null=True, max_digits=22, decimal_places=4, blank=True)
    loadtime = models.DateTimeField()
    statdate = models.IntegerField(primary_key=True)
    class Meta:
        db_table = u't_rp_d_appuse_trend'


class TRpDAppuseCombine(models.Model):
    app_key = models.CharField(max_length=40, primary_key=True)
    channel_no = models.CharField(max_length=100, primary_key=True)
    app_version = models.CharField(max_length=50, primary_key=True)
    subtype = models.CharField(max_length=50, primary_key=True)
    c_useracc = models.DecimalField(null=True, max_digits=45, decimal_places=4, blank=True)
    c_user_p7 = models.DecimalField(null=True, max_digits=22, decimal_places=4, blank=True)
    c_user_p30 = models.DecimalField(null=True, max_digits=22, decimal_places=4, blank=True)
    s_usetime_p7 = models.DecimalField(null=True, max_digits=22, decimal_places=4, blank=True)
    c_usernew = models.DecimalField(null=True, max_digits=44, decimal_places=4, blank=True)
    c_user = models.DecimalField(null=True, max_digits=44, decimal_places=4, blank=True)
    c_useapp = models.DecimalField(null=True, max_digits=44, decimal_places=4, blank=True)
    c_usetime = models.DecimalField(null=True, max_digits=44, decimal_places=4, blank=True)
    s_usetime = models.DecimalField(null=True, max_digits=44, decimal_places=4, blank=True)
    statdate = models.IntegerField(primary_key=True)
    class Meta:
        db_table = u't_rp_d_appuse_combine'


class TDimAppFilter(models.Model):
    app_key = models.CharField(max_length=40, primary_key=True)
    channel_no = models.CharField(max_length=100, primary_key=True)
    app_version = models.CharField(max_length=50, primary_key=True)
    loadtime = models.DateTimeField()
    statdate = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u't_dim_app_filter'


class TDimWeek(models.Model):
    i_week = models.IntegerField(primary_key=True)
    i_weekstart = models.IntegerField(null=True, blank=True)
    i_weekend = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u't_dim_week'


class TRpWAppuseSum(models.Model):
    app_key = models.CharField(max_length=40, primary_key=True)
    channel_no = models.CharField(max_length=100, primary_key=True)
    app_version = models.CharField(max_length=50, primary_key=True)
    subtype = models.CharField(max_length=50, primary_key=True)
    c_usernew = models.DecimalField(null=True, max_digits=22, decimal_places=4, blank=True)
    c_user = models.DecimalField(null=True, max_digits=22, decimal_places=4, blank=True)
    c_useapp = models.DecimalField(null=True, max_digits=22, decimal_places=4, blank=True)
    c_usetime = models.DecimalField(null=True, max_digits=22, decimal_places=4, blank=True)
    s_usetime = models.DecimalField(null=True, max_digits=22, decimal_places=4, blank=True)
    loadtime = models.DateTimeField()
    statweek = models.IntegerField(primary_key=True)
    class Meta:
        db_table = u't_rp_w_appuse_sum'


class TRpMAppuseSum(models.Model):
    app_key = models.CharField(max_length=40, primary_key=True)
    channel_no = models.CharField(max_length=100, primary_key=True)
    app_version = models.CharField(max_length=50, primary_key=True)
    subtype = models.CharField(max_length=50, primary_key=True)
    c_usernew = models.DecimalField(null=True, max_digits=22, decimal_places=4, blank=True)
    c_user = models.DecimalField(null=True, max_digits=22, decimal_places=4, blank=True)
    c_useapp = models.DecimalField(null=True, max_digits=22, decimal_places=4, blank=True)
    c_usetime = models.DecimalField(null=True, max_digits=22, decimal_places=4, blank=True)
    s_usetime = models.DecimalField(null=True, max_digits=22, decimal_places=4, blank=True)
    loadtime = models.DateTimeField()
    statmonth = models.IntegerField(primary_key=True)
    class Meta:
        db_table = u't_rp_m_appuse_sum'


class TRpDAppuseReturnuser(models.Model):
    statdate = models.IntegerField(primary_key=True)
    app_key = models.CharField(max_length=40, primary_key=True)
    channel_no = models.CharField(max_length=100, primary_key=True)
    app_version = models.CharField(max_length=50, primary_key=True)
    subtype = models.CharField(max_length=50, primary_key=True)
    c_usernew = models.DecimalField(null=True, max_digits=22, decimal_places=4, blank=True)
    c_user = models.DecimalField(null=True, max_digits=22, decimal_places=4, blank=True)
    c_usernew_return = models.DecimalField(null=True, max_digits=22, decimal_places=4, blank=True)
    c_user_return = models.DecimalField(null=True, max_digits=22, decimal_places=4, blank=True)
    loadtime = models.DateTimeField()
    loaddate = models.IntegerField(null=True, blank=True)
    predate = models.IntegerField(primary_key=True)
    class Meta:
        db_table = u't_rp_d_appuse_returnuser'


class TRpWAppuseReturnuser(models.Model):
    statweek = models.IntegerField(primary_key=True)
    app_key = models.CharField(max_length=40, primary_key=True)
    channel_no = models.CharField(max_length=100, primary_key=True)
    app_version = models.CharField(max_length=50, primary_key=True)
    subtype = models.CharField(max_length=50, primary_key=True)
    c_usernew = models.DecimalField(null=True, max_digits=22, decimal_places=4, blank=True)
    c_user = models.DecimalField(null=True, max_digits=22, decimal_places=4, blank=True)
    c_usernew_return = models.DecimalField(null=True, max_digits=22, decimal_places=4, blank=True)
    c_user_return = models.DecimalField(null=True, max_digits=22, decimal_places=4, blank=True)
    loadtime = models.DateTimeField()
    loadweek = models.IntegerField(null=True, blank=True)
    preweek = models.IntegerField(primary_key=True)
    class Meta:
        db_table = u't_rp_w_appuse_returnuser'


class TRpDAppuseVersion(models.Model):
    app_key = models.CharField(max_length=40, primary_key=True)
    channel_no = models.CharField(max_length=100, primary_key=True)
    app_version = models.CharField(max_length=50, primary_key=True)
    subtype = models.CharField(max_length=50, primary_key=True)
    c_useracc = models.DecimalField(null=True, max_digits=22, decimal_places=4, blank=True)
    c_usernew = models.DecimalField(null=True, max_digits=22, decimal_places=4, blank=True)
    update_user = models.DecimalField(null=True, max_digits=22, decimal_places=4, blank=True)
    c_user = models.DecimalField(null=True, max_digits=22, decimal_places=4, blank=True)
    c_useapp = models.DecimalField(null=True, max_digits=22, decimal_places=4, blank=True)
    statdate = models.IntegerField(primary_key=True)
    class Meta:
        db_table = u't_rp_d_appuse_version'


class TRpHAppuseSum(models.Model):
    app_key = models.CharField(max_length=40, primary_key=True)
    channel_no = models.CharField(max_length=100, primary_key=True)
    app_version = models.CharField(max_length=50, primary_key=True)
    subtype = models.CharField(max_length=50, primary_key=True)
    c_usernew = models.DecimalField(null=True, max_digits=22, decimal_places=4, blank=True)
    c_user = models.DecimalField(null=True, max_digits=22, decimal_places=4, blank=True)
    c_useapp = models.DecimalField(null=True, max_digits=22, decimal_places=4, blank=True)
    c_usetime = models.DecimalField(null=True, max_digits=22, decimal_places=4, blank=True)
    s_usetime = models.DecimalField(null=True, max_digits=22, decimal_places=4, blank=True)
    loadtime = models.DateTimeField()
    statdate = models.IntegerField(primary_key=True)
    stathour = models.IntegerField(primary_key=True)
    class Meta:
        db_table = u't_rp_h_appuse_sum'


class TRpMAppuseReturnuser(models.Model):
    statmonth = models.IntegerField(primary_key=True)
    app_key = models.CharField(max_length=40, primary_key=True)
    channel_no = models.CharField(max_length=100, primary_key=True)
    app_version = models.CharField(max_length=50, primary_key=True)
    subtype = models.CharField(max_length=50, primary_key=True)
    c_usernew = models.DecimalField(null=True, max_digits=22, decimal_places=4, blank=True)
    c_user = models.DecimalField(null=True, max_digits=22, decimal_places=4, blank=True)
    c_usernew_return = models.DecimalField(null=True, max_digits=22, decimal_places=4, blank=True)
    c_user_return = models.DecimalField(null=True, max_digits=22, decimal_places=4, blank=True)
    loadtime = models.DateTimeField()
    loadmonth = models.IntegerField(null=True, blank=True)
    premonth = models.IntegerField(primary_key=True)
    class Meta:
        db_table = u't_rp_m_appuse_returnuser'


class TRpDAppuseUsetimes(models.Model):
    app_key = models.CharField(max_length=40, primary_key=True)
    channel_no = models.CharField(max_length=100, primary_key=True)
    app_version = models.CharField(max_length=50, primary_key=True)
    subtype = models.CharField(max_length=50, primary_key=True)
    usetimes = models.CharField(max_length=50, primary_key=True)
    c_usernew = models.DecimalField(null=True, max_digits=22, decimal_places=4, blank=True)
    c_user = models.DecimalField(null=True, max_digits=22, decimal_places=4, blank=True)
    c_useapp = models.DecimalField(null=True, max_digits=22, decimal_places=4, blank=True)
    c_usetime = models.DecimalField(null=True, max_digits=22, decimal_places=4, blank=True)
    s_usetime = models.DecimalField(null=True, max_digits=22, decimal_places=4, blank=True)
    loadtime = models.DateTimeField()
    statdate = models.IntegerField(primary_key=True)
    class Meta:
        db_table = u't_rp_d_appuse_usetimes'


class PtTotalEventWeb(models.Model):
    app_key = models.CharField(max_length=40)
    event_id = models.CharField(max_length=200)
    event_name = models.CharField(max_length=200, blank=True)
    event_type = models.CharField(max_length=45)
    business_type = models.CharField(max_length=45, blank=True)
    c_time = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = u'pt_total_event_web'
        unique_together = ('app_key', 'event_id')


class TRpDAppuseEventSum(models.Model):
    app_key = models.CharField(max_length=40, primary_key=True)
    channel_no = models.CharField(max_length=100, primary_key=True)
    app_version = models.CharField(max_length=50, primary_key=True)
    event_id = models.CharField(max_length=200, primary_key=True)
    c_usernew = models.DecimalField(null=True, max_digits=22, decimal_places=4, blank=True)
    c_user = models.DecimalField(null=True, max_digits=22, decimal_places=4, blank=True)
    c_event = models.DecimalField(null=True, max_digits=22, decimal_places=4, blank=True)
    c_useapp = models.DecimalField(null=True, max_digits=22, decimal_places=4, blank=True)
    c_usetime = models.DecimalField(null=True, max_digits=22, decimal_places=4, blank=True)
    s_usetime = models.DecimalField(null=True, max_digits=22, decimal_places=4, blank=True)
    loadtime = models.DateTimeField()
    statdate = models.IntegerField(primary_key=True)
    class Meta:
        db_table = u't_rp_d_appuse_event_sum'


class TSysEventCategory(models.Model):
    id = models.BigIntegerField(primary_key=True)
    main_category = models.CharField(max_length=50, blank=True)
    sub_category = models.CharField(max_length=50, blank=True)
    description = models.CharField(max_length=80, blank=True)
    m_time = models.DateTimeField()
    c_time = models.DateTimeField()
    class Meta:
        db_table = u't_sys_event_category'


class TRpDAppuseEventSumParams(models.Model):
    app_key = models.CharField(max_length=40, primary_key=True)
    channel_no = models.CharField(max_length=100, primary_key=True)
    app_version = models.CharField(max_length=50, primary_key=True)
    event_id = models.CharField(max_length=200, primary_key=True)
    param_key = models.CharField(max_length=200, primary_key=True)
    param_value = models.CharField(max_length=200, primary_key=True)
    c_params_count = models.DecimalField(null=True, max_digits=22, decimal_places=4, blank=True)
    c_user = models.DecimalField(null=True, max_digits=22, decimal_places=4, blank=True)
    loadtime = models.DateTimeField()
    statdate = models.IntegerField(primary_key=True)
    class Meta:
        db_table = u't_rp_d_appuse_event_sum_params'


class TRpDAppuseTimeregion(models.Model):
    app_key = models.CharField(max_length=40, primary_key=True)
    channel_no = models.CharField(max_length=100, primary_key=True)
    app_version = models.CharField(max_length=50, primary_key=True)
    subtype = models.CharField(max_length=50, primary_key=True)
    timeregion = models.CharField(max_length=50, primary_key=True)
    c_usernew = models.DecimalField(null=True, max_digits=22, decimal_places=4, blank=True)
    c_user = models.DecimalField(null=True, max_digits=22, decimal_places=4, blank=True)
    c_useapp = models.DecimalField(null=True, max_digits=22, decimal_places=4, blank=True)
    c_usetime = models.DecimalField(null=True, max_digits=22, decimal_places=4, blank=True)
    s_usetime = models.DecimalField(null=True, max_digits=22, decimal_places=4, blank=True)
    loadtime = models.DateTimeField()
    statdate = models.IntegerField(primary_key=True)
    class Meta:
        db_table = u't_rp_d_appuse_timeregion'


class TRpDAppuseTimeregionOnce(models.Model):
    app_key = models.CharField(max_length=40, primary_key=True)
    channel_no = models.CharField(max_length=100, primary_key=True)
    app_version = models.CharField(max_length=50, primary_key=True)
    subtype = models.CharField(max_length=50, primary_key=True)
    timeregion = models.CharField(max_length=50, primary_key=True)
    c_usernew = models.DecimalField(null=True, max_digits=22, decimal_places=4, blank=True)
    c_user = models.DecimalField(null=True, max_digits=22, decimal_places=4, blank=True)
    c_useapp = models.DecimalField(null=True, max_digits=22, decimal_places=4, blank=True)
    c_usetime = models.DecimalField(null=True, max_digits=22, decimal_places=4, blank=True)
    s_usetime = models.DecimalField(null=True, max_digits=22, decimal_places=4, blank=True)
    loadtime = models.DateTimeField()
    statdate = models.IntegerField(primary_key=True)
    class Meta:
        db_table = u't_rp_d_appuse_timeregion_once'


class TRpWAppuseUsetimes(models.Model):
    app_key = models.CharField(max_length=40, primary_key=True)
    channel_no = models.CharField(max_length=100, primary_key=True)
    app_version = models.CharField(max_length=50, primary_key=True)
    subtype = models.CharField(max_length=50, primary_key=True)
    usetimes = models.CharField(max_length=50, primary_key=True)
    c_usernew = models.DecimalField(null=True, max_digits=22, decimal_places=4, blank=True)
    c_user = models.DecimalField(null=True, max_digits=22, decimal_places=4, blank=True)
    c_useapp = models.DecimalField(null=True, max_digits=22, decimal_places=4, blank=True)
    c_usetime = models.DecimalField(null=True, max_digits=22, decimal_places=4, blank=True)
    s_usetime = models.DecimalField(null=True, max_digits=22, decimal_places=4, blank=True)
    loadtime = models.DateTimeField()
    statweek = models.IntegerField(primary_key=True)
    class Meta:
        db_table = u't_rp_w_appuse_usetimes'


class TRpMAppuseUsetimes(models.Model):
    app_key = models.CharField(max_length=40, primary_key=True)
    channel_no = models.CharField(max_length=100, primary_key=True)
    app_version = models.CharField(max_length=50, primary_key=True)
    subtype = models.CharField(max_length=50, primary_key=True)
    usetimes = models.CharField(max_length=50, primary_key=True)
    c_usernew = models.DecimalField(null=True, max_digits=22, decimal_places=4, blank=True)
    c_user = models.DecimalField(null=True, max_digits=22, decimal_places=4, blank=True)
    c_useapp = models.DecimalField(null=True, max_digits=22, decimal_places=4, blank=True)
    c_usetime = models.DecimalField(null=True, max_digits=22, decimal_places=4, blank=True)
    s_usetime = models.DecimalField(null=True, max_digits=22, decimal_places=4, blank=True)
    loadtime = models.DateTimeField()
    statmonth = models.IntegerField(primary_key=True)
    class Meta:
        db_table = u't_rp_m_appuse_usetimes'


class VRpDRealtimeStat(models.Model):
    app_key = models.CharField(max_length=40, db_column='APP_KEY', primary_key=True) # Field name made lowercase.
    statdate = models.IntegerField(db_column='STATDATE', primary_key=True) # Field name made lowercase.
    c_usernew = models.DecimalField(decimal_places=4, null=True, max_digits=44, db_column='C_USERNEW', blank=True) # Field name made lowercase.
    c_usernew_change_rate = models.DecimalField(decimal_places=3, null=True, max_digits=49, db_column='C_USERNEW_CHANGE_RATE', blank=True) # Field name made lowercase.
    c_user = models.DecimalField(decimal_places=4, null=True, max_digits=44, db_column='C_USER', blank=True) # Field name made lowercase.
    c_user_change_rate = models.DecimalField(decimal_places=3, null=True, max_digits=49, db_column='C_USER_CHANGE_RATE', blank=True) # Field name made lowercase.
    c_useapp = models.DecimalField(decimal_places=4, null=True, max_digits=44, db_column='C_USEAPP', blank=True) # Field name made lowercase.
    c_useapp_change_rate = models.DecimalField(decimal_places=3, null=True, max_digits=49, db_column='C_USEAPP_CHANGE_RATE', blank=True) # Field name made lowercase.
    stathour = models.IntegerField(db_column='STATHOUR', primary_key=True) # Field name made lowercase.
    class Meta:
        db_table = u'v_rp_d_realtime_stat'


class UmengApps(models.Model):
    app_key = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    created_at = models.CharField(max_length=100)
    updated_at = models.CharField(max_length=100)
    platform = models.CharField(max_length=100)
    mark = models.SmallIntegerField()

    class Meta:
        db_table = u'umeng_apps'

