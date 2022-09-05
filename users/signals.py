"""Signals for the users app"""
from typing import Any, Union
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models.expressions import Combinable

from users.models import Profile


@receiver(post_save, sender=User)
def create_profile(
    sender: str, instance: Union[User, Combinable], created: bool, **kwargs: Any
) -> None:
    """Create a profile for the user who just created his account"""
    del sender, kwargs
    if created:
        Profile.objects.create(user=instance)
