"""Forms for the diets app"""
import datetime
import json
from json.decoder import JSONDecodeError

from django import forms
from django.core import serializers
from django.forms import ValidationError, fields

from diets.models import Diet, Ingredient, Meal, ThroughMealIngr


def validate_day_post_save(request):
    """Validate the POST save data from the day"""
    try:
        json_object = json.loads(request.body)
        meals = [
            Meal.objects.get(name=obj.object.name, pk=obj.object.pk)
            for obj in serializers.deserialize("json", json_object["meals"])
        ]
        meal_nums = [
            int(x) for x in (json_object["meal_nums"][1:-1].split(","))
        ]
        date = json_object["date"]
    except (JSONDecodeError, KeyError, ValueError, Meal.DoesNotExist):
        return False
    if len(meals) != len(meal_nums) or not (meals and meal_nums and date):
        return False
    return meals, meal_nums, date


class MealCreateForm(forms.ModelForm):
    """Form for creating meals with searched and selected ingredients"""

    class Meta:
        """We don't include the author field, it will be mentioned in `save`"""

        model = Meal
        fields = ("name", "description", "recipe", "image")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def verify_ingredients(self):
        """Verify that the ingredient data was correct"""
        ingr_data = self.data.get("ingredient_data")
        amounts = self.data.get("amounts")
        if not ingr_data or not amounts:
            raise ValidationError("Invalid ingredient data")
        try:
            ingr_arr = [
                Ingredient.objects.get(name=obj.object.name)
                for obj in serializers.deserialize("json", ingr_data)
            ]
            amounts_arr = [int(obj) for obj in amounts.split(",")]
            assert len(ingr_arr) == len(amounts_arr)
        except Exception as exc:
            raise ValidationError("Incoherent ingredient data") from exc
        return ingr_arr, amounts_arr

    def clean(self):
        """Clean ingredients and amounts to the cleaned data"""
        ingredient_data, amounts = self.verify_ingredients()
        clean_data = self.cleaned_data
        clean_data["ingredients"] = ingredient_data
        clean_data["amounts"] = amounts
        return clean_data

    def save(self, author):
        """Save data with additional and create ingredient relations"""
        clean_data = self.cleaned_data
        my_meal = Meal.objects.create(
            name=clean_data["name"],
            description=clean_data["description"],
            recipe=clean_data["recipe"],
            image=clean_data["image"],
            author=author,
        )
        my_meal.save()
        for k in range(len(clean_data["ingredients"])):
            ThroughMealIngr.objects.create(
                meal=my_meal,
                ingredient=clean_data["ingredients"][k],
                amount=clean_data["amounts"][k],
            ).save()


class DietCreateForm(forms.ModelForm):
    """A form to create a diet (grab and backup days from a user)"""

    class Meta:
        """Don't include the auhtor as he will be added in the save() method"""

        model = Diet
        fields = ("name", "public", "description", "date")

    def save(self, author):
        """Save the diet and create the day backups & relations"""
        my_diet = Diet.objects.create(**self.cleaned_data, author=author)
        dates = [my_diet.date + datetime.timedelta(days=i) for i in range(8)]
        my_diet.save(dates)


class DietImportForm(forms.Form):
    """A form to import diets into your day"""

    date = fields.DateField()

    def clean(self):
        """Clean the slug and add it to the data"""
        slug = self.data.get("slug")
        if not slug:
            raise ValidationError("No slug")
        clean_data = self.cleaned_data
        clean_data["slug"] = slug
        return clean_data

    def save(self, user):
        """Fill the days of the user with the days from the selected diet"""
        clean_data = self.cleaned_data
        diet = Diet.objects.filter(slug=clean_data["slug"]).first()
        if not diet:
            raise ValidationError("No diet with that slug")

        diet.fill_days(user, clean_data["date"])
