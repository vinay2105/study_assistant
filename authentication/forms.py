from django import forms 
from django.forms import ModelForm

from .models import User, Profile

class RegistrationForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

        widgets = {
            'password': forms.PasswordInput
        }


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['full_name', 'date_of_birth', 'api_key']

        widgets ={
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'api_key': forms.TextInput(attrs={'placeholder': 'Enter your API key'})
        }