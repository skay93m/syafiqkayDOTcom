from django.shortcuts import render
from django.http import HttpResponse
from django.urls import path

def home(request):
    return render(request, 'taskmanager/home.html')
