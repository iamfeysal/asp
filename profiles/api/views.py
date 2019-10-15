from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response

from profiles.api.serializers import UserProfileSerializer
from profiles.models import UserProfile
from users.models import User


class ListUsersProfiles(viewsets.ModelViewSet):
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()
    authentication_classes = (TokenAuthentication,)

    # permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        print("create user profile function")
        if 'user_profile' in request.data:
            user = User.objects.get(id=id)
            print('user profile is:', user.email)
            try:
                user = User.objects.get(user=user.id)
                user.save()
                serializer = UserProfileSerializer(user, many=False)
                response = {'message': 'user profile updated',
                            'result': serializer.data}
                print(response)
                return Response(response, status=status.HTTP_200_OK)

            except user.DoesNotExist:
                User.objects.create(use=user)
                serializer = UserProfileSerializer(user, many=False)
                response = {'message': 'user profile created',
                            'result': serializer.data}
                print(response)
                return Response(response, status=status.HTTP_200_OK)
            # response = {'message':'user updated','result':serializer.data}
            # return Response(response,status=status.HTTP_200_OK)

        else:
            response = {'message': 'you need to provide user profile', }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
