from django.urls import path
from . import views


urlpatterns = [
  path('', views.home, name='home'),
  path('habits/', views.habits_index, name='index'),
  path('habits/<int:habit_id>/', views.habits_detail, name='detail'),
  path('habits/create/', views.HabitCreate.as_view(), name='create'),
  path('calendar/', views.calendar, name='calendar'),
]