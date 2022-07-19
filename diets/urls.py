"""
URL configuration for the diet app -
for example the link to browse would be 'example.com/diet/browse'
"""

from django.urls import path

from diets.views.diet_views import (
    DietBrowse,
    DietCreate,
    DietDelete,
    DietDetail,
    DietImport,
)
from diets.views.meal_views import (
    homepage_view,
    DayCreate,
    MealBrowse,
    MealCreate,
    MealDelete,
    MealDetail,
)

urlpatterns = [
    path("", homepage_view, name="home"),
    path("day/create/", DayCreate.as_view(), name="day-create"),
    path("meals/create/", MealCreate.as_view(), name="meal-create"),
    path("meals/browse/", MealBrowse.as_view(), name="meal-browse"),
    path("meals/<pk>/", MealDetail.as_view(), name="meal-detail"),
    path("meals/<pk>/delete/", MealDelete.as_view(), name="meal-delete"),
    path("diet/create/", DietCreate.as_view(), name="diet-create"),
    path("diet/browse/", DietBrowse.as_view(), name="diet-browse"),
    path("diet/<slug>/import/", DietImport.as_view(), name="diet-import"),
    path("diet/<slug>/", DietDetail.as_view(), name="diet-detail"),
    path("diet/<slug>/delete/", DietDelete.as_view(), name="diet-delete"),
]
