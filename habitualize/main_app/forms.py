from django import forms
from .models import Habit, Event
from django.forms import ModelForm, DateInput

# class YourForm(forms.Form):
#     usernamename = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-style'}))
#     password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-style'}))
#     passwordconfirmation = forms.CharField(widget=forms.PasswordConfirmationInput(attrs={'class': 'form-style'}))

class HabitForm(forms.ModelForm):
    class Meta:
        model = Habit
        fields = ['name', 'goal', 'make_or_break', 'status']
        widgets = {
            'status': forms.RadioSelect(choices=((True, 'Active'),(False, 'Inactive')))
        }

class EventForm(ModelForm):
  class Meta:
    model = Event
    # datetime-local is a HTML5 input type, format to make date time show on fields
    widgets = {
      'start_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
      'end_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
    }
    fields = '__all__'

  def __init__(self, *args, **kwargs):
    super(EventForm, self).__init__(*args, **kwargs)
    # input_formats to parse HTML5 datetime-local input to datetime field
    self.fields['start_time'].input_formats = ('%Y-%m-%dT%H:%M',)
    self.fields['end_time'].input_formats = ('%Y-%m-%dT%H:%M',)

