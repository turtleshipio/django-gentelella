from datetime import datetime, timedelta
from app import config
import jwt

def issue_token(username, phone, pickup_user_id, name, pickteam_id):
    now = datetime.utcnow()
    payload = {
        'username': username,
        'phone': phone,
        'pickup_user_id': pickup_user_id,
        'pickteam_id' : pickteam_id,
        'name': name,
        'acc_type' : 'pickup',
        'iat': now,
        'exp': now + timedelta(5)
    }
    jwt_token = jwt.encode(payload, config.JWT['secret'], config.JWT['algorithm'])
    token = jwt_token.decode('utf-8')
    print(token)
    return token