from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class CustomUser(AbstractUser):
    """Extended User class"""
    last_answer = models.DateTimeField(null=True, blank=True, default=None)
