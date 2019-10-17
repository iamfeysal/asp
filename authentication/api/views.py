from django.conf import settings
from django.contrib.auth import login, logout
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.generics import GenericAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.models import PasswordResetRequest
from authentication.api.serializers import LoginSerializer, TokenSerializer, \
    ResetPasswordSerializer, ConfirmResetPasswordSerializer, \
    ChangePasswordSerializer
from users.api.serializers import UserSerializer
from commands.helpers import send_email_for_password_reset, validate_string
from commands.messages import send_email
from commands.repositories import find_active_password_request
from django.template.loader import get_template
from django.core.mail import send_mail
from users.models import User


class UserViewSet(viewsets.ModelViewSet):
    """User ViewSet.

    get:
    List all users

    put:
    Create new user with the given validated data

    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAuthenticated,)


    def create(self, request):
        print('hit create view')
        """
        Create user with validated data from the serializer class
        """
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            # print(serializer.is_valid)
            User.objects._create_user(**serializer.validated_data)
            nickname = serializer.data['email']
            print(nickname)
            recipient = [serializer.data['email']]
            print(recipient)
            email_subject = 'DUENDE FOOTBALL - Confirmation Profile Activation'
            print(email_subject)
            message = get_template('registration/email_signup.html').render(
                {
                    'nickname': nickname,
                }
            )
            print(message)

            send_mail(email_subject,
                      message,
                      'iamfeysal@gmail.com',
                      recipient,
                      fail_silently=False,
                      html_message=message,
                      )
            print(send_mail)

            return Response(serializer.validated_data,
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(GenericAPIView) :
    """Login View.

    post:
    Accept the following POST parameters: ``email``, ``password``
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
        print('login api views function')
        self.user = self.serializer.validated_data['user']
        # print(self.user)
        self.token, created = self.token_model.objects.get_or_create(
            user=self.user
        )
        # print(self.token)
        if getattr(settings, 'REST_SESSION_LOGIN', True):
            login(self.request, self.user)

    def get_response(self):
        print('response function')
        resp_dict = {'key' : self.response_serializer(
            self.token).data['key'], 'is_staff' : self.user.is_staff}
        print(resp_dict)
        return Response(resp_dict, status=status.HTTP_200_OK)

    def get_error_response(self) :
        return Response(
            self.serializer.errors, status=status.HTTP_401_UNAUTHORIZED
            # HTTP_400_BAD_REQUEST
        )

    def post(self, request, *args, **kwargs) :
        print('post request of auth api')
        self.serializer = self.get_serializer(data=self.request.data)
        if self.serializer.is_valid():
            print(self.serializer.is_valid())
            self.login()
        if not self.serializer.is_valid():
            # what kind of error do we have
            is_invalid_credentials = getattr(
                self.serializer, "invalid_credentials", False)
            if is_invalid_credentials:
                return Response(self.serializer.errors,
                                status=status.HTTP_401_UNAUTHORIZED)
            is_inactive_account = getattr(
                self.serializer, "account_inactive", False)
            if is_inactive_account:
                return Response(self.serializer.errors,
                                status=status.HTTP_403_FORBIDDEN)
            return self.get_error_response()
        return self.get_response()


class LogoutView(APIView):
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


class ResetPasswordView(GenericAPIView):
    """Reset Password View.

    Resets user's password
    post:
    Takes ``phone or email`` request field and,
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


class ChangePassword(APIView) :
    def put(self, request, email, format=None):
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