# taskmanager/views.py

from django.views.generic import TemplateView, ListView, CreateView, DetailView
from django.utils.decorators import method_decorator
from syafiqkaydotcom.decorators import ensure_200_status
from .models import Task, Sprint, Epic

# homepage and help page

@method_decorator(ensure_200_status, name='get')
class ViewTaskManagerHomepage(TemplateView):
    template_name = 'home_and_help/task_manager_homepage.html'

@method_decorator(ensure_200_status, name='get')
class ViewTaskManagerHelpPage(TemplateView):
    template_name = 'home_and_help/task_manager_help_page.html'

# task pages
@method_decorator(ensure_200_status, name='get')
class ViewTaskList(ListView):
    model = Task
    template_name = 'task/task_list.html'
    context_object_name = 'tasks'
    

@method_decorator(ensure_200_status, name='get') 
class ViewTaskCreate(CreateView):
    model = Task
    template_name = 'task/task_form.html'
    fields = '__all__'
    success_url = '/tasks/'
    
@method_decorator(ensure_200_status, name='get') 
class ViewTaskDetail(DetailView):
    template_name = "task/task_detail.html"
    model = Task
    context_object_name = 'task'
    