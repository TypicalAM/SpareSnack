"""Appconfig for the diets app"""
from django.apps import AppConfig


class DietsConfig(AppConfig):
    """Configure the app"""

    default_auto_field = "django.db.models.BigAutoField"
    name = "diets"
