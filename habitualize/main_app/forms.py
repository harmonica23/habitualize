from django import forms

class YourForm(forms.Form):
    usernamename = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-style'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-style'}))
    passwordconfirmation = forms.CharField(widget=forms.PasswordConfirmationInput(attrs={'class': 'form-style'}))
