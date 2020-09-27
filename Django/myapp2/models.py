# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class Basiccompanyinfo(models.Model):
    share_code = models.CharField(primary_key=True, max_length=4)
    share_name = models.TextField(blank=True, null=True)
    english_name = models.TextField(blank=True, null=True)
    company_marketname = models.TextField(db_column='Company_MarketName', blank=True, null=True)  # Field name made lowercase.
    industry = models.TextField(blank=True, null=True)
    company_create_date = models.TextField(db_column='Company_Create_Date', blank=True, null=True)  # Field name made lowercase.
    company_share_open_date = models.TextField(db_column='Company_Share_Open_Date', blank=True, null=True)  # Field name made lowercase.
    kesan = models.TextField(blank=True, null=True)
    company_address = models.TextField(db_column='Company_Address', blank=True, null=True)  # Field name made lowercase.
    company_summary = models.TextField(blank=True, null=True)
    company_total_share = models.TextField(blank=True, null=True)
    company_total_market_price = models.TextField(blank=True, null=True)
    return_rate = models.TextField(blank=True, null=True)
    return_per_share = models.TextField(blank=True, null=True)
    return_yymm = models.TextField(blank=True, null=True)
    limit_price = models.TextField(blank=True, null=True)
    per = models.TextField(blank=True, null=True)
    pbr = models.TextField(blank=True, null=True)
    eps1 = models.TextField(blank=True, null=True)
    eps2 = models.TextField(blank=True, null=True)
    high_price_thisyear = models.TextField(blank=True, null=True)
    high_price_thisyear_date = models.TextField(blank=True, null=True)
    low_price_thisyear = models.TextField(blank=True, null=True)
    low_price_thisyear_date = models.TextField(blank=True, null=True)
    credit_buy = models.TextField(blank=True, null=True)
    credit_sale = models.TextField(blank=True, null=True)
    current_price = models.TextField(blank=True, null=True)
    current_price_time = models.TextField(blank=True, null=True)
    yestoday_price = models.TextField(blank=True, null=True)
    start_price = models.TextField(blank=True, null=True)
    high_price = models.TextField(blank=True, null=True)
    low_price = models.TextField(blank=True, null=True)
    total_trade_share = models.TextField(blank=True, null=True)
    total_trade_money = models.TextField(blank=True, null=True)

    class Meta:
        app_label = 'myapp2'
        managed = False
        db_table = 'BasicCompanyInfo'


class CaclValuesTbl(models.Model):
    share_code = models.CharField(primary_key=True, max_length=4)
    data_type = models.CharField(max_length=20)
    data_json = models.TextField()

    class Meta:
        app_label = 'myapp2'
        managed = False
        db_table = 'Cacl_Values_TBL'
        unique_together = (('share_code', 'data_type'),)


class CacheTable(models.Model):
    cache_lable = models.CharField(max_length=200)
    cache_content = models.TextField()

    class Meta:
        app_label = 'myapp2'
        managed = False
        db_table = 'Cache_Table'


class Dailyshareinfo(models.Model):
    trade_date = models.DateField(primary_key=True)
    share_code = models.CharField(max_length=4)
    industry_code = models.CharField(max_length=4)
    share_name = models.TextField()
    start_price = models.DecimalField(max_digits=10, decimal_places=2)
    high_price = models.DecimalField(max_digits=10, decimal_places=2)
    low_price = models.DecimalField(max_digits=10, decimal_places=2)
    finishi_price = models.DecimalField(max_digits=10, decimal_places=2)
    trade_total = models.BigIntegerField()
    market = models.TextField()

    class Meta:
        app_label = 'myapp2'
        managed = False
        db_table = 'DailyShareInfo'
        unique_together = (('trade_date', 'share_code'),)
