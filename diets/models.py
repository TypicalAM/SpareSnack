from django.contrib.auth.models import User
from django.db import models
from django.db.models.deletion import CASCADE
from django.template.defaultfilters import slugify
from django.utils import timezone
from django.urls.base import reverse_lazy

def get_sentinel() -> User:
    return User.objects.get_or_create(username='[deleted]')[0]

class Ingredient(models.Model):
    name        = models.CharField(max_length=50, default='ingr')
    image       = models.ImageField(default='ingr_thumb/default.jpg',upload_to='ingr_thumb')

    def __str__(self):
        return f'{self.name}'

class Meal(models.Model):
    name        = models.CharField(max_length=50, default='mymeal')
    description = models.CharField(max_length=50, null=True)
    recipe      = models.TextField(max_length=1000,null=True)
    image       = models.ImageField(default='meal_thumb/default.jpg',upload_to='meal_thumb')
    author      = models.ForeignKey(User,on_delete=models.SET(get_sentinel))
    ingredients = models.ManyToManyField(Ingredient, through='IntermediaryMealIngredient')
    url         = models.URLField(null=True)

    def save(self, *args, **kwargs):
        if not self.url:
            self.url = self.get_absolute_url()
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse_lazy("meal-detail", kwargs={"pk": self.pk})

    def __str__(self):
        return f'{self.name}'

class IntermediaryMealIngredient(models.Model):
    meal        = models.ForeignKey(Meal, on_delete=CASCADE)
    ingredient  = models.ForeignKey(Ingredient, on_delete=CASCADE)
    amount      = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.meal},{self.ingredient}'

class Day(models.Model):
    date        = models.DateField(default=timezone.now)
    author      = models.ForeignKey(User, on_delete=models.SET(get_sentinel))
    meals       = models.ManyToManyField(Meal, through='IntermediaryDayMeal')
    backup      = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.date},{self.author}'

class IntermediaryDayMeal(models.Model):
    meal        = models.ForeignKey(Meal,on_delete=models.CASCADE)
    day         = models.ForeignKey(Day,on_delete=models.CASCADE)
    meal_num    = models.PositiveSmallIntegerField()

    def __str__(self):
        return f'{self.day},{self.meal}'

class Diet(models.Model):
    name        = models.CharField(max_length=50)
    public      = models.BooleanField()
    author      = models.ForeignKey(User,on_delete=models.SET(get_sentinel))
    date        = models.DateField(default=timezone.now)
    description = models.TextField(max_length=200)
    days        = models.ManyToManyField(Day)
    slug        = models.SlugField(null=False, unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse_lazy("diet-detail", kwargs={"slug": self.slug})

    def __str__(self):
        return f'{self.date},{self.author}'
