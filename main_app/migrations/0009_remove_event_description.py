# Generated by Django 5.0.1 on 2024-01-19 21:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0008_event_alter_habit_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='description',
        ),
    ]
