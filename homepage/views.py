from django.shortcuts import render
from .models import Rirekisho

def homepage(request):
    rirekisho = Rirekisho.objects.order_by('-id').first()  # Latest due to ordering
    return render(request, "homepage/homepage.html", {
        "rirekisho": rirekisho,
    })
