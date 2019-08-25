from django.urls import path,re_path, include
from rest_framework.authtoken.views import obtain_auth_token

from authentication.api_views import ListUsersView, LoginView, LogoutView, \
    ListUsersProfiles, UserFeedbackViewSet, ConfirmResetPasswordView, \
    ChangePasswordView, ResetPasswordView
from authentication.views import SignUp
from rest_framework import routers


router = routers.DefaultRouter()
router.register('user', ListUsersView, ListUsersProfiles)
router.register('profiles', ListUsersProfiles)
router.register(r'userfeedback', UserFeedbackViewSet)



app_name = "authentication"


urlpatterns = [
    path('sign_up', SignUp, name='sign_up'),
    re_path('', include(router.urls)),
    re_path(r'^auth-token$', obtain_auth_token),
    # re_path(r'^users$', ListUsersView.as_view({'get': 'list'})),
    # re_path(r'^user_profiles$', ListUsersProfiles.as_view({'get': 'list'})),
    re_path(r'^login$', LoginView.as_view(), name='login'),
    re_path(r'^logout$', LogoutView.as_view(), name='logout'),
    re_path(r'^password/reset$',ResetPasswordView.as_view(), name='password_reset'),
    re_path(r'^password/resetconfirm$', ConfirmResetPasswordView.as_view(),
            name='password_reset_confirm'),
    re_path(r'^password/change$', ChangePasswordView.as_view(), name='password_change'),
]