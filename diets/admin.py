# TODO
from django.contrib import admin

from .models import Ingredient, Meal, IntermediaryMealIngredient, IntermediaryDayMeal, Day, Diet

admin.site.register(Ingredient)
admin.site.register(Meal)
admin.site.register(Day)
admin.site.register(IntermediaryMealIngredient)
admin.site.register(IntermediaryDayMeal)
admin.site.register(Diet)
