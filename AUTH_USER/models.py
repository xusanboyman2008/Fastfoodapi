from datetime import timedelta
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from rest_framework.authtoken.models import Token


class User(AbstractUser):
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=150)
    email = models.EmailField(max_length=150, unique=True,blank=True,null=True)
    bio = models.TextField(blank=True,null=True)
    avatar = models.ImageField(blank=True,null=True)
    role = models.CharField(max_length=150, default="User")

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


class Permissions(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField(max_length=100)

    def __str__(self):
        return self.name


class Permission(models.Model):
    id = models.AutoField(primary_key=True)
    permissions = models.ManyToManyField(Permissions, related_name='permissions', blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return ", ".join([perm.name for perm in self.permissions.all()])
