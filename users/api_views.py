from rest_framework import generics, filters, viewsets
from rest_framework.authentication import TokenAuthentication
from users.serializers import UserSerializer

from users.models import User

class ListUsersView(viewsets.ModelViewSet) :
    serializer_class = UserSerializer
    queryset = User.objects.all()
    authentication_classes = (TokenAuthentication,)
