from rest_framework import serializers, exceptions
from django.contrib.auth import authenticate, update_session_auth_hash, \
    get_user_model
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from authentication.auth_backends import AuthenticationBackend
from django.utils.translation import ugettext_lazy as _
from authentication.models import User, UserProfile, Skill, UserFeedback, \
    Notification


class UserProfileSerializer(serializers.ModelSerializer) :
    foot_choice = serializers.CharField(source='get_foot_choice_display')
    nationality = serializers.CharField(source='get_nationality_display')
    gender = serializers.CharField(source='get_gender_display')
    print("hit user serializer")

    class Meta:
        model = UserProfile
        # users = serializers.ReadOnlyField()
        fields = (
            "id", "user", "nickname","birth_date", "foot_choice", 
            "nationality", "current_status", "gender", "age")
        
class UserFeedbackSerializer(serializers.ModelSerializer):
    """
    Serializer for working with the feedback model
    """

    class Meta:
        model = UserFeedback
        fields = ("feedback_by", "message", "date_submitted",
                  "message_polarity")


class UserSkillsSerializer(serializers.ModelSerializer) :
    name = serializers.CharField()
    print("hit user serializer")

    class Meta :
        model = Skill
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer) :
    print("hit user serializer")
    userprofile = UserProfileSerializer(read_only=True)
    userfeedback = UserFeedbackSerializer(read_only=True)
    skills = UserSkillsSerializer(read_only=True, many=True)

    class Meta :
        model = User
        fields = (
            "id", "email", "full_name", "password", "date_joined", 
            "last_login", "followers_count","following_count",
            "userfeedback", "userprofile", "skills", )

        # read_only_fields = ('date_joined', "password", 'last_login', 'userprofile')
        extra_kwargs = {'password' : {'write_only' : True, 'required' : True}, }

        def create(self, validated_data) :
            """ Create user using given validated fields """
            # profile_data = validated_data.pop('profile')
            # password = validated_data.pop('password')
            # user = User(**validated_data)
            # user.set_password(password)
            # user.save()
            user = User.objects.create_user(**validated_data)
            return user

        def update(self, instance, validated_data) :
            """ Update user details """
            profile_data = validated_data.pop('profile')
            profile = instance.profile

            instance.email = validated_data.get('email', instance.email)
            instance.save()
            profile.birth_date = profile_data.get('birth_date',
                                                  profile.birth_date)
            profile.foot_choice = profile_data.get('foot_choice',
                                                   profile.foot_choice)
            profile.nationality = profile_data.get('nationality',
                                                   profile.nationality)
            profile.marital_status = profile_data.get('marital_status',
                                                      profile.marital_status)
            profile.age = profile_data.get('age', profile.age)
            return profile
            # instance.email = validated_data.get(
            #     'email', instance.email)
            # instance.save()
            # email = validated_data.get('email', None)
            # password = validated_data.get('password', None)
            # confirm_password = validated_data.get('confirm_password', None)
            # 
            # if password and confirm_password and password == confirm_password :
            #     instance.set_password(password)
            #     instance.save()
            # update_session_auth_hash(self.context.get('request'), instance)
            # return instance


class LoginSerializer(serializers.Serializer) :
    """ Logs in existing users """
    email = serializers.EmailField(required=True, allow_blank=False)
    password = serializers.CharField(
        style={'input_type' : 'password'}, required=True)

    def create(self, validated_data) :
        pass

    def update(self, instance, validated_data) :
        pass

    def validate(self, attrs) :
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
        

class NotificationSerializer(serializers.ModelSerializer):

    creator = UserSerializer()
    class Meta:
     model = Notification
     fields = '__all__'