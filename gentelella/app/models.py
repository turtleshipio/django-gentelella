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

        
class TCGroup(models.Model):
    group = models.ForeignKey(Group, on_delete = models.SET_NULL, null=True)
    main_user = models.ForeignKey(TCUser, on_delete = models.SET_NULL, null=True)

    org_name = models.CharField(max_length=191, null=True)
    account_number = models.CharField(max_length=191, null=True)
    bank = models.CharField(max_length=191, null=True)
    bank_account_number = models.CharField(max_length=191, null=True)
    bank_holder_name = models.CharField(max_length=191, null=True)
    mobile_phone  = models.CharField(max_length=11, null=False, default="01088958454")


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
    fmt_color = models.CharField(null=False, max_length=10, verbose_name="컬러 포맷")
    fmt_price = models.CharField(null=False, max_length=10, verbose_name="도매가 포맷")
    fmt_count = models.CharField(null=False, max_length=10, verbose_name="수량 포맷")
    fmt_request = models.CharField(null=True, max_length=10, verbose_name="요청사항 포맷")


    def __str__(self):
        return self.fmt_name

    class Meta:
        db_table = 'order_formats'
        managed = True
        verbose_name = "Order Format"
        verbose_name_plural = "Order Formats"


class TCRetailer(TCGroup):


    city = models.CharField(max_length=10, blank=False, null=False, default="서울")
    biz_num = models.CharField(max_length=10, blank=True,null=True)
    biz_type = models.CharField(max_length=30, blank=True, null=True)
    store_type = models.CharField(max_length=30, blank=True, null=True)
    address = models.CharField(max_length=191, blank=True, null=True)

    order_format = models.OneToOneField(
        OrderFormats,
        on_delete=None,
        null=True,

    )
    pickteam = models.ForeignKey(TCPickteam, null=True, on_delete=None, related_name="tc_retailer_pickteam")


    def __str__(self):
        return self.org_name if (self.org_name is not None or self.org_name != "") else "TC Retailer Object"
    
    class Meta:
        managed = True
        db_table = 'tc_retailer'
        verbose_name = "TC Retailer"
        verbose_name_plural = "TC Retailers"


class TurtlechainUser:

    username = ""
    acc_type = ""
    retailer_id = ""
    retailer_name = ""
    pickup_user_id = ""
    pickteam_id = ""
    name = ""
    org_id = ""

    def __init__(self, obj):

        if obj.__class__.__name__ == "RetailUser":
            self.username = obj.username
            self.acc_type = "retail"
            self.retailer_id = obj.retailer_id
            self.org_id = obj.retailer_id
            self.retailer_name = obj.retailer_name
            self.name = obj.name

            rp = RetailerPickteam.objects.get(retailer_name=obj.retailer_name)
            self.pickteam_id = rp.pickteam_id

        elif obj.__class__.__name__== "PickupUser":

            self.username = obj.username
            self.acc_type = "pickup"
            self.pickteam_id = obj.pickteam_id
            self.pickup_user_id = obj.pickup_user_id
            self.name = obj.name
            self.org_id = obj.pickteam_id

        else:
            raise ValueError


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

    def __str__(self):
        return self.ws_name

    class Meta:
        managed = True
        db_table = 'wsbytcgroup'
        verbose_name = "TCGroup's Wholesaler"
        verbose_name_plural = "TCGroup's Wholesalers"


class Ws(models.Model):
    id = models.BigAutoField(primary_key=True)
    ws_name = models.CharField(max_length=30)
    building_name = models.CharField(max_length=30)
    location = models.CharField(max_length=30)
    floor = models.CharField(max_length=30)
    ws_phone = models.CharField(max_length=30)
    updated_time = models.DateTimeField(blank=True, null=True)
    org_id = models.BigIntegerField()
    acc_type = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'ws'


class Permissions(models.Model):
    policy_name = models.CharField(primary_key=True, max_length=30)
    username = models.CharField(max_length=100)
    acc_type = models.CharField(max_length=30)
    org_id = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'permissions'


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
    retailer_name = models.CharField( max_length=20)
    business_number = models.CharField(unique=True, max_length=20)
    business_type = models.CharField(max_length=20)
    store_type = models.CharField(max_length=20)
    address = models.CharField(max_length=512)
    bank_account_num = models.CharField(max_length=20)
    bank = models.CharField(max_length=20)
    bank_holder_name = models.CharField(max_length=20)
    created_time = models.DateTimeField(blank=True, auto_now=True, null=True)
    
    pickteam_id = models.IntegerField()
    main_user_id = models.IntegerField()

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
    retailer_name = models.CharField(max_length=30, blank=True, default="")
    retailer = models.ForeignKey(Retailer, on_delete=models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'retail_user'

    def __str__(self):
        return self.name


class Order(models.Model):
    order_id = models.BigAutoField(primary_key=True)
    username = models.CharField(max_length=100, blank=True, null=True)
    retailer = models.ForeignKey(Retailer, on_delete=models.DO_NOTHING, null=True)
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
    credit = models.IntegerField
    memo = models.CharField(max_length=100, blank=True, default="")


    updated_time = models.DateTimeField()
    created_time = models.DateTimeField()

    credit = models.ForeignKey(Credits, on_delete=models.DO_NOTHING, related_name="order_of_credits", null=True)
    is_deleted = models.CharField(max_length=10, blank=True, null=True)


    notify_id = models.CharField(max_length=100, default="")
    building = models.CharField(max_length=100, default="")
    pickteam_id = models.IntegerField()
    retailer_name = models.CharField(max_length=30, default="")

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


class RetailerPickteam(models.Model):
    retailer_name = models.CharField(max_length=100, primary_key=True)
    pickteam_id = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'retailer_pickteam'

class PickupUser(models.Model):
    pickup_user_id = models.BigAutoField(primary_key=True)
    username = models.CharField(unique=True, max_length=30)
    password = models.CharField(max_length=512)
    name = models.CharField(max_length=12, blank=True, null=True)
    email = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=12)
    pickteam_id = models.BigIntegerField(blank=True, null=True)
    updated_time = models.DateTimeField(blank=True, null=True)
    account_type = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pickup_user'

class PickteamPickuser(models.Model):
    user_id = models.BigIntegerField(primary_key=True)
    pickteam_id = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'pickteam_pickuser'

class Pickteam(models.Model):
    pickteam_id = models.BigIntegerField(primary_key=True)
    pickteam_name = models.CharField(unique=True, max_length=20, blank=True, null=True)
    business_number = models.CharField(unique=True, max_length=20, blank=True, null=True)
    business_type = models.CharField(max_length=20, blank=True, null=True)
    bank_account_num = models.CharField(max_length=20, blank=True, null=True)
    bank = models.CharField(max_length=20, blank=True, null=True)
    bank_holder_name = models.CharField(max_length=20, blank=True, null=True)
    created_time = models.DateTimeField(blank=True, null=True)
    retailer_id = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'pickteam'

class StoreSyles(models.Model):

    style_id = models.BigIntegerField(primary_key=True)
    style_en = models.CharField(max_length=1024)
    style_kr = models.CharField(max_length=1024)

    class Meta:
        managed = False
        db_table = 'store_styles'



