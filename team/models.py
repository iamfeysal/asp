from django.db import models
from asp.config.settings.local import AUTH_USER_MODEL
# from users.models import User
from users.users_managers import PlayerManager


# Create your models here.


class Team(models.Model):
    name = models.CharField(max_length=64, unique=True)
    description = models.TextField(max_length=1024)
    logo = models.ImageField()
    players = models.ManyToManyField(AUTH_USER_MODEL, through='Player')

    def __str__(self):
        return self.name


class Player(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

    # other_fields =

    def __str__(self):
        return str(self.user) if self.user else ''

    objects = PlayerManager()
