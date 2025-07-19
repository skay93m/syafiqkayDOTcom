# taskmanager/views.py

from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from syafiqkaydotcom.decorators import ensure_200_status

# homepage and help page

@method_decorator(ensure_200_status, name='get')
class ViewTaskManagerHomepage(TemplateView):
    template_name = 'home_and_help/task_manager_homepage.html'

@method_decorator(ensure_200_status, name='get')
class ViewTaskManagerHelpPage(TemplateView):
    template_name = 'home_and_help/task_manager_help_page.html'
    