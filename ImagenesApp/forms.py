from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Archivo


class LoginForm(AuthenticationForm):
    username= forms.CharField(widget=forms.TextInput(attrs={
        'placeholder':'Ingresa tu usuario ',
           
    }))
    password= forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'Ingresa tu contraseña',
        'class':'fadeIn third',
        
    }))
    
class EditarArchivos(forms.ModelForm):
    class Meta:
        model = Archivo
        fields = ('nombre', 'archivo', 'es_video')
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'archivo': forms.FileInput(attrs={'class': 'form-control-file'}),
            'es_video': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
