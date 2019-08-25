from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.conf import settings
from django.db.models.signals import pre_save
from rest_framework.authtoken.models import Token
from authentication.messages import send_mail
from django.dispatch import receiver
from django.db.models.signals import post_save
from datetime import datetime
from django_countries.fields import CountryField
from django.utils import timezone
from asp.settings import AUTH_USER_MODEL

from authentication.managers import UserManager


class Skill(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        
        permissions = (
            ("view_category", "view category"),
            ("add_category", "Add category"),
            ("delete_category", "Delete category"),
        )
    
    def __str__(self) :
        return self.name


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
    skills = models.ManyToManyField(Skill)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta :
        permissions = (
            ("viw_user", "view user"),
            ("ad_user", "Add user"),
            ("dlt_user", "Delete user"),
        )

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

    def email_user(self, subject='welcome', message='welcome', 
                   from_email='iamfeysal@gmail.com', **kwargs):
        print('hit email function')
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)
        print(send_mail)

    def pre_save_listener(sender, instance, *args, **kwargs):
        if instance.is_player :
            instance.is_coach = False
        if instance.is_coach :
            instance.is_player = False

    pre_save.connect(receiver=pre_save_listener, sender=AUTH_USER_MODEL)


class UserProfile(models.Model) :
    GENDER_CHOICES = (
        ('m', 'Male'),
        ('f', 'Female'),
        ('pns', 'Prefer not to say'),
    )

    PREFERED_PLAY_FOOT = (
        ('r', 'Right'),
        ('l', 'Left'),
        ('b', 'Both'),
    )

    owner = models.OneToOneField(AUTH_USER_MODEL, null=True,
                                on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profiles')
    birth_date = models.DateField(null=True)
    foot_choice = models.CharField(max_length=1, choices=PREFERED_PLAY_FOOT,
                                   null=True)
    nationality = CountryField()
    gender = models.CharField(max_length=1,
                              choices=GENDER_CHOICES, null=True)
    current_status = models.CharField(max_length=255,
                                      help_text='free agent or playing for larriskos  fc',
                                      blank=True, null=True)
    fans = models.IntegerField(default=0)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    second_name = models.CharField(max_length=255, blank=True, null=True)
    nickname = models.CharField(max_length=255, blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    
    class Meta:
        permissions = (
            ("view_profile", "view profile"),
            ("add_profile", "Add profile"),
            ("delete_profile", "Delete profile"),
        )

    def age(self) :
        if self.birth_date is None :
            pass
        else:
            # handle case where there's no value for checkout 
            return int((datetime.now().date() - self.birth_date).days / 365.25)

    def full_name(self) :
        """
        :return: 
        """
        full_name = '%s %s' % (self.first_name, self.second_name)
        return full_name.strip()

    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def update_user_profile(sender, instance, created, **kwargs) :
        if created:
            UserProfile.objects.create(user=instance)
            instance.userprofile.save()
        else:
            print('updated')

class PasswordResetRequest(models.Model):
    """Password request model

    Stores Password Reset Details and data.

    Extends:
        BaseModel

    Variables:
        uuid {str}
        token {str}
        reset_user {User}
        expiry_date {DateTimeField}
        is_active {bool}
    """

    uuid = models.CharField(max_length=48)
    token = models.CharField(max_length=128)
    reset_user = models.ForeignKey(User, on_delete=models.CASCADE)
    expiry_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    def has_expired(self):
        """Check whether is past expiry data"""
        if timezone.now() > self.expiry_date:
            self.is_active = False
            self.save()
            return True
        return False
    
    
class UserFeedback(models.Model):
    """User Feedback model

    User Feed back collection form

    Extends:
        BaseModel

    Variables:
        FEEDBACK_CHOICES {tuple}
        feedback_by {User}
        message {text}
        date_submitted {DateTimeField}
        message_polarity {str}
    """

    FEEDBACK_CHOICES = (
        ("positive", "Positive Experience"),
        ("negative", "Negative Experience"),
        ("undefined", "Undefined"),
    )

    owner = models.ForeignKey(AUTH_USER_MODEL, blank=True, null=True,
                                    on_delete=models.SET_NULL)
    message = models.TextField(null=True, blank=True)
    date_submitted = models.DateTimeField(null=True)
    message_polarity = models.CharField(max_length=50, blank=True, null=True,
                                        choices=FEEDBACK_CHOICES,
                                        default="undefined")