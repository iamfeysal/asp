from rest_framework import serializers

from team.models import Team


class TeamSerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(required=False)

    class Meta:
        model = Team
        fields = '__all__'


class TeamSerializerCreate(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Team
        fields = '__all__'
