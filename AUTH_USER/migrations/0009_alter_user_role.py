# Generated by Django 5.1.4 on 2025-01-08 05:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AUTH_USER', '0008_alter_user_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(blank=True, default='User', max_length=150, null=True),
        ),
    ]
