from django.db import models
from django.contrib.auth.models import AbstractUser

class Profile(AbstractUser):
    email = models.EmailField(unique=True)
    bio = models.TextField(null=True, blank=True)
    picture = models.ImageField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
