# Generated by Django 5.1.4 on 2025-01-03 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='stock',
            name='size',
            field=models.FloatField(null=True),
        ),
    ]
