# Generated by Django 5.1.4 on 2025-01-10 06:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_status_draft'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='status',
            name='deleted',
        ),
    ]
