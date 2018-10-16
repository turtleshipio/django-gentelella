from datetime import datetime, timedelta
import pytz
import jwt
from app import config
import random
import string
from app.models import *
import hashlib





def getYesterdayDateAt11pm():

    today = datetime.utcnow()
    today = today.replace(tzinfo=pytz.timezone("Asia/Seoul"))
    yesterday = today - timedelta(days=1)
    yesterday = yesterday.replace(hour=23, minute=0, second=0)

    return yesterday

def decode_token(token):

    try:
        token = jwt.decode(token, config.JWT['secret'], config.JWT['algorithm'])
        return token
    except:
        return None


def issue_token(username, phone, retailer_id,retailer_name, name):

    now = datetime.utcnow()
    payload = {
        'username': username,
        'phone': phone,
        'retailer_id': retailer_id,
        'retailer_name' : retailer_name,
        'acc_type' : 'retailer',
        'name': name,
        'iat': now,
        'exp': now + timedelta(5)
    }
    jwt_token = jwt.encode(payload, config.JWT['secret'], config.JWT['algorithm'])
    token = jwt_token.decode('utf-8')
    return token


def get_context_from_token(token):

    context = {}
    if token['acc_type'] == "retailer":

        context['retail_user'] = {
            'username': token['username'],
            'retailer_id': token['retailer_id'],
            'phone': token['phone'],
            'name': token['name'],
        }

    if token['acc_type'] == 'pickup':

        context['pickup_user'] = {
            'username' : token['username'],
            'pickteam_id' : token['pickteam_id'],
            'phone' : token['phone'],
            'name' : token['name'],
        }

    return context

''' 
def get_user_from_token(decoded_token):

    t_user = None
    username = decoded_token['username']
    acc_type = decoded_token['acc_type']
    print("**********************")
    print(acc_type)

    if acc_type == "retailer":
        t_user = RetailUser.objects.get(username=username)
    if acc_type == "pickup":
        t_user = PickupUser.objects.get(username=username)

    if t_user is not None:
        t_user = TurtlechainUser(t_user)
    return t_user

def get_retail_user_from_token(decoded_token):


    retail_user = {
        'username': decoded_token['username'],
        'retailer_id': decoded_token['retailer_id'],
        'phone': decoded_token['phone'],
        'name': decoded_token['name'],
        'retailer_name' : decoded_token['retailer_name'],
    }
    return retail_user


def get_decoded_token(token):
    return decode_token(token)

'''
def get_uuid(n):
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(n))


def create_order_num(retailer_name, ws_name, building):
    date = str(datetime.now().date()).encode('utf-8')
    date = hashlib.md5(date).hexdigest()
    retailer_name = hashlib.md5(retailer_name.encode('utf-8')).hexdigest()
    ws_name = hashlib.md5(ws_name.encode('utf-8')).hexdigest()
    building = hashlib.md5(building.encode('utf-8')).hexdigest()

    order_num = ''.join([date, ws_name, building])
    order_num = hashlib.md5(order_num.encode('utf-8')).hexdigest()
    return order_num



def create_notify_id(timestamp, index, ws_name, retailer_name, product_name):

    if timestamp is None or index is None or ws_name is None or retailer_name is None or product_name is None:
        return False, "parameter is None"

    if type(timestamp) != str or type(index) != str or type(ws_name) != str or type(retailer_name) != str or type(product_name) != str:
        return False, "parameter type is not str"


    timestamp = hashlib.md5(timestamp.encode('utf-8')).hexdigest()
    index = hashlib.md5(index.encode('utf-8')).hexdigest()
    ws_name = hashlib.md5(ws_name.encode('utf-8')).hexdigest()
    retailer_name = hashlib.md5(retailer_name.encode('utf-8')).hexdigest()
    product_name = hashlib.md5(product_name.encode('utf-8')).hexdigest()

    notify_id = ''.join([timestamp, index, retailer_name, product_name])

    return notify_id

def check_whitespace(s):
    s = str(s)
    return bool(not s or s.isspace() and s == '')

