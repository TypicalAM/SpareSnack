"""Test views for the diets app"""
from datetime import datetime
from http import HTTPStatus

from django.contrib.auth.models import User
from django.http.response import JsonResponse
from django.test import Client, TestCase
from django.urls.base import reverse

from ..models import Day, Ingredient, Meal, ThroughDayMeal


class TestMealViews(TestCase):
    """Test the views for the meal functionality"""

    def setUp(self) -> None:
        self.client = Client()
        self.user = User.objects.create(username="testuser", password="12345")
        self.meal = Meal.objects.create(
            name="Potato soup",
            description="Quick soup",
            recipe="Put potato in broth",
            author=self.user,
        )
        self.ingr1 = Ingredient.objects.create(name="Potato")
        self.ingr2 = Ingredient.objects.create(name="Chicken Broth")
        self.day = Day.objects.create(author=self.user)
        ThroughDayMeal(meal=self.meal, day=self.day, meal_num=2).save()

    def test_nologin_redirect(self) -> None:
        response = self.client.get(reverse("meal-create"))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_meal_create_get_noargs(self) -> None:
        self.client.force_login(self.user)
        response = self.client.get(reverse("meal-create"))
        self.assertTemplateUsed(response, "meal/create.html")
        self.assertTrue("form" in response.context)

    def test_meal_create_get_search(self) -> None:
        self.client.force_login(self.user)
        response = self.client.get(
            reverse("meal-create"),
            {"q": "Chicken"},
            HTTP_ACCEPT="application/json",
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIsInstance(response, JsonResponse)

    def test_meal_create_post_right(self) -> None:
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("meal-create"),
            {
                "name": "test",
                "description": "test2",
                "recipe": "recipe1",
                "amounts": "10,20,30",
                "ingredient_data": """
                [
                    {
                        "model": "diets.ingredient",
                        "fields": {
                            "name": "Potato",
                            "image": "ingr_thumb/default.jpg"
                        }
                    },
                    {
                        "model": "diets.ingredient",
                        "fields": {
                            "name": "Chicken Broth",
                            "image": "ingr_thumb/default.jpg"
                        }
                    },
                    {
                        "model": "diets.ingredient",
                        "fields": {
                            "name": "Potato",
                            "image": "ingr_thumb/default.jpg"
                        }
                    }
                ]
                """,
            },
        )
        new_meal = Meal.objects.all()[1]
        self.assertEqual(new_meal.name, "test")
        self.assertEqual(len(new_meal.ingredients.all()), 3)
        self.assertRedirects(response, reverse("day-create"))

    def test_meal_create_post_nonexistent_ingr(self) -> None:
        self.client.force_login(self.user)
        # Check the response with a non-existent ingredient 'Ptato'
        response = self.client.post(
            reverse("meal-create"),
            {
                "name": "test",
                "description": "test2",
                "recipe": "recipe1",
                "amounts": "10,20",
                "ingredient_data": """
                [
                    {
                        "model": "diets.ingredient",
                        "fields": {
                            "name": "Potat",
                            "image": "ingr_thumb/default.jpg"
                        }
                    },
                    {
                        "model": "diets.ingredient",
                        "fields": {
                            "name": "Chicken Broth",
                            "image": "ingr_thumb/default.jpg"
                        }
                    }
                ]
                """,
            },
        )
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    def test_meal_create_post_no_amounts(self) -> None:
        self.client.force_login(self.user)
        # Check the response with a non-existent ingredient 'Ptato'
        response = self.client.post(
            reverse("meal-create"),
            {
                "name": "test",
                "description": "test2",
                "recipe": "recipe1",
                "ingredient_data": """
                [
                    {
                        "model": "diets.ingredient",
                        "fields": {
                            "name": "Potat",
                            "image": "ingr_thumb/default.jpg"
                        }
                    },
                    {
                        "model": "diets.ingredient",
                        "fields": {
                            "name": "Chicken Broth",
                            "image": "ingr_thumb/default.jpg"
                        }
                    }
                ]
                """,
            },
        )
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    def test_meal_browse_get(self) -> None:
        response = self.client.get(reverse("meal-browse"))
        self.assertTemplateUsed(response, "meal/browse.html")
        self.assertTrue("object_list" in response.context)

    def test_meal_detail_get_right(self) -> None:
        meal = Meal.objects.all()[0]
        response = self.client.get(
            reverse("meal-detail", kwargs={"pk": meal.pk})
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_meal_detail_get_wrong_pk(self) -> None:
        response = self.client.get(reverse("meal-detail", kwargs={"pk": 2}))
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)


