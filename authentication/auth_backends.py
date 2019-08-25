"""
ModelBackends for authentication
"""

import logging
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

LOGGER = logging.getLogger(__name__)
USER = get_user_model()


class AuthenticationBackend(ModelBackend):
    """
    Authenticates Users
    """

    def authenticate(self, **credentials):
        """Authenticate action

        Get user either according to username, email or phone and authenticate
        against the given password
        """
        # username or email patch since django default is username
        # username = credentials.get('username')
        email = credentials.get('email')

        login_parameter = email
        pwd_valid = credentials.get('password')

        if login_parameter and pwd_valid :
            try :
                user = USER.objects.get(
                    Q(email__iexact=login_parameter))
            except USER.DoesNotExist as not_exists_e:
                LOGGER.error(not_exists_e)
                return None
            if user.check_password(pwd_valid):
                return user

    def has_perm(self, user_obj, perm, obj=None):
        if perm == "view_users" :
            return True  
            # everybody can view
        # otherwise only the owner or the superuser can delete
        return user_obj.is_active and obj.user.pk == user_obj.pk

    def has_perms(self, user_obj, perm_list, obj=None) :
        return all(self.has_perm(user_obj, perm, obj) for perm in perm_list)


