from django.shortcuts import render

def home(request):
    return render(request, 'taskmanager/tm_home.html')

def help(request):
    return render(request, 'taskmanager/tm_help.html')
