from django.urls import path
from . import views



urlpatterns = [
  path('', views.home, name='home'),
  path('habits/', views.habits_index, name='index'),
  path('habits/<int:habit_id>/', views.habits_detail, name='detail'),
  path('habits/create/', views.HabitCreate.as_view(), name='create'),
  path('accounts/signup/', views.signup, name='signup'),
  path('habits/<int:pk>/update/', views.HabitUpdate.as_view(), name='habits_update'),
  path('habits/<int:pk>/delete/', views.HabitDelete.as_view(), name='habits_delete'),
  path('calendar/', views.CalendarView.as_view(), name='calendar'),
  path('habit/<int:habit_id>/<str:habit_name>/event/new/', views.event, name='event_new'),
  path('calendar/previous/', views.prev_month, name='prev_month_calendar'),
  path('calendar/next/', views.next_month, name='next_month_calendar'),
  path('event/edit/<int:event_id>/', views.event, name='event_edit'),
  path('random_quote/', views.random_quote_view, name='random_quote')
]