from datetime import datetime

from django.conf import settings
from django.db import models

# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_countries.fields import CountryField

from asp.settings import AUTH_USER_MODEL


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

    user = models.OneToOneField(AUTH_USER_MODEL, null=True,
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
    nickname = models.CharField(max_length=255, blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    
    class Meta :
        permissions = (
            ("view_profile", "view profile"),
            ("add_profile", "Add profile"),
            ("delete_profile", "Delete profile"),
        )
        
    def __str__(self):
        return  " @ " + str(self.nickname)

    def age(self):
        if self.birth_date is None:
            pass
        else:
            # handle age when birth_date is not null
            return int((datetime.now().date() - self.birth_date).days / 365.25)


    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def update_user_profile(sender, instance, created, **kwargs) :
        if created:
            UserProfile.objects.create(user=instance)
            instance.userprofile.save()
        else:
            print('updated')