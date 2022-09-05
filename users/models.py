"""Models for the users app"""

from typing import Any
from django.contrib.auth.models import User
from django.db import models
from django_resized import ResizedImageField

from core.utils import UploadAndRename, image_clean_up


class Profile(models.Model):
    """A profile for the user to change his preferences"""

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_metric = models.BooleanField(default=True)
    fats = models.FloatField(default=0)
    protein = models.FloatField(default=0)
    carbs = models.FloatField(default=0)
    image = ResizedImageField(
        size=[160, 160],
        default="users/default_avatar.png",
        upload_to=UploadAndRename("users/profile_pictures"),
    )

    def __str__(self) -> str:
        """Additional data for debugging"""
        return f"{self.user.username}'s Profile"

    def save(self, *args: Any, **kwargs: Any) -> None:
        """Clean up after the old image if we have a new one"""
        image_clean_up(self)
        super().save(*args, **kwargs)
