from django.shortcuts import render, redirect, reverse 
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.utils import timezone
from django.http import HttpResponse
from .models import Habit, Event, Journal
from django.urls import reverse
from .utils import Calendar
from django.utils.safestring import mark_safe
from datetime import date, datetime, timedelta
from .forms import HabitForm, RegisterUserForm, EventForm, JournalForm
from django.utils import timezone
import calendar
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
import requests


@login_required
def create_journal(request):
    user = request.user
    today = date.today()

    active_habits = Habit.objects.filter(user=user, status=True)

    context = {
        'active_habits': active_habits
    }
    if request.method == 'POST':
        form = JournalForm(request.POST)
        if form.is_valid():
            print(form)
            new_journal = form.save(commit=False)
            new_journal.user = request.user
            new_journal.date_created = today
            new_journal.save()
            return redirect('journal_index')

    else:
        form = JournalForm()

    context['form'] = form
    return render(request, 'main_app/journal_form.html', context)



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

@login_required
def journal_index(request):
  order_by = request.GET.get('order_by', 'id')
  journals = Journal.objects.filter(user=request.user).order_by(order_by)
  context = {
        'journals': journals,
        'current_order': order_by,
    }
  return render(request, 'main_app/journal_index.html', {
    'journals': journals
  })

def home(request):
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
        return render(request, 'home.html', {'quote': data['quoteText']})
    except requests.exceptions.RequestException as e:
        print(f"Error fetching quote: {e}")
        return render(request, 'home.html', {'quote': 'Error fetching quote. Please try again later.'})

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
    
class EventNew(CreateView, LoginRequiredMixin):
  
    def create_form(request, habit_id, habit_name):
      instance = Event()
      template_name = 'event_edit.html'
      form = EventForm(request.POST or None, instance=instance)
      if request.POST and form.is_valid():
        new_event=form.save(commit=False)
        new_event.habit_id=habit_id
        new_event.user_id=request.user.id
        new_event.title=habit_name
        new_event.save()
        return HttpResponseRedirect(reverse('calendar'))
      return render(request, 'event_edit.html', {'form': form})

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
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = getattr(self.request, 'user', None)
        if user is not None:
          d = get_date(self.request.GET.get('day', None))
          cal = Calendar(d.year, d.month)
          html_cal = cal.formatmonth(withyear=True, user_id=self.request.user)
          context['calendar'] = mark_safe(html_cal)
          context['prev_month'] = prev_month(d)
          #context['next_month'] = next_month(d)
        else:
          context['calendar'] = "User not authenticated"
        return context

def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return date(year, month, day=1)
    return timezone.now().date()

def prev_month(d):
    first = timezone.now().date().replace(day=1)
    prev_month = first - timedelta(days=1)
    url = reverse('calendar') + f"?month={prev_month.year}-{prev_month.month:02d}"
    return redirect(url)

def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month

@login_required
def event(request, event_id):
    instance = Event()
    template_name = 'event_edit.html'
    form = EventForm(request.POST or None, instance=instance)
    if request.POST and form.is_valid():
      
        new_event=form.save(commit=False)
        new_event.event_id=event_id
        new_event.user_id=request.user.id
        new_event.save()
        return HttpResponseRedirect(reverse('calendar'))
    return render(request, 'event_edit.html', {'form': form})

def index(request):
    habits = Habit.objects.all()
    search_query = request.GET.get('search')
    if search_query:
        habits = habits.filter(name__icontains=search_query)
    context = {'habits': habits}
    return render(request, 'habits/index.html', context)


