"""Test models for the foods app"""
import datetime

from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from django.test import TestCase
from django.urls.base import reverse

from foods.models import (
    Day,
    Diet,
    Ingredient,
    Meal,
    ThroughDayMeal,
    ThroughMealIngr,
)


class TestModels(TestCase):
    """Test the models functionality for the foods app"""

    def setUp(self) -> None:
        self.user = User.objects.create(username="testuser", password="12345")
        self.meal = Meal.objects.create(
            name="Potato soup",
            description="Quick soup",
            recipe="Put potato in broth",
            author=self.user,
        )
        self.ingr1 = Ingredient.objects.create(
            name="Potato",
            measure_type="fruits",
            convert_rate=300,
            fats=0.1,
            carbs=21,
            protein=2.5,
        )
        self.ingr2 = Ingredient.objects.create(
            name="Chicken Broth",
            measure_type="liters",
            convert_rate=1,
            fats=1.0,
            carbs=1.0,
            protein=1.0,
        )
        self.day = Day.objects.create(date="2022-05-18", author=self.user)
        ThroughDayMeal.objects.create(meal=self.meal, day=self.day, meal_num=1)
        self.diet = Diet.objects.create(
            name="An exmple diet",
            description="An example description of the diet",
            author=self.user,
            date=datetime.date(2022, 5, 18),
            end_date=datetime.date(2022, 5, 21),
        )
        self.diet.save_days()

    def test_ingredient_default_fields(self) -> None:
        self.assertEqual(self.ingr1.image.url, "/media/ingr_thumb/default.jpg")
        self.assertEqual(self.ingr2.image.url, "/media/ingr_thumb/default.jpg")

    def test_meal_default_fields(self) -> None:
        self.assertEqual(self.meal.author.username, "testuser")
        self.assertEqual(
            self.meal.url, reverse("foods_meal_detail", kwargs={"pk": None})
        )
        self.meal.save()
        self.assertEqual(
            self.meal.url,
            reverse("foods_meal_detail", kwargs={"pk": self.meal.pk}),
        )
        self.assertEqual(self.meal.image.url, "/media/meal_thumb/default.jpg")
        self.assertEqual(self.meal.fats, 0)
        self.assertEqual(self.meal.protein, 0)
        self.assertEqual(self.meal.carbs, 0)

    def test_meal_intermediary_no_amount(self) -> None:
        with self.assertRaises(TypeError):
            ThroughMealIngr.objects.create(
                meal=self.meal, ingredient=self.ingr1
            )
            ThroughMealIngr.objects.create(
                meal=self.meal, ingredient=self.ingr1
            )

    def test_meal_intermediary_conversion(self) -> None:
        inter = ThroughMealIngr.objects.create(
            meal=self.meal, ingredient=self.ingr1, amount=2
        )
        inter2 = ThroughMealIngr.objects.create(
            meal=self.meal, ingredient=self.ingr2, amount=300
        )
        self.assertEquals(inter.grams, 600)
        self.assertEquals(inter2.grams, 300)
        [rel.delete() for rel in ThroughMealIngr.objects.all()]

    def test_meal_save_ingredients(self) -> None:
        ingredients = [self.ingr1, self.ingr2]
        amounts = [2, 300]
        self.meal.save_ingredients(ingredients, amounts)
        self.assertEqual(len(ingredients), len(ThroughMealIngr.objects.all()))

        self.assertEqual(self.meal.fats, 3.6)
        self.assertEqual(self.meal.protein, 18.0)
        self.assertEqual(self.meal.carbs, 129.0)

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

    def test_diet_save_backups(self) -> None:
        self.assertIsInstance(self.diet.days.all().first(), Day)
        self.assertTrue(self.diet.days.first().backup)
        self.assertEqual(self.diet.days.first().meals.first(), self.meal)

    def test_diet_fill_days(self) -> None:
        self.diet.fill_days(self.user, "2022-05-10")
        filled_day = Day.objects.filter(
            date="2022-05-10", author=self.user, backup=False
        ).first()
        self.assertIsNotNone(filled_day)
        if filled_day:
            self.assertEqual(filled_day.meals.first(), self.meal)

    def test_diet_delete(self) -> None:
        self.assertTrue(Day.objects.filter(backup=True))
        self.diet.delete()
        self.assertFalse(Day.objects.filter(backup=True))
