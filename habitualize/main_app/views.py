from django.shortcuts import render
from .models import Habit
from django.views.generic import ListView

# Create your views here.
def home(request):
  return render(request, 'home.html')

def habits_list(request):
  return render(request, 'habits/list.html', {
    'habits': habits
  })

def habits_detail(request, habit_id):
  habit = Habit.objects.get(id=habit_id)
  return render(request, 'habits/detail.html',{
    'habit': habit
  })

class HabitList(ListView):
  model = Habit