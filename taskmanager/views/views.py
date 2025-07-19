# taskmanager/views/views.py
from django.views.generic import TemplateView

class HomePageView(TemplateView):
    template_name = "templates/taskmanager.html"

class HelpPageView(TemplateView):
    template_name = "templates/help.html"
