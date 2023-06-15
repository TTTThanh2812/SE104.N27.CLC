from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class SignInForm(AuthenticationForm):
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'placeholder': 'Enter your email address here',
        'class': 'focus:outline-none self-center w-full'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Enter your password here',
        'class': 'focus:outline-none w-full'
    }))

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
    
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Full name here',
        'class': 'focus:outline-none self-center w-full'
    }))
    email = forms.CharField(widget=forms.EmailInput(attrs={
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