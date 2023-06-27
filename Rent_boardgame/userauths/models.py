from django.db import models
from django.contrib.auth.models import AbstractUser
from shortuuid.django_fields import ShortUUIDField


class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100)
    user_id = ShortUUIDField(unique=True, primary_key=True, prefix="user", alphabet='1234567890', length=6, max_length=100)
    phone_number = models.CharField(max_length=20, blank=True)  
    address = models.CharField(max_length=255, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username