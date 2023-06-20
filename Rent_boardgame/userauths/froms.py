from django import forms
from django.contrib.auth.forms import UserCreationForm
from userauths.models import User


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email') #, 'password1', 'password2'
    
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Full name here',
        'class': 'focus:outline-none self-center w-full'
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'placeholder': 'Enter your email address',
        'class': 'focus:outline-none self-center w-full'
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Enter your password',
        'class': 'focus:outline-none self-center w-full'
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirm password',
        'class': 'focus:outline-none self-center w-full'
    }))