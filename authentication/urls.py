from django.urls import path,re_path, include
from rest_framework.authtoken.views import obtain_auth_token

from authentication.api_views import ListUsersView, LoginView, LogoutView, \
    ListUsersProfiles
from rest_framework import routers


router = routers.DefaultRouter()
router.register('user', ListUsersView, ListUsersProfiles)
router.register('user profiles', ListUsersProfiles)



app_name = "authentication"


urlpatterns = [
    re_path('', include(router.urls)),
    re_path(r'^', include(router.urls)),
    re_path(r'^auth-token$', obtain_auth_token),
    re_path(r'^login$', LoginView.as_view(), name='login'),
    re_path(r'^logout$', LogoutView.as_view(), name='logout'),
]