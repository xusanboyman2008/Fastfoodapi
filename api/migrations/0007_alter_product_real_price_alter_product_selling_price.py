# Generated by Django 5.1.4 on 2025-01-04 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_remove_product_price_product_real_price_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='real_price',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='product',
            name='selling_price',
            field=models.FloatField(),
        ),
    ]
