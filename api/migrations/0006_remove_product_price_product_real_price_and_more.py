# Generated by Django 5.1.4 on 2025-01-04 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_rename_ingredients_recipe_ingredient'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='price',
        ),
        migrations.AddField(
            model_name='product',
            name='real_price',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='selling_price',
            field=models.FloatField(blank=True, default=0),
        ),
        migrations.AddField(
            model_name='recipe',
            name='change_price',
            field=models.FloatField(null=True),
        ),
    ]
