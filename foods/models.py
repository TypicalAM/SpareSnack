"""Models for the foods app"""
import datetime
from typing import Any, Sequence

from django.contrib.auth.models import User
from django.db import models
from django.db.models.deletion import CASCADE
from django.template.defaultfilters import slugify
from django.urls.base import reverse
from django_resized import ResizedImageField

from core.utils import UploadAndRename, image_clean_up


class Ingredient(models.Model):
    """Ingredients are a part of meals, they dictate the amount of calories in a meal"""

    name = models.CharField(max_length=100)
    measure_type = models.CharField(max_length=50)
    convert_rate = models.FloatField(default=1)
    fats = models.FloatField(default=0)
    protein = models.FloatField(default=0)
    carbs = models.FloatField(default=0)
    image = ResizedImageField(
        size=[200, 200],
        default="foods/default_ingredient_thumbnail.jpg",
        upload_to=UploadAndRename("foods/ingredient_thumbnails"),
    )

    def __str__(self) -> str:
        return f"{self.name} measured with {self.measure_type} at {self.convert_rate}g per 1 item"

    def save(self, *args: Any, **kwargs: Any) -> None:
        """Clean up after the old image if we have a new one"""
        image_clean_up(self)
        super().save(*args, **kwargs)

    def get_base_calories(self) -> int:
        """Get the calories for 100 grams of a certain food"""
        return round(self.fats * 8 + self.protein * 4 + self.carbs * 4)

    def convert_from_grams(self, grams: float) -> float:
        """Display to the user the amount of the item, having the item in grams

        Example:    Mango.measure_type = FRUITS
                    Mango.convert_rate = 300
                    if grams is 600 we are returning '2 FRUITS'

                    Sugar.measure_type = TBSP
                    Sugar.convert_rate = 15
                    if grams is 45 we are returning '3 TBSP'
        """
        return round(grams / self.convert_rate, 2)

    def convert_to_grams(self, quantity: float) -> float:
        """A function analogous to `convert_from_grams`

        Example:    Mango.measure_type = FRUITS
                    Mango.convert_rate = 300
                    if quantity is 2 we are returning '600 grams'

                    Sugar.measure_type = TBSP
                    Sugar.convert_rate = 15
                    if quantity is 4 we are returning '60 grams'
        """
        return round(quantity * self.convert_rate)


class Meal(models.Model):
    """Meals have ingredients, they are also included in days"""

    name = models.CharField(max_length=100, default="mymeal")
    description = models.CharField(max_length=200, null=True)
    recipe = models.TextField(max_length=1000, null=True)
    url = models.URLField(null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    ingredients = models.ManyToManyField(Ingredient, through="ThroughMealIngr")
    fats = models.FloatField(default=0)
    protein = models.FloatField(default=0)
    carbs = models.FloatField(default=0)
    image = ResizedImageField(
        size=[1000, 1500],
        crop=["middle", "center"],
        default="foods/default_meal_thumbnail.jpg",
        upload_to=UploadAndRename("foods/meal_thumbnails"),
    )

    class Meta:
        """Set the ordering by pk"""

        ordering = ["pk"]

    def __str__(self) -> str:
        return f"{self.name}"

    def save(self, *args: Any, **kwargs: Any) -> None:
        """Set the url for the meal and clean up old images"""
        image_clean_up(self)
        self.url = self.get_absolute_url()
        super().save(*args, **kwargs)

    def get_absolute_url(self) -> str:
        """Generate the attribute url for the meal"""
        return reverse("foods_meal_detail", kwargs={"pk": self.pk})

    def save_ingredients(
        self, ingredients: Sequence[Ingredient], amounts: Sequence[float]
    ) -> None:
        """Create the necessary relations for ingredients"""
        for ingredient, amount in zip(ingredients, amounts):
            relation = ThroughMealIngr.objects.create(
                meal=self, ingredient=ingredient, amount=amount
            )
            self.fats += relation.fats
            self.carbs += relation.carbs
            self.protein += relation.protein
        self.save()


class ThroughMealIngr(models.Model):
    """Through model between meals and ingredients"""

    meal = models.ForeignKey(Meal, on_delete=CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=CASCADE)
    amount = models.FloatField()
    grams = models.PositiveIntegerField(default=0)
    fats = models.FloatField(default=0)
    protein = models.FloatField(default=0)
    carbs = models.FloatField(default=0)

    def __str__(self) -> str:
        return f"{self.meal},{self.ingredient}"

    def save(self, *args: Any, **kwargs: Any) -> None:
        """Convert from native to grams"""
        self.grams = self.ingredient.convert_to_grams(self.amount)
        self.fats = round(self.ingredient.fats / 100 * self.grams, 2)
        self.protein = round(self.ingredient.protein / 100 * self.grams, 2)
        self.carbs = round(self.ingredient.carbs / 100 * self.grams, 2)
        super().save(*args, **kwargs)


class Day(models.Model):
    """The main field used to connect meals to users."""

    date = models.DateField(default=datetime.date.today)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    meals = models.ManyToManyField(Meal, through="ThroughDayMeal")
    backup = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.date},{self.author}"

    def save_meals(
        self, meals: Sequence[Meal], meal_nums: Sequence[int]
    ) -> None:
        """Create the necessary relations for meals"""
        for rel in ThroughDayMeal.objects.filter(day=self):
            rel.delete()
        for meal, meal_num in zip(meals, meal_nums):
            ThroughDayMeal.objects.create(
                day=self, meal=meal, meal_num=meal_num
            )

    def get_macros(self) -> list[float]:
        """Get the total calories from the meals"""
        relations = ThroughDayMeal.objects.filter(day=self)
        macros = [0.0, 0.0, 0.0, 0.0]
        for relation in relations:
            macros[0] += relation.meal.fats
            macros[1] += relation.meal.protein
            macros[2] += relation.meal.carbs

        macros[3] = macros[0] * 8 + macros[1] * 4 + macros[2] * 4
        return macros


