# Generated by Django 5.0.1 on 2024-01-24 00:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0022_journal_mood'),
    ]

    operations = [
        migrations.AddField(
            model_name='journal',
            name='question',
            field=models.BooleanField(default=False),
        ),
    ]
