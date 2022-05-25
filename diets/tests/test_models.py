from django.contrib.auth.models import User
from django.test import TestCase
from django.urls.base import reverse
from django.db.utils import IntegrityError

from ..models import Day, Ingredient, Meal, IntermediaryMealIngredient


class TestModels(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(username="testuser", password="12345")
        self.meal = Meal.objects.create(
            name="Potato soup",
            description="Quick soup",
            recipe="Put potato in broth",
            author=self.user,
        )
        self.ingr1 = Ingredient.objects.create(name="Potato")
        self.ingr2 = Ingredient.objects.create(name="Chicken Broth")
        self.day = Day.objects.create(date="2022-05-18", author=self.user)

    def test_ingredient_default_fields(self) -> None:
        self.assertEqual(self.ingr1.image.url, "/media/ingr_thumb/default.jpg")
        self.assertEqual(self.ingr2.image.url, "/media/ingr_thumb/default.jpg")

    def test_meal_default_fields(self) -> None:
        self.assertEqual(self.meal.author.username, "testuser")
        self.assertEqual(self.meal.url, reverse("meal-detail", kwargs={"pk": None}))
        self.meal.save()
        self.assertEqual(
            self.meal.url, reverse("meal-detail", kwargs={"pk": self.meal.pk})
        )
        self.assertEqual(self.meal.image.url, "/media/meal_thumb/default.jpg")

    def test_meal_intermediary_no_amount(self) -> None:
        with self.assertRaises(IntegrityError):
            self.inter = IntermediaryMealIngredient.objects.create(
                meal=self.meal, ingredient=self.ingr1
            )
            self.inter2 = IntermediaryMealIngredient.objects.create(
                meal=self.meal, ingredient=self.ingr1
            )

    def test_meal_intermediary(self) -> None:
        self.inter = IntermediaryMealIngredient.objects.create(
            meal=self.meal, ingredient=self.ingr1, amount=200
        )
        self.inter2 = IntermediaryMealIngredient.objects.create(
            meal=self.meal, ingredient=self.ingr2, amount=300
        )
        self.assertEquals(self.ingr1, self.meal.ingredients.all()[0])
        self.assertEquals(self.ingr2, self.meal.ingredients.all()[1])
        self.assertEquals(self.inter2.amount, 300)
