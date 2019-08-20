from rest_framework import generics, filters, viewsets, status
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth import login, logout

from django.conf import settings
from rest_framework.generics import GenericAPIView
from rest_framework.settings import api_settings
from rest_framework.views import APIView

from authentication.serializers import UserSerializer, LoginSerializer, \
    TokenSerializer, UserProfileSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated

from authentication.models import User, UserProfile


class ListUsersView(viewsets.ModelViewSet) :
    serializer_class = UserSerializer
    queryset = User.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    # # filter the collections
    # filter_backends = (DjangoFilterBackend, filters.SearchFilter,
    #                    filters.OrderingFilter,)
    # filter_fields = ('username')
    # ordering_fields = ('date_joined',)
    # search_fields = ('username')

    def post(self, request, format=None) :
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid() :
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # def create(self, validated_data):
    # 
    #     # create user 
    #     user = User.objects.create(
    #         email = validated_data['email'],
    #         password= validated_data['password']
    #         # etc ...
    #     )
    # 
    #     profile_data = validated_data.pop('profile')
    #     # create profile
    #     profile = UserProfile.objects.create(
    #         user = user,
    #         nationality = profile_data['nationality'],
    #         # etc...
    #     )


class ListUsersProfiles(viewsets.ModelViewSet) :
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    

    # # filter the collections
    # filter_backends = (DjangoFilterBackend, filters.SearchFilter,
    #                    filters.OrderingFilter,)
    # filter_fields = ('username')
    # ordering_fields = ('date_joined',)
    # search_fields = ('username')

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

    #     print('create post method')
    #     """
    #     Create user with validated data from the serializer class
    #     """
    #     serializer = self.serializer_class(data=request.data)
    # 
    #     if serializer.is_valid():
    #         User.objects.create_user(**serializer.validated_data)
    #         print('create method', serializer.validated_data)
    # 
    #         return Response(serializer.validated_data,
    #                         status=status.HTTP_201_CREATED)
    #     else:
    #         User.objects.get(**serializer.validated_data)
    #         response = {'message':'getting item','result':serializer.validated_data,}
    #         print('get method', response)
    #         return Response(response, status=status.HTTP_200_OK)
    # return Response({
    #     'status': 'Bad request',
    #     'message': 'User account could not be created with received data.'
    # }, status=status.HTTP_400_BAD_REQUEST)


class LoginView(GenericAPIView):
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
