"""Views concerning the user"""
from typing import Any, Optional, cast
from allauth.account.views import LogoutView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import render
from django.urls.base import reverse_lazy
from django.views.generic.base import View
from django.views.generic.edit import UpdateView

from foods.models import Diet, Meal
from users.models import Profile


class UserProfileView(View):
    """View for showing the user his/her profile"""

    template_name = "profile/index.html"

    def get(self, request: HttpRequest) -> HttpResponse:
        """Update the request with the logged in user to display his data"""
        context = {
            "user": request.user,
            "meals": Meal.objects.filter(author=cast(User, self.request.user)),
            "diets": Diet.objects.filter(author=cast(User, self.request.user)),
        }
        from django.db import connection

        return render(request, self.template_name, context=context)


profile = login_required(UserProfileView.as_view())


class ProperLogoutView(LogoutView):
    """Override the default redirect url for the logout view"""

    def get_redirect_url(self) -> str:  # pylint: disable=no-self-use
        """Let's redirect to our logout_done view"""
        return reverse_lazy("foods_meal_browse")


logout = login_required(ProperLogoutView.as_view())


class ChangeGoalsView(SuccessMessageMixin, UpdateView):
    """Change preferred amounts of fats, sugars and carbs"""

    model = Profile
    template_name = "profile/change_goals.html"
    context_object_name = "profile"
    fields = ("fats", "protein", "carbs")
    success_url = reverse_lazy("account_profile")
    success_message = "The preferences have been changed"

    def get_object(self, queryset: Optional[QuerySet[Any]] = None) -> Profile:
        """Return the user profile instance"""
        user = cast(User, self.request.user)
        return Profile.objects.get(user=user)


change_goals = login_required(ChangeGoalsView.as_view())


class ChangeAvatarView(SuccessMessageMixin, UpdateView):
    """Change the avatar of the user"""

    model = Profile
    template_name = "profile/change_avatar.html"
    context_object_name = "profile"
    fields = ("image",)
    success_url = reverse_lazy("account_profile")
    success_message = "The avatar image has been changed"

    def get_object(self, queryset: Optional[QuerySet[Any]] = None) -> Profile:
        """Return the user profile instance"""
        user = cast(User, self.request.user)
        return Profile.objects.get(user=user)


change_avatar = login_required(ChangeAvatarView.as_view())
