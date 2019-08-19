from django.urls import path, include
from users.api_views import ListUsersView
from rest_framework import routers


router = routers.DefaultRouter()
router.register('user', ListUsersView)

urlpatterns = [
    path('',include(router.urls))
]