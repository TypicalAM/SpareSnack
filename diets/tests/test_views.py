from django.contrib.auth.models import User
from django.test import Client, TestCase
from ..models import Day, Ingredient, IntermediaryDayMeal, Meal


class TestViews(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.user = User.objects.create(username="testuser")
        self.ingr1 = Ingredient.objects.create(name="Potato")
        self.ingr2 = Ingredient.objects.create(name="Chicken Broth")
        meal = Meal.objects.create(
            name="name meal", description="desc", recipe="recipe", author=self.user
        )
        self.day1 = Day.objects.create(author=self.user)
        IntermediaryDayMeal(meal=meal, day=self.day1, meal_num=2).save()

    def test_post(self):
        self.client.force_login(self.user)
        response = self.client.post(
            "/d/meals/create/",
            {
                "name": "test",
                "description": "test2",
                "recipe": "recipe1",
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
                "amounts": "10,20,30",
            },
        )
        self.assertEqual(response.status_code, 302)

    def test_2get(self):
        self.client.force_login(self.user)
        response = self.client.get("/d/day/create?d=2022-05-18")
        print(str(response.content, encoding="utf8"))
