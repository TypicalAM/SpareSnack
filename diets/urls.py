"""
URL configuration for the diet app -
for example the link to browse would be 'example.com/diet/browse'
"""

from django.urls import path

from diets.views import diet_views, meal_views

urlpatterns = [
    path("", meal_views.homepage_view, name="home"),
    path("day/create/", meal_views.day_create, name="day-create"),
    path("meals/create/", meal_views.create, name="meal-create"),
    path("meals/browse/", meal_views.browse, name="meal-browse"),
    path("meals/<pk>/", meal_views.detail, name="meal-detail"),
    path("meals/<pk>/delete/", meal_views.delete, name="meal-delete"),
    path("diet/create/", diet_views.create, name="diet-create"),
    path("diet/browse/", diet_views.browse, name="diet-browse"),
    path("diet/<slug>/import/", diet_views.imprt, name="diet-import"),
    path("diet/<slug>/", diet_views.detail, name="diet-detail"),
    path("diet/<slug>/delete/", diet_views.delete, name="diet-delete"),
]
