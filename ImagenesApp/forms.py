from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class LoginForm(AuthenticationForm):
    username= forms.CharField(widget=forms.TextInput(attrs={
        'placeholder':'Ingresa tu usuario ',
           
    }))
    password= forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'Ingresa tu contraseña',
        'class':'fadeIn third',
        
    }))
    