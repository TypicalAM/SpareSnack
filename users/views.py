"""Views concerning the user"""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls.base import reverse_lazy
from django.views.generic import FormView, ListView
from django.views.generic.base import View

from diets.models import Diet, Meal

from .forms import UserCreationForm


class UserDiets(ListView, LoginRequiredMixin):
    """ListView for showing the user his/her diets"""

    model = Diet
    context_object_name = "diets"
    template_name = "users/diets.html"
    paginate_by = 1

    def get_queryset(self, *args, **kwargs):
        """Get only the diets which the user has authored"""
        queryset = super(UserDiets, self).get_queryset(*args, **kwargs)
        return queryset.filter(author=self.request.user)


class UserMeals(ListView, LoginRequiredMixin):
    """ListView for showing the user his/her diets"""

    model = Meal
    context_object_name = "meals"
    template_name = "users/meals.html"
    paginate_by = 5

    def get_queryset(self, *args, **kwargs):
        """Get only the meals which the user has authored"""
        queryset = super(UserMeals, self).get_queryset(*args, **kwargs)
        return queryset.filter(author=self.request.user)


class UserProfile(View, LoginRequiredMixin):
    """View for showing the user his/her profile"""

    template_name = "users/profile.html"

    def get(self, *_):
        """Add the user to the context to show his profile"""
        context = {}
        context["user"] = self.request.user
        return render(self.request, self.template_name, context)


class UserRegisterView(FormView):
    """View for creating an account for the user"""

    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "users/register.html"
