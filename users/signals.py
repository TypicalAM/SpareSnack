"""Signals for the users app"""
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from users.models import Profile


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    """Create a profile for the user who just created his account"""
    if created:
        Profile.objects.create(user=instance).save()
