# Generated by Django 4.0.6 on 2023-11-03 23:22

import core.utils
import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_resized.forms


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Day',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=datetime.date.today)),
                ('backup', models.BooleanField(default=False)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('measure_type', models.CharField(max_length=50)),
                ('convert_rate', models.FloatField(default=1)),
                ('fats', models.FloatField(default=0)),
                ('protein', models.FloatField(default=0)),
                ('carbs', models.FloatField(default=0)),
                ('image', django_resized.forms.ResizedImageField(crop=None, default='foods/default_ingredient_thumbnail.jpg', force_format=None, keep_meta=False, quality=75, scale=None, size=[200, 200], upload_to=core.utils.UploadAndRename('foods/ingredient_thumbnails'))),
            ],
        ),
        migrations.CreateModel(
            name='Meal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='mymeal', max_length=100)),
                ('description', models.CharField(max_length=200, null=True)),
                ('recipe', models.TextField(max_length=1000, null=True)),
                ('url', models.URLField(null=True)),
                ('fats', models.FloatField(default=0)),
                ('protein', models.FloatField(default=0)),
                ('carbs', models.FloatField(default=0)),
                ('image', django_resized.forms.ResizedImageField(crop=['middle', 'center'], default='foods/default_meal_thumbnail.jpg', force_format=None, keep_meta=False, quality=75, scale=None, size=[1000, 1500], upload_to=core.utils.UploadAndRename('foods/meal_thumbnails'))),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['pk'],
            },
        ),
        migrations.CreateModel(
            name='ThroughMealIngr',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField()),
                ('grams', models.PositiveIntegerField(default=0)),
                ('fats', models.FloatField(default=0)),
                ('protein', models.FloatField(default=0)),
                ('carbs', models.FloatField(default=0)),
                ('ingredient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='foods.ingredient')),
                ('meal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='foods.meal')),
            ],
        ),
        migrations.CreateModel(
            name='ThroughDayMeal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('meal_num', models.PositiveSmallIntegerField()),
                ('day', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='foods.day')),
                ('meal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='foods.meal')),
            ],
        ),
        migrations.AddField(
            model_name='meal',
            name='ingredients',
            field=models.ManyToManyField(through='foods.ThroughMealIngr', to='foods.ingredient'),
        ),
        migrations.CreateModel(
            name='Diet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('public', models.BooleanField(default=True)),
                ('date', models.DateField()),
                ('end_date', models.DateField()),
                ('description', models.TextField(max_length=200)),
                ('slug', models.SlugField(unique=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('days', models.ManyToManyField(to='foods.day')),
            ],
            options={
                'ordering': ['pk'],
            },
        ),
        migrations.AddField(
            model_name='day',
            name='meals',
            field=models.ManyToManyField(through='foods.ThroughDayMeal', to='foods.meal'),
        ),
    ]