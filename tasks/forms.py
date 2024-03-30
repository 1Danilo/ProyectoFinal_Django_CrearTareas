from  django import forms
from django.contrib.auth.models import User
from .models import Avatar
from .models import Task
from  django.contrib.auth.forms import UserChangeForm

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['titulo', 'descripcion', 'important']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Escribe un Título'},),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Escribe una Descripción'}, ),
            'important': forms.CheckboxInput(attrs={'class': 'form-check-input'}, )
        }

class EditarUsuario(UserChangeForm):

    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name"]

class AvatarForm(forms.ModelForm):
    class Meta:
        model = Avatar
        fields = ['imagen']