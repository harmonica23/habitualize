from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


# Create your models here.
class Habit(models.Model):
  name = models.CharField(max_length=100)
  streak = models.IntegerField()
  make_or_break = models.CharField(max_length=100)
  user = models.ForeignKey(User, on_delete=models.CASCADE)

  def __str__(self):
    return f'{self.name} ({self.id})'
  
  def get_absolute_url(self):
    return reverse('index', kwargs={'habit_id': self.id})

class Journal(models.Model):
  entry = models.CharField(max_length=500)

class Mood(models.Model):
  mood = object