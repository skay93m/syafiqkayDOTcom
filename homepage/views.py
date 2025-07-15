from django.shortcuts import render

# Render the homepage view
def homepage(request):
    return render(request, 'homepage/homepage.html')