from django.shortcuts import render
from django.views.generic import ListView
from .models import Task

def home(request):
    return render(request, 'taskmanager/taskmanager.html')

def help(request):
    return render(request, 'taskmanager/help.html')

def task_list(request):
    tasks = Task.objects.all()
    return render(request, 'taskmanager/task_list.html', {'tasks': tasks})