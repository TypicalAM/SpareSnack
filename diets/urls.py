"""
URL configuration for the diet app -
all URLs in this file need to have a 'd/' prefix,
for example the link to browse would be 'example.com/d/browse'
"""

from django.urls import path
from .views import MealCreate, DayCreate, DietBrowse, DietDetail, DietCreate

urlpatterns = [
        path('day/create/',         DayCreate.as_view(),  name='day-create'),
        path('meals/create/',       MealCreate.as_view(), name='meal-create'),
        path('diet/create/',        DietCreate.as_view(), name='diet-create'),
        path('diet/browse/',        DietBrowse.as_view(), name='diet-browse'),
        path('diet/<pk>/',          DietDetail.as_view(), name='diet-detail'),
]

# TODO ADD 404 HANDLER
