"""
URL configuration for the diet app -
for example the link to browse would be 'example.com/diet/browse'
"""

from django.urls import path
from .views import DietCreate, DietBrowse, DietDetail, DietImport
from .views import MealCreate, MealBrowse, MealDetail, DayCreate

urlpatterns = [
        path('day/create/',         DayCreate .as_view(), name='day-create' ),
        path('meals/create/',       MealCreate.as_view(), name='meal-create'),
        path('meals/browse/',       MealBrowse.as_view(), name='meal-browse'),
        path('meals/<pk>/',         MealDetail.as_view(), name='meal-detail'),
        path('diet/create/',        DietCreate.as_view(), name='diet-create'),
        path('diet/browse/',        DietBrowse.as_view(), name='diet-browse'),
        path('diet/import/',        DietImport.as_view(), name='diet-import'),
        path('diet/<slug>/',        DietDetail.as_view(), name='diet-detail'),
]

# TODO ADD 404 HANDLER
