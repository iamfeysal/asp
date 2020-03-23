from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from rest_framework.authtoken.models import Token
from django.utils import timezone

from asp.config.settings.local import AUTH_USER_MODEL


class PasswordResetRequest(models.Model):
    """Password request model

    Stores Password Reset Details and data.

    Extends:
        BaseModel

    Variables:
        uuid {str}
        token {str}
        reset_user {User}
        expiry_date {DateTimeField}
        is_active {bool}
    """

    uuid = models.CharField(max_length=48)
    token = models.CharField(max_length=128)
    reset_user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    expiry_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    def has_expired(self):
        """Check whether is past expiry data"""
        if timezone.now() > self.expiry_date:
            self.is_active = False
            self.save()
            return True
        return False
