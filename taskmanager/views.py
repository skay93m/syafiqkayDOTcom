from django.shortcuts import render

def home(request):
    return render(request, 'taskmanager/tm_base.html')

def help(request):
    return render(request, 'taskmanager/tm_help.html')
