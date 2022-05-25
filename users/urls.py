"""
URL configuration for the users app -
all URLs in this file need to have a 'accounts/' prefix,
for example the link to browse would be 'example.com/accounts/login'
"""

from django.contrib.auth import views as auth_views
from django.urls import path

from .views import UserProfile, UserRegisterView, UserDiets, UserMeals

urlpatterns = [
    path("profile/", UserProfile.as_view(), name="profile"),
    path("profile/meals", UserMeals.as_view(), name="meals"),
    path("profile/diets", UserDiets.as_view(), name="diets"),
    path("register/", UserRegisterView.as_view(), name="register"),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="login.html"),
        name="login",
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(template_name="logout.html"),
        name="logout",
    ),
]
