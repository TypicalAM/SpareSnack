"""Views concerning the user"""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.base import View
from django.views.generic.edit import FormView
from diets.models import Diet, Meal

from users.forms import UserCreationForm


class UserProfileView(LoginRequiredMixin, View):
    """View for showing the user his/her profile"""

    template_name = "profile/index.html"

    def get(self, request):
        """Update the request with the logged in user to display his data"""
        context = {
            "user": request.user,
            "meals": Meal.objects.filter(author=self.request.user),
            "diets": Diet.objects.filter(author=self.request.user),
        }
        return render(request, self.template_name, context=context)


class UserRegisterView(FormView):
    """View for creating an account for the user"""

    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "register.html"

    def form_valid(self, form):
        """Save the user to the database if the form was correct"""
        form.save()
        return super().form_valid(form)
