from rest_framework import serializers, exceptions
from django.contrib.auth import authenticate, update_session_auth_hash, \
    get_user_model
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from authentication.auth_backends import AuthenticationBackend
from django.utils.translation import ugettext_lazy as _
from authentication.models import User


class UserSerializer(serializers.ModelSerializer) :
    print("hit user serializer")

    class Meta :
        model = User
        fields = (
        "id", "email", "password", "date_joined", "last_login")

        read_only_fields = ('date_joined', 'last_login',)

        def create(self, validated_data) :
            """ Create user using given validated fields """
            return User.objects.create(**validated_data)

        def update(self, instance, validated_data) :
            """ Update user details """
            instance.email = validated_data.get(
                'email', instance.email)
            instance.save()
            email = validated_data.get('email', None)
            password = validated_data.get('password', None)
            confirm_password = validated_data.get('confirm_password', None)

            if password and confirm_password and password == confirm_password :
                instance.set_password(password)
                instance.save()
            update_session_auth_hash(self.context.get('request'), instance)
            return instance


class LoginSerializer(serializers.Serializer) :
    """ Logs in existing users """
    email = serializers.EmailField(required=True, allow_blank=False)
    password = serializers.CharField(
        style={'input_type' : 'password'}, required=True)

    def create(self, validated_data) :
        pass

    def update(self, instance, validated_data) :
        pass

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        auth = AuthenticationBackend()

        if email and password :
            user = auth.authenticate(email=email, password=password)
        else :
            msg = _('Must include "email" and "password".')
            raise exceptions.ValidationError(msg)

        # Did we get back an active user?
        if user :
            if not user.is_active :
                msg = _('User account is disabled.')
                setattr(self, "account_inactive", True)
                raise exceptions.ValidationError(msg)
        else :
            msg = _('Unable to log in with provided credentials.')
            setattr(self, "invalid_credentials", True)
            raise exceptions.ValidationError(msg)

        attrs['user'] = user
        return attrs


class TokenSerializer(serializers.ModelSerializer) :
    """Token model serializer for fields: key"""

    class Meta :
        model = Token
        fields = ('key',)
