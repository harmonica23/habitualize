from django.urls import path
from . import views

urlpatterns = [
  path('', views.home, name='home'),
  path('habits/', views.habits_list, name='list'),
  path('habits/<int:habit_id>/', views.habits_detail, name='detail'),
]