# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import AbstractUser, Group
from app import custom_db





class TCUser(AbstractUser):
    phone = models.CharField(max_length=11)
    full_name = models.CharField(max_length=30, null=False)

    def get_full_name(self):
      
      return self.full_name

    def has_tcperm(self, codename):
        perms = self.get_all_permissions()
        codename = '.'.join(['app', codename])

        return True if codename in perms else False

    def has_tcperms(self, codenames):
        perms = self.get_all_permissions()
        result = True
        for codename in codenames:
            temp_codename = 'app.' + codename
            if temp_codename not in perms:
                result = False

        return result

    class Meta:
        managed=True
        db_table = "tc_user"
        verbose_name = "TC User"
        verbose_name_plural = "TC Users"


class TCOrg(models.Model):
    group = models.ForeignKey(Group, on_delete=models.DO_NOTHING, default=2)
    main_user = models.ForeignKey(TCUser, on_delete = models.SET_NULL, null=True)
    org_name = models.CharField(max_length=191, null=True)

    account_number = models.CharField(max_length=191, null=True, default="")
    bank = models.CharField(max_length=191, null=True, default="")
    bank_account_number = models.CharField(max_length=191, null=True, default="")
    bank_holder_name = models.CharField(max_length=191, null=True, default="")


    def __str__(self):
        return self.org_name if (self.org_name is not None or self.org_name != "") else "TC Org Object"

    class Meta:
        db_table='tc_org'
        managed=True
        verbose_name = "TC Org"
        verbose_name_plural = "TC Orgs"


class TCGroup(models.Model):
    group = models.ForeignKey(Group, on_delete = models.SET_NULL, null=True)
    main_user = models.ForeignKey(TCUser, on_delete = models.SET_NULL, null=True)

    type = models.CharField(max_length=10, null=True)
    org_name = models.CharField(max_length=191, null=True)
    account_number = models.CharField(max_length=191, null=True)
    bank = models.CharField(max_length=191, null=True)
    bank_account_number = models.CharField(max_length=191, null=True)
    bank_holder_name = models.CharField(max_length=191, null=True)


    def __str__(self):
        return self.org_name if (self.org_name is not None or self.org_name != "") else "TC Group Object"

    class Meta:
        db_table='tc_group'
        managed=True
        verbose_name = "TC Group"
        verbose_name_plural = "TC Groups"


class TCPickteam(TCGroup):
    
    def __str__(self):
        return self.main_user.get_full_name() if self.main_user is not None else "TC Pickteam Object"
        
    class Meta:
        managed=True
        db_table = 'tc_pickteam'
        verbose_name = "TC Pickteam"
        verbose_name_plural = "TC Pickteams"


class OrderFormats(models.Model):

    DEFAULT_PK = -1

    fmt_name = models.CharField(null=False, default="", max_length=10, verbose_name="포맷명")
    fmt_ws_name = models.CharField(null=False, max_length=10, verbose_name="도매명 포맷")
    fmt_product_name = models.CharField(null=False, max_length=10, verbose_name="장끼명 포맷")
    fmt_sizeNcolor = models.CharField(null=False, max_length=10, verbose_name="사이즈 및 컬러 포맷")
    fmt_color = models.CharField(null=False, blank=True, max_length=10, verbose_name="컬러 포맷")
    fmt_count = models.CharField(null=False, max_length=10, verbose_name="수량 포맷")
    fmt_price = models.CharField(null=False, max_length=10, verbose_name="도매가 포맷")
    fmt_request = models.CharField(null=True, blank=True, max_length=10, verbose_name="요청사항 포맷")
    fmt_datetime = models.CharField(null=True, blank=True, max_length=20, verbose_name="날짜")

    def __str__(self):
        return self.fmt_name

    def get_format_str(self):

        li = [self.fmt_ws_name, self.fmt_product_name, self.fmt_sizeNcolor, self.fmt_color, self.fmt_count, self.fmt_price, self.fmt_request]
        formats = [i for i in li if bool(i or not i.isspace()) and i != '']
        return ', '.join(formats)

    def get_format_dict(self):

        return {
            'fmt_ws_name' : self.fmt_ws_name,
            'fmt_product_name' : self.fmt_product_name,
            'fmt_sizeNcolor' : self.fmt_sizeNcolor,
            'fmt_color' : self.fmt_color,
            'fmt_count' : self.fmt_count,
            'fmt_price' : self.fmt_price,
            'fmt_request' : self.fmt_request,
            'str' : self.get_format_str()
        }



    class Meta:
        db_table = 'order_formats'
        managed = True
        verbose_name = "Order Format"
        verbose_name_plural = "Order Formats"


class BulkAddWsFormat(models.Model):
    format = models.CharField(max_length=30, blank=False, null=False, default="")
    required = models.BooleanField()

    def __str__(self):
        return self.format

    class Meta:
        managed = True
        db_table ="bulk_ws_formats"
        verbose_name = "Bulk Ws Format"
        verbose_name_plural = "Bulk Ws Formats"

class TCRetailer(TCGroup):

    #city = models.CharField(max_length=10, blank=False, null=False, default="서울")
    #biz_num = models.CharField(max_length=10, blank=True,null=True)
    #biz_type = models.CharField(max_length=30, blank=True, null=True)
    #store_type = models.CharField(max_length=30, blank=True, null=True)
    #address = models.CharField(max_length=191, blank=True, null=True)

    order_format = models.ForeignKey(
        OrderFormats,
        on_delete=models.CASCADE,
        null=True,

    )
    #pickteam = models.ForeignKey(TCPickteam, null=True, on_delete=None, related_name="tc_retailer_pickteam")
    pickteam= models.ForeignKey(TCOrg, null=True, on_delete=None, related_name="ret_pt")
    parser = models.CharField(default="BaseParser", max_length=30)

    def __str__(self):
        return self.org_name if (self.org_name is not None or self.org_name != "") else "TC Retailer Object"
    
    class Meta:
        managed = True
        db_table = 'tc_retailer'
        verbose_name = "TC Retailer"
        verbose_name_plural = "TC Retailers"





