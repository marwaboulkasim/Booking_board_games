from django.contrib.auth.models import AbstractUser
from django.db import models
from tables_app.models import Game

class User(AbstractUser):
    last_name = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    pseudo = models.CharField(max_length=50, unique=True)
    phone = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    favorite_games = models.ManyToManyField("tables_app.Game", blank=True, related_name='fans')

    def __str__(self):
        return self.username


