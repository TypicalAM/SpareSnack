"""
URL configuration for the users app
"""

from django.urls import path

from diets.views.diet_views import UserDiets
from diets.views.meal_views import UserMeals
from users.views import UserProfile

urlpatterns = [
    path("profile/", UserProfile.as_view(), name="profile"),
    path("profile/meals", UserMeals.as_view(), name="meals"),
    path("profile/diets", UserDiets.as_view(), name="diets"),
]
