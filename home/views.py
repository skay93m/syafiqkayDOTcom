from django.shortcuts import render
from datetime import datetime

def home(request):
    context = {
        'page_title': 'Home Page',
        'user_name': 'Visitor',
        'message': 'Welcome to our website!'
    }
    return render(request, 'home/index.html', context)

def testing_guide(request):
    context = {
        'current_date': datetime.now().strftime('%B %d, %Y'),
        'project_name': 'syafiq-kay-dotcom-manual-rebuild'
    }
    return render(request, 'home/testing_guide.html', context)