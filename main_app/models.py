from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


# Create your models here.
class Habit(models.Model):
    name = models.CharField(max_length=100)
    goal = models.IntegerField(default=0)
    frequency = models.CharField(max_length=100)
    unit = models.CharField(max_length=100) 
    make_or_break = models.CharField(max_length=100)
    status = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=50, null=True, blank=True) 
  
    category_choices = [
        ('Health', 'Health'),
        ('Fitness', 'Fitness'),
        ('Personal Development', 'Personal Development'),
        ('Relationships', 'Relationships'),
        ('Other', 'Other'),
    ]

    def __str__(self):
      return f'{self.name} ({self.id})'

    def get_absolute_url(self):
      return reverse('detail', kwargs={'habit_id': self.id})

class Journal(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  entry = models.CharField(max_length=500)
  habit = models.ForeignKey(Habit, on_delete=models.CASCADE)
  date = models.DateField('Journal Date')
  class Meta:
    ordering = ['-date']

  def __str__(self):
      return f"{self.user.username}'s Journal Entry"

class Mood(models.Model):
  mood = object

class Event(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE, null=True, default=None)

    def __str__(self):
        return self.title
    @property
    def get_html_url(self):
        url = reverse('event_edit', args=(self.id,))
        return f'<a href="{url}"> {self.title} </a>'
    def get_absolute_url(self):
      return reverse('detail', kwargs={'event_id': self.id})