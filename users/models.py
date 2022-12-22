import itertools
from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser
from django.core import validators
from django.core.mail import send_mail
from django.db import models
from django.db.models import ImageField
from django.template.defaultfilters import slugify
# from sorl.thumbnail import ImageField


# Create your models here.
from django.db.models.signals import post_save, pre_save
from django.utils.translation import gettext_lazy as _
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from asp.config.settings.local import AUTH_USER_MODEL
from users.users_managers import UserManager, PlayerManager
from team.models import Team


class Skill(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        permissions = (
            ("view_category", "view category"),
            ("add_category", "Add category"),
            ("delete_category", "Delete category"),
        )

    def __str__(self):
        return self.name


POSITION_CHOICES = (
    (0, "Keeper"),
    (1, "Defence"),
    (2, "Midfield"),
    (3, "Attack")
)

MEMBERSHIP_CHOICES = (
    (0, "banned"),
    (1, "member"),
    (2, "moderator"),
    (3, "admin")
)


class User(AbstractBaseUser):
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
                                    'unique': _("A user with that"
                                                " username already exists."), }
                                )
    first_name = models.CharField(_('first name'), max_length=255, blank=True)
    last_name = models.CharField(_('last name'), max_length=100, blank=True)
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    avatar = ImageField(upload_to='avatars/%Y/%m',
                        default='avatars/default/user.png')
    date_joined = models.DateTimeField(verbose_name='date joined',
                                       auto_now_add=True)
    is_player = models.BooleanField('player status', default=True)
    is_coach = models.BooleanField('coach status', default=False)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    skills = models.ManyToManyField(Skill)
    followers = models.ManyToManyField("self", blank=True, symmetrical=False,
                                       related_name="followers_set")
    following = models.ManyToManyField("self", blank=True, symmetrical=False,
                                       related_name="following_set")
    role = models.IntegerField(choices=MEMBERSHIP_CHOICES, default=1)
    position = models.IntegerField(choices=POSITION_CHOICES, default=1)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    @property
    def full_name(self):
        """A longer formal identifier for the user.

        Returns first name plus the last name
        """
        return '%s %s' % (self.first_name, self.last_name)

    @property
    def short_name(self):
        """A short, informal identifier for the user.

        Returns last name as short name
        """
        return self.last_name

    @property
    def profile_picture(self):
        """Return user's profile picture (avatar)"""
        return self.avatar

    def __str__(self):
        """String Representation."""

        return self.email

    def save(self, force_insert=False, force_update=False,
             using=None, update_fields=None, ):
        """Override save model.
         save email or last name as username if it is null else saves the
         username"""
        if not self.username:
            max_length = self.__class__._meta.get_field('username').max_length
            self.username = orig = slugify(
                self.last_name or self.email)[:max_length]
            for x in itertools.count(1):
                if not self.__class__.objects.filter(
                        username=self.username).exists():
                    break
                self.username = "%s-%d" % (orig[:max_length - len(str(x)) - 1],
                                           x)
        else:
            self.username = slugify(self.username)

        super(User, self).save(force_insert=force_insert,
                               force_update=force_update, using=using,
                               update_fields=update_fields)

    def has_perm(self, perm, obj=None):
        return self.is_admin

    # Does this user have permission to view this app? (ALWAYS YES FOR
    # SIMPLICITY)

    def has_module_perms(self, app_label):
        """

        :param app_label: 
        :return: 
        """
        return True

    def email_user(self, subject='welcome', message='welcome',
                   from_email='iamfeysal@gmail.com', **kwargs):
        print('hit email function')
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)
        print(send_mail)

    # @receiver(post_save, sender=settings.AUTH_USER_MODEL,)
    # def make_player(self, email, **kwargs):
    #     user = User.objects.get(email=email)
    #     user.is_player = True
    #     user.save()
    #
    # def make_coach(self, email, **kwargs):
    #     user = User.objects.get(email=email)
    #     user.is_coach = True
    #     user.save()

    def pre_save_listener(sender, instance, *args, **kwargs):
        if instance.is_player:
            instance.is_coach = False
        if instance.is_coach:
            instance.is_player = False

    pre_save.connect(receiver=pre_save_listener, sender=AUTH_USER_MODEL,)

    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def create_auth_token(sender, instance=None, created=False, **kwargs):
        """Create Auth Token

        This code is triggered whenever a new user has been created
        and saved to the database
        """
        if created:
            Token.objects.create(user=instance)

    @property
    def followers_count(self):
        return self.followers.all().count()

    @property
    def following_count(self):
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


class Notification(models.Model):
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

    class Meta:
        ordering = ['-notification_type']

    def __str__(self):
        return 'From : {} - To : {}'.format(self.creator, self.to)
