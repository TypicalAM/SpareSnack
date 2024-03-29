"""App configuration for the users app"""
from django.apps import AppConfig


class UsersConfig(AppConfig):
    """Configure the app"""

    default_auto_field = "django.db.models.BigAutoField"
    name = "users"

    def ready(self) -> None:
        """Make sure that signals are loaded"""
        import users.signals  # pylint: disable=import-outside-toplevel,unused-import
