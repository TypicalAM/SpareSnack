"""Admin configuration for the diets app"""
from django.contrib import admin

from .models import (
    Ingredient,
    Meal,
    IntermediaryMealIngredient,
    IntermediaryDayMeal,
    Day,
    Diet,
)

admin.site.register(Ingredient)
admin.site.register(Meal)
admin.site.register(Day)
admin.site.register(Diet)

admin.site.register(IntermediaryMealIngredient)
admin.site.register(IntermediaryDayMeal)
