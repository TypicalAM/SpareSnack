"""Views concerning the user"""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.views.generic.detail import DetailView


class UserProfile(LoginRequiredMixin, DetailView):
    """View for showing the user his/her profile"""

    model = User
    context_object_name = "diets"
    template_name = "diet/browse.html"
