from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from .models import Habit, Event
from django.urls import reverse
from .utils import Calendar
from django.utils.safestring import mark_safe
from datetime import datetime
from .forms import HabitForm, RegisterUserForm, EventForm
from django.utils.safestring import mark_safe
from datetime import datetime, timedelta
from calendar import monthcalendar
from .utils import prev_month, next_month

# Create your views here.
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
  return render(request, 'habits/detail.html',{
    'habit': habit
  })

class HabitCreate(LoginRequiredMixin, CreateView):
    model = Habit
    form_class = HabitForm
    template_name = 'main_app/habit_form.html'
    success_url = '/habits'

    def form_valid(self, form):
        form.instance.user = self.request.user
        new_category = form.cleaned_data.get('new_category')

        if new_category:
            form.instance.category = new_category

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = datetime.today()
        d = get_date(self.request.GET.get('month', None))


        try: 
          prev_month_value = prev_month(d)
          next_month_value = next_month(d)
        except Exception as e:
          print(f"Error calculating prev_month and next_month: {e}")
          prev_month_value = ''
          next_month_value = ''

        cal = Calendar(d.year, d.month)
        html_cal = cal.formatmonth(withyear=True)

        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month_value
        context['next_month'] = next_month_value

        return context

def get_date(req_month):
    if req_month:
        year, month = (int(x) for x in req_month.split('-'))
        return datetime(year, month, day=1)
    return datetime.today()

def prev_month(d):
    prev_month = d - timedelta(days=1)
    month = f"{prev_month.year}-{prev_month.month:02d}"
    return month

def next_month(d):
    next_month = d + timedelta(days=32)
    month = f"{next_month.year}-{next_month.month:02d}"
    return month

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