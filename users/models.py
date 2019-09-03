import uuid
from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser
from django.core.mail import send_mail
from django.db import models

# Create your models here.
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from asp.settings import AUTH_USER_MODEL
from users.users_managers import UserManager


class Skill(models.Model) :
    name = models.CharField(max_length=50)

    class Meta :
        permissions = (
            ("view_category", "view category"),
            ("add_category", "Add category"),
            ("delete_category", "Delete category"),
        )

    def __str__(self) :
        return self.name


class User(AbstractBaseUser):
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    displayed_name = models.CharField(verbose_name='displayed_name', 
                                      max_length=60, null=True, blank=True,
                                      unique=True)
    date_joined = models.DateTimeField(verbose_name='date joined',
                                       auto_now_add=True)
    is_player = models.BooleanField('player status', default=False)
    is_coach = models.BooleanField('coach status', default=False)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    second_name = models.CharField(max_length=255, blank=True, null=True)
    skills = models.ManyToManyField(Skill)
    followers = models.ManyToManyField("self", blank=True, symmetrical=False,
                                       related_name="followers_set")
    following = models.ManyToManyField("self", blank=True, symmetrical=False,
                                       related_name="following_set")
    
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta :
        permissions = (
            ("viw_user", "view user"),
            ("ad_user", "Add user"),
            ("dlt_user", "Delete user"),
        )

    # def __str__(self):
    #     if self.displayed_name == None :
    #         return 'displayed is none'
    #     return self.displayed_name.split('@')[0]
    def __str__(self):
        return self.email

    # def full_name(self):
    #     """
    #     :return:
    #     """
    #     full_name = '%s %s' % (self.first_name, self.second_name)
    #     return full_name.strip()

    def has_perm(self, perm, obj=None):
        return self.is_admin

    # Does this user have permission to view this app? (ALWAYS YES FOR
    # SIMPLICITY)

    def has_module_perms(self, app_label) :
        """

        :param app_label: 
        :return: 
        """
        return True
    

    def email_user(self, subject='welcome', message='welcome',
                   from_email='iamfeysal@gmail.com', **kwargs) :
        print('hit email function')
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)
        print(send_mail)

    def random_username(sender, instance, **kwargs):
        if not instance.displayed_name :
            instance.displayed_name = uuid.uuid4().hex[:30]

    models.signals.pre_save.connect(random_username, sender=settings.AUTH_USER_MODEL)

    def pre_save_listener(sender, instance, *args, **kwargs) :
        if instance.is_player :
            instance.is_coach = False
        if instance.is_coach :
            instance.is_player = False

    pre_save.connect(receiver=pre_save_listener, sender=AUTH_USER_MODEL)
    
    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def create_auth_token(sender, instance=None, created=False, **kwargs) :
        """Create Auth Token

        This code is triggered whenever a new user has been created
        and saved to the database
        """
        if created:
            Token.objects.create(user=instance)


    @property
    def followers_count(self) :
        return self.followers.all().count()

    @property
    def following_count(self) :
        return self.following.all().count()


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
        ('positive', 'Positive Experience'),
        ('negative', 'Negative Experience'),
        ('undefined', 'Undefined'),
    )

    user = models.ForeignKey(AUTH_USER_MODEL, blank=True, null=True,
                              on_delete=models.CASCADE)
    message = models.TextField(null=True, blank=True)
    date_submitted = models.DateTimeField(null=True)
    message_polarity = models.CharField(max_length=50, blank=True, null=True,
                                        choices=FEEDBACK_CHOICES,
                                        default="undefined")


class Notification(models.Model) :
    TYPE_CHOICES = (
        ('like', 'Like'),  # first for DB, second for Admin pannel
        ('comment', 'Comment'),
        ('follow', 'Follow')
    )

    creator = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.PROTECT,
                                related_name='creator')
    to = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.PROTECT,
                           related_name='to')
    notification_type = models.CharField(max_length=20, choices=TYPE_CHOICES)

    class Meta :
        ordering = ['-notification_type']

    def __str__(self) :
        return 'From : {} - To : {}'.format(self.creator, self.to)