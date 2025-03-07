"""Appconfig for the foods app"""
from django.apps import AppConfig


class FoodsConfig(AppConfig):
    """Configure the app"""

    default_auto_field = "django.db.models.BigAutoField"
    name = "foods"
