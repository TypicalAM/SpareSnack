from django.test import TestCase
from ..models import Ingredient, Meal, IntermediaryMealIngredient, get_sentinel

class TestModels(TestCase):
    def setUp(self) -> None:
        self.ingr1 = Ingredient.objects.create(
            name='Potato',
            caloric_values=[0.1, 22.2, 2.6],
            serving_suffix='grams (small potato)'
        )
        self.ingr2 = Ingredient.objects.create(
            name='Chicken Broth',
            caloric_values=[0.5, 1.1, 1.6],
            one_serving=250,
            serving_suffix='grams (one cup)'
        )
        self.meal = Meal.objects.create(
            name='Potato soup',
            recipe='Put potato in broth',
            author=get_sentinel(),
        )
