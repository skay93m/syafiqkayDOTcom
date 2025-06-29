from django.shortcuts import render
from django.http import HttpResponse

# homepage/views.py
def homepage(request):
    return render(request, "homepage.html")
