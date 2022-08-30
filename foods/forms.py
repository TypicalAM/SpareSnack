"""Forms for the foods app"""
from django import forms
from django.core.serializers import deserialize
from django.core.serializers.base import DeserializationError
from django.forms import ValidationError, fields
from django.template.defaultfilters import slugify

from foods.models import Day, Diet, Ingredient, Meal


class DayCreateForm(forms.Form):
    """A form to make creating days easier"""

    meals = fields.CharField()
    meal_nums = fields.CharField()
    date = fields.DateField()

    def clean_meals(self):
        """Ensure meal format"""
        msg = "Incoherent meal data"
        data = self.cleaned_data.get("meals")

        try:
            des = deserialize("json", data)
            data = [
                Meal.objects.get(name=obj.object.name, pk=obj.object.pk)
                for obj in des
            ]
        except (Meal.DoesNotExist, DeserializationError) as exc:
            raise ValidationError(msg) from exc
        return data

    def clean_meal_nums(self):
        """Ensure meal_nums format"""
        msg = "Incoherent meal numbers data"
        data = self.cleaned_data.get("meal_nums")
        data_split = data[1:-1].split(",")

        if not all(x.isnumeric() for x in data_split):
            raise ValidationError(msg)
        return [int(x) for x in data_split]

    def clean(self):
        """Make sure that meals can be paired with meal_nums"""
        msg = "Incoherent meals and meal_nums pairing"
        cleaned_data = super().clean()
        meals = cleaned_data.get("meals")
        meal_nums = cleaned_data.get("meal_nums")

        if meals and meal_nums:
            if len(meal_nums) != len(meals):
                raise ValidationError(msg)

    def save(self, author):
        """Save the day and create the relations"""
        date = self.cleaned_data.pop("date")
        meals = self.cleaned_data.pop("meals")
        meal_nums = self.cleaned_data.pop("meal_nums")

        Day.objects.get(date=date, author=author, backup=False).save_meals(
            meals, meal_nums
        )


class MealCreateForm(forms.ModelForm):
    """Form for creating meals with searched and selected ingredients"""

    ingredient_data = forms.CharField(required=True)
    amounts = forms.CharField(required=True)

    class Meta:
        """We don't include the author field, it will be mentioned in `save`"""

        model = Meal
        fields = ("name", "description", "recipe", "image")

    def clean_ingredients(self, ingredients, amounts):
        """Verify that the ingredient data was correct"""
        msg = "Incoherent ingredient data"
        result = {}
        try:
            ingredients_array = [
                Ingredient.objects.get(name=obj.object.name)
                for obj in deserialize("json", ingredients)
            ]
            amounts_array = [float(obj) for obj in amounts.split(",")]
        except (
            ValueError,
            Ingredient.DoesNotExist,
            AttributeError,
            DeserializationError,
        ):
            self.add_error("ingredient_data", ValidationError(msg))
        else:
            if len(ingredients_array) != len(amounts_array):
                self.add_error("ingredient_data", ValidationError(msg))
            result.update(
                {
                    "ingredient_data": ingredients_array,
                    "amounts": amounts_array,
                }
            )
        return result

    def clean(self):
        """Clean ingredients and amounts to the cleaned data"""
        super().clean()
        result = self.clean_ingredients(
            self.cleaned_data.get("ingredient_data"),
            self.cleaned_data.get("amounts"),
        )
        if result:
            self.cleaned_data.update(result)

    def save(self, author):
        """Save data with additional and create ingredient relations"""
        ingredients = self.cleaned_data.pop("ingredient_data")
        amounts = self.cleaned_data.pop("amounts")

        Meal.objects.create(
            **self.cleaned_data, author=author
        ).save_ingredients(ingredients, amounts)


class DietCreateForm(forms.ModelForm):
    """A form to create a diet (grab and backup days from a user)"""

    class Meta:
        """Don't include the auhtor as he will be added in the save() method"""

        model = Diet
        fields = ("name", "public", "description", "date", "end_date")

    def clean_dates(self, start_date, end_date):
        """Verify that the date data was correct"""
        msg = "End date should be greater than start date."
        msg2 = "Diets should have less than 15 days."

        if start_date and end_date:
            if end_date <= start_date:
                self.add_error("end_date", ValidationError(msg))
            if (end_date - start_date).days > 14:
                self.add_error("end_date", ValidationError(msg2))

    def clean(self):
        """Make sure we don't have two slugs which are the same"""
        msg = "A diet with a similar name already exists"
        super().clean()

        if Diet.objects.filter(
            slug=slugify(self.cleaned_data.get("name", ""))
        ).exists():
            self.add_error("name", ValidationError(msg))

        self.clean_dates(
            self.cleaned_data.get("date"), self.cleaned_data.get("end_date")
        )

    def save(self, author):
        """Save the diet and create the day backups & relations"""
        Diet.objects.create(**self.cleaned_data, author=author).save_days()


class DietImportForm(forms.Form):
    """A form to import diets into your day"""

    date = fields.DateField()
    slug = fields.SlugField()

    def clean(self):
        """make sure that the slug corresponds to a diet"""
        msg = "No diet with that slug"

        super().clean()
        diet = Diet.objects.filter(slug=self.cleaned_data.get("slug")).first()

        if diet:
            self.cleaned_data.update({"diet": diet})
        else:
            self.add_error("__all__", ValidationError(msg))

    def save(self, user):
        """Fill the days of the user with the days from the selected diet"""
        self.cleaned_data.get("diet").fill_days(
            user, self.cleaned_data.get("date")
        )
