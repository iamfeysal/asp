from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from authentication.messages import send_mail
from django.dispatch import receiver
from django.db.models.signals import post_save
from datetime import datetime
from django_countries.fields import CountryField
from asp.settings import AUTH_USER_MODEL

from authentication.managers import UserManager


class User(AbstractBaseUser) :
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    date_joined = models.DateTimeField(verbose_name='date joined',
                                       auto_now_add=True)
    is_player = models.BooleanField('player status', default=False)
    is_coach = models.BooleanField('coach status', default=False)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self) :
        return self.email

    def has_perm(self, perm, obj=None) :
        return self.is_admin

    # Does this user have permission to view this app? (ALWAYS YES FOR
    # SIMPLICITY)

    def has_module_perms(self, app_label) :
        """

        :param app_label: 
        :return: 
        """
        return True

    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def create_auth_token(sender, instance=None, created=False, **kwargs) :
        """Create Auth Token

        This code is triggered whenever a new user has been created
        and saved to the database
        """
        if created :
            Token.objects.create(user=instance)

    def email_user(self, subject, message, from_email=None, **kwargs) :
        """Send an email to this user"""
        return send_mail(
            subject, message, [self.email], from_email=from_email, **kwargs)


class UserProfile(models.Model) :
    MARITAL_STATUS_CHOICES = (
        ('m', 'Single'),
        ('f', 'Engaged'),
        ('pns', 'Prefer not to say'),
    )
    PREFERED_PLAY_FOOT = (
        ('r', 'Right'),
        ('l', 'Left'),
        ('b', 'Both'),
    )

    user = models.OneToOneField(AUTH_USER_MODEL, null=True,
                                on_delete=models.CASCADE)
    birth_date = models.DateField(null=True)
    foot_choice = models.CharField(max_length=1, choices=PREFERED_PLAY_FOOT,
                                   null=True)
    nationality = CountryField()
    marital_status = models.CharField(max_length=1,
                                      choices=MARITAL_STATUS_CHOICES, null=True)


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs) :
    if created :
        UserProfile.objects.create(user=instance)
    instance.profile.save()

    @property
    def age(self) :
        return int((datetime.now().date() - self.birth_date).days / 365.25)
