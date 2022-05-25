# Generated by Django 4.0.4 on 2022-05-21 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("diets", "0008_remove_diet_url_slug"),
    ]

    operations = [
        migrations.AddField(
            model_name="diet",
            name="desc",
            field=models.SlugField(default=123, unique=True),
            preserve_default=False,
        ),
    ]
