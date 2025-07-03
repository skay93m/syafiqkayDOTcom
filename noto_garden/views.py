from django.shortcuts import render

# noto_garden/views.py
def coming_soon(request):
    return render(request, "noto_garden/coming_soon.html")
