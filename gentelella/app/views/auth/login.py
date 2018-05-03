from django.template import loader
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from passlib.apps import custom_app_context as pwd_context

from app.models import *
from django.shortcuts import redirect, render
from app.forms import *
from app.backend import RetailUserBackend
#from passlib.hash import sha256_crypt
from app import utils
from app.decorators import require_token
from app import pickup_utils
import json


def retail_login(request, username, password):
    context = {}
    context['login_error'] = ""
    context['signup_error'] = ""
    context['content'] = ""
    context['ws_perm'] = False

    try:
        retail_user = RetailUser.objects.exclude(retailer_id=-1).get(username=username)
        pwd_valid = pwd_context.verify(password, retail_user.password)

        user = TurtlechainUser(retail_user)
        org_id = user.org_id    
        context['t_user'] = user

        if pwd_valid:
            token = utils.issue_token(username, retail_user.phone, retail_user.retailer_id, retail_user.retailer_name,
                                      retail_user.name)
            request.session['token'] = token
            if Permissions.objects.filter(org_id=org_id, policy_name="wholesale").exists():
                context['ws_perm'] = True
            return context, True

    except:
        context['login_error'] = True
        return context, False

    return context, False



def pickup_login(request, username, password):

    context = {}
    context['login_error'] = ""
    context['signup_error'] = ""
    context['content'] = ""
    context['ws_perm'] = False

    try:
        pickup_user = PickupUser.objects.exclude(pickup_user_id=-1).get(username=username)
        pwd_valid = pwd_context.verify(password, pickup_user.password)

        user = TurtlechainUser(pickup_user)
        org_id = user.org_id
        context['t_user'] = user


        if pwd_valid:
            token = pickup_utils.issue_token(username, pickup_user.phone, pickup_user.pickup_user_id, pickup_user.name, pickup_user.pickteam_id)
            request.session['token'] = token

            if Permissions.objects.filter(org_id=org_id, policy_name="wholesale").exists():
                context['ws_perm'] = True
            return context, True

    except PickupUser.DoesNotExist:
        context['login_error'] = True
        return context, False
    except ValueError:
        context['login_error'] = True
        return context, False

    print(context['ws_perm'])
    return context, False
    
