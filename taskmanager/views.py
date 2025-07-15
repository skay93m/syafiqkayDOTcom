from django.shortcuts import render

def home(request):
    return render(request, 'taskmanager/taskmanager.html')

def help(request):
    return render(request, 'taskmanager/help.html')
