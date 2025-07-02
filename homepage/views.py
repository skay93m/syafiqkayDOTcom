from django.shortcuts import render
from .models import Rirekisho

def homepage(request):
    # Fetch the latest Rirekisho entry
    try:
        rirekisho = Rirekisho.objects.latest('version')
    except Rirekisho.DoesNotExist:
        rirekisho = None
    return render(request, "homepage.html", {
        "rirekisho": rirekisho,
    })
