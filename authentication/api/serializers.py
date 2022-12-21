from rest_framework import exceptions
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from authentication.auth_backends import AuthenticationBackend
from django.utils.translation import gettext_lazy as _


class LoginSerializer(serializers.Serializer):
    """ Logs in existing users """
    email = serializers.EmailField(required=True, allow_blank=False)
    password = serializers.CharField(
        style={'input_type': 'password'}, required=True)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        auth = AuthenticationBackend()

        if email and password:
            user = auth.authenticate(email=email, password=password)
        else:
            msg = _('Must include "email" and "password".')
            raise exceptions.ValidationError(msg)

        # Did we get back an active user?
        if user:
            if not user.is_active:
                msg = _('User account is disabled.')
                setattr(self, "account_inactive", True)
                raise exceptions.ValidationError(msg)
        else:
            msg = _('Unable to log in with provided credentials.')
            setattr(self, "invalid_credentials", True)
            raise exceptions.ValidationError(msg)

        attrs['user'] = user
        return attrs


class TokenSerializer(serializers.ModelSerializer):
    """Token model serializer for fields: key"""

    class Meta:
        model = Token
        fields = ('key',)


class ResetPasswordSerializer(serializers.Serializer):
    """
    Serializer for requesting a password reset
    """
    email = serializers.CharField(required=False)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class ConfirmResetPasswordSerializer(serializers.Serializer):
    """Serializer for confirming a password reset"""

    new_password = serializers.CharField(max_length=128)
    new_password_repeat = serializers.CharField(max_length=128)
    uuid = serializers.CharField(required=True)
    token = serializers.CharField(required=True)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class ChangePasswordSerializer(serializers.Serializer):
    """Serializer for updating a password."""

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass
