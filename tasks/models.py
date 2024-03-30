from django.db import models
from django.contrib.auth.models import User
from django import forms
# Create your models here.

class Task(models.Model):
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    fecha_de_creacion = models.DateTimeField(auto_now_add=True)
    fecha_completada = models.DateTimeField(null=True, blank=True)
    important = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.titulo + ' - author:  ' + self.user.username

class Avatar(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='avatares', null=True, blank=True)

class AvatarForm(forms.ModelForm):
    class Meta:
        model = Avatar
        fields = ['imagen']