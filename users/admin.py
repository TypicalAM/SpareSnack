"""Admin configuration for the diets app"""
from django.contrib import admin

from users.models import Profile

admin.site.register(Profile)
