from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response

from rest_framework.views import APIView
from team.models import Team

# Create your views here.
from team.serializers import TeamSerializer, TeamSerializerCreate


class TeamView(APIView):
    @staticmethod
    def get(request):
        teams = Team.objects.all()
        return Response(TeamSerializer(teams, many=True).data)

    @staticmethod
    def post(request):
        serializer = TeamSerializerCreate(validated_data=request.data,
                                          context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(TeamSerializer(serializer.instance).data,
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