class TestDayViews(TestCase):
    """Test the views for the day functionality"""

    def setUp(self) -> None:
        self.client = Client()
        self.user = User.objects.create(username="testuser", password="12345")
        self.meal = Meal.objects.create(
            name="Potato soup",
            description="Quick soup",
            recipe="Put potato in broth",
            author=self.user,
        )
        self.day = Day.objects.create(author=self.user)
        ThroughDayMeal(meal=self.meal, day=self.day, meal_num=2).save()

    def test_nologin_redirect(self) -> None:
        response = self.client.get(reverse("day-create"))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_day_create_get_noargs(self) -> None:
        self.client.force_login(self.user)
        response = self.client.get(reverse("day-create"))
        self.assertTemplateUsed(response, "day/create.html")

    def test_day_create_get_search(self) -> None:
        self.client.force_login(self.user)
        response = self.client.get(
            reverse("day-create"),
            {"q": "Potato soup"},
            HTTP_ACCEPT="application/json",
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIsInstance(response, JsonResponse)

    def test_day_create_get_nonexisting_day(self) -> None:
        fake_date = "2000-01-01"
        self.client.force_login(self.user)
        response = self.client.get(
            reverse("day-create"),
            {"d": fake_date},
            HTTP_ACCEPT="application/json",
        )
        self.assertIsInstance(response, JsonResponse)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTrue(Day.objects.filter(date=fake_date))

    def test_day_create_get_existing_day(self) -> None:
        self.client.force_login(self.user)
        response = self.client.get(
            reverse("day-create"),
            {"d": datetime.strftime(self.day.date, "%Y-%m-%d")},
            HTTP_ACCEPT="application/json",
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIsInstance(response, JsonResponse)
        self.assertTrue(len(response.content) > 20)
        self.client.force_login(self.user)

    def test_day_create_post_right(self) -> None:
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("day-create"),
            {
                "meal_nums": "[0]",
                "date": datetime.strftime(self.day.date, "%Y-%m-%d"),
                "meals": """
                [
                    {
                    "model" : "diets.meal",
                    "pk" : 1,
                    "fields": {
                        "name" : "Potato soup",
                        "description":"Quick soup",
                        "recipe":"Put potato in broth",
                        "image":"meal_thumb/default.jpg",
                        "author":1,
                        "url":null
                        }
                    }
                ]
                """,
            },
            content_type="application/json",
        )
        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        self.assertIsInstance(response, JsonResponse)
        self.assertTrue(len(self.day.meals.all()))

    def test_day_create_post_nonexistent_meal(self) -> None:
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("day-create"),
            {
                "meal_nums": "[0]",
                "date": datetime.strftime(self.day.date, "%Y-%m-%d"),
                "meals": """
                [
                    {
                    "model" : "diets.meal",
                    "pk" : 1,
                    "fields": {
                        "name" : "Nonexistent",
                        "description":"Quick soup",
                        "recipe":"Put potato in broth",
                        "image":"meal_thumb/default.jpg",
                        "author":1,
                        "url":null
                        }
                    }
                ]
                """,
            },
            content_type="application/json",
        )
        self.assertIsInstance(response, JsonResponse)
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    def test_day_create_post_no_mealnums(self) -> None:
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("day-create"),
            {
                "date": datetime.strftime(self.day.date, "%Y-%m-%d"),
                "meals": """
                [
                    {
                    "model" : "diets.meal",
                    "pk" : 1,
                    "fields": {
                        "name" : "Potato soup",
                        "description":"Quick soup",
                        "recipe":"Put potato in broth",
                        "image":"meal_thumb/default.jpg",
                        "author":1,
                        "url":null
                        }
                    }
                ]
                """,
            },
            content_type="application/json",
        )
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertIsInstance(response, JsonResponse)
