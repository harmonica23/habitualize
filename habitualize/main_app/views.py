from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.http import HttpResponse
from .models import Habit, Event
from django.urls import reverse
from .utils import Calendar
from django.utils.safestring import mark_safe
from datetime import date, datetime, timedelta
from .forms import HabitForm, RegisterUserForm, EventForm
from django.utils import timezone
import calendar
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
import requests

@login_required
def habits_index(request):
  order_by = request.GET.get('order_by', 'created_at')
  habits = Habit.objects.filter(user=request.user).order_by(order_by)
  context = {
        'habits': habits,
        'current_order': order_by,
    }
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
  event_form = EventForm()
  return render(request, 'habits/detail.html',{
    'habit': habit,
    'event_form':event_form
  })

class HabitCreate(LoginRequiredMixin, CreateView):
    model = Habit
    form_class = HabitForm
    template_name = 'main_app/habit_form.html'
    success_url = '/habits'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class HabitUpdate(LoginRequiredMixin, UpdateView):
    model = Habit
    form_class = HabitForm
    template_name = 'habits/habit_update.html'

    def get_success_url(self):
        return reverse('detail', kwargs={'habit_id': self.object.id})
  


class HabitDelete(LoginRequiredMixin, DeleteView):
  model = Habit
  success_url = '/habits'

  
def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = RegisterUserForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('index')
    else:
      error_message = 'Invalid sign up - try again'
  form = RegisterUserForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)


class CalendarView(ListView):
    model = Event
    template_name = 'calendar.html'
    def get_queryset(self):
        return Event.objects.filter(user=self.request.user)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = getattr(self.request, 'user', None)
        if user is not None:
          d = get_date(self.request.GET.get('day', None))
          print(d)
          cal = Calendar(d.year, d.month)
          html_cal = cal.formatmonth(withyear=True)
          context['calendar'] = mark_safe(html_cal)
        else:
          context['calendar'] = "User not authenticated"
        return context


def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return date(year, month, day=1)
    return timezone.now().date()

def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month

def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month

@login_required
def event(request, event_id=None):
    instance = Event()
    if event_id:
        instance = get_object_or_404(Event, pk=event_id)
    else:
        instance = Event()
    
    form = EventForm(request.POST or None, instance=instance)
    if request.POST and form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('cal:calendar'))
    return render(request, 'cal/event.html', {'form': form})


def get_forismatic_quote():
    url = "http://api.forismatic.com/api/1.0/"
    params = {
        "method": "getQuote",
        "format": "json",
        "lang": "en",
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        return data["quoteText"]
    except requests.exceptions.RequestException as e:
        print(f"Error fetching quote: {e}")
        return None

def random_quote_view(request):
    quote = get_forismatic_quote()
  
    return render(request, 'random_quote.html', {'random_quote': quote})


