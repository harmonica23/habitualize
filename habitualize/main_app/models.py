from django.db import models

# Create your models here.
class Habit(models.Model):
  name = models.CharField(max_length=100)
  streak = models.IntegerField()
  make_or_break = models.CharField(max_length=100)

class Journal(models.Model):
  entry = models.CharField(max_length=500)

class Mood(models.Model):
  mood = object