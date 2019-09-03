from rest_framework import serializers

from profiles.models import UserProfile


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