from rest_framework import generics, filters, viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework import serializers, exceptions
from django.contrib.auth import login, logout
from . import serializers, models


from django.conf import settings
from rest_framework.generics import GenericAPIView, UpdateAPIView
from rest_framework.settings import api_settings
from rest_framework.views import APIView

from authentication.serializers import UserSerializer, LoginSerializer, \
    TokenSerializer, UserProfileSerializer, UserFeedbackSerializer, \
    ChangePasswordSerializer, ResetPasswordSerializer, \
    ConfirmResetPasswordSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, AllowAny

from authentication.models import User, UserProfile, UserFeedback, PasswordResetRequest


from authentication.messages import send_mail, send_email
from authentication.repositories import find_active_password_request
from authentication.helpers import validate_string, send_email_for_password_reset


class ListUsersView(viewsets.ModelViewSet) :
    serializer_class = UserSerializer
    queryset = User.objects.all()
    authentication_classes = (TokenAuthentication,)

    # permission_classes = (IsAuthenticated,)

    def post(self, request, format=None) :
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListUsersProfiles(viewsets.ModelViewSet) :
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()
    authentication_classes = (TokenAuthentication,)

    # permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs) :
        print("create user profile function")
        if 'user_profile' in request.data :
            user = User.objects.get(id=id)
            print('user profile is:', user.email)
            try :
                user = User.objects.get(user=user.id)
                user.save()
                serializer = UserProfileSerializer(user, many=False)
                response = {'message' : 'user profile updated',
                            'result' : serializer.data}
                print(response)
                return Response(response, status=status.HTTP_200_OK)


            except :
                User.objects.create(use=user)
                serializer = UserProfileSerializer(user, many=False)
                response = {'message' : 'user profile created',
                            'result' : serializer.data}
                print(response)
                return Response(response, status=status.HTTP_200_OK)
            # response = {'message':'user updated','result':serializer.data}
            # return Response(response,status=status.HTTP_200_OK)

        else :
            response = {'message' : 'you need to provide user profile', }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class LoginView(GenericAPIView) :
    print('hit login view')
    """Login View.

    post:
    Accept the following POST parameters: ``username``, ``password``
    Return the REST Framework Token Object's key, after validating through
    the serializer
    Else returns status_code = 401 if user with login credentials does not
    exist or 403 if the user exist but the account is deactivated, 400 if bad
    request
    """

    serializer_class = LoginSerializer
    token_model = Token
    response_serializer = TokenSerializer

    def login(self) :
        self.user = self.serializer.validated_data['user']
        print(self.user)
        self.token, created = self.token_model.objects.get_or_create(
            user=self.user)
        print(self.token)
        if getattr(settings, 'REST_SESSION_LOGIN', True) :
            login(self.request, self.user)

    def get_response(self) :
        resp_dict = {'key' : self.response_serializer(
            self.token).data['key'], 'is_staff' : self.user.is_staff}
        return Response(resp_dict, status=status.HTTP_200_OK)

    def get_error_response(self) :
        return Response(
            self.serializer.errors, status=status.HTTP_401_UNAUTHORIZED
            # HTTP_400_BAD_REQUEST
        )

    def post(self, request, *args, **kwargs) :
        self.serializer = self.get_serializer(data=self.request.data)
        if not self.serializer.is_valid() :
            # what kind of error do we have
            is_invalid_credentials = getattr(
                self.serializer, "invalid_credentials", False)
            if is_invalid_credentials :
                return Response(self.serializer.errors,
                                status=status.HTTP_401_UNAUTHORIZED)
            is_inactive_account = getattr(
                self.serializer, "account_inactive", False)
            if is_inactive_account :
                return Response(self.serializer.errors,
                                status=status.HTTP_403_FORBIDDEN)
            return self.get_error_response()
        self.login()
        return self.get_response()


class LogoutView(APIView) :
    """Logout View.

    post:
    Calls Django logout method, delete the token object
    assigned to the current User object.
    Accepts/Returns nothing.
    """

    def post(self, request) :
        try :
            request.user.auth_token.delete()
        except Exception :
            pass
        logout(request)
        return Response({"success" : "Successfully logged out."},
                        status=status.HTTP_200_OK)

class ResetPasswordView(GenericAPIView) :
    """Reser Password View.

    Resets user's password
    post:
    Takes ``phone`` request field and,
    Returns either ``success`` or ``failed``
    """

    serializer_class = ResetPasswordSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs) :
        # fetch submitted data
        reset_status, token, uuid = \
            send_email_for_password_reset(request, request.data['email'])

        if token :
            resp_status = status.HTTP_200_OK
        else :
            resp_status = status.HTTP_400_BAD_REQUEST

        return Response(
            {"status" : reset_status, "uuid" : uuid},
            status=resp_status)


