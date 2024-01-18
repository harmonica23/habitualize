from django.db import models
from django.urls import reverse


# Create your models here.
class Habit(models.Model):
  name = models.CharField(max_length=100)
  streak = models.IntegerField()
  make_or_break = models.CharField(max_length=100)

  def __str__(self):
    return f'{self.name} ({self.id})'
  
  def get_absolute_url(self):
    return reverse('detail', kwargs={'habit_id': self.id})

class Journal(models.Model):
  entry = models.CharField(max_length=500)

class Mood(models.Model):
  mood = object