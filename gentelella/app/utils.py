from datetime import datetime, timedelta
import pytz
import jwt
from app import config
import random
import string

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
        'name': name,
        'iat': now,
        'exp': now + timedelta(5)
    }
    jwt_token = jwt.encode(payload, config.JWT['secret'], config.JWT['algorithm'])
    token = jwt_token.decode('utf-8')
    return token


def get_context_from_token(token):

    context = {
        'retail_user': {
            'username': token['username'],
            'retailer_id': token['retailer_id'],
            'phone': token['phone'],
            'name': token['name'],
        }
    }

    return context


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


def get_uuid(n):
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(n))