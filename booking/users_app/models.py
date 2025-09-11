from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = models.EmailField(unique=True)
    pseudo = models.CharField(max_length=50, unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    favorite_games = models.ManyToManyField("tables_app.Game", blank=True, related_name='fans')

    def __str__(self):
        return self.username


