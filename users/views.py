"""Views concerning the user"""
from allauth.account.views import LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls.base import reverse_lazy
from django.views.generic.base import View

from diets.models import Diet, Meal


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