class Buildings(models.Model):
    building_name = models.CharField(max_length=512, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    holiday = models.CharField(max_length=100, blank=True, null=True)
    description = models.CharField(max_length=1024, blank=True, null=True)
    business_hour = models.CharField(max_length=100, blank=True, null=True)
    updated_time = models.DateTimeField(auto_now_add=True, blank=True)

    class Meta:
        managed = False
        db_table = 'buildings'

class WsByTCGroup(models.Model):
    ws_name = models.CharField(max_length=30)
    building = models.CharField(max_length=30)
    location = models.CharField(max_length=30)
    floor = models.CharField(max_length=30)
    col = models.CharField(max_length=5, null=True, default="")
    ws_phone = models.CharField(max_length=30)
    group = models.ForeignKey(TCGroup, on_delete=None, default=3)
    updated_time = models.DateTimeField(auto_now_add=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    ws_phone_second = models.CharField(max_length=30, default="")
    org = models.ForeignKey(TCOrg, on_delete=None, default=1)

    def __str__(self):
        return self.ws_name

    class Meta:
        managed = True
        db_table = 'wsbytcgroup'
        verbose_name = "TCGroup's Wholesaler"
        verbose_name_plural = "TCGroup's Wholesalers"









class Order(models.Model):


    order_id = models.BigAutoField(primary_key=True)
    username = models.CharField(max_length=100, blank=True, null=True)
    ws_name = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=10, blank=True, null=True)
    ws_phone = models.CharField(max_length=12, null=False)
    ws_store_phone = models.CharField(max_length=12, null=True)
    product_name = models.CharField(max_length=50)
    sizencolor = models.CharField(db_column='sizeNcolor', max_length=1024)  # Field name made lowercase.

    price = models.IntegerField(null=True, blank=True)
    count = models.IntegerField(null=True, blank=True)
    floor = models.CharField(max_length=30, blank=True, default="")
    location = models.CharField(max_length=30, blank=True, default="")
    oos = models.IntegerField
    memo = models.CharField(max_length=100, blank=True, default="")


    updated_time = models.DateTimeField()
    created_time = models.DateTimeField()
    created_date = models.DateField(null=True, default=None)

    is_deleted = models.BooleanField(null=False, default=False, name="is_deleted")


    notify_id = models.CharField(max_length=100, default="")
    building = models.CharField(max_length=100, default="")
    retailer_name = models.CharField(max_length=30, default="")
    pickteam = models.ForeignKey(TCPickteam, on_delete=None, null=True, db_column="pickteam_id" )
    retailer = models.ForeignKey(TCRetailer, on_delete=None, null=True)

    read = models.BooleanField(default=False)


    def get_order_name(self):
        return '/ '.join([self.ws_name, self.product_name])

    def __str__(self):
        return self.get_order_name()

    class Meta:
        managed = True
        db_table = 'orders'





class OrderGroup():

    pickteam_id = None
    retailer_name = None

    ws_count= None
    created_time = None
    total_count = None
    total_amount = None
    orders = None

    def __init__(self, pickteam_id = None, retailer_name=None):

        self.pickteam_id = pickteam_id
        self.retailer_name = retailer_name

    def get_orders_by_pickteam(self):

        if self.pickteam_id is None:
            return []
        try:
            query = "SELECT " \
                    "created_date AS date, " \
                    "retailer_name, " \
                    "COUNT(DISTINCT(ws_name)) AS ws_count, " \
                    "COUNT(*) AS orders_count, " \
                    "SUM(price * count) AS total_amt " \
                    "FROM orders " \
                    "WHERE pickteam_id={pickteam_id} AND " \
                    "created_date > DATE('2018-09-18') " \
                    "GROUP BY date, retailer_name " \
                    "ORDER BY date desc".format(pickteam_id=self.pickteam_id)

            print(query)
            rs = custom_db.dict_fetchall(query)
            return rs

        except Exception as e:
            print("!!!!!!!!!!!!")
            print("!!!!!!!!!!!!")
            print("!!!!!!!!!!!!")
            print(str(e))
            print("!!!!!!!!!!!!")
            print("!!!!!!!!!!!!")
            print("!!!!!!!!!!!!")
            return []

    def get_orders_by_retailer(self):

        if self.retailer_name is None:
            return []

        rs = None

        try:

            query = "SELECT " \
                    "created_date AS created_date, " \
                    "COUNT(DISTINCT(ws_name)) AS ws_count, " \
                    "COUNT(*) AS orders_count, " \
                    "SUM(price * count) AS total_amt " \
                    "FROM orders " \
                    "WHERE retailer_name='{retailer_name}' AND " \
                    "created_date > DATE('2018-09-18') " \
                    "GROUP BY created_date " \
                    "ORDER BY created_date desc".format(retailer_name=self.retailer_name)

            print(query)
            rs = custom_db.dict_fetchall(query)

            return rs

        except:
            return []

class DailyGMV(models.Model):

    created_date = models.DateField()
    orders_cnt = models.IntegerField()
    tnsct_vol = models.BigIntegerField()

    class Meta:

        managed=True
        db_table="dailygmv"


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


class Temp(models.Model):

    username = models.CharField(max_length=50, default="")
    full_name= models.CharField(max_length=50, default="")
    phone= models.CharField(max_length=50, default="")
    password= models.CharField(max_length=50, default="")

