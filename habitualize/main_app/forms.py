from django import forms
from .models import Habit
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