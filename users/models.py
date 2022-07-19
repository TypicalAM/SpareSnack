"""Models for the users app"""
from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    """A profile for the user to change his preferences"""

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default="avatar.png", upload_to="profile_pics")

    def __str__(self):
        """Additional data for debugging"""
        return f"{self.user.username} Profile"
