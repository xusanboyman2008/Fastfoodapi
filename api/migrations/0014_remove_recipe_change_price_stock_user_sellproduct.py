# Generated by Django 5.1.4 on 2025-01-05 13:08

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0013_rename_measurement_ingredientgram_amount_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipe',
            name='change_price',
        ),
        migrations.AddField(
            model_name='stock',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='SellProduct',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('amount', models.FloatField()),
                ('changes', models.TextField(blank=True, null=True)),
                ('price', models.FloatField()),
                ('updated_price', models.FloatField()),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('deleted', models.BooleanField(default=False)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
