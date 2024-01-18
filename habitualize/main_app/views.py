from django.shortcuts import render
from django.views.generic.edit import CreateView
from .models import Habit


# Create your views here.
def habits_index(request):
  habits = Habit.objects.all()
  return render(request, 'habits/index.html', {
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