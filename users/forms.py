"""User forms for registering/logging in"""
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class UserRegisterForm(UserCreationForm):
    """Register the user to the site"""

    email = forms.EmailField()

    class Meta:
        """Require double password field"""

        model = User
        fields = ["username", "email", "password1", "password2"]
