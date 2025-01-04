from datetime import timedelta
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from rest_framework.authtoken.models import Token


class User(AbstractUser):
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=150)
    email = models.EmailField(max_length=150, unique=True)
    bio = models.TextField()
    avatar = models.ImageField()

    def __str__(self):
        return self.username

    REQUIRED_FIELDS = []


class ExpiringToken(Token):
    expires_at = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(hours=1)  # Set expiration time to 2 hours
        super().save(*args, **kwargs)

    def is_expired(self):
        return timezone.now() > self.expires_at
