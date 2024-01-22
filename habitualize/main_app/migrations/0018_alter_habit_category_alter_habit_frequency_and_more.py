# Generated by Django 5.0.1 on 2024-01-22 16:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0017_alter_habit_category_alter_habit_unit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='habit',
            name='category',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='habit',
            name='frequency',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='habit',
            name='goal',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='habit',
            name='unit',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
