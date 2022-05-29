"""Test models for the diets app"""
# TODO: Add test for filling the days
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from django.test import TestCase
from django.urls.base import reverse
from django.utils import timezone

from ..models import (
    Day,
    Diet,
    Ingredient,
    ThroughDayMeal,
    ThroughMealIngr,
    Meal,
)


class TestModels(TestCase):
    """Test the models functionality for the diets app"""

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
        self.diet = Diet.objects.create(
            name="An exmple diet",
            description="An example description of the diet",
            author=self.user,
        )

    def test_ingredient_default_fields(self) -> None:
        self.assertEqual(self.ingr1.image.url, "/media/ingr_thumb/default.jpg")
        self.assertEqual(self.ingr2.image.url, "/media/ingr_thumb/default.jpg")

    def test_meal_default_fields(self) -> None:
        self.assertEqual(self.meal.author.username, "testuser")
        self.assertEqual(
            self.meal.url, reverse("meal-detail", kwargs={"pk": None})
        )
        self.meal.save()
        self.assertEqual(
            self.meal.url, reverse("meal-detail", kwargs={"pk": self.meal.pk})
        )
        self.assertEqual(self.meal.image.url, "/media/meal_thumb/default.jpg")

    def test_meal_intermediary_no_amount(self) -> None:
        with self.assertRaises(IntegrityError):
            ThroughMealIngr.objects.create(
                meal=self.meal, ingredient=self.ingr1
            )
            ThroughMealIngr.objects.create(
                meal=self.meal, ingredient=self.ingr1
            )

    def test_meal_intermediary(self) -> None:
        inter = ThroughMealIngr.objects.create(
            meal=self.meal, ingredient=self.ingr1, amount=200
        )
        inter2 = ThroughMealIngr.objects.create(
            meal=self.meal, ingredient=self.ingr2, amount=300
        )
        self.assertEquals(self.ingr1, self.meal.ingredients.all()[0])
        self.assertEquals(self.ingr2, self.meal.ingredients.all()[1])
        self.assertEquals(inter.amount, 200)
        self.assertEquals(inter2.amount, 300)

    def test_day_default_fields(self) -> None:
        self.assertFalse(self.day.backup)
        self.assertEqual(self.day.author, self.user)

    def test_day_intermediary_no_meal_num(self) -> None:
        with self.assertRaises(IntegrityError):
            ThroughDayMeal.objects.create(day=self.day, meal=self.meal)

    def test_day_intermediary(self) -> None:
        inter = ThroughDayMeal.objects.create(
            meal=self.meal, day=self.day, meal_num=3
        )
        self.assertEqual(self.day.meals.all().first(), inter.meal)
        self.assertEqual(inter.meal_num, 3)

    def test_diet_default_fields(self) -> None:
        self.assertTrue(self.diet.public)
        self.assertEqual(self.diet.date.day, timezone.now().day)

    def test_diet_manytomany(self) -> None:
        self.diet.days.add(self.day)
        self.assertIsInstance(self.diet.days.all().first(), Day)
