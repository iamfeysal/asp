from rest_framework import permissions


class SuPermission(permissions.BasePermission) :

    def has_permission(self, request, view) :
        print("hit permission function")
        if request.user.is_authenticated and request.user.is_superuser:
            return "pass"
