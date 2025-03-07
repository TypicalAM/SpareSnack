"""Admin configuration for the users app"""
from django.contrib import admin

from users.models import Profile

admin.site.register(Profile)
