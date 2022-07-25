# Generated by Django 4.0.6 on 2022-07-25 19:57

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Day",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date", models.DateField(default=datetime.date.today)),
                ("backup", models.BooleanField(default=False)),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Ingredient",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(default="ingr", max_length=100)),
                (
                    "image",
                    models.ImageField(
                        default="ingr_thumb/default.jpg", upload_to="ingr_thumb"
                    ),
                ),
                ("measure_type", models.CharField(max_length=50)),
                ("convert_rate", models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name="Meal",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(default="mymeal", max_length=100)),
                ("description", models.CharField(max_length=200, null=True)),
                ("recipe", models.TextField(max_length=1000, null=True)),
                (
                    "image",
                    models.ImageField(
                        default="meal_thumb/default.jpg", upload_to="meal_thumb"
                    ),
                ),
                ("url", models.URLField(null=True)),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ["pk"],
            },
        ),
        migrations.CreateModel(
            name="ThroughMealIngr",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("amount", models.FloatField()),
                ("grams", models.PositiveIntegerField(default=0)),
                (
                    "ingredient",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="diets.ingredient",
                    ),
                ),
                (
                    "meal",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="diets.meal",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ThroughDayMeal",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("meal_num", models.PositiveSmallIntegerField()),
                (
                    "day",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="diets.day",
                    ),
                ),
                (
                    "meal",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="diets.meal",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="meal",
            name="ingredients",
            field=models.ManyToManyField(
                through="diets.ThroughMealIngr", to="diets.ingredient"
            ),
        ),
        migrations.CreateModel(
            name="Diet",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("public", models.BooleanField(default=True)),
                ("date", models.DateField()),
                ("end_date", models.DateField()),
                ("description", models.TextField(max_length=200)),
                ("slug", models.SlugField(unique=True)),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                ("days", models.ManyToManyField(to="diets.day")),
            ],
            options={
                "ordering": ["pk"],
            },
        ),
        migrations.AddField(
            model_name="day",
            name="meals",
            field=models.ManyToManyField(
                through="diets.ThroughDayMeal", to="diets.meal"
            ),
        ),
    ]
