from django.urls import include, re_path
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

from authentication.api.views import ChangePasswordView, \
    ConfirmResetPasswordView, LoginView, LogoutView, ResetPasswordView, \
    UserViewSet

router = routers.DefaultRouter()
router.register(r'createuser', UserViewSet)

app_name = "authentication"

urlpatterns = [
    re_path('', include(router.urls)),
    re_path(r'^auth-token$', obtain_auth_token),
    re_path(r'^login$', LoginView.as_view(), name='login'),
    re_path(r'^logout$', LogoutView.as_view(), name='logout'),
    re_path(r'^password/reset$', ResetPasswordView.as_view(),
            name='password_reset'),
    re_path(r'^password/resetconfirm$', ConfirmResetPasswordView.as_view(),
            name='password_reset_confirm'),
    re_path(r'^password/change$', ChangePasswordView.as_view(),
            name='password_change'),
]
