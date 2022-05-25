"""App configuration for the users app"""
from django.apps import AppConfig


class UsersConfig(AppConfig):
    """Configure the app"""

    default_auto_field = "django.db.models.BigAutoField"
    name = "users"
