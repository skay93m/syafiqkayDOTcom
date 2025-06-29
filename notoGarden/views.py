from django.shortcuts import render
from django.http import HttpResponse

# notogarden/views.py
def coming_soon(request):
    return render(request, "notoGarden/coming_soon.html")
