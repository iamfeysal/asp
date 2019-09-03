from django.urls import re_path, include
from rest_framework import routers

from profiles.api.views import ListUsersProfiles

router = routers.DefaultRouter()

router.register('',ListUsersProfiles)

urlpatterns = [
    re_path('', include(router.urls)),
]

