"""
repositories
"""
import uuid
from datetime import timedelta
from hashlib import sha512
from random import random

from django.utils import timezone

from asp.config.settings.base import AUTH_USER_MODEL
from authentication.models import PasswordResetRequest
from users.models import User


def new_reset_request_for_user_with_phone_number(phone_number):
    user = AUTH_USER_MODEL.objects.get(phone=phone_number)
    token = random.randint(100000, 999999)
    generated_uuid = uuid.uuid4().hex
    return PasswordResetRequest.objects.create(
        uuid=generated_uuid,
        token=token,
        reset_user=user,
        expiry_date=timezone.now() + timedelta(hours=1))


def new_reset_request_for_user_with_email(email_address):
    user = User.objects.get(email=email_address)
    # make the reset token as unique as possible, assuming user is not null
    generated_uuid = uuid.uuid4().hex
    token = _generate_token(email_address, generated_uuid)
    return PasswordResetRequest.objects.create(
        uuid=generated_uuid,
        token=token,
        reset_user=user,
        expiry_date=timezone.now() + timedelta(hours=1))


def _generate_token(email_address, random_uuid):
    encoded_str = "{0}-{1}".format(email_address, random_uuid).encode('utf-8')
    hash_str = sha512(encoded_str)
    return hash_str.hexdigest()


def find_active_password_request(token, unique_id=None):
    if unique_id is None:
        return PasswordResetRequest.objects.get(
            token=token, is_active=True, expiry_date__gte=timezone.now())
    else:
        return PasswordResetRequest.objects.get(
            uuid=unique_id, token=token, is_active=True,
            expiry_date__gte=timezone.now())


def reset_password(token, new_password):
    password_request = find_active_password_request(token)
    _change_user_password(password_request.reset_user, new_password)
    _deactivate_password_reset_request(password_request)
    return password_request.reset_user, password_request


def _deactivate_password_reset_request(password_reset_request):
    password_reset_request.is_active = False
    password_reset_request.save()


def _change_user_password(user, new_password):
    user.set_password(new_password)
    user.save()
