# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models

class OrderConfirm(models.Model):
    order_id = models.BigAutoField(primary_key=True)
    ws_status = models.CharField(max_length=10, blank=True, null=True)
    pick_status = models.CharField(max_length=10, blank=True, null=True)
    updated_time = models.DateTimeField()
    created_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'order_confirm'

class Credits(models.Model):
    credit_id = models.BigAutoField(primary_key=True)
    retailer_id = models.IntegerField(blank=True, null=True)
    ws_name = models.CharField(max_length=100, blank=True, null=True)
    exp_date = models.DateTimeField(blank=True, null=True)
    resolved = models.CharField(max_length=10, blank=True, null=True)
    updated_time = models.DateTimeField()
    created_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'credits'


class Buildings(models.Model):
    building_name = models.CharField(max_length=512, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    holiday = models.CharField(max_length=100, blank=True, null=True)
    description = models.CharField(max_length=1024, blank=True, null=True)
    business_hour = models.CharField(max_length=100, blank=True, null=True)
    updated_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'buildings'




class User(models.Model):
    user_id = models.BigAutoField(primary_key=True)
    username = models.CharField(unique=True, max_length=254, blank=True, null=True)
    password = models.CharField(max_length=512, blank=True, null=True)
    name = models.CharField(max_length=12, blank=True, null=True)
    email = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=12, blank=True, null=True)
    org = models.CharField(max_length=100, blank=True, null=True)
    last_login_time = models.DateTimeField(blank=True, null=True)
    updated_time = models.DateTimeField(blank=True, null=True)
    account_type = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user'


class Wholesalers(models.Model):
    ws_id = models.BigAutoField(primary_key=True)
    ws_name = models.CharField(max_length=512)
    building_name = models.CharField(max_length=512)
    location = models.CharField(max_length=20)
    product_count = models.IntegerField(blank=True, null=True)
    updated_time = models.DateTimeField(blank=True, null=True)
    floor = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'wholesalers'


class Retailer(models.Model):
    retailer_id = models.BigAutoField(primary_key=True)
    retailer_name = models.CharField(unique=True, max_length=20)
    business_number = models.CharField(unique=True, max_length=20)
    business_type = models.CharField(max_length=20)
    store_type = models.CharField(max_length=20)
    address = models.CharField(max_length=512)
    bank_account_num = models.CharField(max_length=20)
    bank = models.CharField(max_length=20)
    bank_holder_name = models.CharField(max_length=20)
    created_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'retailer'


class RetailUser(models.Model):
    user_idx = models.BigAutoField(primary_key=True)
    username = models.CharField(unique=True, max_length=254)
    password = models.CharField(max_length=512)
    name = models.CharField(max_length=12, blank=True, null=True)
    email = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=12)
    updated_time = models.DateTimeField(blank=True, null=True)
    account_type = models.CharField(max_length=100, blank=True, null=True)
    retailer = models.ForeignKey(Retailer, on_delete=models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'retail_user'

    def __str__(self):
        return self.name


class Orders(models.Model):
    order_id = models.BigAutoField(primary_key=True)
    username = models.CharField(max_length=100, blank=True, null=True)
    retailer = models.ForeignKey(Retailer, on_delete=models.DO_NOTHING, null=True)
    ws_name = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=10, blank=True, null=True)
    ws_phone = models.CharField(max_length=12)
    product_name = models.CharField(max_length=50)
    sizencolor = models.CharField(db_column='sizeNcolor', max_length=1024)  # Field name made lowercase.
    option2 = models.CharField(max_length=1024, blank=True, null=True)
    price = models.IntegerField(null=True, blank=True)
    count = models.IntegerField(null=True, blank=True)
    floor = models.CharField(max_length=30, blank=True, default="")
    location = models.CharField(max_length=30, blank=True, default="")
    oos = models.CharField(max_length=30, blank=True, null=True)
    request = models.CharField(max_length=1024, blank=True, null=True)
    internal_name = models.CharField(max_length=1024, blank=True, null=True)
    internal_code1 = models.CharField(max_length=1024, blank=True, null=True)
    internal_code2 = models.CharField(max_length=1024, blank=True, null=True)
    internal_code3 = models.CharField(max_length=1024, blank=True, null=True)
    internal_code4 = models.CharField(max_length=1024, blank=True, null=True)
    internal_code5 = models.CharField(max_length=1024, blank=True, null=True)
    updated_time = models.DateTimeField()
    created_time = models.DateTimeField()
    ordergroup_id = models.BigIntegerField()
    credit = models.ForeignKey(Credits, on_delete=models.DO_NOTHING, related_name="order_of_credits", null=True)
    is_deleted = models.CharField(max_length=10, blank=True, null=True)
    excel_origin = models.CharField(max_length=10, blank=True, null=True)
    naver_order_id = models.CharField(max_length=30, blank=True, null=True)
    naver_order_group_id = models.CharField(max_length=30, blank=True, null=True)
    buyer_name = models.CharField(max_length=30, blank=True, null=True)
    pay_origin = models.CharField(max_length=30, blank=True, null=True)
    product_num = models.CharField(max_length=30, blank=True, null=True)
    buyer_phone = models.CharField(max_length=30, blank=True, null=True)
    product_name_retailer = models.CharField(max_length=30, blank=True, null=True)
    buyer_pay_method = models.CharField(max_length=30, blank=True, null=True)
    buyer_address = models.CharField(max_length=30, blank=True, null=True)
    depart_loc = models.CharField(max_length=30, blank=True, null=True)
    postal_code = models.CharField(max_length=30, blank=True, null=True)
    retailer_price = models.IntegerField()
    buyer_id = models.CharField(max_length=30, blank=True, null=True)
    receiver_name = models.CharField(max_length=30, blank=True, null=True)
    delivery_method = models.CharField(max_length=30, blank=True, null=True)
    deliverer = models.CharField(max_length=30, blank=True, null=True)
    delivery_id = models.CharField(max_length=30, blank=True, null=True)
    sales_channel = models.CharField(max_length=30, blank=True, null=True)
    marketing_channel = models.CharField(max_length=30, blank=True, null=True)
    buyer_order_count = models.IntegerField()
    retailer_product_code = models.CharField(max_length=30, blank=True, null=True)
    notify_id = models.CharField(max_length=100, default="")
    building = models.CharField(max_length=100, default="")

    class Meta:
        managed = False
        db_table = 'orders'


class Notify(models.Model):

    notify_id = models.CharField(primary_key=True, max_length=20)
    ws_name = models.CharField(max_length=100)
    retailer_id = models.BigIntegerField()
    prd1 = models.CharField(max_length=100)
    prd_count = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'notify'