class ConfirmResetPasswordView(GenericAPIView):
    """Confirm password request from api post

    Arguements:
        new_password{string}
        new_password_repeat{string}
        uuid{string}
    """

    serializer_class = ConfirmResetPasswordSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        resp = {}
        try:
            password_request = find_active_password_request(
                token=request.data['token'], unique_id=request.data['uuid'])

        except PasswordResetRequest.DoesNotExist:
            resp['status'] = "failed"
            resp['message'] = "An unexpected error occurred."
            response_status = status.HTTP_400_BAD_REQUEST
            send_email(
                'Password Reset: Red Flag',
                'Incorrect password request Initiated with uuid:{} and '
                'token:{}'.format(request.data['uuid'],
                                  request.data['token']),
                settings.UNAUTHORISED_REQUEST,
                from_email='iamfeysal@gmail.com',
                fail_silently=False,
            )
            return Response(resp, status=response_status)

        try:
            if request.data['new_password'] \
                    == request.data['new_password_repeat']:

                message, string_is_valid = \
                    validate_string(request.data['new_password'])

                if string_is_valid:
                    password_request.reset_user \
                        .set_password(request.data['new_password'])
                    password_request.reset_user.save()
                    password_request.is_active = False
                    password_request.save()
                    resp['status'] = "success"
                    resp['message'] = "password successfully changed"
                    response_status = status.HTTP_200_OK
                else:
                    resp['status'] = "failed"
                    resp['message'] = message
                    response_status = status.HTTP_400_BAD_REQUEST
            else:
                resp['status'] = "failed"
                resp['message'] = "password do not match"
                response_status = status.HTTP_400_BAD_REQUEST
        except Exception as exception:
            resp['status'] = "failed"
            resp['message'] = "An error occurred."
            # this should be moved to logging
            send_email(
                'Password Request Error',
                'Error:{}'.format(exception),
                settings.UNAUTHORISED_REQUEST,
                from_email='iamfeysal@gmail.com',
                fail_silently=False,
            )
            response_status = status.HTTP_400_BAD_REQUEST

        return Response(resp, status=response_status)


class ChangePasswordView(UpdateAPIView):
    """Change Password View.

    Calls Django Auth SetPasswordForm save method.
    Accepts the following POST parameters:
    ``old_password``, ``new_password1``, ``new_password2``
    Returns the success/fail message.
    """

    serializer_class = ChangePasswordSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(
                    serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]},
                                status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response("New password has been saved.",
                            status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserFeedbackViewSet(viewsets.ModelViewSet):
    """
    Lists user feedbacks
    """

    queryset = UserFeedback.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = UserFeedbackSerializer

class Notifications(APIView):
    def get(self, request, format=None):
        user = request.user
        notifications = models.Notification.objects.filter(to=user)

        serializer = serializers.NotificationSerializer(notifications, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)



def create_notification(creator, to, notification_type, image=None, comment=None):

    notifiation = models.Notification.objects.create(
        creator=creator,
        to=to,
        notification_type=notification_type,
    )
    notifiation.save()

class FollowUser(APIView) :
    def post(self, request, user_id, format=None) :
        user = request.user

        try:
            user_to_follow = models.User.objects.get(id=user_id)
        except models.User.DoesNotExist :
            return Response(status=status.HTTP_404_NOT_FOUND)

        user.following.add(user_to_follow)
        user_to_follow.followers.add(user)
        user.save()
        create_notification(user, user_to_follow, 'follow')

        return Response(status=status.HTTP_200_OK)

# Url : path("<int:user_id>/unfollow/", view=views.UnFollowUser.as_view(), name="unfollow_user")
class UnFollowUser(APIView) :
    def put(self, request, user_id, format=None) :
        user = request.user

        try:
            user_to_follow = models.User.objects.get(id=user_id)
        except models.User.DoesNotExist :
            return Response(status=status.HTTP_404_NOT_FOUND)

        user.following.remove(user_to_follow)
        user_to_follow.followers.remove(user)

        return Response(status=status.HTTP_200_OK)


# path("<first_name>/followers", view=views.UserFollowers.as_view(), name="user_followers")
class UserFollowers(APIView):
    def get(self, request, first_name, format=None):
        try :
            found_user = models.User.objects.get(first_name=first_name)
            print(found_user)
        except models.User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if found_user.userprofile == True:
            user_followers = found_user.userprofile.followers.all()
            print(user_followers)
        else: 
           user_followers = found_user.followers.all()
           print("no user profile for followers", user_followers)
        serializer = serializers.UserSerializer(user_followers, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)


# path("<first_name>/following", view=views.UserFollowing.as_view(), name="user_following")
class UserFollowing(APIView) :
    def get(self, request, first_name, format=None):
        try:
            found_user = models.User.objects.get(first_name=first_name)
        except models.User.DoesNotExist :
            return Response(status=status.HTTP_404_NOT_FOUND)
        if found_user.userprofile == True:
            user_following = found_user.following.all()
            print(user_following)
        else:
            user_following = found_user.followers.all()
            print("no user profile for following", user_following)
        serializer = serializers.UserSerializer(user_following, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)


# path("search/", view=views.Search.as_view(), name="search")       
class Search(APIView) :
    def get(self, request, format=None) :
        email = request.query_params.get('email', None)
        if email is not None :
            users = models.User.objects.filter(username__istartswith=email)
            serializer = serializers.UserSerializer(users, many=True)

            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else :
            return Response(status=status.HTTP_400_BAD_REQUEST)


# path("<username>/password", view=views.ChangePassword.as_view(), name="change_password")
class ChangePassword(APIView) :
    def put(self, request, email, format=None) :
        user = request.user

        if user.email == email :
            current_password = request.data.get('current_password', None)
            if current_password is not None :
                passwords_match = user.check_password(current_password)
                if passwords_match :
                    new_password = request.data.get('new_password', None)
                    if new_password is not None :
                        user.set_password(new_password)
                        user.save()
                        return Response(status=status.HTTP_200_OK)
                    else :
                        return Response(status=status.HTTP_400_BAD_REQUEST)
                else :
                    return Response(status=status.HTTP_400_BAD_REQUEST)
            else :
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else :
            return Response(status=status.HTTP_401_UNAUTHORIZED)