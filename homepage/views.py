from django.shortcuts import render
from .models import Rirekisho

def homepage(request):
<<<<<<< HEAD
    # Fetch the latest Rirekisho entry
    try:
        rirekisho = Rirekisho.objects.latest('version')
    except Rirekisho.DoesNotExist:
        rirekisho = None
    return render(request, "homepage.html", {
=======
    rirekisho = Rirekisho.objects.order_by('-id').first()  # Latest due to ordering
    return render(request, "homepage/homepage.html", {
>>>>>>> fec6094 (Refactor notoGarden app: rename to noto_garden, remove unused files, and update settings)
        "rirekisho": rirekisho,
    })
