import json
import hmac
import hashlib
import base64
from django.conf import settings

from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()



def base64_encode(data):
    return base64.urlsafe_b64encode(data).decode('utf-8').rstrip('=')

def base64_decode_bytes(data: str):
    pending = '=' * (4 - len(data) % 4)
    return base64.urlsafe_b64decode(f'{data}{pending}'.encode())

def base64_decode(data: str):
    return base64_decode_bytes(data).decode('utf-8')


def create_url(payload):
    json_payload = json.dumps(payload)

    payload_base64 = base64_encode(json_payload.encode())

    data_to_sign = f'{payload_base64}'.encode()

    signature = hmac.new(settings.SECRET_KEY.encode(), data_to_sign, hashlib.sha256).digest()

    signature_base64 = base64_encode(signature)

    return f'{payload_base64}.{signature_base64}'


def verify_url(url):
    parts = url.split('.')

    if len(parts) != 2:
        return None

    payload_base64, signature_base64 = parts

    payload = json.loads(base64_decode(payload_base64))

    data_to_sign = f'{payload_base64}'.encode()

    signature_request = base64_decode_bytes(signature_base64)

    signature = hmac.new(settings.SECRET_KEY.encode(), data_to_sign, hashlib.sha256).digest()
    
    if signature_request != signature:
        return None

    if payload['expired_date'] < timezone.now().timestamp():
        return None
    
    user = User.objects.get(id=payload['id']) 
    user.is_active = True
    user.save()


