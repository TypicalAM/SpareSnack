"""Models for the users app"""
from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    """A profile for the user to change his preferences"""

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(
        default="users/default_avatar.png", upload_to="users/profile_pictures"
    )
    is_metric = models.BooleanField(default=True)

    fats = models.FloatField(default=0)
    protein = models.FloatField(default=0)
    carbs = models.FloatField(default=0)

    def __str__(self):
        """Additional data for debugging"""
        return f"{self.user.username}'s Profile"
