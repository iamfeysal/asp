import itertools

import jwt
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.conf import settings
from datetime import datetime, timedelta
from django.core import validators
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.defaultfilters import slugify
from rest_framework.authtoken.models import Token
from authentication.messages import send_mail
from django.utils.translation import ugettext_lazy as _


from authentication.managers import UserManager


class User(AbstractBaseUser) :
    username = models.SlugField(_('username'), max_length=50, unique=True,
                                help_text=_('Required. 50 characters or fewer.'
                                            ' Letters, digits and'
                                            ' @/./+/-/_ only.'),
                                validators=[validators.RegexValidator(
                                    r'^[\w.@+-]+$',
                                    _('Enter a valid username. '
                                      'This value may contain only letters,'
                                      ' numbers and @/./+/-/_ characters.'),
                                    'invalid'), ],
                                error_messages={
                                    'unique' : _("A user with that"
                                                 " username already exists."), }
                                )

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
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self) :
        return self.email


    # @property
    # def token(self) :
    #     dt = datetime.now() + timedelta(days=60)
    #     token = jwt.encode({
    #         'id' : self.pk,
    #         'exp' : int(dt.strftime('%s'))
    #     }, settings.SECRET_KEY, algorithm='HS256')
    #     return token.decode('utf-8')


    # For checking permissions. to keep it simple all admin have ALL permissons
    def has_perm(self, perm, obj=None) :
        return self.is_admin

    # Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
    def has_module_perms(self, app_label) :
        return True

    def save(self, force_insert=False, force_update=False,
             using=None, update_fields=None):
        """Override save model."""
        if not self.username:
            max_length = self.__class__._meta.get_field('username').max_length
            self.username = orig = slugify(
                 self.email)[:max_length]
            for x in itertools.count(1):
                if not self.__class__.objects.filter(
                        username=self.username).exists():
                    break
                self.username = "%s-%d" % (orig[:max_length -
                                                len(str(x)) - 1], x)
        else:
            self.username = slugify(self.username)

        super(User, self).save(force_insert=force_insert,
                               force_update=force_update, using=using,
                               update_fields=update_fields)

    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def create_auth_token(sender, instance=None, created=False, **kwargs):
        """Create Auth Token

        This code is triggered whenever a new user has been created
        and saved to the database
        """
        if created:
            Token.objects.create(user=instance)

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user"""
        return send_mail(
            subject, message, [self.email], from_email=from_email, **kwargs)