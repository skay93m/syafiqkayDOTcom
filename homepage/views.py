from django.shortcuts import render
from .models import Rirekisho

def homepage(request):
    rirekisho = Rirekisho.objects.prefetch_related('work_experiences', 'educations').first()  # Latest due to ordering
    work_experiences = rirekisho.work_experiences.all() if rirekisho else []
    educations = rirekisho.educations.all() if rirekisho else []
    return render(request, "homepage.html", {
        "rirekisho": rirekisho,
        "work_experiences": work_experiences,
        "educations": educations,
    })
