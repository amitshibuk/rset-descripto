# Generated by Django 5.1.7 on 2025-04-03 18:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0002_create_groups'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='closed',
            field=models.BooleanField(default=False),
        ),
    ]
