from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from .models import Habit


# Create your views here.
def habits_index(request):
  habits = Habit.objects.filter(user=request.user)
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
  
class HabitUpdate(UpdateView):
  model = Habit
  fields = '__all__'

class HabitDelete(DeleteView):
  model = Habit
  success_url = '/habits'
  
def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('index')
    else:
      error_message = 'Invalid sign up - try again'
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)