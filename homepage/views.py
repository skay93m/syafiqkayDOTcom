from django.shortcuts import render
from .models import Rirekisho


# Render the homepage view
def homepage(request):
    rirekisho = Rirekisho.objects.order_by('-id').first()
    return render(request, "homepage/homepage.html", {
        "rirekisho": rirekisho,
    })