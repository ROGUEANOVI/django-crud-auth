from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError
from .models import Task
from .forms import FormCreateTask, FormEditTask
from django.utils import timezone

# Create your views here.
def home(request):
  return render(request, "home.html")

def signUp(request):
  if request.method == "GET":
    return render(request, "signup.html", {"form": UserCreationForm})
  else:
    if request.POST['password1'] ==request.POST['password2']:
      try:
        userRegiter = User.objects.create_user(username=request.POST["username"], password=request.POST["password1"])
        userRegiter.save()
        login(request, userRegiter)
        return redirect("tasks")
      except IntegrityError:
        return render(request, "signup.html", {"form": UserCreationForm, "error": "Usuario ya existe"})
    else:
      return render(request, "signup.html", {"form": UserCreationForm, "error": "Las contraseñas no coinciden"})

def signIn(request):
  if request.method == "GET":
    return render(request, "signin.html", {"form": AuthenticationForm})
  else:
    userValid = authenticate(request, username=request.POST["username"], password=request.POST["password"])
    if userValid is None:
      return render(request, "signin.html", {"form": AuthenticationForm, "error": "Nombre de usuario o contraseña incorrecto(a)"})
    else:
      login(request, userValid)
      return redirect("tasks")

def signOut(request):
  logout(request, )
  return redirect("home")

def listTasks(request):
  tasks = Task.objects.filter(user=request.user)
  return render(request, "list-tasks.html",{"tasks": tasks})

def createTask(request):
  if request.method == "GET":
    return render(request, "create-task.html", {"form": FormCreateTask})
  else:
    try:
      taskForm = FormCreateTask(request.POST)
      new_task = taskForm.save(commit=False)
      new_task.user = request.user
      new_task.save()
      return redirect("tasks")
    except ValueError:
      return render(request, "create-task.html", {"form": FormCreateTask, "error": "Datos NO validos"})

def detailsTask(request, id):
  # task = Task.objects.get(id=id)
  task = get_object_or_404(Task, id=id)
  return render(request, "details-task.html", {"task": task})

def editTask(request, id):
  if request.method == "GET":
    task = get_object_or_404(Task, id=id, user=request.user)
    form = FormEditTask(instance=task)
    return render(request, "edit-task.html", {"form": form})
  else:
    try:
      task = get_object_or_404(Task, id=id, user=request.user)
      taskForm = FormEditTask(request.POST, instance=task)
      taskForm.save()
      return redirect("tasks")
    except ValueError:
      return render(request, "edit-task.html", {"form": FormEditTask, "error": "Datos NO validos"})

def completeTask(request, id):
  task = get_object_or_404(Task, id=id, user=request.user)
  if request.method == "POST":
    task.datecompleted = timezone.now()
    task.save()
    return redirect("tasks")

def deleteTask(request, id):
  task = get_object_or_404(Task, id=id, user=request.user)
  if request.method == "POST":
    task.delete()
    return redirect("tasks")

def listCompletedTasks(request):
  completedTasks = Task.objects.filter(user=request.user, datecompleted__isnull=False)
  return render(request, "list-completed-tasks.html",{"completedTasks": completedTasks})