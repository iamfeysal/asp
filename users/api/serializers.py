from rest_framework import serializers

from profiles.api.serializers import UserProfileSerializer
from users.models import User, UserFeedback, Skill, Notification


class UserFeedbackSerializer(serializers.ModelSerializer):
    """
    Serializer for working with the feedback model
    """

    class Meta:
        model = UserFeedback
        fields = ("user", "message", "date_submitted",
                  "message_polarity")


class UserSkillsSerializer(serializers.ModelSerializer) :
    name = serializers.CharField()

    class Meta :
        model = Skill
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    userprofile = UserProfileSerializer(read_only=True)
    # userfeedback, = UserFeedbackSerializer()
    skills = UserSkillsSerializer(read_only=True, many=True)

    class Meta:
        model = User
        fields = (
            "id", "email", "password", "date_joined", "displayed_name",
            "last_login", "followers_count","following_count",
             "userprofile", "skills", )

        # read_only_fields = ('date_joined', "password", 'last_login', 'userprofile')
        extra_kwargs = {'password' : {'write_only' : True, 'required' : True}, }

        def create(self, validated_data) :
            print('hit users serializer create function')
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


class NotificationSerializer(serializers.ModelSerializer):

    creator = UserSerializer()
    class Meta:
     model = Notification
     fields = '__all__'