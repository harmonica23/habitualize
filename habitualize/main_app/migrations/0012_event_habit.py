# Generated by Django 5.0.1 on 2024-01-20 22:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0011_alter_habit_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='habit',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='main_app.habit'),
        ),
    ]
