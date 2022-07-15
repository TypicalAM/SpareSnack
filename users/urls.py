"""
URL configuration for the users app
"""

from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordChangeDoneView,
    PasswordChangeView,
)
from django.urls import path

from diets.views.diet_views import UserDiets
from diets.views.meal_views import UserMeals
from users.views import UserProfileView, UserRegisterView

urlpatterns = [
    path("profile/", UserProfileView.as_view(), name="profile"),
    path("profile/meals", UserMeals.as_view(), name="meals"),
    path("profile/diets", UserDiets.as_view(), name="diets"),
    path(
        "login/",
        LoginView.as_view(template_name="auth/login.html"),
        name="login",
    ),
    path(
        "logout/",
        LogoutView.as_view(template_name="auth/logout.html"),
        name="logout",
    ),
    path(
        "register/",
        UserRegisterView.as_view(template_name="auth/register.html"),
        name="register",
    ),
    path(
        "profile/change_pw/",
        PasswordChangeView.as_view(template_name="auth/password_change.html"),
        name="password-change",
    ),
    path(
        "profile/change_pw/done",
        PasswordChangeDoneView.as_view(
            template_name="auth/password_change_done.html"
        ),
        name="password-change-done",
    ),
]
