"""Views concerning the user"""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.base import View
from django.views.generic.edit import FormView

from users.forms import UserCreationForm


class UserProfileView(LoginRequiredMixin, View):
    """View for showing the user his/her profile"""

    template_name = "profile/index.html"

    def get(self, request):
        """Update the request with the logged in user to display username"""
        context = {"user": request.user}
        return render(request, self.template_name, context=context)


class UserRegisterView(FormView):
    """View for creating an account for the user"""

    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "register.html"
