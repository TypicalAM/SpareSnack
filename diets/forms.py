import datetime
from django import forms
from django.core import serializers
from django.forms import ValidationError

from .models import Day, Diet, Ingredient, IntermediaryDayMeal, IntermediaryMealIngredient, Meal

class MealForm(forms.ModelForm):
    class Meta:
        model   = Meal
        fields  = ('name', 'description', 'recipe', 'image')
    def __init__(self, author, *args, **kwargs):
        self.author = author
        super(MealForm, self).__init__(*args, **kwargs)

    def verify_ingredients(self):
        ingr_data   = self.data.get('ingredient_data')
        amounts     = self.data.get('amounts')
        if not ingr_data or not amounts:
            raise ValidationError('Invalid ingredient data')
        try:
            ingr_arr    = [Ingredient.objects.get(name=obj.object.name) for obj in serializers.deserialize("json",ingr_data)]
            amounts_arr = [int(obj) for obj in amounts.split(',')]
            assert len(ingr_arr) == len(amounts_arr)
        except:
            raise ValidationError('Incoherent ingredient data')
        return ingr_arr, amounts_arr

    def clean(self):
        ingredient_data, amounts    = self.verify_ingredients()
        clean_data                  = self.cleaned_data
        clean_data['ingredients']   = ingredient_data
        clean_data['amounts']       = amounts
        return clean_data

    def save(self):
        clean_data = self.cleaned_data
        my_meal = Meal.objects.create(
                name        = clean_data['name'],
                description = clean_data['description'],
                recipe      = clean_data['recipe'],

                image       = clean_data['image'],
                author      = self.author
                )
        my_meal.save()
        for k in range(len(clean_data['ingredients'])):
            IntermediaryMealIngredient.objects.create(
                    meal        = my_meal,
                    ingredient  = clean_data['ingredients'][k],
                    amount      = clean_data['amounts'][k]
                    )

class DietForm(forms.ModelForm):

    class Meta:
        model   = Diet
        fields  = ('name', 'public', 'description', 'date')

    def save(self, author):
        my_diet     = Diet.objects.create(**self.cleaned_data, author=author)
        dates       = [my_diet.date + datetime.timedelta(days=i) for i in range(8)]
        my_diet.save()
        for date in dates:
            instance, created = Day.objects.get_or_create(date=date, author=author, backup=False)
            if created:
                instance.backup=True
                instance.save()
            else:
                relations = IntermediaryDayMeal.objects.filter(day=instance)
                instance.pk = None
                instance.backup = True
                instance.save() # generates a new instance
                for relation in relations:
                    relation.pk = None
                    relation.day = instance
                    relation.save()
            my_diet.days.add(instance)
