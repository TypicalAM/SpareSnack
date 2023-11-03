"""Admin configuration for the foods app"""
from django.contrib import admin

from foods.models import (
    Day,
    Diet,
    Ingredient,
    Meal,
    ThroughDayMeal,
    ThroughMealIngr,
)

admin.site.register(Ingredient)
admin.site.register(Meal)
admin.site.register(Day)
admin.site.register(Diet)

admin.site.register(ThroughMealIngr)
admin.site.register(ThroughDayMeal)
