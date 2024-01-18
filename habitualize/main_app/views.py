from django.shortcuts import render
from django.views.generic.edit import CreateView
from .models import Habit


# Create your views here.
def habits_list(request):
  habits = Habit.objects
  return render(request, 'habits/list.html', {
    'habits': habits
  })

def home(request):
  return render(request, 'home.html')

def calendar(request):
  return render(request, 'calendar.html')

def habits_detail(request, habit_id):
  habit = Habit.objects.get(id=habit_id)
  return render(request, 'habits/detail.html',{
    'habit': habit
  })

class HabitCreate(CreateView):
  model = Habit
  fields = '__all__'
  success_url='/habits'

  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)