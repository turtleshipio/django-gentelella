from app.models import *
from passlib.apps import custom_app_context as pwd_context
from app.views.auth import checks
from app import utils



def create_turtlechain_user(data_js):
    
    username = data_js['username']
    password = data_js['password']
    retailer_name = data_js['retailer_name']
    business_number = data_js['business_number']
    name = data_js['name']
    phone = data_js['phone']
    styles = data_js['styles']
    
    print("username is:\t{0}".format(username))
    print("password is:\t{0}".format(password))
    print("retailer_name is:\t{0}".format(retailer_name))
    print("business_number is:\t{0}".format(business_number))
    print("name is:\t{0}".format(name))
    print("phone is:\t{0}".format(phone))
    print("styles is:\t{0}".format(styles))


    exists = Retailer.objects.filter(business_number=business_number).exists()
    if exists:
        return False, None, None
    
    exists = RetailUser.objects.filter(username=username).exists()
    if exists:
        return False, None, None

    user = TCUser.objects.create_user(username=username, email=None, password=password, full_name=name)
    group = Group.objects.get(name='retailer_group')
    tc_pickteam = TCPickteam.objects.get(main_user_id=3)
    format = OrderFormats.objects.create(fmt_name=user.full_name, fmt_ws_name="도매명", fmt_product_name="장끼명", fmt_sizeNcolor="사이즈", fmt_color="컬러", fmt_count="수량", fmt_price="도매가", fmt_request="요청사항")
    tc_group = TCGroup.objects.create(group=group, main_user=user, type="retailer", org_name=retailer_name, account_number="", bank="", bank_account_number="", bank_holder_name="", mobile_phone=phone)

    tc_retailer = TCRetailer.objects.create(
        group= group,
        main_user= user,
        type="personal",
        org_name=retailer_name,
        account_number = "",
        bank = "",
        bank_account_number = "",
        bank_holder_name = "",
        mobile_phone = phone,
        city = "서울",
        biz_num = "",
        biz_type = "",
        store_type = "",
        address = "",
        order_format = format,
        pickteam = tc_pickteam

    )
    return True, user

