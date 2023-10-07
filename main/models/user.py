from django.contrib.auth.models import AbstractUser
from django.db import models
from main.services.storage_backends import public_storage


class User(AbstractUser):
    class Roles(models.TextChoices):
        DEVELOPER = "developer"
        MANAGER = "manager"
        ADMIN = "admin"

    role = models.CharField(
        max_length=255, default=Roles.DEVELOPER, choices=Roles.choices
    )
    username = models.CharField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    email = models.CharField(max_length=255)
    date_of_birth = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=30, null=True, blank=True)
    avatar_picture = models.ImageField(null=True, storage=public_storage)