class ThroughDayMeal(models.Model):
    """Through model between days and meals to denote meal numbers"""

    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    day = models.ForeignKey(Day, on_delete=models.CASCADE)
    meal_num = models.PositiveSmallIntegerField()

    def __str__(self) -> str:
        return f"{self.day},{self.meal}"


class Diet(models.Model):
    """Diets have days, which are backups of the real days of the user"""

    name = models.CharField(max_length=100)
    public = models.BooleanField(default=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    end_date = models.DateField()
    description = models.TextField(max_length=200)
    days = models.ManyToManyField(Day)
    slug = models.SlugField(null=False, unique=True)

    class Meta:
        """Set the ordering by pk"""

        ordering = ["pk"]

    def __str__(self) -> str:
        return f"{self.date},{self.author}"

    def save(self, *args: Any, **kwargs: Any) -> None:
        """Set the slug field, create days or the backups of the days"""
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self) -> str:
        """Generate the url for foods_diet_details"""
        return reverse("foods_diet_detail", kwargs={"slug": self.slug})

    def get_import_url(self) -> str:
        """Generate the url for diet imports"""
        return reverse("foods_diet_import", kwargs={"slug": self.slug})

    def delete(self, *args: Any, **kwargs: Any) -> tuple[int, dict[str, int]]:
        """Delete the diet and the associated backup days"""
        for day in self.days.all():
            day.delete()
        return super().delete(*args, **kwargs)

    def save_days(self) -> None:
        """Create days or the backups of the days"""
        delta = (self.end_date - self.date).days + 1
        dates = (
            self.date + datetime.timedelta(days=date) for date in range(delta)
        )

        for date in dates:
            instance, created = Day.objects.get_or_create(
                date=date, author=self.author, backup=False
            )
            if created:
                instance.backup = True
                instance.save()
            else:
                relations = ThroughDayMeal.objects.filter(day=instance)
                instance.pk = None
                instance.backup = True
                instance.save()  # generates a new instance
                for relation in relations:
                    relation.pk = None
                    relation.day = instance
                    relation.save()

            self.days.add(instance)

    def fill_days(self, user: User, date: Any) -> None:
        """Fill the days of the `user` from `date` with the selected diet"""

        if isinstance(date, str):
            origin = datetime.datetime.strptime(date, "%Y-%m-%d")
        else:
            origin = date

        for delta in range(len(self.days.all())):
            date = origin + datetime.timedelta(days=delta)
            day = Day.objects.filter(date=date, author=user).first()
            if day:
                day.delete()

        for idx, day in enumerate(self.days.all()):
            relations = ThroughDayMeal.objects.filter(day=day)
            day.date = origin + datetime.timedelta(days=idx)
            day.backup = False
            day.author = user
            day.save()
            for relation in relations:
                relation.day = day
                relation.save()
