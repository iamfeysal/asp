from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager) :
    """Create user given email and password"""

    def create_user(self, email, password, **extra_fields):
        print('print create user view function')
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(
            email=self.normalize_email(email),
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_normal_user(self, email, password=None, **extra_fields) :
        """Create standard user account without any privileges"""
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

    def create_staff(self, email, password=None, **extra_fields) :
        """Create Staff user account"""
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Staff must have is_staff=True.')

        return self._create_user(email, password, **extra_fields)
