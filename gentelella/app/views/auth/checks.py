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
from app import pickup_utils
import json

def check_business_number(request):


    data_js = json.loads(request.body.decode('utf-8'))
    business_number = data_js['business_number']
    payload = {'msg': None}
    try:
        exists = Retailer.objects.filter(business_number=business_number).exists()

        if exists:
            payload['msg'] = 'error'
        else:
            payload['msg'] = 'ok'

        return HttpResponse(json.dumps(payload))

    except Retailer.DoesNotExist:
        return HttpResponse("error")
        
        
def check_signup(request):

    data_js = json.loads(request.body.decode('utf-8'))
    username = data_js['username']
    payload = {'msg': None}
    try:
        exists = RetailUser.objects.filter(username=username).exists()

        if exists:
            payload['msg'] = 'error'
        else:
            payload['msg'] = 'ok'

        return HttpResponse(json.dumps(payload))

    except RetailUser.DoesNotExist:
        return HttpResponse("error")
    return HttpResponse(str(e))