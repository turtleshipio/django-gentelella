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
    
    enc_password = pwd_context.encrypt(password)
    
    exists = Retailer.objects.filter(business_number=business_number).exists()
    if exists:
        return False, None, None
    
    exists = RetailUser.objects.filter(username=username).exists()
    if exists:
        return False, None, None
    
    
    retailer = Retailer(
        retailer_name=retailer_name,
        business_number=business_number,
        business_type="personal",
        pickteam_id=3,
        main_user_id=-1,
        store_type="offline",
        address=" ",
        bank_account_num=" ",
        bank=" ",
        bank_holder_name=" "
    )
    
    
    retailer.save()
    
    retail_user = RetailUser(
        username = username,
        password = enc_password,
        name = name,
        phone = phone,
        retailer_name = retailer_name,
        retailer = retailer    
        )
        
    retail_user.save()
    
    rp = RetailerPickteam(
        retailer_name=retailer_name,
        pickteam_id=retailer.pickteam_id
        )
        
    rp.save()
    
    t_user = TurtlechainUser(retail_user)
    token = utils.issue_token(username, retail_user.phone, retail_user.retailer_id, retail_user.retailer_name,
                                      retail_user.name)
    return True, t_user, token

