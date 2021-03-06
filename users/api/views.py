from rest_framework import viewsets, status, serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

import users
from users.api.serializers import UserFeedbackSerializer, UserSerializer
from users.models import User, Notification, UserFeedback
from users.api.serializers import NotificationSerializer


#
# class ListUsersView(viewsets.ModelViewSet):
#     
#     # print('hit list user view')
#     serializer_class = UserSerializer
#     queryset = User.objects.all()
#     authentication_classes = (TokenAuthentication,)
#     # # permission_classes = (IsAuthenticated,)
# 
#     def post(self, request, format=None) :
#         
#         print('hit user post-------------------------')
#         serializer = self.serializer_class(data=request.data)
#         print(serializer)
#         if serializer.is_valid():
#             print(serializer.is_valid())
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class UserViewSet(viewsets.ModelViewSet):
#     """User ViewSet.
#
#     get:
#     List all users
#
#     put:
#     Create new user with the given validated data
#
#     """
#
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     authentication_classes = (TokenAuthentication,)
#     # permission_classes = (IsAuthenticated,)
#
#
#     def create(self, request):
#         print('hit create view')
#         """
#         Create user with validated data from the serializer class
#         """
#         serializer = self.serializer_class(data=request.data)
#
#         if serializer.is_valid():
#             print(serializer.is_valid)
#             User.objects._create_user(**serializer.validated_data)
#             return Response(serializer.validated_data,
#                             status=status.HTTP_201_CREATED)
#
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserFeedbackViewSet(viewsets.ModelViewSet):
    """
            Lists user feedbacks
    """

    queryset = UserFeedback.objects.all()
    # permission_classes = (IsAuthenticated,)
    serializer_class = UserFeedbackSerializer


class Notifications(APIView):
    """
            Notification view.
    """
    def get(self, request, format=None):
        user = request.user
        notifications = Notification.objects.filter(to=user)
        serializer = NotificationSerializer(notifications, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


def create_notification(creator, to, notification_type, image=None,
                        comment=None):
    notifiation = Notification.objects.create(
        creator=creator,
        to=to,
        notification_type=notification_type,
    )
    notifiation.save()


class ExploreCoaches(APIView):
    """
            search and find coaches on the site
    """

    def get(self, request, fomrat=None):
        last_five = User.objects.filter(is_coach=True)

        serializer = UserSerializer(last_five, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class ExplorePlayers(APIView):
    """
            search and find players on the site
    """
    def get(self, request, fomrat=None):
        last_five = User.objects.filter(is_player=True)

        serializer = UserSerializer(last_five, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class FollowUser(APIView):
    """
            follow users in the site, both players and coaches
    """
    def post(self, request, user_id, format=None):
        user = request.user

        try:
            user_to_follow = users.models.User.objects.get(id=user_id)
        except users.models.User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        user.following.add(user_to_follow)
        user_to_follow.followers.add(user)
        user.save()
        create_notification(user, user_to_follow, 'follow')

        return Response(status=status.HTTP_200_OK)


class UnFollowUser(APIView):
    """
            unfollow users
    """
    def put(self, request, user_id, format=None):
        user = request.user

        try:
            user_to_follow = users.models.User.objects.get(id=user_id)
        except users.models.User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        user.following.remove(user_to_follow)
        user_to_follow.followers.remove(user)

        return Response(status=status.HTTP_200_OK)


class UserFollowers(APIView):
    """
            list and check user followers
    """
    def get(self, request, first_name, format=None):
        try:
            found_user = users.models.User.objects.get(first_name=first_name)
            print(found_user)
        except users.models.User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if found_user.userprofile == True:
            user_followers = found_user.userprofile.followers.all()
            print(user_followers)
        else:
            user_followers = found_user.followers.all()
            print("no user profile for followers", user_followers)
        serializer = UserSerializer(user_followers, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)


class UserFollowing(APIView):
    """
            list and check user following
    """
    def get(self, request, first_name, format=None):
        try:
            found_user = users.models.User.objects.get(first_name=first_name)
            print(found_user)
        except users.models.User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if found_user.userprofile is True:
            user_following = found_user.following.all()
            print(user_following)
        else:
            user_following = found_user.followers.all()
            print("no user profile for following", user_following)
        serializer = UserSerializer(user_following, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)


class Search(APIView):
    """
            search users by email
    """
    def get(self, request, format=None):
        email = request.query_params.get('email', None)
        if email is not None:
            users = User.objects.filter(
                username__istartswith=email)
            serializer = UserSerializer(users, many=True)

            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
