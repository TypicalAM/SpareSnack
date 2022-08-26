"""Views concerning the user"""
from allauth.account.views import LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.urls.base import reverse_lazy
from django.views.generic.base import View
from django.views.generic.edit import UpdateView

from diets.models import Diet, Meal
from users.models import Profile


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


class ProperLogoutView(LogoutView):
    """Override the default redirect url for the logout view"""

    def get_redirect_url(self):  # pylint: disable=no-self-use
        """Let's redirect to our logout_done view"""
        return reverse_lazy("meal-browse")


class ChangePreferencesView(
    LoginRequiredMixin, SuccessMessageMixin, UpdateView
):
    """Change preferred amounts of fats, sugars and carbs"""

    model = Profile
    template_name = "profile/change_preferences.html"
    fields = ("fats", "protein", "carbs")
    success_url = reverse_lazy("account_profile")
    success_message = "The preferences have been changed"

    def get_object(self):
        """Return the user profile instance"""
        return self.request.user.profile
