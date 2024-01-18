from django.shortcuts import render
from django.views.generic.edit import CreateView
from .models import Habit


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

class HabitCreate(CreateView):
  model = Habit
  fields = '__all__'