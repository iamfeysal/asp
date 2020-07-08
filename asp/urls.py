from django.contrib import admin
from django.urls import path, re_path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('authentication/', include('authentication.api.urls')),
    path('users/', include('users.api.urls')),
    path('profiles/', include('profiles.api.urls')),
    path('teams/', include('team.urls')),
    # path('commands', include('commands.api.urls')),



]
