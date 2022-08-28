"""
URL configuration for the diet app -
for example the link to browse would be 'example.com/diet/browse'
"""

from django.urls import path

from foods.views import diet_views, meal_views

urlpatterns = [
    path("", meal_views.homepage_view, name="foods_home"),
    path("day/create/", meal_views.day_create, name="foods_day_create"),
    path("meals/create/", meal_views.create, name="foods_meal_create"),
    path("meals/browse/", meal_views.browse, name="foods_meal_browse"),
    path("meals/<pk>/", meal_views.detail, name="foods_meal_detail"),
    path("meals/<pk>/delete/", meal_views.delete, name="foods_meal_delete"),
    path("diet/create/", diet_views.create, name="foods_diet_create"),
    path("diet/browse/", diet_views.browse, name="foods_diet_browse"),
    path("diet/<slug>/import/", diet_views.imprt, name="foods_diet_import"),
    path("diet/<slug>/", diet_views.detail, name="foods_diet_detail"),
    path("diet/<slug>/delete/", diet_views.delete, name="foods_diet_delete"),
]
