"""Models for the diets app"""
import datetime

from django.contrib.auth.models import User
from django.db import models
from django.db.models.deletion import CASCADE
from django.template.defaultfilters import slugify
from django.urls.base import reverse


def get_sentinel() -> User:
    """Get the sentinel user (in case data gets deleted but needs to remain)"""
    return User.objects.get_or_create(username="[deleted]")[0]


class Ingredient(models.Model):
    """Ingredients are intertwined with meals"""

    name = models.CharField(max_length=100, default="ingr")
    image = models.ImageField(
        default="ingr_thumb/default.jpg", upload_to="ingr_thumb"
    )

    measure_type = models.CharField(max_length=50)
    convert_rate = models.FloatField()

    fats = models.FloatField(default=0)
    protein = models.FloatField(default=0)
    carbs = models.FloatField(default=0)

    def convert_from_grams(self, grams):
        """Display to the user the amount of the item, having the item in grams

        Example:    Mango.measure_type = FRUITS
                    Mango.convert_rate = 300
                    if grams is 600 we are returning '2 FRUITS'

                    Sugar.measure_type = TBSP
                    Sugar.convert_rate = 15
                    if grams is 45 we are returning '3 TBSP'
        """
        return round(grams / self.convert_rate, 2)

    def convert_to_grams(self, quantity):
        """A function analogous to `convert_from_grams`

        Example:    Mango.measure_type = FRUITS
                    Mango.convert_rate = 300
                    if quantity is 2 we are returning '600 grams'

                    Sugar.measure_type = TBSP
                    Sugar.convert_rate = 15
                    if quantity is 4 we are returning '60 grams'
        """
        return round(quantity * self.convert_rate)

    def __str__(self):
        return f"{self.name} measured with {self.measure_type} at {self.convert_rate}g per 1 item"


class Meal(models.Model):
    """Meals have ingredients, they are also included in days"""

    name = models.CharField(max_length=100, default="mymeal")
    description = models.CharField(max_length=200, null=True)
    recipe = models.TextField(max_length=1000, null=True)
    image = models.ImageField(
        default="meal_thumb/default.jpg", upload_to="meal_thumb"
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    ingredients = models.ManyToManyField(Ingredient, through="ThroughMealIngr")
    url = models.URLField(null=True)

    def save(self, *args, **kwargs):
        """Set the url for the meal"""
        self.url = self.get_absolute_url()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """Generate the attribute url for the meal"""
        return reverse("meal-detail", kwargs={"pk": self.pk})

    def __str__(self):
        return f"{self.name}"

    class Meta:
        """Set the ordering by pk"""

        ordering = ["pk"]


class ThroughMealIngr(models.Model):
    """Through model between meals and ingredients"""

    meal = models.ForeignKey(Meal, on_delete=CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=CASCADE)
    amount = models.FloatField()
    grams = models.PositiveIntegerField(default=0)

    fats = models.FloatField(default=0)
    protein = models.FloatField(default=0)
    carbs = models.FloatField(default=0)

    def __str__(self):
        return f"{self.meal},{self.ingredient}"

    def save(self, *args, **kwargs):
        """Convert from native to grams"""
        self.grams = self.ingredient.convert_to_grams(self.amount)
        self.fats = self.ingredient.fats / 100 * self.grams
        self.protein = self.ingredient.protein / 100 * self.grams
        self.carbs = self.ingredient.carbs / 100 * self.grams
        super().save(*args, **kwargs)


class Day(models.Model):
    """The main field used to connect meals to users."""

    date = models.DateField(default=datetime.date.today)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    meals = models.ManyToManyField(Meal, through="ThroughDayMeal")
    backup = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.date},{self.author}"


class ThroughDayMeal(models.Model):
    """Through model between days and meals to denote meal numbers"""

    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    day = models.ForeignKey(Day, on_delete=models.CASCADE)
    meal_num = models.PositiveSmallIntegerField()

    def __str__(self):
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

    def save(self, *args, **kwargs):
        """Set the slug field, create days or the backups of the days"""
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

        delta = (self.end_date - self.date).days + 1
        dates = (self.date + datetime.timedelta(days=i) for i in range(delta))

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

    def delete(self, *args, **kwargs):
        """Delete the diet and the associated backup days"""
        for day in self.days.all():
            day.delete()
        super().delete(*args, **kwargs)

    def fill_days(self, user, date):
        """Fill the days of the `user` from `date` with the selected diet"""

        if isinstance(date, str):
            origin = datetime.datetime.strptime(date, "%Y-%m-%d")
        else:
            origin = date

        for i in range(len(self.days.all())):
            date = origin + datetime.timedelta(days=i)
            day = Day.objects.filter(date=date, author=user).first()
            if day:
                day.delete()

        for i, day in enumerate(self.days.all()):
            relations = ThroughDayMeal.objects.filter(day=day)
            day.date = origin + datetime.timedelta(days=i)
            day.backup = False
            day.author = user
            day.save()
            for relation in relations:
                relation.day = day
                relation.save()

    def get_absolute_url(self):
        """Generate the url for diet-details"""
        return reverse("diet-detail", kwargs={"slug": self.slug})

    def __str__(self):
        return f"{self.date},{self.author}"

    class Meta:
        """Set the ordering by pk"""

        ordering = ["pk"]
