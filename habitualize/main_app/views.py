from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Habit


# Create your views here.
@login_required
def habits_index(request):
  habits = Habit.objects.filter(user=request.user)
  return render(request, 'habits/index.html', {
    'habits': habits
  })

def home(request):
  return render(request, 'home.html')

@login_required
def calendar(request):
  return render(request, 'calendar.html')

@login_required
def habits_detail(request, habit_id):
  habit = Habit.objects.get(id=habit_id)
  return render(request, 'habits/detail.html',{
    'habit': habit
  })

class HabitCreate(LoginRequiredMixin, CreateView):
  model = Habit
  fields = ['name', 'goal', 'make_or_break']
  success_url ='/habits'

  def form_valid(self, form):
    form.instance.user = self.request.user 
    return super().form_valid(form)
  
class HabitUpdate(LoginRequiredMixin, UpdateView):
  model = Habit
  fields = ['name', 'goal', 'make_or_break']

class HabitDelete(LoginRequiredMixin, DeleteView):
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