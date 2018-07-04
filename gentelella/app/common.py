from app.models import *

def check_permission(user, perm):
    return user.has_tcperm(perm)

def check_group(user, group):
    return user.groups.filter(name=group).exists()


def get_retailer_name(user):

    is_retailer = check_group(user, 'retailer_group')
    if is_retailer:
        return TCRetailer.objects.get(main_user=user).org_name
