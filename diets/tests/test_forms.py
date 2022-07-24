"""Test forms for the diets app"""
from django.contrib.auth.models import User
from django.core import serializers
from django.test import TestCase
from diets.forms import DietImportForm, MealCreateForm, DietCreateForm
from diets.models import Diet, Ingredient


class TestForms(TestCase):
    """Test the forms functionality for the diets app"""

    def setUp(self) -> None:
        self.ingr1 = Ingredient.objects.create(name="Potato")
        self.ingr2 = Ingredient.objects.create(name="Chicken Broth")

        self.user = User.objects.create(username="testuser", password="12345")
        self.diet = Diet.objects.create(
            name="Example diet", author=self.user, description="test"
        )
        self.diet.save(["2020-02-10"])

    def test_meal_create_basic_fields(self) -> None:
        data = []
        data.append(
            {
                "name": "Recipe",
                "description": "My recipe",
                "recipe": "Put the eggs in the broth",
            }
        )
        data.append(
            {
                "name": "Recipe",
                "description": "My recipe",
                "recipe": "Put the eggs in the broth",
                "amounts": "1,2,3",
            }
        )
        data.append(
            {
                "name": "Recipe",
                "description": "My recipe",
                "recipe": "Put the eggs in the broth",
                "ingredient_data": "...",
            }
        )
        for mydata in data:
            form = MealCreateForm(data=mydata)
            self.assertIn(
                ["Invalid ingredient data"],
                form.errors.values(),
            )

    def test_meal_create_wrong_amounts(self) -> None:
        data = {
            "name": "Recipe",
            "description": "My recipe",
            "recipe": "Put the eggs in the broth",
            "amounts": "10,20,30",
            "ingredient_data": serializers.serialize(
                "json", Ingredient.objects.all()
            ),
        }
        form = MealCreateForm(data=data)
        self.assertIn(["Incoherent ingredient data"], form.errors.values())

        data["amounts"] = "10"
        form = MealCreateForm(data=data)
        self.assertIn(["Incoherent ingredient data"], form.errors.values())

    def test_meal_create_right(self) -> None:
        data = {
            "name": "Recipe",
            "description": "My recipe",
            "recipe": "Put the eggs in the broth",
            "amounts": "10,20",
            "ingredient_data": serializers.serialize(
                "json", Ingredient.objects.all()
            ),
        }
        form = MealCreateForm(data=data)
        self.assertTrue(form.is_valid())

    def test_diet_create_wrong_date(self) -> None:
        data = {
            "name": "My diet",
            "public": False,
            "description": "example diet",
        }

        form = DietCreateForm(data=data)
        self.assertEqual(form.errors.get("date"), ["This field is required."])

        data["date"] = "2020-20-20"
        form = DietCreateForm(data=data)
        self.assertEqual(form.errors.get("date"), ["Enter a valid date."])

    def test_diet_create_existing_slug(self) -> None:
        data = {
            "name": "example dieT",
            "public": False,
            "description": "example diet",
            "date": "2020-02-10",
        }

        form = DietCreateForm(data=data)
        self.assertIn(
            ["A diet with a similar name already exists"], form.errors.values()
        )

    def test_diet_create_right(self) -> None:
        data = {
            "name": "My diet",
            "public": False,
            "description": "example diet",
            "date": "2020-02-10",
        }

        form = DietCreateForm(data=data)
        self.assertTrue(form.is_valid())

    def test_diet_import_wrong_date(self) -> None:
        data = {
            "date": "2020-20-20",
            "slug": "example-diet",
        }
        form = DietImportForm(data=data)
        self.assertEqual(form.errors.get("date"), ["Enter a valid date."])

    def test_diet_import_wrong_slug(self) -> None:
        data = {
            "date": "2020-10-02",
            "slug": "bad-slug",
        }
        form = DietImportForm(data=data)
        self.assertIn(["No diet with that slug"], form.errors.values())
