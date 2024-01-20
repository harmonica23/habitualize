from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import Habit, Event
from django.forms import ModelForm, DateInput


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Create User Name', widget=forms.TextInput(attrs={'class': ['form_style', 'sub_title', 'form_area', 'form_group']}))
    password1 = forms.CharField(label='Create Password', widget=forms.PasswordInput(attrs={'class': ['form_style', 'sub_title', 'form_area', 'form_group']}))
    password2 = forms.CharField(label='Re-enter Password', widget=forms.PasswordInput(attrs={'class': ['form_style', 'sub_title', 'form_area', 'form_group']}))

    class Meta:
        model = User
        fields = ('username',)

    def __init__(self, *args, **kwargs):
        super(RegisterUserForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = ['form_style', 'sub_title', 'form_area', 'form_group']  
        self.fields['password1'].widget.attrs['class'] = ['form_style', 'sub_title', 'form_area', 'form_group'] 
        self.fields['password2'].widget.attrs['class'] = ['form_style', 'sub_title', 'form_area', 'form_group'] 


class HabitForm(forms.ModelForm):
    new_category = forms.CharField(max_length=50, required=False, label='New Category')

    class Meta:
        model = Habit
        fields = ['name', 'goal', 'make_or_break', 'category', 'new_category', 'status']
        widgets = {
            'status': forms.RadioSelect(choices=((True, 'Active'), (False, 'Inactive')))
        }

    def clean(self):
        cleaned_data = super().clean()
        category = cleaned_data.get('category')
        new_category = cleaned_data.get('new_category')

        if not category and not new_category:
            raise forms.ValidationError('Please select a category or enter a new one.')

        return cleaned_data


class EventForm(ModelForm):
    class Meta:
        model = Event
        widgets = {
            'start_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'end_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        }
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        self.fields['start_time'].input_formats = ('%Y-%m-%dT%H:%M',)
        self.fields['end_time'].input_formats = ('%Y-%m-%dT%H:%M',)
