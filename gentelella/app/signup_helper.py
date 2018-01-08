from app.models import *
from app import utils


def create_retailer(retailer_name, business_number, business_type, pickteam_id, main_user_id):
    retailer = Retailer(
        retailer_name=retailer_name,
        business_number=business_number,
        business_type=business_type,
        pickteam_id=pickteam_id,
        main_user_id=main_user_id,
        store_type="offline",
        address=" ",
        bank_account_num=" ",
        bank=" ",
        bank_holder_name=" "
    )

    retailer = [retailer]
    Retailer.objects.bulk_create(retailer)

def update_retailer_id(retailer_name, name):
    retailer = Retailer.objects.get(retailer_name=retailer_name)
    retailer_id = retailer.retailer_id

    RetailUser.objects.filter(name=name).update(retailer_id=retailer_id, retailer_name=retailer_name)

def create_rp(retailer_name):

    retailer = Retailer.objects.get(retailer_name=retailer_name)
    rp = RetailerPickteam(
        retailer_name=retailer_name,
        pickteam_id=retailer.pickteam_id
    )
    rp = [rp]
    RetailerPickteam.objects.bulk_create(rp)