"""Admin configuration for the diets app"""
from django.contrib import admin

from .models import (
    Ingredient,
    Meal,
    ThroughMealIngr,
    ThroughDayMeal,
    Day,
    Diet,
)

admin.site.register(Ingredient)
admin.site.register(Meal)
admin.site.register(Day)
admin.site.register(Diet)

admin.site.register(ThroughMealIngr)
admin.site.register(ThroughDayMeal)
