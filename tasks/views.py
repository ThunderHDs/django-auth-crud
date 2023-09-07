from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import TaskForm
from .models import Task
from django.utils import timezone
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    return render(request, 'home.html')

def signup(request):
    #Para diferenciar mediante que metodo se estan obteniendo los datos GET o POST
    if request.method =='GET':
          return render(request, 'signup.html', {
        'form':UserCreationForm})
    else:
        #Validacion de contraseñas confirmada
        print(request)
        if request.POST['password1'] == request.POST['password2']:
            #Validar datos en base de datos
            try:
                #Registro del usuario
                #Creacion del usuario para guardar en la base de datos
                user = User.objects.create_user(username = request.POST['username'], password = request.POST['password1'])
                #Guardado del usuario en la base de datos
                user.save()
                login(request, user) #Creacion de cookie de sesion para autenticar el usuario
                return redirect('tasks')
            except IntegrityError: #Con el integrity pedimos considerar excepciones que estan dedicadas a un error en especifico
                #Usuario ya existe, en caso de errores enviamos error de que usario ya existe en la misma pagina
                return render(request, 'signup.html', {'form':UserCreationForm,  "error": 'Username already exists'})
        return render(request, 'signup.html', {'form':UserCreationForm,  "error": 'Password do not match'})

@login_required
def tasks(request):
    #tasks = Task.objects.all() #Traeme todos los elementos de la tabla Task y metelos en una variable tipo diccionario
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True)#Con la propiedad filter de objects podemos indicarle un parametro para traer los datos
    return render(request, 'tasks.html', {'tasks':tasks})#Con el parametro datecompleted_isnull indicamos que solo me traiga las tareas no completadas


@login_required
def tasks_completed(request):
    #tasks = Task.objects.all() #Traeme todos los elementos de la tabla Task y metelos en una variable tipo diccionario
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')#Con el order_by ordenamos por lo indicado en el parametro entre ()
    return render(request, 'tasks.html', {'tasks':tasks})#Con el parametro datecompleted_isnull indicamos que solo me traiga las tareas no completadas

@login_required
def create_task(request):
    if request.method == 'GET':
        return render(request, 'create_task.html', {'form': TaskForm})
    else:
        try:
            form = TaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'create_task.html', {
                'form':TaskForm, 
                'error': 'Please provide valid data'})

@login_required
def task_detail(request, task_id):#Obtenemos el parametro task_id que nos indica cual de todas es
    if request.method == 'GET':
        task = get_object_or_404(Task, pk=task_id, user=request.user)
        form = TaskForm(instance=task)#Con este metodo obtenemos un formulario para modificar el test de las tareas
        return render(request, 'task_detail.html', {'task':task, 'form':form})
    else:
        try:
            task = get_object_or_404(Task, pk=task_id, user=request.user)
            form = TaskForm(request.POST, instance=task)#Tomara los nuevos datos de las tareas y los actualizara
            form.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'task_detail.html', {'task':task, 'form':form, 'error': "Error updating task"})

@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.datecompleted = timezone.now()
        task.save()
        return redirect('tasks')

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()#metodo para deletear la tarea o objeto
        return redirect('tasks')

@login_required
def signout(request):
    logout(request)
    return redirect('home')

def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {'form': AuthenticationForm})#Para comprobar usuario existente y realizar login
    else:
        #Si viene por metodo post entonces comprobamos e iniciamos sesion
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        #Validamos si el usuario existe o no realizamos una accion
        if user is None:
            return render(request, 'signin.html', {
                'form': AuthenticationForm, 
                'error': 'Username or Password is incorrect'})#Para comprobar usuario existente y realizar login
        else:
            login(request, user)
            return redirect('tasks')
