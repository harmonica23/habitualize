# Generated by Django 5.0.1 on 2024-01-20 20:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0010_merge_20240120_2002'),
    ]

    operations = [
        migrations.AlterField(
            model_name='habit',
            name='category',
            field=models.CharField(blank=True, choices=[('Health', 'Health'), ('Fitness', 'Fitness'), ('Personal Development', 'Personal Development'), ('Relationships', 'Relationships'), ('Other', 'Other')], max_length=50, null=True),
        ),
    ]