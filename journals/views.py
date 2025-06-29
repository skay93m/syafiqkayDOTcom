from django.shortcuts import render
from django.http import HttpResponse

def coming_soon(request):
    return render(request, "journals/coming_soon.html")