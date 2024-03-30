from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import TaskForm, EditarUsuario, AvatarForm
from .models import Task, Avatar
from django.utils import timezone
from django.contrib.auth.decorators import login_required

# Create your views here.


def home(request):
    avatar = None
    if request.user.is_authenticated:
        if hasattr(request.user, 'avatar'):
            avatar = request.user.avatar
    return render(request, 'home.html', {'avatar': avatar})

def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form': UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            # Registro de Usuario
            try:
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password2'])
                login(request, user)
                return redirect('tasks')
            except IntegrityError:
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    "error": 'Usuario ya existente.'
                })
        else:
            return render(request, 'signup.html', {
                'form': UserCreationForm,
                "error": 'La contraseña no coincide, verifica nuevamente'
            })

@login_required
def agregar_avatar(request):
    if request.method == 'GET':
        formulario = AvatarForm(request.POST, request.FILES)

        if formulario.is_valid():

            info = formulario.cleaned_data

            usuario_actual = User.objects.get(username=request.user)
            nuevo_avatar = Avatar(usuario=usuario_actual, imagen=info["imagen"])
            nuevo_avatar.save()
            return render(request, 'base.html')
    else:

        formulario = agregar_avatar()

# Vista de editar el perfil
@login_required
def editarPerfil(request):

    usuario = request.user

    if request.method == 'POST':

        miFormulario = EditarUsuario(request.POST, instance=usuario)

        if miFormulario.is_valid():

            miFormulario.save()
            return render(request, "base.html")

    else:

        miFormulario = EditarUsuario(instance=usuario)

    return render(request, 'editar_usuario.html', {'miFormulario': miFormulario})

@login_required
def tasks(request):
    tasks = Task.objects.filter(user=request.user, fecha_completada__isnull=True)
    if not tasks:  # Si no hay tareas disponibles
        message = "No hay tareas disponibles."
        return render(request, 'tasks.html', {'message': message})
    else:
        return render(request, 'tasks.html', {'tasks': tasks})

@login_required
def tasks_completed(request):
    tasks = Task.objects.filter(user=request.user, fecha_completada__isnull=False).order_by
    ('-fecha_completada')
    if not tasks:  # Si no hay tareas disponibles
        message = "No hay tareas disponibles."
        return render(request, 'tasks.html', {'message': message})
    else:
        return render(request, 'tasks.html', {'tasks': tasks})

@login_required
def create_task(request):

    if request.method == 'GET':
        return render(request, 'create_task.html', {
            'form': TaskForm
        })
    else:
       try:
           form = TaskForm(request.POST)
           new_task = form.save(commit=False)
           new_task.user = request.user
           new_task.save()
           return redirect('tasks')
       except ValueError:
           return render(request, 'create_task.html', {
               'form': TaskForm,
               'Error': 'Por favor, ingrese datos validos'
           })

@login_required
def task_detail(request, task_id):
    if request.method == 'GET':
        task = get_object_or_404(Task, pk=task_id)
        form = TaskForm(instance=task)
        return render(request, 'task_detail.html', {'task': task, 'form': form})
    else:
        try:
            task = get_object_or_404(Task, pk=task_id, user=request.user)
            form = TaskForm(request.POST, instance=task)
            form.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'task_detail.html', {'task': task, 'form': form,
            'Error': "Al actualizar tarea"})

@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.fecha_completada = timezone.now()
        task.save()
        return redirect('tasks')

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')

@login_required
def signout(request):
    logout(request)
    return  redirect('home')

def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
            'form': AuthenticationForm()
        })
    else:
        user = authenticate(
                request, username=request.POST['username'], password=request.POST
                ['password'])
        if user is None:
            return render(request, 'signin.html', {
                'form': AuthenticationForm(),
                'Error': 'Tu usuario o contraseña es incorrecta'
            })
        else:
            login(request, user)
            return redirect('tasks')

