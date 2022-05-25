"""Models for the diets app"""
from django.contrib.auth.models import User
from django.db import models
from django.db.models.deletion import CASCADE
from django.template.defaultfilters import slugify
from django.utils import timezone
from django.urls.base import reverse


def get_sentinel() -> User:
    """Get the sentinel user (in case data gets deleted but needs to remain)"""
    return User.objects.get_or_create(username="[deleted]")[0]


class Ingredient(models.Model):
    """Ingredients are intertwined with meals"""

    name = models.CharField(max_length=50, default="ingr")
    image = models.ImageField(default="ingr_thumb/default.jpg", upload_to="ingr_thumb")

    def __str__(self):
        return f"{self.name}"


class Meal(models.Model):
    """Meals have ingredients, they are also included in days"""

    name = models.CharField(max_length=50, default="mymeal")
    description = models.CharField(max_length=50, null=True)
    recipe = models.TextField(max_length=1000, null=True)
    image = models.ImageField(default="meal_thumb/default.jpg", upload_to="meal_thumb")
    author = models.ForeignKey(User, on_delete=models.SET(get_sentinel))
    ingredients = models.ManyToManyField(
        Ingredient, through="IntermediaryMealIngredient"
    )
    url = models.URLField(null=True)

    def save(self, *args, **kwargs):
        """Set the url for the meal"""
        self.url = self.get_absolute_url()
        super(Meal, self).save(*args, **kwargs)

    def get_absolute_url(self):
        """Generate the attribute url for the meal"""
        return reverse("meal-detail", kwargs={"pk": self.pk})

    def __str__(self):
        return f"{self.name}"


class IntermediaryMealIngredient(models.Model):
    """Through model between meals and ingredients"""

    meal = models.ForeignKey(Meal, on_delete=CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=CASCADE)
    amount = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.meal},{self.ingredient}"


class Day(models.Model):
    """Days have meals, days are included in diets"""

    date = models.DateField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.SET(get_sentinel))
    meals = models.ManyToManyField(Meal, through="IntermediaryDayMeal")
    backup = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.date},{self.author}"


class IntermediaryDayMeal(models.Model):
    """Through model between days and meals to denote meal numbers"""

    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    day = models.ForeignKey(Day, on_delete=models.CASCADE)
    meal_num = models.PositiveSmallIntegerField()

    def __str__(self):
        return f"{self.day},{self.meal}"


class Diet(models.Model):
    """Diets have days, which are backups of the real days of the user"""

    name = models.CharField(max_length=50)
    public = models.BooleanField()
    author = models.ForeignKey(User, on_delete=models.SET(get_sentinel))
    date = models.DateField(default=timezone.now)
    description = models.TextField(max_length=200)
    days = models.ManyToManyField(Day)
    slug = models.SlugField(null=False, unique=True)

    def save(self, *args, **kwargs):
        """Set the slug field"""
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        """Generate the url for diet-details"""
        return reverse("diet-detail", kwargs={"slug": self.slug})

    def __str__(self):
        return f"{self.date},{self.author}"
