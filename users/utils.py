import time
import random
from datetime import datetime, timedelta
from django.core.mail import send_mail
from django.conf import settings
from django.core.cache import cache

def get_cache_key(username, flow):
    return f"register_{username}" if flow == 'register' else f"forgot_password_{username}"

def generate_and_send_otp(email, flow='register'):
    otp = random.randint(100000, 999999)
    if flow == 'register':
        subject = 'Your One Time Password (OTP) for ShelfWise'
        message = f'Your OTP code is {otp}'
    else:
        subject = 'Your One Time Password (OTP) for Password Reset'
        message = f'Your OTP code for password reset is {otp}'
    recipient_list = [email]
    email_from = settings.EMAIL_HOST_USER
    send_mail(subject, message, email_from, recipient_list, fail_silently=False)
    return otp

def set_cache_otp(username, otp, data, flow="register"):
    now = time.time()
    cache_data = {
        'otp': otp,
        'data': data,
        'last_sent': now,
    }
    cache_key = get_cache_key(username, flow)
    cache.set(cache_key, cache_data, timeout=60)  # 1 minutes expiry
    dt_object = datetime.fromtimestamp(now) + timedelta(minutes=3)
    iso_datetime = dt_object.isoformat()
    return iso_datetime

def verify_otp(username, otp, flow="register"):
    cache_key = get_cache_key(username, flow)
    cache_data = cache.get(cache_key)
    current_time = time.time()
    if not cache_data:
        message_registeration = 'No active registration session found. Please start the registration process again'
        message_reset_password = 'No active password reset session found. Please start the password reset process again.'
        return False, message_registeration if flow == 'register' else message_reset_password
    if abs(current_time - cache_data['last_sent']) > 60:
        return False, 'OTP expired. Try resend OTP.'
    if cache_data['otp'] != int(otp):
        return False, 'Invalid OTP'
    return True, cache_data

def delete_cache(cache_key):
    cache.delete(cache_key)
