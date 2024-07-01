import time
from datetime import datetime
from datetime import timedelta
from rest_framework_simplejwt.tokens import RefreshToken
import jwt


def create_bearer_token(obj):
    refresh = RefreshToken.for_user(obj)
    return str(refresh.access_token)


def create_sms_token(credentials):
    time.sleep(2)
    sms_code = '1234'
    now = datetime.utcnow()
    payload = {
        'iat': now,
        'nbf': now,
        'exp': now + timedelta(minutes=5),
        'credentials': dict(credentials),
        'sent_sms_code': sms_code,
    }
    token = jwt.encode(payload, '')
    return token
