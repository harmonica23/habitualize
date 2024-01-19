# Generated by Django 5.0.1 on 2024-01-19 19:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0006_habit_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='habit',
            name='category',
            field=models.CharField(blank=True, choices=[('Health', 'Health'), ('Fitness', 'Fitness'), ('Personal Development', 'Personal Development'), ('Relationships', 'Relationships')], max_length=50),
        ),
    ]
